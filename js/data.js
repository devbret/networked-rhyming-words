export const idOf = (v) => (typeof v === "object" ? v.id : v);

export const familyOf = (d) => d.family ?? d.id;

export function prepareGraph(graph) {
  const rawNodes = graph.nodes.map((d) => ({ ...d }));
  const rawLinks = graph.links.map((d) => ({ ...d }));

  const degree = new Map(rawNodes.map((n) => [n.id, 0]));
  rawLinks.forEach(({ source, target }) => {
    const s = idOf(source);
    const t = idOf(target);
    degree.set(s, (degree.get(s) || 0) + 1);
    degree.set(t, (degree.get(t) || 0) + 1);
  });

  const nodes = rawNodes.filter((n) => (degree.get(n.id) || 0) > 0);
  const nodeIdSet = new Set(nodes.map((n) => n.id));

  const links = rawLinks
    .map((l) => ({
      ...l,
      source: idOf(l.source),
      target: idOf(l.target),
    }))
    .filter((l) => nodeIdSet.has(l.source) && nodeIdSet.has(l.target));

  return { nodes, links };
}

export function buildNeighbors(nodes, links) {
  const map = new Map();
  nodes.forEach((n) => map.set(n.id, new Set([n.id])));
  links.forEach(({ source, target }) => {
    const s = idOf(source);
    const t = idOf(target);
    map.get(s).add(t);
    map.get(t).add(s);
  });
  return map;
}
