import { animate } from "motion";
import { NOTES } from "./notes";

export type HookMap = Record<number, (() => void) | undefined>;
export type StepMap = Record<number, (() => boolean) | undefined>;

export const hooks: { enter: HookMap; leave: HookMap; step: StepMap } = {
  enter: {},
  leave: {},
  step: {},
};

const slides: HTMLElement[] = [];
let cur = 0;
let helpEl: HTMLElement;
let ovEl: HTMLElement;
let notesEl: HTMLElement;
let progressEl: HTMLElement;
let counterEl: HTMLElement;

export function S(id: string): number {
  return slides.findIndex((s) => s.id === id);
}

export function currentIndex(): number {
  return cur;
}

export function enterCurrent(): void {
  const enter = hooks.enter[cur];
  if (enter !== undefined) enter();
}

function frags(i: number): HTMLElement[] {
  return [...slides[i].querySelectorAll<HTMLElement>(".frag")];
}

function choreographFragment(el: HTMLElement, index: number): void {
  animate(
    el,
    { opacity: [0, 1], y: [18, 0] },
    { type: "spring", stiffness: 260, damping: 26, delay: Math.min(index * 0.06, 0.4) },
  );
}

function transitionSlide(el: HTMLElement, back: boolean): void {
  animate(
    el,
    {
      opacity: [0, 1],
      x: [back ? -90 : 90, 0],
      scale: [0.965, 1],
    },
    { type: "spring", stiffness: 120, damping: 22 },
  );
}

export function showSlide(i: number, revealAll?: boolean): void {
  i = Math.max(0, Math.min(slides.length - 1, i));
  if (hooks.leave[cur] !== undefined) {
    const fn = hooks.leave[cur];
    if (fn !== undefined) fn();
  }
  slides[cur].classList.remove("active", "back");
  const back = i < cur;
  cur = i;
  slides[cur].classList.toggle("back", back);
  slides[cur].classList.add("active");
  const list = frags(cur);
  list.forEach((f, k) => {
    const on = revealAll === true;
    f.classList.toggle("on", on);
    if (on) choreographFragment(f, k);
  });
  transitionSlide(slides[cur], back);
  history.replaceState(null, "", "#" + String(cur + 1));
  progressEl.style.width = ((cur + 1) / slides.length) * 100 + "%";
  counterEl.textContent = cur + 1 + " / " + slides.length;
  notesEl.innerHTML = NOTES[cur] ?? "";
  const enter = hooks.enter[cur];
  if (enter !== undefined) enter();
}

export function next(): void {
  const step = hooks.step[cur];
  if (step !== undefined && step()) return;
  const f = frags(cur).find((x) => !x.classList.contains("on"));
  if (f !== undefined) {
    f.classList.add("on");
    choreographFragment(f, frags(cur).indexOf(f));
    return;
  }
  if (cur < slides.length - 1) showSlide(cur + 1);
}

export function prev(): void {
  if (cur > 0) showSlide(cur - 1, true);
}

export function fit(): void {
  const s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  const stage = document.getElementById("stage");
  if (stage !== null) stage.style.transform = "scale(" + s + ")";
}

function buildOverview(): void {
  const g = ovEl.querySelector(".grid");
  if (g === null) return;
  g.innerHTML = "";
  slides.forEach((s, i) => {
    const d = document.createElement("div");
    d.className = "thumb" + (i === cur ? " cur" : "");
    d.tabIndex = 0;
    const title = s.dataset.title ?? "Slide " + String(i + 1);
    d.innerHTML = "<b>" + String(i + 1) + "</b>" + title;
    const go = (): void => {
      ovEl.classList.remove("on");
      showSlide(i, true);
    };
    d.onclick = go;
    d.onkeydown = (e: KeyboardEvent) => {
      if (e.key === "Enter") go();
    };
    g.appendChild(d);
  });
}

export function initDeck(): void {
  document.querySelectorAll<HTMLElement>(".slide").forEach((s) => slides.push(s));
  helpEl = document.getElementById("help") as HTMLElement;
  ovEl = document.getElementById("overview") as HTMLElement;
  notesEl = document.getElementById("notes") as HTMLElement;
  progressEl = document.getElementById("progress") as HTMLElement;
  counterEl = document.getElementById("counter") as HTMLElement;

  (document.getElementById("next") as HTMLButtonElement).onclick = next;
  (document.getElementById("prev") as HTMLButtonElement).onclick = prev;
  window.addEventListener("resize", fit);
  fit();

  window.addEventListener("keydown", (e: KeyboardEvent) => {
    const t = e.target as HTMLElement | null;
    if (t !== null && t.tagName === "INPUT" && ["ArrowLeft", "ArrowRight", "Home", "End"].includes(e.key))
      return;
    if (t !== null && t.tagName === "BUTTON" && e.key === " ") return;
    const k = e.key;
    if (k === "Escape") {
      helpEl.classList.remove("on");
      ovEl.classList.remove("on");
      return;
    }
    if (k === "?") {
      helpEl.classList.toggle("on");
      return;
    }
    if (k === "o" || k === "O") {
      buildOverview();
      ovEl.classList.toggle("on");
      return;
    }
    if (k === "n" || k === "N") {
      notesEl.classList.toggle("on");
      return;
    }
    if (k === "f" || k === "F") {
      if (document.fullscreenElement !== null) void document.exitFullscreen();
      else void document.documentElement.requestFullscreen();
      return;
    }
    if (ovEl.classList.contains("on") || helpEl.classList.contains("on")) return;
    if (k === "ArrowRight" || k === " " || k === "PageDown") {
      e.preventDefault();
      next();
    } else if (k === "ArrowLeft" || k === "PageUp") {
      e.preventDefault();
      prev();
    } else if (k === "Home") {
      showSlide(0);
    } else if (k === "End") {
      showSlide(slides.length - 1, true);
    } else if (/^[0-5]$/.test(k) && cur === S("s-h3d")) {
      const fn = (window as unknown as { h3select?: (i: number) => void }).h3select;
      if (fn !== undefined) fn(Number(k));
    }
  });

  const start = parseInt((location.hash || "#1").slice(1), 10);
  showSlide(Number.isNaN(start) ? 0 : start - 1, (start || 1) > 1);
}
