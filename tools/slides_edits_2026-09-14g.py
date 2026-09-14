"""Seventh pass on the deck (2026-09-14): coherence audit against the docx.

Decisions of the author on 2026-09-14 (docs/research/decisoes-auditoria-2026-09-14.html):
the FrontierHarness bar "oh-my-pi" stays (it is a row of the post, not an
arm); the references slide lists the same 20 entries as the project, so
HarnessRank (2026) and Opencode Zen (2026b) enter REFS and the gateway on
the budget slide is cited; dist/apresentacao-pcc.html is removed, so this
script no longer touches it.

Other pairs follow the docx: Finn has 21 closed issues, #2–#22 under the
map #1; the declared purpose of Claude Code is the one of paragraph [58];
the classification note drops the handbook citation removed on 2026-09-14;
the budget/quota answer reads "reduce coverage before repetitions" ([65]);
the Wilcoxon pairs are k, n being constructions per cell; the ReAct card
matches content.ts; comments and the content header carry 17 slides.

Applies to deck/index.html (whitespace-tolerant) and deck/src TypeScript
(exact). Pairs already applied are skipped, so the script can be rerun.

Usage:
    python tools/slides_edits_2026-09-14g.py
    cd deck && npx prettier --write index.html src && npm run build
"""

from pathlib import Path

_src = Path("tools/deck_edits_2026-09-14.py").read_text(encoding="utf-8")
_ns: dict = {}
exec(compile(_src.split("# --- index.html")[0], "deck_edits_helpers", "exec"), _ns)
_apply = _ns["apply"]
ws_pattern = _ns["ws_pattern"]


def apply(path: Path, pairs: list, tolerant: bool) -> None:
    text = path.read_text(encoding="utf-8")
    present = (lambda n: ws_pattern(n).search(text) is not None) if tolerant else (lambda n: n in text)
    todo = [(o, n) for o, n in pairs if not present(n)]
    if todo:
        _apply(path, todo, tolerant)
    else:
        print(f"{path}: nothing to do")


DECK_MARKUP: list[tuple[str, str]] = [
    # slide 5: 21 issues are #2–#22; #1 is the map
    (
        "21 <em>issues</em> fechadas pelo autor (#1–#22) fixam produto e pilha",
        "21 <em>issues</em> fechadas pelo autor (#2–#22, sob o mapa #1) fixam produto e pilha",
    ),
    # slide 9: initial card equals TL[0].claim in content.ts
    (
        "O laço observar/agir mínimo. É um <em>harness</em> legítimo, o mais raso; o pi fica perto dele.",
        "O laço observar/agir mínimo. É um <em>harness</em> legítimo, o mais raso; o pi, com quatro ferramentas, fica perto dele.",
    ),
    # slide 10: declared purpose as in [58]
    (
        "A ferramenta foi o Claude Code e a finalidade foi a síntese e a conferência de fontes.",
        "A ferramenta foi o Claude Code e a finalidade foi entender o tema do projeto e ajudar a buscar mais artigos sobre ele.",
    ),
    (
        "Projeto, §3, parágrafos de classificação e de declaração do método (YuukiFST, 2026; Brasil, 2026).",
        "Projeto, §3, parágrafos de classificação e de declaração do método (YuukiFST, 2026b; Brasil, 2026).",
    ),
    # slide 14: [65] reduces coverage before repetitions
    (
        "Resposta: n ≥ 3, mediana com dispersão, cobertura antes de repetições.",
        "Resposta: n ≥ 3, mediana com dispersão, reduzir cobertura antes de reduzir repetições.",
    ),
    # slide 15: the gateway gets its citation
    (
        "Tabelas 1 e 2 do projeto. <em>Gateway</em>: OpenCode Zen. Limite vinculante",
        "Tabelas 1 e 2 do projeto. <em>Gateway</em>: OpenCode Zen (Opencode, 2026b). Limite vinculante",
    ),
    # slide 16: same 20 entries as the project
    (
        '<section class="slide" data-title="Referências citadas nos slides">',
        '<section class="slide" data-title="Referências">',
    ),
    (
        "Referências citadas nos slides<small>formato ABNT abreviado; lista completa com 20 entradas no projeto, seção 6</small>",
        "Referências<small>formato ABNT abreviado; as 20 entradas do projeto, seção 6, todas sobre o <em>harness</em></small>",
    ),
    # comments follow the real slide numbers
    ("<!-- 6 OBJETIVOS ESPECÍFICOS -->", "<!-- 7 OBJETIVOS ESPECÍFICOS -->"),
    ("<!-- 6 HIPÓTESES -->", "<!-- 8 HIPÓTESES -->"),
    ("<!-- 7 REFERENCIAL -->", "<!-- 9 REFERENCIAL -->"),
    ("<!-- 8 CLASSIFICAÇÃO DA PESQUISA -->", "<!-- 10 CLASSIFICAÇÃO DA PESQUISA -->"),
    ("<!-- 9 MÉTODO -->", "<!-- 11 MÉTODO -->"),
    ("<!-- 10 BRAÇOS E MATRIZ -->", "<!-- 12 BRAÇOS E MATRIZ -->"),
    ("<!-- 11 SUCC/MTOK -->", "<!-- 13 SUCC/MTOK -->"),
    ("<!-- 12 LIMITAÇÕES -->", "<!-- 14 LIMITAÇÕES -->"),
    ("<!-- 13 ORÇAMENTO E CRONOGRAMA -->", "<!-- 15 ORÇAMENTO E CRONOGRAMA -->"),
    ("<!-- 14 REFERÊNCIAS -->", "<!-- 16 REFERÊNCIAS -->"),
    ("<!-- 15 FECHO -->", "<!-- 17 FECHO -->"),
]

