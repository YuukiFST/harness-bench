import { S, hooks } from "../deck";

// Slide "Hipóteses": the bars are static SVG in index.html (FrontierHarness,
// Runta 2026); on enter they grow from zero to their data-w width.
export function initFork(): void {
  const s = document.getElementById("forksvg");
  if (!(s instanceof SVGSVGElement)) return;
  hooks.enter[S("s-hip")] = () => {
    s.querySelectorAll<SVGRectElement>(".grow").forEach((r) => {
      const w = r.dataset.w ?? "0";
      r.style.transition = "none";
      r.setAttribute("width", "0");
      window.setTimeout(() => {
        r.style.transition = "width 1.2s cubic-bezier(.2,.8,.2,1)";
        r.setAttribute("width", w);
      }, 80);
    });
  };
}
