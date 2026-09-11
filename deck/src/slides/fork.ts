import { L1 } from "../content";
import { S, hooks } from "../deck";

function fmt(n: number): string {
  return n.toLocaleString("pt-BR");
}

export function initFork(): void {
  const s = document.getElementById("forksvg");
  if (!(s instanceof SVGSVGElement)) return;
  const x0 = 90;
  const y0 = 500;
  const w = 660;
  const hh = 240;
  const max = 70000;
  let h =
    `<defs>` +
    `<marker id="arr" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12z" fill="#f5b638"/></marker>` +
    `<linearGradient id="api" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9cc2f5"/><stop offset="1" stop-color="#3b7bd6" stop-opacity=".15"/></linearGradient>` +
    `<linearGradient id="aomp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe19a"/><stop offset="1" stop-color="#f5b638" stop-opacity=".15"/></linearGradient>` +
    `</defs>` +
    `<rect x="40" y="40" width="300" height="110" rx="16" fill="#121923" stroke="#3b7bd6" stroke-width="3"/>` +
    `<text x="190" y="85" text-anchor="middle" fill="#fff" font-size="34" font-weight="700">pi</text>` +
    `<text x="190" y="125" text-anchor="middle" fill="#8b98a8" font-size="22">${fmt(L1.pi.first)} bytes · ${L1.pi.schemas} esquemas</text>` +
    `<line id="forkedge" x1="345" y1="95" x2="440" y2="95" stroke="#f5b638" stroke-width="4" marker-end="url(#arr)" stroke-dasharray="8 8"/>` +
    `<text x="392" y="70" text-anchor="middle" fill="#f5b638" font-size="20">fork</text>` +
    `<rect x="460" y="40" width="300" height="110" rx="16" fill="#121923" stroke="#f5b638" stroke-width="3"/>` +
    `<text x="610" y="85" text-anchor="middle" fill="#fff" font-size="34" font-weight="700">oh-my-pi</text>` +
    `<text x="610" y="125" text-anchor="middle" fill="#8b98a8" font-size="22">${fmt(L1.omp.first)} bytes · ${L1.omp.schemas} esquemas</text>` +
    `<text x="400" y="200" text-anchor="middle" fill="#e8edf2" font-size="26">1ª requisição: <tspan fill="#f5b638" font-weight="700">11,4×</tspan> os bytes, <tspan fill="#f5b638" font-weight="700">13,6×</tspan> os tokens (16.714 vs 1.228)</text>` +
    `<text x="400" y="245" text-anchor="middle" fill="#8b98a8" font-size="22">bytes por requisição, passos 0–4 (medição própria, Camada 1)</text>`;
  for (const v of [0, 20000, 40000, 60000]) {
    const y = y0 - (v / max) * hh;
    h +=
      `<line x1="${x0}" y1="${y}" x2="${x0 + w}" y2="${y}" stroke="#243040"/>` +
      `<text x="${x0 - 8}" y="${y + 7}" text-anchor="end" fill="#8b98a8" font-size="18">${v / 1000}k</text>`;
  }
  const series: { key: "pi" | "omp"; col: string }[] = [
    { key: "pi", col: "#3b7bd6" },
    { key: "omp", col: "#f5b638" },
  ];
  series.forEach(({ key, col }) => {
    const pts = L1[key].steps.map((v, i) => [x0 + 40 + (i * (w - 80)) / 4, y0 - (v / max) * hh] as const);
    const line = pts.map((p) => p.join(",")).join(" ");
    const area =
      `M${pts[0][0]},${y0} ` + pts.map((p) => `L${p[0]},${p[1]}`).join(" ") + ` L${pts[4][0]},${y0} Z`;
    h += `<path d="${area}" fill="url(#a${key})" opacity=".55"/>`;
    h += `<polyline class="grow" data-k="${key}" points="${line}" fill="none" stroke="${col}" stroke-width="5" stroke-linecap="round" stroke-dasharray="1200" stroke-dashoffset="1200"/>`;
    pts.forEach((p, i) => {
      const v = L1[key].steps[i];
      h +=
        `<circle cx="${p[0]}" cy="${p[1]}" r="8" fill="${col}" stroke="#0b0f14" stroke-width="2"><title>${key === "pi" ? "pi" : "oh-my-pi"} · passo ${i}: ${fmt(v)} bytes</title></circle>` +
        `<text x="${p[0]}" y="${y0 + 30}" text-anchor="middle" fill="#8b98a8" font-size="18">${i}</text>`;
    });
    const last = pts[4];
    h += `<text x="${last[0]}" y="${last[1] + (key === "pi" ? -18 : 36)}" text-anchor="end" fill="${col}" font-size="22">${key === "pi" ? "pi" : "oh-my-pi"}</text>`;
  });
  s.innerHTML = h;
  // Aresta animada (fluxo pi -> oh-my-pi).
  let edgeT: number | null = null;
  const flowEdge = (): void => {
    const e = s.querySelector("#forkedge");
    if (e === null) return;
    let off = 0;
    if (edgeT !== null) cancelAnimationFrame(edgeT);
    const step = (): void => {
      off = (off + 1) % 32;
      e.setAttribute("stroke-dashoffset", String(-off));
      edgeT = requestAnimationFrame(step);
    };
    step();
  };
  flowEdge();
  hooks.enter[S("s-hip")] = () => {
    s.querySelectorAll(".grow").forEach((p) => {
      const el = p as SVGPolylineElement;
      el.style.transition = "none";
      el.style.strokeDashoffset = "1200";
      window.setTimeout(() => {
        el.style.transition = "stroke-dashoffset 1.6s cubic-bezier(.2,.8,.2,1)";
        el.style.strokeDashoffset = "0";
      }, 80);
    });
  };
}
