import { S, hooks } from "../deck";
import { GANTT, GANTT_MONTHS } from "../content";

export function initLimits(): void {
  const s = document.getElementById("invsvg");
  if (s instanceof SVGSVGElement) {
    const tiers: [string, [number, number]][] = [
      ["nível primário", [0.7, 0.45]],
      ["nível de robustez", [0.4, 0.62]],
    ];
    let h =
      '<defs><linearGradient id="invA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe19a"/><stop offset="1" stop-color="#b07f1c"/></linearGradient>' +
      '<linearGradient id="invB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9cc2f5"/><stop offset="1" stop-color="#1d3f73"/></linearGradient></defs>' +
      '<text x="840" y="24" text-anchor="middle" fill="#8b98a8" font-size="22">Succ/Mtok relativo, ilustrativo: a ordem entre os braços A (âmbar) e B (azul) pode inverter entre níveis de modelo</text>';
    tiers.forEach(([name, v], ti) => {
      const x0 = 200 + ti * 840;
      h += `<text x="${x0 + 300}" y="250" text-anchor="middle" fill="#e8edf2" font-size="24" font-weight="700">${name}</text>`;
      // Grade discreta atrás das barras.
      [0.25, 0.5, 0.75].forEach((g) => {
        h += `<line x1="${x0}" y1="${220 - g * 160}" x2="${x0 + 600}" y2="${220 - g * 160}" stroke="#243040" stroke-dasharray="4 6"/>`;
      });
      v.forEach((val, i) => {
        const x = x0 + 80 + i * 300;
        const hh = val * 160;
        h +=
          `<rect class="ib" x="${x}" y="${220 - hh}" width="160" height="${hh}" rx="10" fill="url(#inv${i === 0 ? "A" : "B"})" stroke="#0b0f14" stroke-width="2" style="transform-origin:${x + 80}px 220px;transform:scaleY(0);transition:transform .8s ${0.3 + ti * 0.4}s cubic-bezier(.2,.8,.2,1)"><title>${name} · braço ${i === 0 ? "A" : "B"}: ${val.toFixed(2)} (ilustrativo)</title></rect>` +
          `<text x="${x + 80}" y="${212 - hh}" text-anchor="middle" fill="#e8edf2" font-size="24">${i !== 0 ? "B" : "A"}</text>`;
      });
    });
    h +=
      '<path d="M780,130 C840,60 840,200 900,130" fill="none" stroke="#ef6b6b" stroke-width="4" stroke-dasharray="10 8"/>' +
      '<text x="840" y="105" text-anchor="middle" fill="#ef6b6b" font-size="22">inversão</text>';
    s.innerHTML = h;
    hooks.enter[S("s-lim")] = () =>
      s.querySelectorAll(".ib").forEach((r) => {
        const el = r as SVGRectElement;
        el.style.transform = "scaleY(0)";
        requestAnimationFrame(() => requestAnimationFrame(() => (el.style.transform = "scaleY(1)")));
      });
  }

  // Ícones vetoriais detalhados por limitação (gradiente + brilho, não caixa chapada).
  const icons = [
    `<svg viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="li0" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe19a"/><stop offset="1" stop-color="#f5b638"/></linearGradient></defs><path d="M32 6 L56 52 L8 52 Z" fill="none" stroke="url(#li0)" stroke-width="4" stroke-linejoin="round"/><path d="M32 22 v12" stroke="url(#li0)" stroke-width="5" stroke-linecap="round"/><circle cx="32" cy="42" r="3.4" fill="#f5b638"/></svg>`,
    `<svg viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="li1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9cc2f5"/><stop offset="1" stop-color="#3b7bd6"/></linearGradient></defs><rect x="10" y="10" width="44" height="44" rx="12" fill="none" stroke="url(#li1)" stroke-width="4"/><path d="M20 32 h14 M32 24 v16" stroke="url(#li1)" stroke-width="4" stroke-linecap="round"/><circle cx="44" cy="44" r="7" fill="none" stroke="url(#li1)" stroke-width="3"/><path d="M44 40 v4 M44 47 v.5" stroke="url(#li1)" stroke-width="3" stroke-linecap="round"/></svg>`,
    `<svg viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="li2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b6f0c2"/><stop offset="1" stop-color="#2f9e5f"/></linearGradient></defs><path d="M8 44 L26 20 L38 34 L46 26 L56 44 Z" fill="none" stroke="url(#li2)" stroke-width="4" stroke-linejoin="round"/><line x1="8" y1="52" x2="56" y2="52" stroke="url(#li2)" stroke-width="3" stroke-linecap="round"/></svg>`,
    `<svg viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="li3" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffc9c9"/><stop offset="1" stop-color="#ef6b6b"/></linearGradient></defs><circle cx="24" cy="32" r="14" fill="none" stroke="url(#li3)" stroke-width="4"/><path d="M36 20 h14 M43 20 v24 M43 32 h10" stroke="url(#li3)" stroke-width="4" stroke-linecap="round"/></svg>`,
  ];
  document.querySelectorAll(".limgrid .lim").forEach((card, i) => {
    if (card.querySelector("svg") !== null) return;
    const wrap = document.createElement("span");
    wrap.innerHTML = icons[i % icons.length];
    const svg = wrap.firstElementChild;
    if (svg !== null) card.appendChild(svg);
    (card as HTMLElement).style.paddingRight = "90px";
  });
}

