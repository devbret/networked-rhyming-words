const svg = d3.select("svg");
let width = +svg.style("width").replace("px", "");
let height = +svg.style("height").replace("px", "");

const g = svg.append("g");

const zoom = d3
  .zoom()
  .scaleExtent([0.05, 16])
  .on("zoom", (event) => {
    g.attr("transform", event.transform);
  });

svg.call(zoom).on("dblclick.zoom", null);

function drag(simulation) {
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

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function tooltipHtml(d) {
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

d3.json("network_data.json").then((graph) => {
  const rawNodes = graph.nodes.map((d) => ({ ...d }));
  const rawLinks = graph.links.map((d) => ({ ...d }));

  const degree = new Map(rawNodes.map((n) => [n.id, 0]));
  rawLinks.forEach(({ source, target }) => {
    const s = typeof source === "object" ? source.id : source;
    const t = typeof target === "object" ? target.id : target;
    degree.set(s, (degree.get(s) || 0) + 1);
    degree.set(t, (degree.get(t) || 0) + 1);
  });

  const nodes = rawNodes.filter((n) => (degree.get(n.id) || 0) > 0);
  const nodeIdSet = new Set(nodes.map((n) => n.id));

  const links = rawLinks
    .map((l) => ({
      ...l,
      source: typeof l.source === "object" ? l.source.id : l.source,
      target: typeof l.target === "object" ? l.target.id : l.target,
    }))
    .filter((l) => nodeIdSet.has(l.source) && nodeIdSet.has(l.target));

  const valueExtent = d3.extent(links, (l) => l.value ?? 1);
  const linkWidth = d3.scaleLinear().domain(valueExtent).range([0.5, 3]);
  const linkOpacity = d3.scaleLinear().domain(valueExtent).range([0.1, 0.7]);

  const families = Array.from(new Set(nodes.map((d) => d.family ?? d.id)));
  const color = d3.scaleOrdinal().domain(families).range(d3.schemeTableau10);

  function computeFamilyCenters() {
    const cols = Math.ceil(Math.sqrt(families.length));
    const spacingX = (width / cols) * 1.3;
    const spacingY = (height / cols) * 1.3;
    const map = new Map();
    families.forEach((f, i) => {
      map.set(f, {
        x: (i % cols) * spacingX + spacingX / 2,
        y: Math.floor(i / cols) * spacingY + spacingY / 2,
      });
    });
    return map;
  }

  let familyCenters = computeFamilyCenters();

  const linkG = g.append("g");
  const nodeG = g.append("g");
  const textG = g.append("g");

  const link = linkG
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke", "#999")
    .attr("stroke-width", (d) => linkWidth(d.value ?? 1))
    .attr("stroke-opacity", (d) => linkOpacity(d.value ?? 1));

  const NODE_R = 10;

  const node = nodeG
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", NODE_R)
    .attr("fill", (d) => color(d.family ?? d.id))
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

  const neighbors = (() => {
    const map = new Map();
    nodes.forEach((n) => map.set(n.id, new Set([n.id])));
    links.forEach(({ source, target }) => {
      map.get(source).add(target);
      map.get(target).add(source);
    });
    return map;
  })();

  const tooltip = d3
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

  const idOf = (v) => (typeof v === "object" ? v.id : v);

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

  const sim = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3
        .forceLink(links)
        .id((d) => d.id)
        .distance(260)
        .strength(0.15),
    )
    .force("charge", d3.forceManyBody().strength(-220))
    .force("collide", d3.forceCollide().radius(NODE_R + 12))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force(
      "familyX",
      d3
        .forceX((d) => familyCenters.get(d.family ?? d.id)?.x ?? width / 2)
        .strength(0.12),
    )
    .force(
      "familyY",
      d3
        .forceY((d) => familyCenters.get(d.family ?? d.id)?.y ?? height / 2)
        .strength(0.12),
    )
    .alphaDecay(0.04)
    .on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
      label.attr("x", (d) => d.x + NODE_R + 4).attr("y", (d) => d.y + 4);
    });

  node.call(drag(sim));

  function zoomToFit() {
    const bounds = g.node().getBBox();
    const scale = Math.min(
      16,
      0.9 / Math.max(bounds.width / width, bounds.height / height),
    );
    const tx = width / 2 - (bounds.x + bounds.width / 2) * scale;
    const ty = height / 2 - (bounds.y + bounds.height / 2) * scale;
    svg
      .transition()
      .duration(700)
      .call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
  }

  setTimeout(zoomToFit, 700);

  window.addEventListener("resize", () => {
    width = +svg.style("width").replace("px", "");
    height = +svg.style("height").replace("px", "");
    familyCenters = computeFamilyCenters();
    sim
      .force("center", d3.forceCenter(width / 2, height / 2))
      .alpha(0.4)
      .restart();
  });
});
