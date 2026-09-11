import { animate } from "motion";
import { TL } from "../content";
import { S, hooks } from "../deck";

let tlI = 0;

function strip(s: string): string {
  return s.replace(/<[^>]+>/g, "");
}

export function tlShow(i: number): void {
  tlI = i;
  const n = TL[i];
  const card = document.getElementById("tlcard");
  if (card !== null) {
    animate(card, { opacity: [1, 0], x: [0, -26] }, { duration: 0.16 })
      .finished.then(() => {
        card.innerHTML =
          `<h3 class="acc" style="margin:0 0 12px;font-size:36px">${n.title} (${n.year})</h3>` +
          `<p style="margin:0;font-size:34px;line-height:1.4">${n.claim}</p>`;
        animate(card, { opacity: [0, 1], x: [26, 0] }, { duration: 0.28 });
        const h3 = card.querySelector("h3");
        if (h3 !== null) animate(h3, { scale: [0.96, 1] }, { type: "spring", stiffness: 300, damping: 18 });
      })
      .catch(() => {
        card.innerHTML =
          `<h3 class="acc" style="margin:0 0 12px;font-size:36px">${n.title} (${n.year})</h3>` +
          `<p style="margin:0;font-size:34px;line-height:1.4">${n.claim}</p>`;
      });
  }
  document.querySelectorAll("#timeline .tln").forEach((g, j) => {
    const on = j <= i;
    const cur = j === i;
    const c = g.querySelector("circle");
    c?.setAttribute("fill", on ? "#f5b638" : "#121923");
    c?.setAttribute("stroke", cur ? "#fff" : on ? "#f5b638" : "#8b98a8");
    if (cur && c instanceof SVGCircleElement) {
      c.style.transformOrigin = `${c.getAttribute("cx")}px 150px`;
      animate(c, { scale: [1, 1.25, 1] }, { duration: 0.5 });
    }
    g.querySelectorAll("text").forEach((t) =>
      t.setAttribute("fill", cur ? "#f5b638" : on ? "#e8edf2" : "#8b98a8"),
    );
  });
}

export function initTimeline(): void {
  const s = document.getElementById("timeline");
  if (!(s instanceof SVGSVGElement)) return;
  let h =
    `<defs><linearGradient id="tlgrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3b7bd6"/><stop offset="1" stop-color="#f5b638"/></linearGradient>` +
    `<filter id="tlglow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>` +
    `<rect x="60" y="142" width="1560" height="16" rx="8" fill="#141d29"/>` +
    `<line x1="60" y1="150" x2="1620" y2="150" stroke="url(#tlgrad)" stroke-width="6" filter="url(#tlglow)"/>`;
  TL.forEach((n, i) => {
    const x = 110 + i * (1500 / (TL.length - 1));
    const up = i % 2 === 0;
    h +=
      `<g class="tln" data-i="${i}" tabindex="0" role="button" aria-label="${strip(n.title)} ${n.year}" style="cursor:pointer">` +
      `<circle cx="${x}" cy="150" r="20" fill="#121923" stroke="#8b98a8" stroke-width="4"/>` +
      `<text x="${x}" y="${up ? 95 : 225}" text-anchor="middle" fill="#8b98a8" font-size="24" font-weight="700">${n.year}</text>` +
      `<text x="${x}" y="${up ? 60 : 260}" text-anchor="middle" fill="#8b98a8" font-size="20">${strip(n.title).split(" · ")[0]}</text></g>`;
  });
  s.innerHTML = h;
  s.querySelectorAll(".tln").forEach((g) => {
    const go = (): void => tlShow(Number((g as SVGGElement).dataset.i));
    (g as SVGGElement).addEventListener("click", go);
    (g as SVGGElement).addEventListener("keydown", (e: Event) => {
      if ((e as KeyboardEvent).key === "Enter") go();
    });
  });
  hooks.enter[S("s-tl")] = () => tlShow(0);
  hooks.step[S("s-tl")] = () => {
    if (tlI < TL.length - 1) {
      tlShow(tlI + 1);
      return true;
    }
    return false;
  };
}
