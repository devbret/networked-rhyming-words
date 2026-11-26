export const svg = d3.select("svg");

export const size = { width: 0, height: 0 };

export function measure() {
  size.width = +svg.style("width").replace("px", "");
  size.height = +svg.style("height").replace("px", "");
}

measure();

export const g = svg.append("g");

const zoom = d3
  .zoom()
  .scaleExtent([0.05, 16])
  .on("zoom", (event) => {
    g.attr("transform", event.transform);
  });

svg.call(zoom).on("dblclick.zoom", null);

export function zoomToFit() {
  const bounds = g.node().getBBox();
  const scale = Math.min(
    16,
    0.9 / Math.max(bounds.width / size.width, bounds.height / size.height),
  );
  const tx = size.width / 2 - (bounds.x + bounds.width / 2) * scale;
  const ty = size.height / 2 - (bounds.y + bounds.height / 2) * scale;
  svg
    .transition()
    .duration(700)
    .call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
}

export function showError(message) {
  svg
    .append("text")
    .attr("x", size.width / 2)
    .attr("y", size.height / 2)
    .attr("text-anchor", "middle")
    .attr("font-family", "sans-serif")
    .attr("font-size", 16)
    .attr("fill", "#900")
    .text(message);
}
