import { animate } from "motion";

function num(id: string): number {
  return Number((document.getElementById(id) as HTMLInputElement).value);
}

const diff = [0.6, 0.8, 0.9, 1.0, 1.1, 1.25, 1.4, 1.55, 1.7];
const CRIT: Record<number, number> = { 9: 5, 8: 3, 7: 2, 6: 0 };

function succ(p: number, tk: number): number {
  return (p * 1e6) / (tk * 1000);
}

function wilcoxon(d: number[]): { W: number; n: number } {
  const nz = d.filter((x) => Math.abs(x) > 1e-9);
  const ranked: { x: number; a: number; r?: number }[] = nz
    .map((x) => ({ x, a: Math.abs(x) }))
    .sort((a, b) => a.a - b.a);
  let i = 0;
  while (i < ranked.length) {
    let j = i;
    while (j < ranked.length - 1 && Math.abs(ranked[j + 1].a - ranked[i].a) < 1e-9) j++;
    const r = (i + j) / 2 + 1;
    for (let k = i; k <= j; k++) ranked[k].r = r;
    i = j + 1;
  }
  let wp = 0;
  let wm = 0;
  ranked.forEach((o) => {
    if (o.x > 0) wp += o.r ?? 0;
    else wm += o.r ?? 0;
  });
  return { W: Math.min(wp, wm), n: nz.length };
}

function paintFill(input: HTMLInputElement): void {
  const pct = ((Number(input.value) - Number(input.min)) / (Number(input.max) - Number(input.min))) * 100;
  input.style.setProperty("--fill", pct + "%");
}

export function initSucc(): void {
  const upd = (): void => {
    const pa = num("pa") / 100;
    const pb = num("pb") / 100;
    const ta = num("ta");
    const tb = num("tb");
    (document.getElementById("pav") as HTMLElement).textContent = pa.toFixed(2).replace(".", ",");
    (document.getElementById("pbv") as HTMLElement).textContent = pb.toFixed(2).replace(".", ",");
    (document.getElementById("tav") as HTMLElement).textContent = ta + " k";
    (document.getElementById("tbv") as HTMLElement).textContent = tb + " k";
    const sa = succ(pa, ta);
    const sb = succ(pb, tb);
    const saEl = document.getElementById("sa") as HTMLElement;
    const sbEl = document.getElementById("sb") as HTMLElement;
    // Transição suave de posição/valor ao mover os controles.
    animate(saEl, { scale: [1.12, 1] }, { duration: 0.25 });
    saEl.textContent = sa.toFixed(2).replace(".", ",");
    sbEl.textContent = sb.toFixed(2).replace(".", ",");
    const A = diff.map((d) => sa / d);
    const B = diff.map((d) => sb / d);
    const D = A.map((a, i) => a - B[i]);
    const w = wilcoxon(D);
    const crit = CRIT[w.n] ?? -1;
    const sig = w.n >= 6 && w.W <= crit;
    const wres = document.getElementById("wres") as HTMLElement;
    wres.innerHTML =
      w.n < 6
        ? "n &lt; 6"
        : `W = ${w.W}, ${sig ? '<span style="color:#7bd88f">p &lt; 0,05</span>' : '<span style="color:#ef6b6b">não significativo</span>'}`;
    animate(wres, { scale: [1.08, 1] }, { duration: 0.3 });

    const svg = document.getElementById("wsvg");
    if (!(svg instanceof SVGSVGElement)) return;
    const mx = Math.max(...A, ...B, 0.01);
    let h =
      '<text x="380" y="30" text-anchor="middle" fill="#8b98a8" font-size="22">Succ/Mtok por unidade · A (âmbar) vs B (azul)</text>';
    for (let i = 0; i < 9; i++) {
      const y = 64 + i * 49;
      const xa = 120 + (A[i] / mx) * 560;
      const xb = 120 + (B[i] / mx) * 560;
      const good = D[i] > 0;
      h +=
        `<text x="100" y="${y + 8}" text-anchor="end" fill="#8b98a8" font-size="22">U${i + 1}</text>` +
        `<line x1="120" y1="${y}" x2="680" y2="${y}" stroke="#1a2432" stroke-width="2"/>` +
        `<line x1="${xa}" y1="${y}" x2="${xb}" y2="${y}" stroke="${good ? "#7bd88f" : "#ef6b6b"}" stroke-width="6" stroke-linecap="round"><title>U${i + 1}: A ${A[i].toFixed(2)} vs B ${B[i].toFixed(2)}</title></line>` +
        `<circle cx="${xa}" cy="${y}" r="10" fill="#f5b638" stroke="#0b0f14" stroke-width="2"><title>A · U${i + 1}: ${A[i].toFixed(2)}</title></circle>` +
        `<circle cx="${xb}" cy="${y}" r="10" fill="#3b7bd6" stroke="#0b0f14" stroke-width="2"><title>B · U${i + 1}: ${B[i].toFixed(2)}</title></circle>`;
    }
    h += `<text x="380" y="512" text-anchor="middle" fill="#8b98a8" font-size="20">segmento verde: A &gt; B · vermelho: A &lt; B · postos sinalizados das diferenças</text>`;
    svg.innerHTML = h;
  };
  ["pa", "pb", "ta", "tb"].forEach((id) => {
    const el = document.getElementById(id);
    if (el instanceof HTMLInputElement) {
      paintFill(el);
      el.addEventListener("input", () => {
        paintFill(el);
        upd();
      });
    }
  });
  upd();
}
