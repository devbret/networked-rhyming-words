import { familyOf } from "./data.js";
import { NODE_R } from "./render.js";
import { size } from "./stage.js";

function computeFamilyCenters(families) {
  const cols = Math.ceil(Math.sqrt(families.length));
  const spacingX = (size.width / cols) * 1.3;
  const spacingY = (size.height / cols) * 1.3;
  const map = new Map();
  families.forEach((f, i) => {
    map.set(f, {
      x: (i % cols) * spacingX + spacingX / 2,
      y: Math.floor(i / cols) * spacingY + spacingY / 2,
    });
  });
  return map;
}

export function createLayout(nodes, links, families) {
  let familyCenters = computeFamilyCenters(families);

  const simulation = d3
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
    .force("center", d3.forceCenter(size.width / 2, size.height / 2))
    .force(
      "familyX",
      d3
        .forceX((d) => familyCenters.get(familyOf(d))?.x ?? size.width / 2)
        .strength(0.12),
    )
    .force(
      "familyY",
      d3
        .forceY((d) => familyCenters.get(familyOf(d))?.y ?? size.height / 2)
        .strength(0.12),
    )
    .alphaDecay(0.04);

  function resize() {
    familyCenters = computeFamilyCenters(families);
    simulation
      .force("center", d3.forceCenter(size.width / 2, size.height / 2))
      .alpha(0.4)
      .restart();
  }

  return { simulation, resize };
}
