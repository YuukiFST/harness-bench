"""Second pass on the deck (2026-09-14): cover, "how it works" slide, closing question.

Author's review of the 2026-09-14 deck: the cover subtitle is gone; a slide
after "Justificativa, tema, problema, objetivo geral" explains how the
experiment runs; the closing question asks how much the harness matters to the
developer's cost. The deck's H1/H2 fork still carried the oh-my-pi ratios
(11,4x / 13,6x, 16.714 tokens) from the retired design; the real pi vs
OpenCode Layer 1 numbers are layer1/data/report.md (5,3x / 5,4x, 6.659 tokens).

Applies to dist/apresentacao-pcc.html (exact match) and to deck/ (whitespace-
tolerant match on index.html, exact on the TypeScript). Every pair must match
exactly once.

Usage:
    python tools/slides_edits_2026-09-14b.py
    cd deck && npx prettier --write index.html src && npm run build
"""

from pathlib import Path

# deck_edits runs its own replacements on import; only its helpers are wanted here.
_src = Path("tools/deck_edits_2026-09-14.py").read_text(encoding="utf-8")
_helpers = _src.split("# --- index.html")[0]
_ns: dict = {}
exec(compile(_helpers, "deck_edits_helpers", "exec"), _ns)
apply = _ns["apply"]

COVER_SUB = (
    '<div style="font-size:38px;color:var(--mute);max-width:1500px">tokens e taxa de sucesso do OpenCode '
    "e do pi na construção de um mesmo SaaS sob um mesmo modelo</div>"
)

HOW_SLIDE = """<!-- 5 COMO O PROJETO FUNCIONA -->
<section class="slide" id="s-como" data-title="Como o projeto funciona">
  <h2>Como o projeto funciona<small>o mesmo produto, construído duas vezes</small></h2>
  <div class="row" style="flex:none;gap:30px;font-size:26px">
    <div class="card col frag"><b class="acc">1 · Um produto</b> · Finn, SaaS de financeiro por voz, dividido em 9 <em>tickets</em> técnicos, cada um com testes de aceitação escritos pelo autor.</div>
    <div class="card col frag"><b class="acc">2 · Dois <em>harnesses</em></b> · OpenCode e pi recebem o mesmo <em>ticket</em>, o mesmo <em>prompt</em>, o mesmo espaço de trabalho congelado e o mesmo modelo.</div>
    <div class="card col frag"><b class="acc">3 · Um contador externo</b> · um <em>proxy</em> entre o <em>harness</em> e o modelo conta requisições, tokens e latência da mesma forma para os dois; n ≥ 3 execuções por célula.</div>
    <div class="card col frag"><b class="acc">4 · Um critério</b> · tokens por <em>ticket</em> concluído e Succ/Mtok, comparados por teste pareado; a Camada 1 separa a parte que é carga fixa por requisição.</div>
  </div>
  <div class="card frag hi" style="margin-top:30px;font-size:28px"><b class="acc">Por que isso justifica o tema</b> · quem paga é o desenvolvedor, na assinatura, e a empresa, em escala; conhecer o <em>harness</em> virou parte do ofício. As comparações publicadas usam tarefas isoladas e não dizem quanto custa entregar um produto inteiro com uma ferramenta em vez de outra. Este projeto mede esse custo.</div>
  <div class="denom">Finn: github.com/YuukiFST/Finn (YuukiFST, 2026a), <em>issues</em> #1–#22. Braços: OpenCode 1.17.9 e pi 0.80.10, código aberto, sem interface. Método detalhado nos slides seguintes.</div>
</section>

<!-- 6 OBJETIVOS ESPECÍFICOS -->"""

