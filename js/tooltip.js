export function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export function tooltipHtml(d) {
  const positions = (d.positions || []).slice(0, 10);
  const more = (d.positions || []).length > 10 ? "…" : "";
  return `
    <div style="font-weight:700;font-size:14px;margin-bottom:6px;">${escapeHtml(d.id)}</div>
    <div style="font-size:12px;line-height:1.4;">
      <div>Count: ${d.count ?? 1}</div>
      <div>Rhyme: ${escapeHtml(d.rhyme_key ?? "—")}</div>
      <div>Family: ${escapeHtml(d.family ?? "—")}</div>
      <div>Line idx: ${positions.join(", ")}${more}</div>
    </div>
  `;
}

export function createTooltip() {
  return d3
    .select("body")
    .append("div")
    .style("position", "absolute")
    .style("pointer-events", "none")
    .style("opacity", 0)
    .style("padding", "10px 12px")
    .style("background", "rgba(0,0,0,0.85)")
    .style("color", "#fff")
    .style("border-radius", "8px")
    .style("font-family", "sans-serif");
}