NOTES: list[tuple[str, str]] = [
    (
        "especificado em 21 issues fechadas antes do experimento (#1 mapa; #2–#10 decisões de produto; #11–#22 decisões técnicas)",
        "especificado em 21 issues fechadas antes do experimento (#2–#22, sob o mapa #1: #2–#10 decisões de produto; #11–#22 decisões técnicas)",
    ),
    ("dedutiva (Gil, 2022; Prodanov; Freitas, 2013).", "dedutiva."),
    (
        "valor crítico de W para n = 9, bilateral, α = 0,05 é 5.",
        "valor crítico de W para k = 9 pares, bilateral, α = 0,05 é 5.",
    ),
    (
        "Preprints marcados. Aqui só as citadas nos slides: sem HarnessRank e Opencode Zen (2026b), citadas só no texto do projeto.",
        "Preprints marcados. As mesmas 20 no slide: HarnessRank (2026) e Opencode Zen (2026b) entraram em 14 set. 2026; o Zen é citado no slide 15.",
    ),
]

CONTENT: list[tuple[str, str]] = [
    (
        "// Conteúdo congelado do deck: textos, números e ordem dos 15 slides.\n// Fonte: dist/apresentacao-pcc.html (auditado). Não alterar palavras nem números.",
        "// Conteúdo congelado do deck: textos, números e ordem dos 17 slides.\n// Fonte: dist/projeto-pcc.docx (tools/docx_prose.py dump), auditado em 2026-09-14. Não alterar palavras nem números.",
    ),
    (
        '  "EARENDIL. <b>Pi, minimal and performant</b>. 2026. Blogue institucional.",\n',
        '  "EARENDIL. <b>Pi, minimal and performant</b>. 2026. Blogue institucional.",\n'
        '  "HARNESSRANK. <b>HarnessRank</b>: coding-agent harness rankings. 2026.",\n',
    ),
    (
        '  "OPENCODE. <b>OpenCode</b>: the open source coding agent. 2026a. Repositório de código.",\n',
        '  "OPENCODE. <b>OpenCode</b>: the open source coding agent. 2026a. Repositório de código.",\n'
        '  "OPENCODE. <b>Zen</b>. 2026b. Documentação do produto.",\n',
    ),
]

apply(Path("deck/index.html"), DECK_MARKUP, tolerant=True)
apply(Path("deck/src/notes.ts"), NOTES, tolerant=False)
apply(Path("deck/src/content.ts"), CONTENT, tolerant=False)