HOW_NOTE = (
    "`<b>Como o projeto funciona [27][43][59][61].</b> [27]: \"Este projeto medirá esse custo construindo o mesmo "
    "produto duas vezes: o Finn, um SaaS de financeiro por voz, será construído com o OpenCode e com o pi, sobre o "
    "mesmo modelo, ticket a ticket, e os tokens de cada braço serão contados fora do harness.\" Dizer em voz alta a "
    "ordem: produto → dois braços → proxy → critério. Camada 1 e Camada 2, matriz e limites vêm nos slides de "
    "método; aqui só a visão geral. \"Conhecer o harness virou parte do ofício\" é [27].`,\n"
)

OLD_Q = (
    "Quantos tokens a mais custa construir o mesmo SaaS com um <em>harness</em> em vez de outro, e quanto disso é "
    "carga fixa?"
)
NEW_Q = (
    "Quanto pesa, para o desenvolvedor que já escolheu o modelo, conhecer o <em>harness</em> antes de pagar por ele?"
)

# --- dist/apresentacao-pcc.html (exact) ---------------------------------------
apply(
    Path("dist/apresentacao-pcc.html"),
    [
        ("  " + COVER_SUB + "\n", ""),
        ("<!-- 5 OBJETIVOS ESPECÍFICOS -->", HOW_SLIDE),
        ("`<b>Objetivos específicos [35]", HOW_NOTE + "`<b>Objetivos específicos [35]"),
        (OLD_Q, NEW_Q),
    ],
    tolerant=False,
)

# --- deck/index.html (prettier-wrapped) ---------------------------------------
apply(
    Path("deck/index.html"),
    [
        ('<div style="font-size: 38px; color: var(--mute); max-width: 1500px"> tokens e taxa de sucesso do OpenCode e do pi na construção de um mesmo SaaS sob um mesmo modelo </div>', ""),
        ("<!-- 5 OBJETIVOS ESPECÍFICOS -->", HOW_SLIDE.replace('class="card col frag"', 'class="card col frag glass"').replace('class="card frag hi"', 'class="card frag hi glass"')),
        (OLD_Q, NEW_Q),
    ],
    tolerant=True,
)

# --- deck/src/notes.ts ---------------------------------------------------------
apply(
    Path("deck/src/notes.ts"),
    [("  `<b>Objetivos específicos [35]", "  " + HOW_NOTE + "  `<b>Objetivos específicos [35]")],
    tolerant=False,
)

# --- deck/src: real pi vs OpenCode ratios, and the arm key named after the arm --
apply(
    Path("deck/src/slides/fork.ts"),
    [
        (
            '<tspan fill="#f5b638" font-weight="700">11,4×</tspan> os bytes, <tspan fill="#f5b638" font-weight="700">13,6×</tspan> os tokens (16.714 vs 1.228)',
            '<tspan fill="#f5b638" font-weight="700">5,3×</tspan> os bytes, <tspan fill="#f5b638" font-weight="700">5,4×</tspan> os tokens (6.659 vs 1.228)',
        ),
        ('<linearGradient id="aomp"', '<linearGradient id="aopencode"'),
        ("${fmt(L1.omp.first)} bytes · ${L1.omp.schemas} esquemas", "${fmt(L1.opencode.first)} bytes · ${L1.opencode.schemas} esquemas"),
        ('const series: { key: "pi" | "omp"; col: string }[] = [', 'const series: { key: "pi" | "opencode"; col: string }[] = ['),
        ('{ key: "omp", col: "#f5b638" },', '{ key: "opencode", col: "#f5b638" },'),
    ],
    tolerant=False,
)
apply(
    Path("deck/src/content.ts"),
    [
        ("export const L1: { pi: Layer1Arm; omp: Layer1Arm } = {", "export const L1: { pi: Layer1Arm; opencode: Layer1Arm } = {"),
        ("  omp: { first: 29997,", "  opencode: { first: 29997,"),
    ],
    tolerant=False,
)
apply(
    Path("deck/README.md"),
    [("ordem dos 15 slides", "ordem dos 16 slides"), ("percorrer os 15 slides", "percorrer os 16 slides")],
    tolerant=False,
)
