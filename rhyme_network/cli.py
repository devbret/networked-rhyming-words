from __future__ import annotations

import argparse
import json
import logging

from .export import export_networkx
from .graph import build_graph

def main():
    parser = argparse.ArgumentParser(description="Build a rhyme network from lyrics.")
    parser.add_argument("-i", "--input", default="text.txt", help="Input lyrics file path")
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
