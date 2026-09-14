import { MATRIX_ARMS, MATRIX_TASKS, MATRIX_TIERS } from "../content";
import { S, hooks } from "../deck";

export function initMatrix(): void {
  const m = document.getElementById("matrix");
  if (m === null) return;
  m.style.gridTemplateColumns = "190px repeat(9,1fr)";
  let h = "";
  MATRIX_TIERS.forEach((tier) => {
    h += `<div class="hdr" style="grid-column:1/-1;justify-content:flex-start;color:#f5b638">${tier}</div><div class="hdr"></div>`;
    for (let t = 1; t <= MATRIX_TASKS; t++) h += `<div class="hdr">U${t}</div>`;
    MATRIX_ARMS.forEach((a) => {
      h += `<div class="hdr" style="justify-content:flex-end;padding-right:10px;color:#e8edf2">${a}</div>`;
      for (let t = 1; t <= MATRIX_TASKS; t++)
        h += `<button class="cell" data-a="${a}" data-t="${t}" data-tier="${tier}" aria-label="${a}, unidade ${t}, ${tier}">n ≥ 3</button>`;
    });
  });
  m.innerHTML = h;
  m.querySelectorAll(".cell").forEach((c) => {
    const cell = c as HTMLButtonElement;
    cell.onclick = () => {
      m.querySelectorAll(".cell").forEach((x) => x.classList.remove("sel"));
      cell.classList.add("sel");
      const info = document.getElementById("cellinfo");
      if (info !== null) {
        info.innerHTML = `Célula (<b>${cell.dataset.a}</b>, ${cell.dataset.tier}), unidade U${cell.dataset.t}: n ≥ 3 construções completas após descartes; tokens da unidade como mediana com dispersão; pareada com a mesma unidade do outro braço no mesmo nível.`;
      }
    };
  });
  hooks.enter[S("s-matrix")] = () => {
    const cells = [...m.querySelectorAll(".cell")];
    cells.forEach((c) => c.classList.remove("on"));
    cells.forEach((c, i) => window.setTimeout(() => c.classList.add("on"), i * 18));
  };
}

export function initClassification(): void {
  // Flip/reveal dos cinco eixos: entram com rotação 3D, saem do giro ao revelar.
  const cards = [...document.querySelectorAll<HTMLElement>("#s-class .axes .card")];
  // Revelação escalonada quando o slide abre.
  const idx = [...document.querySelectorAll(".slide")].findIndex((s) => s.id === "s-class");
  const prev = hooks.enter[idx];
  hooks.enter[idx] = () => {
    if (prev !== undefined) prev();
    cards.forEach((c, i) => {
      c.classList.remove("on");
      window.setTimeout(() => c.classList.add("on"), 150 + i * 130);
    });
  };
}
