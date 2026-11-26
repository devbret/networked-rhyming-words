import { idOf } from "./data.js";
import { tooltipHtml } from "./tooltip.js";

export function drag(simulation) {
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }
  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }
  return d3
    .drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
}

export function bindHover({ node, link, linkOpacity }, neighbors, tooltip) {
  node
    .on("mouseover", (event, d) => {
      const nset = neighbors.get(d.id);
      node.attr("opacity", (o) => (nset.has(o.id) ? 1 : 0.15));
      link.attr("stroke-opacity", (l) => {
        const s = idOf(l.source);
        const t = idOf(l.target);
        const touchesHovered = s === d.id || t === d.id;
        const withinNeighborSet = nset.has(s) && nset.has(t);
        return touchesHovered || withinNeighborSet
          ? linkOpacity(l.value ?? 1)
          : 0.05;
      });
      tooltip.style("opacity", 1).html(tooltipHtml(d));
    })
    .on("mousemove", (event) => {
      tooltip
        .style("left", event.pageX + 12 + "px")
        .style("top", event.pageY + 12 + "px");
    })
    .on("mouseout", () => {
      node.attr("opacity", 1);
      link.attr("stroke-opacity", (d) => linkOpacity(d.value ?? 1));
      tooltip.style("opacity", 0);
    });
}
