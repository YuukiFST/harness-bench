"""Fourth pass on the deck (2026-09-14): external evidence on the hypotheses slide.

The author asked that the pi vs OpenCode figure next to H1/H2 rest on a source
outside the project's own repository. The Camada 1 curves (layer1/data, own
measurement) leave the slide; the panel now shows the two arms in
FrontierHarness (Runta, 2026: pass rate and median cost per pass on the same
model) for H1, and the per-request footprint of pi reported by Earendil (2026)
and by Databricks apud Earendil ("3x less context per turn") for H2. The
Camada 1 instrument stays in the method slides and in the .docx.

Second change: the LLM Wiki method on the classification slide is attributed
to Karpathy (2026), the gist the method comes from
(https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Applies to dist/apresentacao-pcc.html (exact match) and to deck/ (whitespace-
tolerant match on index.html, exact on the TypeScript). Every pair must match
exactly once.

Usage:
    python tools/slides_edits_2026-09-14d.py
    cd deck && npx prettier --write index.html src && npm run build
"""

from pathlib import Path

_src = Path("tools/deck_edits_2026-09-14.py").read_text(encoding="utf-8")
_ns: dict = {}
exec(compile(_src.split("# --- index.html")[0], "deck_edits_helpers", "exec"), _ns)
_apply = _ns["apply"]


def apply(path: Path, pairs: list, tolerant: bool) -> None:
    """Skip pairs whose replacement is already in the file, so the script can
    be rerun after a partial pass."""
    text = path.read_text(encoding="utf-8")
    ws_pattern = _ns["ws_pattern"]
    present = (lambda n: ws_pattern(n).search(text) is not None) if tolerant else (lambda n: n in text)
    todo = [(o, n) for o, n in pairs if not present(n)]
    if todo:
        _apply(path, todo, tolerant)
    else:
        print(f"{path}: nothing to do")

# FrontierHarness (Runta, 2026), table "Pass Rate / Median Cost Per Pass", Kimi K3
# via Fireworks, 30 tasks, one canonical run per task/harness pair. Ratios are the
# author's arithmetic on those two rows.
PI_PASS, PI_COST = 60.0, 2.43
OC_PASS, OC_COST = 50.0, 3.24
BAR_X, BAR_W = 230, 400
COST_MAX = 4.0


def bar(y: int, w: float, col: str, label: str) -> str:
    return (
        f'<rect class="grow" x="{BAR_X}" y="{y}" width="0" height="26" rx="6" fill="{col}" data-w="{w:.1f}"/>'
        f'<text x="{BAR_X + w + 12:.1f}" y="{y + 19}" fill="#e8edf2" font-size="21">{label}</text>'
    )


def ext_svg() -> str:
    """Static panel, 800x560: FrontierHarness rows for the two arms (H1) and the
    per-request footprint of pi from Earendil (H2). Text widths were checked in
    Chrome at 1920x1080 with the deck fonts; keep lines under ~70 characters."""
    pi_pass_w = BAR_W * PI_PASS / 100
    oc_pass_w = BAR_W * OC_PASS / 100
    pi_cost_w = BAR_W * PI_COST / COST_MAX
    oc_cost_w = BAR_W * OC_COST / COST_MAX
    return (
        '<rect x="40" y="30" width="330" height="110" rx="16" fill="#121923" stroke="#3b7bd6" stroke-width="3"/>'
        '<text x="205" y="75" text-anchor="middle" fill="#fff" font-size="34" font-weight="700">pi</text>'
        '<text x="205" y="115" text-anchor="middle" fill="#8b98a8" font-size="21">60,0 % · US$ 2,43 por aprovada</text>'
        '<text x="400" y="93" text-anchor="middle" fill="#8b98a8" font-size="26">vs</text>'
        '<rect x="430" y="30" width="330" height="110" rx="16" fill="#121923" stroke="#f5b638" stroke-width="3"/>'
        '<text x="595" y="75" text-anchor="middle" fill="#fff" font-size="34" font-weight="700">OpenCode</text>'
        '<text x="595" y="115" text-anchor="middle" fill="#8b98a8" font-size="21">50,0 % · US$ 3,24 por aprovada</text>'
        '<text x="400" y="185" text-anchor="middle" fill="#e8edf2" font-size="25"><tspan fill="#f5b638" font-weight="700">H1</tspan> · mesmo modelo: OpenCode paga <tspan fill="#f5b638" font-weight="700">1,33×</tspan> por tarefa aprovada</text>'
        '<text x="400" y="218" text-anchor="middle" fill="#e8edf2" font-size="25">e aprova <tspan fill="#f5b638" font-weight="700">10 pp</tspan> a menos (cálculo do autor)</text>'
        f'<text x="{BAR_X - 14}" y="266" text-anchor="end" fill="#8b98a8" font-size="21">aprovação</text>'
        + bar(243, pi_pass_w, "#3b7bd6", "pi 60,0 %")
        + bar(275, oc_pass_w, "#f5b638", "OpenCode 50,0 %")
        + f'<text x="{BAR_X - 14}" y="341" text-anchor="end" fill="#8b98a8" font-size="21">US$ / aprovada</text>'
        + bar(318, pi_cost_w, "#3b7bd6", "pi 2,43")
        + bar(350, oc_cost_w, "#f5b638", "OpenCode 3,24")
        + '<text x="400" y="400" text-anchor="middle" fill="#8b98a8" font-size="19">FrontierHarness (Runta, 2026) · Kimi K3 · 30 tarefas · 1 tentativa por célula</text>'
        '<rect x="40" y="420" width="720" height="130" rx="16" fill="#121923" stroke="#243040" stroke-width="2"/>'
        '<text x="70" y="458" fill="#e8edf2" font-size="23"><tspan fill="#f5b638" font-weight="700">H2</tspan> · carga por requisição, fonte externa</text>'
        '<text x="70" y="493" fill="#8b98a8" font-size="19">pi: 4 ferramentas; <tspan fill="#e8edf2">prompt e definições abaixo de 1.000 tokens</tspan> (Earendil, 2026)</text>'
        '<text x="70" y="526" fill="#8b98a8" font-size="19">Databricks apud Earendil (2026): <tspan fill="#e8edf2">«3x less context per turn»,</tspan> custo &gt; 2×</text>'
    )


