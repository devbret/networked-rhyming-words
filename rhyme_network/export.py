from __future__ import annotations

import logging
from typing import Dict, List, Optional

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
