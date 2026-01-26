from __future__ import annotations

import argparse
import json
import logging
import re
from functools import lru_cache
from typing import Dict, List, Optional, Tuple, Iterable

import pronouncing

LAST_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*$")

SMART_QUOTES = {
    "\u2018": "'", "\u2019": "'", "\u201B": "'",
    "\u201C": '"', "\u201D": '"', "\u201F": '"',
}

def normalize_smart_quotes(text: str) -> str:
    for k, v in SMART_QUOTES.items():
        text = text.replace(k, v)
    return text

def split_stanzas(text: str) -> List[List[str]]:
    text = text.replace("\r\n", "\n")
    raw = text.split("\n")
    stanzas: List[List[str]] = []
    cur: List[str] = []
    for line in raw:
        if line.strip() == "":
            if cur:
                stanzas.append(cur)
                cur = []
        else:
            cur.append(line)
    if cur:
        stanzas.append(cur)
    return stanzas

def find_last_word(line: str) -> Optional[str]:
    line = line.strip()
    if not line:
        return None
    m = LAST_WORD_RE.search(line)
    return m.group(0).lower() if m else None

@lru_cache(None)
def phones_for_word_cached(word: str) -> Tuple[str, ...]:
    return tuple(pronouncing.phones_for_word(word))

@lru_cache(None)
def rhyming_part_cached(phones: str) -> Optional[str]:
    try:
        return pronouncing.rhyming_part(phones)
    except Exception:
        return None

@lru_cache(None)
def stresses_for_word_cached(word: str) -> Tuple[str, ...]:
    return tuple(pronouncing.stresses(word))

@lru_cache(None)
def rhymes_cached(word: str) -> Tuple[str, ...]:
    return tuple(pronouncing.rhymes(word))

def basic_stem(word: str) -> str:
    if word.endswith("'s"):
        return word[:-2]
    if word.endswith("’s"):
        return word[:-2]
    if word.endswith("es") and len(word) > 3:
        return word[:-2]
    if word.endswith("s") and len(word) > 2:
        return word[:-1]
    return word

def crude_orthographic_rhyme_key(word: str) -> str:
    w = word.lower()
    vowels = "aeiouy"
    last_vowel_idx = -1
    for i in range(len(w) - 1, -1, -1):
        if w[i] in vowels:
            last_vowel_idx = i
            break
    if last_vowel_idx == -1:
        return w[-3:] if len(w) >= 3 else w
    return w[last_vowel_idx:]

def rhyme_key(word: str) -> Tuple[Optional[str], float]:
    phones = phones_for_word_cached(word)
    if phones:
        key = rhyming_part_cached(phones[0])
        if key:
            return key, 1.0

    w2 = basic_stem(word)
    if w2 != word:
        phones2 = phones_for_word_cached(w2)
        if phones2:
            key2 = rhyming_part_cached(phones2[0])
            if key2:
                return key2, 0.8 

    return crude_orthographic_rhyme_key(w2), 0.3

def levenshtein_tokens(a: List[str], b: List[str]) -> int:
    la, lb = len(a), len(b)
    dp = [[0]*(lb+1) for _ in range(la+1)]
    for i in range(la+1):
        dp[i][0] = i
    for j in range(lb+1):
        dp[0][j] = j
    for i in range(1, la+1):
        for j in range(1, lb+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1,     
                           dp[i][j-1] + 1,     
                           dp[i-1][j-1] + cost)
    return dp[la][lb]

def stress_bonus(a: str, b: str) -> float:
    sa = stresses_for_word_cached(a)
    sb = stresses_for_word_cached(b)
    if not sa or not sb:
        return 0.0

    spa, spb = sa[0], sb[0]

    def last_primary_idx(s: str) -> int:
        for i in range(len(s)-1, -1, -1):
            if s[i] == '1':
                return i
        return -1

    ia, ib = last_primary_idx(spa), last_primary_idx(spb)
    if ia == -1 or ib == -1:
        return 0.0

    tail_a, tail_b = spa[ia:], spb[ib:]
    return 0.1 if tail_a == tail_b else 0.0 

def rhyme_strength(a: str, b: str) -> float:
    key_a, conf_a = rhyme_key(a)
    key_b, conf_b = rhyme_key(b)
    if not key_a or not key_b:
        return 0.0

    if key_a == key_b:
        base = 1.0
    else:
        toks_a = key_a.split()
        toks_b = key_b.split()
        if not toks_a or not toks_b:
            toks_a = list(key_a)
            toks_b = list(key_b)
        d = levenshtein_tokens(toks_a, toks_b)
        denom = max(len(toks_a), len(toks_b))
        base = max(0.0, 1.0 - (d / denom))

    bonus = stress_bonus(a, b)
    conf = (conf_a + conf_b) / 2.0
    return max(0.0, min(1.0, (base + bonus) * conf))

