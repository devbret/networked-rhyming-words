import { familyOf } from "./data.js";

export const NODE_R = 10;

export function renderGraph(container, nodes, links, families) {
  const valueExtent = d3.extent(links, (l) => l.value ?? 1);
  const linkWidth = d3.scaleLinear().domain(valueExtent).range([0.5, 3]);
  const linkOpacity = d3.scaleLinear().domain(valueExtent).range([0.1, 0.7]);

  const color = d3.scaleOrdinal().domain(families).range(d3.schemeTableau10);

  const linkG = container.append("g").attr("class", "links");
  const nodeG = container.append("g").attr("class", "nodes");
  const textG = container.append("g").attr("class", "labels");

  const link = linkG
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke", "#999")
    .attr("stroke-width", (d) => linkWidth(d.value ?? 1))
    .attr("stroke-opacity", (d) => linkOpacity(d.value ?? 1));

  const node = nodeG
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", NODE_R)
    .attr("fill", (d) => color(familyOf(d)))
    .attr("stroke", "#000")
    .attr("stroke-width", 1);

  const label = textG
    .selectAll("text")
    .data(nodes)
    .join("text")
    .text((d) => d.id)
    .attr("font-size", 12)
    .attr("font-family", "sans-serif")
    .attr("fill", "#000")
    .attr("pointer-events", "none");

  return { link, node, label, linkOpacity };
}

export function positionElements({ link, node, label }) {
  link
    .attr("x1", (d) => d.source.x)
    .attr("y1", (d) => d.source.y)
    .attr("x2", (d) => d.target.x)
    .attr("y2", (d) => d.target.y);

  node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
  label.attr("x", (d) => d.x + NODE_R + 4).attr("y", (d) => d.y + 4);
}
