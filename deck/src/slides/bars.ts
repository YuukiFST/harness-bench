import { animate, stagger } from "motion";
import { FH } from "../content";
import { S, hooks } from "../deck";

function fmtUS(v: number): string {
  return "US$ " + v.toFixed(2).replace(".", ",");
}
function fmtPct(v: number): string {
  return v.toFixed(1).replace(".", ",") + " %";
}

export function initBars(): void {
  const box = document.getElementById("bars");
  const tip = document.getElementById("barstooltip");
  if (box === null) return;
  box.innerHTML = "";
  const maxCost = Math.max(...FH.map((r) => r.costPerPass));
  // Grade discreta de referência (0, 5, 10, 15, 20 US$).
  const grid = document.createElement("div");
  grid.className = "bargrid";
  grid.style.cssText = "position:relative;height:0;margin:0 0 6px 320px;font-size:20px;color:var(--mute)";
  grid.innerHTML = [0, 5, 10, 15, 20]
    .map((v) => `<span style="position:absolute;left:${(v / 20) * 80}%">| ${v}</span>`)
    .join("");
  box.appendChild(grid);

  FH.forEach((row) => {
    const r = document.createElement("div");
    r.className = "barrow";
    r.tabIndex = 0;
    r.setAttribute(
      "aria-label",
      `${row.name}, aprovação ${fmtPct(row.pass)}, ${fmtUS(row.costPerPass)} por tarefa concluída`,
    );
    const wCost = (row.costPerPass / maxCost) * 80;
    r.innerHTML =
      `<div class="barname">${row.name}</div>` +
      `<div class="barwrap">` +
      [0, 25, 50, 75].map((p) => `<span class="grid-line" style="left:${p}%"></span>`).join("") +
      `<div class="bar cost" style="--w:${wCost}%" data-c="${row.costPerPass}"><span>US$ 0,00</span></div>` +
      `<div class="bar pass" style="--w:${row.pass}%" data-w="${row.pass}"></div>` +
      // Linha de referência: mediana do custo por tarefa.
      `</div><div class="mute">${fmtPct(row.pass)}</div>`;
    const show = (): void => {
      if (tip === null) return;
      const denom = `FrontierHarness · Kimi K3 · 30 tarefas · 1 tentativa/célula · set. 2026`;
      tip.innerHTML =
        `<b style="color:var(--acc)">${row.name}</b> · pass ${fmtPct(row.pass)} · ` +
        `<b>${fmtUS(row.costPerPass)}</b>/tarefa · ${denom}`;
      const rect = (r.querySelector(".barwrap") as HTMLElement).getBoundingClientRect();
      const stage = document.getElementById("stage")?.getBoundingClientRect();
      if (stage !== undefined) {
        tip.style.left = rect.left - stage.left + rect.width * 0.35 + "px";
        tip.style.top = rect.top - stage.top - 64 + "px";
      }
      tip.style.opacity = "1";
    };
    const hide = (): void => {
      if (tip !== null) tip.style.opacity = "0";
    };
    r.addEventListener("mouseenter", show);
    r.addEventListener("focus", show);
    r.addEventListener("mouseleave", hide);
    r.addEventListener("blur", hide);
    box.appendChild(r);
  });
  // Linha de referência vertical da mediana (US$ 3,28).
  const ref = document.createElement("div");
  ref.className = "mute";
  ref.style.cssText = "margin:6px 0 0 320px;font-size:20px";
  ref.innerHTML = `— referência: mediana US$ 3,28 por tarefa concluída`;
  box.appendChild(ref);

  hooks.enter[S("s-bars")] = () => {
    const costs = [...box.querySelectorAll<HTMLElement>(".bar.cost")];
    const passes = [...box.querySelectorAll<HTMLElement>(".bar.pass")];
    costs.forEach((b) => {
      b.style.width = "0";
    });
    passes.forEach((b) => {
      b.style.width = "0";
    });
    animate(costs, { width: ["0%", "var(--w)"] }, { duration: 1.1, delay: stagger(0.09) });
    // Compatibilidade com o contrato: largura final também via style.width.
    costs.forEach((b, i) => {
      window.setTimeout(
        () => {
          b.style.width = b.style.getPropertyValue("--w");
        },
        1200 + i * 90,
      );
    });
    passes.forEach((b, i) => {
      window.setTimeout(
        () => {
          b.style.width = Number(b.dataset.w ?? "0") * 0.8 + "%";
        },
        200 + i * 90,
      );
    });
    const t0 = performance.now();
    const tick = (): void => {
      const u = Math.min(1, (performance.now() - t0) / 1200);
      const e = 1 - Math.pow(1 - u, 3);
      box.querySelectorAll(".bar.cost").forEach((b) => {
        const c = Number((b as HTMLElement).dataset.c ?? "0");
        const span = b.firstElementChild;
        if (span !== null) span.textContent = fmtUS(c * e);
      });
      if (u < 1) requestAnimationFrame(tick);
      else {
        // Claude Code destacado ao final da animação.
        const rows = [...box.querySelectorAll(".barrow")];
        rows.forEach((x) => x.classList.remove("hl"));
        const last = rows[rows.length - 1];
        if (last !== undefined) last.classList.add("hl");
      }
    };
    requestAnimationFrame(tick);
  };
}