def build_graph(
    lyrics_text: str,
    window: Optional[int] = None,
    min_strength: float = 0.6,
    min_freq: int = 1,
) -> Dict[str, List[dict]]:
    lyrics_text = normalize_smart_quotes(lyrics_text)
    stanzas = split_stanzas(lyrics_text)
    lines: List[str] = [ln for stanza in stanzas for ln in stanza]

    last_words: List[Tuple[int, str]] = []
    for i, line in enumerate(lines):
        w = find_last_word(line)
        if w:
            last_words.append((i, w))

    freq: Dict[str, int] = {}
    positions: Dict[str, List[int]] = {}
    for i, w in last_words:
        freq[w] = freq.get(w, 0) + 1
        positions.setdefault(w, []).append(i)

    vocab: List[str] = sorted({w for _, w in last_words if freq[w] >= min_freq})

    idx_by_word: Dict[str, List[int]] = {w: positions[w] for w in vocab}

    rhyme_map: Dict[str, Dict[str, float]] = {w: {} for w in vocab} 

    n = len(vocab)
    for i in range(n):
        a = vocab[i]
        for j in range(i + 1, n):
            b = vocab[j]
            if window is not None:
                if not any(abs(ia - ib) <= window for ia in idx_by_word[a] for ib in idx_by_word[b]):
                    continue
            s = rhyme_strength(a, b)
            if s >= min_strength:
                rhyme_map[a][b] = s
                rhyme_map[b][a] = s

    nodes: List[dict] = []
    for w in vocab:
        key, _conf = rhyme_key(w)
        nodes.append({
            "id": w,
            "group": 1,
            "count": freq[w],
            "positions": positions[w],
            "rhyme_key": key
        })

    links: List[dict] = []
    for a, nbrs in rhyme_map.items():
        for b, s in nbrs.items():
            if a < b:
                links.append({"source": a, "target": b, "value": round(s, 4)})

    adj: Dict[str, set] = {w: set(d.keys()) for w, d in rhyme_map.items()}
    visited: set = set()
    fam_id = 0
    for w in vocab:
        if w in visited:
            continue
        stack = [w]
        comp: List[str] = []
        while stack:
            cur = stack.pop()
            if cur in visited:
                continue
            visited.add(cur)
            comp.append(cur)
            stack.extend(adj.get(cur, []))
        for n in nodes:
            if n["id"] in comp:
                n["family"] = fam_id
        fam_id += 1

    return {"nodes": nodes, "links": links}

def export_networkx(graph: Dict[str, List[dict]], graphml_path: Optional[str], gexf_path: Optional[str]) -> None:
    try:
        import networkx as nx
    except Exception as e:
        logging.warning("networkx not available; skipping GraphML/GEXF export. (%s)", e)
        return

    G = nx.Graph()
    for n in graph["nodes"]:
        node_id = n["id"]
        attrs = {k: v for k, v in n.items() if k != "id"}
        G.add_node(node_id, **attrs)
    for e in graph["links"]:
        G.add_edge(e["source"], e["target"], value=e.get("value", 1.0))

    if graphml_path:
        try:
            nx.write_graphml(G, graphml_path)
            logging.info("Wrote GraphML: %s", graphml_path)
        except Exception as e:
            logging.error("Failed to write GraphML (%s): %s", graphml_path, e)

    if gexf_path:
        try:
            nx.write_gexf(G, gexf_path)
            logging.info("Wrote GEXF: %s", gexf_path)
        except Exception as e:
            logging.error("Failed to write GEXF (%s): %s", gexf_path, e)


def main():
    parser = argparse.ArgumentParser(description="Build a rhyme network from lyrics.")
    parser.add_argument("-i", "--input", default="combined_output.txt", help="Input lyrics file path")
    parser.add_argument("-o", "--output", default="network_data.json", help="Output JSON graph path")
    parser.add_argument("--min-strength", type=float, default=0.6, help="Minimum rhyme strength [0..1]")
    parser.add_argument("--min-freq", type=int, default=1, help="Minimum frequency for a word to be included")
    parser.add_argument("--window", type=int, default=None, help="Max line-distance for rhyme edges (e.g., 4 for couplet/quatrain proximity)")
    parser.add_argument("--graphml", default=None, help="Optional path to write GraphML (requires networkx)")
    parser.add_argument("--gexf", default=None, help="Optional path to write GEXF (requires networkx)")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            lyrics_text = f.read()
    except FileNotFoundError:
        logging.error("Input file not found: %s", args.input)
        return

    graph = build_graph(
        lyrics_text=lyrics_text,
        window=args.window,
        min_strength=args.min_strength,
        min_freq=args.min_freq,
    )

    try:
        with open(args.output, "w", encoding="utf-8") as out:
            json.dump(graph, out, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
        logging.info("Saved %s with %d nodes and %d links.",
                     args.output, len(graph["nodes"]), len(graph["links"]))
    except Exception as e:
        logging.error("Failed to write JSON: %s", e)

    if args.graphml or args.gexf:
        export_networkx(graph, args.graphml, args.gexf)

if __name__ == "__main__":
    main()
