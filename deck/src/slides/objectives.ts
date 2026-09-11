import { animate } from "motion";

export function initObjectives(): void {
  const s = document.getElementById("objring");
  if (!(s instanceof SVGSVGElement)) return;
  const R = 200;
  const C = 2 * Math.PI * R;
  let h =
    `<circle cx="300" cy="300" r="${R}" fill="none" stroke="#243040" stroke-width="10"/>` +
    `<circle id="obprog" cx="300" cy="300" r="${R}" fill="none" stroke="url(#obgrad)" stroke-width="10" stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${C}" transform="rotate(-90 300 300)"/>` +
    `<defs><linearGradient id="obgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe19a"/><stop offset="1" stop-color="#f5b638"/></linearGradient></defs>` +
    `<text x="300" y="292" text-anchor="middle" fill="#f5b638" font-size="30" font-weight="700">critério de</text>` +
    `<text x="300" y="330" text-anchor="middle" fill="#f5b638" font-size="30" font-weight="700">escolha</text>` +
    `<text id="obcount" x="300" y="372" text-anchor="middle" fill="#8b98a8" font-size="26">0 / 7</text>`;
  for (let i = 0; i < 7; i++) {
    const a = -Math.PI / 2 + (i * Math.PI * 2) / 7;
    const x = 300 + Math.cos(a) * R;
    const y = 300 + Math.sin(a) * R;
    h +=
      `<g class="obn" id="ob${i}" style="cursor:pointer">` +
      `<circle cx="${x}" cy="${y}" r="42" fill="#121923" stroke="#243040" stroke-width="3"/>` +
      `<text x="${x}" y="${y + 12}" text-anchor="middle" fill="#8b98a8" font-size="34" font-weight="700">${i + 1}</text></g>`;
  }
  s.innerHTML = h;

  const paint = (lit: number): void => {
    for (let i = 0; i < 7; i++) {
      const g = document.getElementById("ob" + i);
      if (g === null) continue;
      const on = i < lit;
      const c = g.querySelector("circle");
      const t = g.querySelector("text");
      c?.setAttribute("stroke", on ? "#f5b638" : "#243040");
      c?.setAttribute("fill", on ? "#f5b638" : "#121923");
      t?.setAttribute("fill", on ? "#000" : "#8b98a8");
    }
    const prog = document.getElementById("obprog");
    const count = document.getElementById("obcount");
    const target = C * (1 - lit / 7);
    if (prog !== null) {
      const from = Number(prog.dataset.v ?? C);
      animate(from, target, {
        duration: 0.7,
        onUpdate: (v: number) => {
          prog.setAttribute("stroke-dashoffset", String(v));
          prog.dataset.v = String(v);
        },
      });
    }
    if (count !== null) {
      count.textContent = lit + " / 7";
      animate(count, { scale: [1.35, 1] }, { type: "spring", stiffness: 300, damping: 14 });
    }
  };

  const items = [...document.querySelectorAll<HTMLElement>("#objs li")];
  const obs = new MutationObserver(() => {
    const lit = items.filter((li) => li.classList.contains("on")).length;
    paint(lit);
    // Ligação visual lista <-> nó: o item aceso ganha brilho âmbar.
    items.forEach((li, i) => {
      li.style.textShadow = li.classList.contains("on") ? "0 0 22px rgba(245,182,56,.5)" : "none";
      const g = document.getElementById("ob" + i);
      if (g !== null) g.style.filter = li.classList.contains("on") ? "drop-shadow(0 0 10px #f5b638)" : "none";
    });
  });
  items.forEach((li) => obs.observe(li, { attributes: true }));
  // Clique no nó revela o item correspondente.
  for (let i = 0; i < 7; i++) {
    const g = document.getElementById("ob" + i);
    g?.addEventListener("click", () => {
      items.forEach((li, j) => {
        if (j <= i && !li.classList.contains("on")) {
          li.classList.add("on");
        }
      });
    });
  }
  paint(0);
}
