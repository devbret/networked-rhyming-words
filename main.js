import { buildNeighbors, familyOf, prepareGraph } from "./js/data.js";
import { bindHover, drag } from "./js/interaction.js";
import { createLayout } from "./js/layout.js";
import { positionElements, renderGraph } from "./js/render.js";
import { g, measure, showError, zoomToFit } from "./js/stage.js";
import { createTooltip } from "./js/tooltip.js";

d3.json("network_data.json")
  .then((graph) => {
    const { nodes, links } = prepareGraph(graph);
    const families = Array.from(new Set(nodes.map(familyOf)));

    const view = renderGraph(g, nodes, links, families);
    bindHover(view, buildNeighbors(nodes, links), createTooltip());

    const { simulation, resize } = createLayout(nodes, links, families);
    simulation.on("tick", () => positionElements(view));
    view.node.call(drag(simulation));

    setTimeout(zoomToFit, 700);

    window.addEventListener("resize", () => {
      measure();
      resize();
    });
  })
  .catch((err) => {
    console.error("Failed to load network_data.json:", err);
    showError(
      "Could not load network_data.json — run app.py first to generate it.",
    );
  });
