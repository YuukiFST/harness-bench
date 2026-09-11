import "@fontsource/space-grotesk/500.css";
import "@fontsource/space-grotesk/700.css";
import "@fontsource/inter/400.css";
import "@fontsource/inter/600.css";
import "./styles.css";
import { enterCurrent, hooks, initDeck } from "./deck";
import { REFS } from "./content";
import { initBars } from "./slides/bars";
import { initObjectives } from "./slides/objectives";
import { initFork } from "./slides/fork";
import { initTimeline } from "./slides/timeline";
import { initFlow } from "./slides/flow";
import { initMatrix, initClassification } from "./slides/matrix";
import { initSucc } from "./slides/succ";
import { initLimits, initGantt, initRefs } from "./slides/details";
import { initCovers } from "./three/cover";
import { initHarness3D } from "./three/harness";
import { animate, stagger } from "motion";

function splitTitles(): void {
  document.querySelectorAll<HTMLElement>(".split").forEach((h) => {
    const words: string[] = [];
    h.childNodes.forEach((n) => {
      if (n.nodeType === 3) {
        (n.textContent ?? "").split(/(\s+)/).forEach((w) => {
          if (w.length > 0) words.push(w);
        });
      } else if (n instanceof HTMLElement) {
        words.push(n.outerHTML);
      }
    });
    h.innerHTML = words.map((w) => (/^\s+$/.test(w) ? w : `<span class="w">${w}</span>`)).join("");
  });
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const ws = (e.target as HTMLElement).querySelectorAll(".w");
        animate(
          ws,
          { opacity: [0, 1], y: [26, 0], rotateX: [35, 0] },
          { delay: stagger(0.05), duration: 0.7 },
        );
        io.unobserve(e.target);
      });
    },
    { threshold: 0.2 },
  );
  document.querySelectorAll(".slide.cover").forEach((s) => {
    const h = s.querySelector(".split");
    if (h !== null) io.observe(h);
  });
}

function renderRefs(): void {
  const el = document.getElementById("refs");
  if (el !== null) el.innerHTML = REFS.map((r) => "<p>" + r + "</p>").join("");
}

// Ordem load-bearing: initDeck() primeiro popula a lista de slides para que
// S('s-...') resolva o índice certo nos hooks.enter/leave/step registrados abaixo.
initDeck();
try {
  renderRefs();
  splitTitles();
  initCovers();
  initBars();
  initHarness3D();
  initObjectives();
  initFork();
  initTimeline();
  initFlow();
  initMatrix();
  initClassification();
  initSucc();
  initLimits();
  initGantt();
  initRefs();
} catch (err) {
  // Sem retry além do fallback 2D do slide 3D: erro aqui é visível no console.
  console.error(err);
}
// Guarda contra regressão da ordem de init: nenhum hook pode mirar índice -1.
if ("-1" in hooks.enter || "-1" in hooks.leave || "-1" in hooks.step) {
  console.error("hook registrado com S() antes de initDeck()");
}
enterCurrent();