export function initGantt(): void {
  const g = document.getElementById("gantt");
  if (g === null) return;
  let h =
    '<div class="gantt-row"><div></div>' +
    GANTT_MONTHS.map((mm) => `<div class="mute" style="text-align:center">${mm}</div>`).join("") +
    "</div>";
  GANTT.forEach((r, i) => {
    h += `<div class="gantt-row frag" data-i="${i}"><button class="ph">${r.phase}</button>${r.months.map((x) => `<div class="m${x !== 0 ? " x" : ""}"></div>`).join("")}</div>`;
  });
  g.innerHTML = h;
  // Marcador "hoje": setembro 2026 (primeira coluna).
  const marker = document.createElement("div");
  marker.className = "mute";
  marker.style.cssText = "margin:4px 0 0 520px;font-size:20px;color:var(--acc)";
  marker.textContent = "▼ hoje · set. 2026";
  g.appendChild(marker);
  g.querySelectorAll(".gantt-row[data-i]").forEach((r) => {
    const row = r as HTMLElement;
    const btn = row.querySelector(".ph") as HTMLButtonElement;
    btn.onclick = () => {
      g.querySelectorAll(".gantt-row").forEach((x) => {
        x.classList.remove("hi");
        x.querySelectorAll(".m.x").forEach((mm) => mm.classList.remove("hi"));
      });
      row.classList.add("hi");
      row.querySelectorAll(".m.x").forEach((mm) => mm.classList.add("hi"));
    };
    new MutationObserver(() => {
      if (row.classList.contains("on"))
        row
          .querySelectorAll(".m")
          .forEach((mm, k) => window.setTimeout(() => mm.classList.add("on"), k * 90));
      else row.querySelectorAll(".m").forEach((mm) => mm.classList.remove("on"));
    }).observe(row, { attributes: true });
  });
}

export function initRefs(): void {
  // Renderizado em main.ts a partir de REFS; aqui só a entrada escalonada.
  const idx = [...document.querySelectorAll(".slide")].findIndex((s) => s.querySelector("#refs") !== null);
  const prev = hooks.enter[idx];
  hooks.enter[idx] = () => {
    if (prev !== undefined) prev();
    const ps = [...document.querySelectorAll<HTMLElement>("#refs p")];
    ps.forEach((p, i) => {
      p.style.opacity = "0";
      p.style.transform = "translateY(14px)";
      window.setTimeout(() => {
        p.style.transition = "opacity .45s, transform .45s";
        p.style.opacity = "1";
        p.style.transform = "none";
      }, i * 45);
    });
  };
}
