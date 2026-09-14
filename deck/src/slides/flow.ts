import { S, hooks } from "../deck";

let layer = 1;
let flowRaf = 0;
let tokCount = 0;

interface Pk {
  t0: number;
  dir: 1 | -1;
  back?: boolean;
}

export function initFlow(): void {
  const s = document.getElementById("flow");
  if (!(s instanceof SVGSVGElement)) return;
  const nodes: [string, string, number][] = [
    ["harness", "Harness", 150],
    ["proxy", "Proxy reverso", 560],
    ["gw", "Gateway", 970],
    ["model", "Modelo", 1380],
  ];
  let h =
    `<defs><marker id="a2" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="#8b98a8"/></marker>` +
    `<linearGradient id="pipe" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3b7bd6"/><stop offset=".5" stop-color="#f5b638"/><stop offset="1" stop-color="#7bd88f"/></linearGradient></defs>`;
  nodes.forEach(([id, n, x]) => {
    h +=
      `<g id="fn-${id}"><rect x="${x - 130}" y="130" width="260" height="120" rx="18" fill="#121923" stroke="#243040" stroke-width="4" style="filter:drop-shadow(0 10px 22px rgba(0,0,0,.5))"/>` +
      `<text x="${x}" y="202" text-anchor="middle" fill="#fff" font-size="32" font-weight="700" class="lbl">${n}</text></g>`;
  });
  for (let i = 0; i < 3; i++) {
    const x1 = nodes[i][2] + 130;
    const x2 = nodes[i + 1][2] - 130;
    h +=
      `<rect x="${x1}" y="162" width="${x2 - x1}" height="16" rx="8" fill="#141d29"/>` +
      `<line x1="${x1}" y1="170" x2="${x2}" y2="170" stroke="url(#pipe)" stroke-width="5" marker-end="url(#a2)"/>` +
      `<line x1="${x2}" y1="210" x2="${x1}" y2="210" stroke="#8b98a8" stroke-width="3" marker-end="url(#a2)"/>`;
  }
  h +=
    `<g id="pk"></g>` +
    `<text id="tokc" x="840" y="360" text-anchor="middle" fill="#f5b638" font-size="34" font-weight="700">tokens contados no proxy: 0</text>` +
    `<text id="mocklbl" x="1380" y="310" text-anchor="middle" fill="#7bd88f" font-size="26"></text>` +
    `<text x="150" y="310" text-anchor="middle" fill="#8b98a8" font-size="22">braço sob teste</text>` +
    `<text x="970" y="310" text-anchor="middle" fill="#8b98a8" font-size="22">OpenCode Zen · verificação cruzada</text>` +
    `<text id="ltitle" x="840" y="440" text-anchor="middle" fill="#fff" font-size="40" font-weight="700"></text>` +
    `<text id="lsub" x="840" y="490" text-anchor="middle" fill="#8b98a8" font-size="26"></text>`;
  s.innerHTML = h;

  // Pacotes do LLM Wiki (slide 8): fluxo entre as 4 etapas.
  const wiki = document.getElementById("wikiflow");
  let wikiPk: SVGCircleElement[] = [];
  if (wiki instanceof SVGSVGElement) {
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("id", "wikipk");
    wiki.appendChild(g);
    for (let k = 0; k < 5; k++) {
      const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      c.setAttribute("r", "8");
      c.setAttribute("class", "wikipk");
      g.appendChild(c);
      wikiPk.push(c);
    }
  }

  function setLayer(l: number): void {
    layer = l;
    tokCount = 0;
    const title = document.getElementById("ltitle");
    const sub = document.getElementById("lsub");
    const mock = document.getElementById("mocklbl");
    if (title !== null)
      title.textContent = l === 1 ? "Camada 1 · endpoint simulado" : "Camada 2 · modelo real";
    if (sub !== null)
      sub.textContent =
        l === 1
          ? "nada chega ao modelo · conta esquemas, bytes de prompt e tokens por passo · determinística"
          : "construção do produto · proxy reverso conta cada requisição · estocástica, n ≥ 3 por célula";
    if (mock !== null) mock.textContent = l === 1 ? "substituído por endpoint simulado" : "";
    const m = document.querySelector("#fn-model rect");
    m?.setAttribute("stroke", l === 1 ? "#7bd88f" : "#f5b638");
    if (l === 1) m?.setAttribute("stroke-dasharray", "14 10");
    else m?.removeAttribute("stroke-dasharray");
    const lbl = document.querySelector("#fn-model .lbl");
    if (lbl !== null) lbl.textContent = l === 1 ? "Mock" : "Modelo";
    const gw = document.querySelector("#fn-gw rect");
    gw?.setAttribute("opacity", l === 1 ? "0.3" : "1");
    // Morph do último nó: escala + crossfade Mock <-> Modelo.
    const modelG = document.getElementById("fn-model");
    if (modelG !== null) {
      modelG.style.transition = "transform .45s cubic-bezier(.2,.8,.2,1), opacity .3s";
      modelG.style.transformOrigin = "1380px 190px";
      modelG.style.transform = "scale(.92)";
      modelG.style.opacity = ".4";
      window.setTimeout(() => {
        modelG.style.transform = "scale(1)";
        modelG.style.opacity = "1";
      }, 60);
    }
    document.getElementById("l1card")?.classList.toggle("hi", l === 1);
    document.getElementById("l2card")?.classList.toggle("hi", l === 2);
  }

  const pk: Pk[] = [];
  function anim(): void {
    const g = document.getElementById("pk");
    const t = performance.now() / 1000;
    const x0 = 280;
    const end = (layer === 1 ? 560 : 1380) - 130;
    if (Math.random() < 0.06) pk.push({ t0: t, dir: 1 });
    let out = "";
    for (let i = pk.length - 1; i >= 0; i--) {
      const p = pk[i];
      const u = (t - p.t0) / 1.6;
      if (u >= 1) {
        pk.splice(i, 1);
        if (p.dir > 0) tokCount += Math.floor(180 + Math.random() * 400);
        continue;
      }
      const seg = (x: number): boolean => {
        const gaps: [number, number][] = [
          [430, 690],
          [840, 1100],
        ];
        return gaps.some(([a, b]) => x > a && x < b);
      };
      const x = p.dir > 0 ? x0 + (end - x0) * u : end - (end - x0) * u;
      if (layer === 2 && seg(x)) continue;
      // Rastro: círculo principal + eco desvanecido.
      const trail = 26 * (1 - u);
      out += `<circle cx="${x - (p.dir > 0 ? trail : -trail)}" cy="${p.dir > 0 ? 170 : 210}" r="4" fill="#f5b638" opacity=".35"/>`;
      out += `<circle cx="${x}" cy="${p.dir > 0 ? 170 : 210}" r="9" fill="#f5b638" style="filter:drop-shadow(0 0 8px #f5b638)"/>`;
      if (u > 0.5 && p.back !== true) {
        p.back = true;
        pk.push({ t0: t, dir: -1, back: true });
      }
    }
    if (g !== null) g.innerHTML = out;
    const tok = document.getElementById("tokc");
    // Contador acelera na Camada 2 (mais tráfego até o modelo real).
    if (tok !== null) tok.textContent = "tokens contados no proxy: " + tokCount.toLocaleString("pt-BR");
    // Pacotes do LLM Wiki derivam do mesmo relógio.
    wikiPk.forEach((c, k) => {
      const u = (t * 0.25 + k / wikiPk.length) % 1;
      const x = 355 + u * (1210 - 355);
      c.setAttribute("cx", String(x));
      c.setAttribute("cy", "60");
      c.setAttribute("opacity", u > 0.02 && u < 0.98 ? "1" : "0");
    });
    const slides = document.querySelectorAll(".slide");
    if (slides[S("s-flow")]?.classList.contains("active") === true) flowRaf = requestAnimationFrame(anim);
  }

  hooks.enter[S("s-flow")] = () => {
    setLayer(1);
    cancelAnimationFrame(flowRaf);
    anim();
  };
  hooks.leave[S("s-flow")] = () => cancelAnimationFrame(flowRaf);
  hooks.step[S("s-flow")] = () => {
    if (layer === 1) {
      setLayer(2);
      return true;
    }
    return false;
  };
}