OLD_SVG_COL = '<div class="col" style="flex:0 0 800px"><svg id="forksvg" viewBox="0 0 800 560" style="width:100%;height:100%"></svg></div>'
NEW_SVG_COL = (
    '<div class="col" style="flex:0 0 800px"><svg id="forksvg" viewBox="0 0 800 560" style="width:100%;height:100%">'
    + ext_svg()
    + "</svg></div>"
)

OLD_DENOM = (
    '<div class="denom">Camada 1, medição própria: primeira requisição da mesma tarefa, endpoint simulado, n = 1 '
    "(determinístico), tokenizador cl100k_base, 28 ago. 2026. pi 0.80.10, OpenCode 1.17.9.</div>"
)
NEW_DENOM = (
    '<div class="denom">H1: FrontierHarness (Runta, 2026), blogue institucional, 1 set. 2026; Kimi K3 via Fireworks, '
    "30 tarefas, 1 tentativa por célula, pi v0.84.2, OpenCode v1.18.19; 1,33× e 10 pp calculados pelo autor. "
    "H2: Earendil (2026), blogue institucional, 4 ago. 2026; Databricks apud Earendil (2026).</div>"
)

# The dist deck renders the old Camada 1 figure from an inline script; the block
# is replaced whole by the bar animation.
DIST_JS_START = "// ---------- slide 6: pi vs OpenCode (Camada 1, layer1/data/first_request.csv e step_growth.csv) ----------"
DIST_JS_NEW = """// ---------- slide 6: pi vs OpenCode (FrontierHarness, Runta 2026; Earendil 2026) ----------
(function(){
  const s=document.getElementById('forksvg');
  hooks.enter[S('s-hip')]=()=>s.querySelectorAll('.grow').forEach(r=>{r.style.transition='none';r.setAttribute('width','0');setTimeout(()=>{r.style.transition='width 1.2s cubic-bezier(.2,.8,.2,1)';r.setAttribute('width',r.dataset.w);},80);});
})();"""

OLD_NOTE_HIP = (
    "Dados do gráfico: layer1/data/first_request.csv e step_growth.csv (pi 5.676 bytes / 1.228 tokens / 4 esquemas; "
    "OpenCode 29.997 bytes / 6.659 tokens / 9 esquemas; 5,3x em bytes, 5,4x em tokens; crescimento por passo 555 vs "
    "698 bytes). Esses números não estão no projeto (proposta descreve o que será feito); estão no repositório."
)
NEW_NOTE_HIP = (
    "Painel da direita, tudo fonte externa: H1 usa as duas linhas do FrontierHarness [26][52] (pi 60,0% / US$ 2,43; "
    "OpenCode 50,0% / US$ 3,24; mesmo modelo Kimi K3 via Fireworks, 30 tarefas, 1 tentativa por célula, versões "
    "pi v0.84.2 e OpenCode v1.18.19 no repositório do eval); 1,33x e 10 pp são conta do autor sobre a tabela. H2 usa "
    "Earendil 2026 (pi: 4 ferramentas, prompt de sistema e definições abaixo de 1.000 tokens) e Databricks apud "
    "Earendil (\"Pi sent about 3x less context per turn\"; custo por tarefa acima de 2x com qualidade igual) [52][60]. "
    "A Camada 1 (medição própria, layer1/data) sai deste slide e fica no método; se perguntarem por números próprios, "
    "eles estão no repositório."
)

