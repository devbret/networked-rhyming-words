from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .phonetics import rhyme_key
from .scoring import MAX_STRESS_BONUS, base_from_keys, rhyme_strength
from .text import find_last_word, normalize_smart_quotes, split_stanzas

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

    keys: Dict[str, Optional[str]] = {w: rhyme_key(w)[0] for w in vocab}

    buckets: Dict[str, List[str]] = {}
    for w in vocab:
        k = keys[w]
        if k:
            buckets.setdefault(k, []).append(w)

    rhyme_map: Dict[str, Dict[str, float]] = {w: {} for w in vocab}

    def maybe_add_edge(a: str, b: str) -> None:
        if window is not None:
            if not any(abs(ia - ib) <= window
                       for ia in idx_by_word[a] for ib in idx_by_word[b]):
                return
        s = rhyme_strength(a, b)
        if s >= min_strength:
            rhyme_map[a][b] = s
            rhyme_map[b][a] = s

    unique_keys = list(buckets.keys())
    for i, ka in enumerate(unique_keys):
        words_a = buckets[ka]
        m = len(words_a)
        for x in range(m):
            for y in range(x + 1, m):
                maybe_add_edge(words_a[x], words_a[y])
        for j in range(i + 1, len(unique_keys)):
            kb = unique_keys[j]
            if base_from_keys(ka, kb) + MAX_STRESS_BONUS < min_strength:
                continue
            for a in words_a:
                for b in buckets[kb]:
                    maybe_add_edge(a, b)

    nodes: List[dict] = []
    for w in vocab:
        nodes.append({
            "id": w,
            "group": 1,
            "count": freq[w],
            "positions": positions[w],
            "rhyme_key": keys[w]
        })
    node_by_id: Dict[str, dict] = {nd["id"]: nd for nd in nodes}

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
        for cid in comp:
            node_by_id[cid]["family"] = fam_id
        fam_id += 1

    return {"nodes": nodes, "links": links}