# Classification slide: the method is Karpathy's.
OLD_IA_DIST = "Levantamento das fontes com um <em>LLM Wiki</em> no repositório do projeto."
NEW_IA_DIST = "Levantamento das fontes com um <em>LLM Wiki</em> (Karpathy, 2026) no repositório do projeto."
OLD_IA_DECK = "Levantamento e auditoria das fontes com um <em>LLM Wiki</em> no repositório do projeto."
NEW_IA_DECK = "Levantamento e auditoria das fontes com um <em>LLM Wiki</em> (Karpathy, 2026) no repositório do projeto."
OLD_NOTE_IA = "[58]: LLM Wiki no repositório (YuukiFST, 2026b);"
NEW_NOTE_IA = "[58]: LLM Wiki, padrão de Karpathy (2026), instanciado no repositório (YuukiFST, 2026b);"

KARPATHY_REF = (
    '  "KARPATHY, A. <b>LLM Wiki</b>: a pattern for building personal knowledge bases using LLMs. 2026. '
    'Gist (GitHub).",\n'
)


def replace_dist_js(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    start = text.index(DIST_JS_START)
    end = text.index("})();", start) + len("})();")
    if text.count(DIST_JS_START) != 1:
        raise SystemExit(f"{path}: Camada 1 script block not unique")
    path.write_text(text[:start] + DIST_JS_NEW + text[end:], encoding="utf-8")
    print(f"{path}: Camada 1 script replaced")


OLD_SVG_COL_DECK = OLD_SVG_COL.replace("flex:0 0 800px", "flex: 0 0 800px").replace(
    "width:100%;height:100%", "width: 100%; height: 100%"
)
NEW_SVG_COL_DECK = NEW_SVG_COL.replace("flex:0 0 800px", "flex: 0 0 800px").replace(
    "width:100%;height:100%", "width: 100%; height: 100%"
)

dist = Path("dist/apresentacao-pcc.html")
apply(
    dist,
    [
        (OLD_SVG_COL, NEW_SVG_COL),
        (OLD_DENOM, NEW_DENOM),
        (OLD_NOTE_HIP, NEW_NOTE_HIP),
        (OLD_IA_DIST, NEW_IA_DIST),
        (OLD_NOTE_IA, NEW_NOTE_IA),
    ],
    tolerant=False,
)
if DIST_JS_START in dist.read_text(encoding="utf-8"):
    replace_dist_js(dist)

apply(
    Path("deck/index.html"),
    [
        (OLD_SVG_COL_DECK, NEW_SVG_COL_DECK),
        (OLD_DENOM, NEW_DENOM),
        (OLD_IA_DECK, NEW_IA_DECK),
    ],
    tolerant=True,
)
apply(
    Path("deck/src/notes.ts"),
    [(OLD_NOTE_HIP, NEW_NOTE_HIP), (OLD_NOTE_IA, NEW_NOTE_IA)],
    tolerant=False,
)
apply(
    Path("deck/src/content.ts"),
    [
        (
            '  "KAPOOR, S. <em>et al.</em> <b>Holistic Agent Leaderboard</b>. arXiv:2510.11977, 2025. <em>Preprint</em>.",\n',
            '  "KAPOOR, S. <em>et al.</em> <b>Holistic Agent Leaderboard</b>. arXiv:2510.11977, 2025. <em>Preprint</em>.",\n'
            + KARPATHY_REF,
        ),
        # Camada 1 numbers no longer feed a slide; the data block is gone with fork.ts.
        (
            "export interface Layer1Arm {\n  first: number;\n  tok: number;\n  schemas: number;\n"
            "  steps: [number, number, number, number, number];\n}\n\n",
            "",
        ),
        (
            "export const L1: { pi: Layer1Arm; opencode: Layer1Arm } = {\n"
            "  pi: { first: 5676, tok: 1228, schemas: 4, steps: [5676, 6231, 6786, 7341, 7896] },\n"
            "  opencode: { first: 29997, tok: 6659, schemas: 9, steps: [29997, 30695, 31393, 32091, 32789] },\n"
            "};\n\n",
            "",
        ),
    ],
    tolerant=False,
)

Path("deck/src/slides/fork.ts").write_text(
    '''import { S, hooks } from "../deck";

// Slide "Hipóteses": the bars are static SVG in index.html (FrontierHarness,
// Runta 2026); on enter they grow from zero to their data-w width.
export function initFork(): void {
  const s = document.getElementById("forksvg");
  if (!(s instanceof SVGSVGElement)) return;
  hooks.enter[S("s-hip")] = () => {
    s.querySelectorAll<SVGRectElement>(".grow").forEach((r) => {
      const w = r.dataset.w ?? "0";
      r.style.transition = "none";
      r.setAttribute("width", "0");
      window.setTimeout(() => {
        r.style.transition = "width 1.2s cubic-bezier(.2,.8,.2,1)";
        r.setAttribute("width", w);
      }, 80);
    });
  };
}
''',
    encoding="utf-8",
)
print("deck/src/slides/fork.ts: rewritten")
