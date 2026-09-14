"""Bring deck/ (the Vite rebuild of the deck) to the Finn experiment (2026-09-14).

Same content changes as tools/slides_edits_2026-09-14.py, applied to the
prettier-wrapped deck/index.html with whitespace-tolerant matching, and to the
TypeScript data and slide modules. Every pair must match exactly once.

Usage:
    python tools/deck_edits_2026-09-14.py
    cd deck && npx prettier --write index.html src && npm run build
"""

import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location("slides", Path("tools/slides_edits_2026-09-14.py"))
slides = importlib.util.module_from_spec(spec)
spec.loader.exec_module(slides)


def ws_pattern(old: str) -> re.Pattern:
    r"""Prettier rewraps text and may break lines at tag boundaries, so any
    whitespace run matches `\s+` and tag edges tolerate optional whitespace."""
    parts = [re.escape(p) for p in re.split(r"\s+", old.strip())]
    pat = r"\s+".join(parts)
    pat = pat.replace(re.escape("<"), r"\s*<").replace(re.escape(">"), r"\s*>\s*")
    return re.compile(pat)


def apply(path: Path, pairs: list[tuple[str, str]], tolerant: bool) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if tolerant:
            pat = ws_pattern(old)
            hits = pat.findall(text)
            if len(hits) != 1:
                raise SystemExit(f"{path}: expected 1 match, found {len(hits)}:\n{old[:120]}")
            text = pat.sub(lambda _m: new, text, count=1)
        else:
            if text.count(old) != 1:
                raise SystemExit(f"{path}: expected 1 match, found {text.count(old)}:\n{old[:120]}")
            text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"{path}: {len(pairs)} replacements")


# --- index.html: the markup pairs of the dist script that live in markup here --
MARKUP_SKIP = (
    "r.innerHTML=", "const L1=", "// ----------", "font-size=\"34\"", "1ª requisição",
    "const x0=", "for(const v of", "${k===", "['2022'", "const arms=", "m.style.grid",
    "<div class=\"hdr\"", "`Célula", "const diff=", "const CRIT=", "for(let i=0;i<8",
    "<text x=\"380\"", "['Construção", "'DATACURVE", "'HUANG", "'NING", "'YUUKIFST",
    "desfecho da tarefa · proxy", "<line x1=\"345\"",
    "Molda o estilo", "Esquemas viajam", "Conta requisições",  # H3 texts live in content.ts here
    "<span style=\"color:var(--bad)\">",  # prettier spaces the style attribute; restated below
    "Escrita do projeto concluída em 11 set.",  # deck denom never carried the day
)
html_pairs = [(o, n) for o, n in slides.R if not o.lstrip().startswith(MARKUP_SKIP)]
# The dist deck has no "glass" class and lists the specific-objective items with
# the same text, so the remaining pairs match here modulo wrapping. Two pairs
# differ in class attributes and are restated:
html_pairs = [p for p in html_pairs if 'class="card hi" style="padding:20px 30px"' not in p[0]
              and 'class="card" style="padding:20px 30px"' not in p[0]
              and '<div class="denom">DeepSWE' not in p[0]]
html_pairs += [
    ("<b class=\"acc\"><em>Harness</em> zero</b> · controle. Laço observar/agir, 3 ferramentas, &lt; 400 linhas de Python, sem planejamento, compactação ou <em>retry</em>.",
     "<b class=\"acc\">Braços</b> · OpenCode e pi: código aberto, sem interface (<code>opencode run</code>, <code>pi --mode json</code>), URL base OpenAI-compatível. Nenhum <em>harness</em> escrito pelo projeto."),
    ("<b class=\"acc\">Suíte</b> · 8 tarefas Python do DeepSWE, fixadas por <em>commit</em> e SHA-256. Crédito parcial: fração de testes do verificador.",
     "<b class=\"acc\">Suíte</b> · Finn, 9 <em>tickets</em> técnicos; espaço de trabalho congelado por SHA-256 a cada <em>ticket</em>. Escore: fração dos testes de aceitação do autor, <em>held-out</em>."),
    ("<b class=\"acc\">Limite único</b> · relógio de parede 3× a mediana do <em>harness</em> zero nas tarefas-piloto. Sem teto de passos, já que o teto seria uma decisão de projeto do <em>harness</em>. Saída máxima idêntica via <em>proxy</em>.",
     "<b class=\"acc\">Limite único</b> · relógio de parede 3× a maior mediana dos braços nos <em>tickets</em>-piloto. Sem teto de passos, já que o teto seria uma decisão de projeto do <em>harness</em>. Saída máxima idêntica via <em>proxy</em>."),
    ("DeepSWE (Huang <em>et al.</em>, 2026): 113 tarefas, 91 repositórios; soluções de referência com 668 linhas em média, contra 32,8 no SWE-bench. Braços provisórios até os portões de confiabilidade.",
     "Finn (YuukiFST, 2026a): SaaS multiempresa de financeiro por voz, 21 <em>tickets</em> fechados antes do experimento; pilha fixa TypeScript, TanStack Start, tRPC, Drizzle, PostgreSQL, Vitest. T1 tenant · T2 governança · T3 <em>flags</em> · T4 <em>pipeline</em> de voz · T5 confirmação · T6 log · T7 relatório · T8 agendador · T9 cobrança."),
    ("<span style=\"color: var(--bad)\">falhada</span>: agente não cumpriu; é resultado, escore zero (estouro do relógio incluído).",
     "<span style=\"color: var(--bad)\">não concluída</span>: agente não concluiu o <em>ticket</em>; é resultado, entra com a fração de testes aprovada (estouro do relógio incluído)."),
    ("Orçamento R$ 0,00 · cronograma set. 2026 – jan. 2027",
     "Orçamento R$ 0,00 · cronograma ago. 2026 – jan. 2027"),
]
# The deck's budget/gantt denom and the ReAct timeline card were already
# phrased differently from dist; handle whatever the tolerant match finds.
apply(Path("deck/index.html"), html_pairs, tolerant=True)

# --- content.ts ---------------------------------------------------------------
apply(Path("deck/src/content.ts"), [
    ("o gráfico mostra as 7 com valor no texto do post. Razão 17,5× calculada pelo autor. Blogue institucional, não revisado por pares.",
     "o gráfico mostra as 7 com valor no texto do post; Pi e OpenCode, em âmbar, são os dois braços deste projeto. Razão 17,5× calculada pelo autor. Blogue institucional, não revisado por pares."),
    ("Na Camada 1, pi envia 2.499 bytes; oh-my-pi, 25.395 (10,2×).", "Na Camada 1, pi envia 2.499 bytes; OpenCode, 9.738 (3,9×)."),
    ("Esquemas viajam a cada requisição: 4 no pi, 11 no oh-my-pi.", "Esquemas viajam a cada requisição: 4 no pi, 9 no OpenCode."),
    ("Conta requisições, tokens e latência igual para todos os braços.", "Conta requisições, tokens e latência igual para os dois braços."),
    ("  omp: { first: 64945, tok: 16714, schemas: 11, steps: [64945, 65273, 65898, 66523, 67148] },",
     "  omp: { first: 29997, tok: 6659, schemas: 9, steps: [29997, 30695, 31393, 32091, 32789] },"),
    ("o mais raso; ponto de partida do <em>harness</em> zero.", "o mais raso; o pi, com quatro ferramentas, fica perto dele."),
    ("  months: [number, number, number, number, number];", "  months: [number, number, number, number, number, number];"),
    ('export const GANTT_MONTHS: string[] = ["Set", "Out", "Nov", "Dez", "Jan"];',
     'export const GANTT_MONTHS: string[] = ["Ago", "Set", "Out", "Nov", "Dez", "Jan"];'),
    ('  { phase: "Leitura e levantamento bibliográfico", months: [1, 1, 0, 0, 0] },\n'
     '  { phase: "Definição do tema, do problema e das hipóteses", months: [1, 1, 0, 0, 0] },\n'
     '  { phase: "Construção do instrumento e do harness zero", months: [0, 1, 1, 0, 0] },\n'
     '  { phase: "Escrevendo introdução", months: [0, 0, 1, 0, 0] },\n'
     '  { phase: "Escrevendo referencial teórico", months: [0, 0, 1, 0, 0] },\n'
     '  { phase: "Escrevendo material e método", months: [0, 0, 1, 1, 0] },\n'
     '  { phase: "Execução da matriz de experimentos", months: [0, 0, 0, 1, 1] },\n'
     '  { phase: "Análise dos resultados", months: [0, 0, 0, 0, 1] },\n'
     '  { phase: "Elaborando as referências", months: [0, 0, 0, 0, 1] },\n'
     '  { phase: "Revisão final e preparação da apresentação", months: [0, 0, 0, 0, 1] },',
     '  { phase: "Leitura e levantamento bibliográfico", months: [1, 1, 0, 0, 0, 0] },\n'
     '  { phase: "Definição do tema, do problema e das hipóteses", months: [1, 1, 0, 0, 0, 0] },\n'
     '  { phase: "Construção do instrumento e dos estados de referência", months: [0, 0, 1, 1, 0, 0] },\n'
     '  { phase: "Escrevendo introdução", months: [1, 1, 0, 0, 0, 0] },\n'
     '  { phase: "Escrevendo referencial teórico", months: [1, 1, 0, 0, 0, 0] },\n'
     '  { phase: "Escrevendo material e método", months: [1, 1, 0, 0, 0, 0] },\n'
     '  { phase: "Execução da matriz de experimentos", months: [0, 0, 0, 0, 1, 1] },\n'
     '  { phase: "Análise dos resultados", months: [0, 0, 0, 0, 0, 1] },\n'
     '  { phase: "Elaborando as referências", months: [1, 1, 0, 0, 0, 0] },\n'
     '  { phase: "Revisão final e preparação da apresentação", months: [0, 1, 0, 0, 0, 0] },'),
    ('  "DATACURVE. <b>Pier</b>: a Harbor fork built for DeepSWE. 2026. Repositório de código.",\n',
     '  "EARENDIL. <b>Pi, minimal and performant</b>. 2026. Blogue institucional.",\n'),
    ('  "HUANG, W. <em>et al.</em> <b>DeepSWE</b>: measuring frontier coding agents on original, long-horizon engineering tasks. arXiv:2607.07946, 2026. <em>Preprint</em>.",\n'
     '  "JIMENEZ, C. E. <em>et al.</em> <b>SWE-bench</b>: can language models resolve real-world GitHub issues? ICLR, 2024.",\n', ""),
    ('  "NING, X. <em>et al.</em> <b>Code as agent harness</b>. arXiv:2605.18747, 2026. <em>Preprint</em>.",\n',
     '  "NING, X. <em>et al.</em> <b>Code as agent harness</b>. arXiv:2605.18747, 2026. <em>Preprint</em>.",\n'
     '  "OPENCODE. <b>OpenCode</b>: the open source coding agent. 2026a. Repositório de código.",\n'),
    ('  "YUUKIFST. <b>harness-bench</b>: runner, dados brutos e scripts de análise deste projeto. 2026. Repositório de código.",\n',
     '  "YUUKIFST. <b>Finn</b>: SaaS universal de financeiro por voz. 2026a. Repositório de código.",\n'
     '  "YUUKIFST. <b>harness-bench</b>: executor, prompts, testes de aceitação, dados brutos e scripts de análise deste projeto. 2026b. Repositório de código.",\n'),
    ('export const MATRIX_ARMS: string[] = ["harness zero", "pi", "oh-my-pi", "terceiros…"];',
     'export const MATRIX_ARMS: string[] = ["OpenCode", "pi"];'),
    ("export const MATRIX_TASKS = 8;", "export const MATRIX_TASKS = 9;"),
    ('{ k: "Abordagem", v: "quanti + quali", w: "medir custo e sucesso; atribuir a decisão" }',
     '{ k: "Abordagem", v: "quanti + quali", w: "medir tokens e sucesso; atribuir à carga fixa ou aos passos" }'),
    ('{ k: "Objetivos", v: "exploratória", w: "linhagem fixa sem precedente" }',
     '{ k: "Objetivos", v: "exploratória", w: "mesmo produto completo, dois <em>harnesses</em>, sem precedente" }'),
    ('    w: "VI: <em>harness</em> · controladas: modelo, tarefa, limites · grupo de controle",',
     '    w: "VI: <em>harness</em> · controladas: modelo, <em>ticket</em>, espaço de trabalho, limites",'),
    ('  "<b>2</b> Suíte com objetivos numerados e <em>oracle</em> próprio",', '  "<b>2</b> Finn em <em>tickets</em> com testes de aceitação do autor",'),
    ('  "<b>3</b> <em>Harness</em> zero em laço ReAct (controle)",', '  "<b>3</b> Espaço de trabalho congelado e idêntico por <em>ticket</em>",'),
    ('  "<b>4</b> Mesma suíte, mesmo modelo, todos os braços, com repetição",', '  "<b>4</b> Cada <em>ticket</em> nos dois <em>harnesses</em>, mesmo modelo e <em>prompt</em>, n ≥ 3",'),
    ('  "<b>6</b> Custo relatado × custo medido no <em>proxy</em>",', '  "<b>6</b> Tokens relatados × tokens medidos no <em>proxy</em>",'),
    ('  "<b>7</b> Publicar <em>runner</em>, dados e scripts, custo zero",', '  "<b>7</b> Publicar executor, <em>prompts</em>, testes, dados e scripts, custo zero",'),
], tolerant=False)

# --- slide modules --------------------------------------------------------------
apply(Path("deck/src/slides/fork.ts"), [
    ('`<line id="forkedge" x1="345" y1="95" x2="440" y2="95" stroke="#f5b638" stroke-width="4" marker-end="url(#arr)" stroke-dasharray="8 8"/>` +\n'
     '    `<text x="392" y="70" text-anchor="middle" fill="#f5b638" font-size="20">fork</text>` +',
     '`<text x="400" y="103" text-anchor="middle" fill="#8b98a8" font-size="26">vs</text>` +'),
    ('font-size="34" font-weight="700">oh-my-pi</text>', 'font-size="34" font-weight="700">OpenCode</text>'),
    ('${key === "pi" ? "pi" : "oh-my-pi"} · ', '${key === "pi" ? "pi" : "OpenCode"} · '),
    ("// Aresta animada (fluxo pi -> oh-my-pi).", "// Aresta animada (removida com o par pi/oh-my-pi; o seletor abaixo nao encontra nada)."),
    ('font-size="22">${key === "pi" ? "pi" : "oh-my-pi"}</text>`;', 'font-size="22">${key === "pi" ? "pi" : "OpenCode"}</text>`;'),
    ("  const max = 70000;", "  const max = 35000;"),
    ("  for (const v of [0, 20000, 40000, 60000]) {", "  for (const v of [0, 10000, 20000, 30000]) {"),
], tolerant=False)
apply(Path("deck/src/slides/matrix.ts"), [
    ('m.style.gridTemplateColumns = "190px repeat(8,1fr)";', 'm.style.gridTemplateColumns = "190px repeat(9,1fr)";'),
    ('color:${ai !== 0 ? "#e8edf2" : "#f5b638"}">${a}</div>`;', 'color:#e8edf2">${a}</div>`;'),
    ('h += `<button class="cell${ai !== 0 ? "" : " ctrl"}" data-a="${a}" data-t="${t}" data-tier="${tier}" aria-label="${a}, tarefa ${t}, ${tier}">n ≥ 3</button>`;',
     'h += `<button class="cell" data-a="${a}" data-t="${t}" data-tier="${tier}" aria-label="${a}, ticket ${t}, ${tier}">n ≥ 3</button>`;'),
    ("    MATRIX_ARMS.forEach((a, ai) => {", "    MATRIX_ARMS.forEach((a) => {"),
    ('          `Célula (<b>${cell.dataset.a}</b>, tarefa ${cell.dataset.t}, ${cell.dataset.tier}): n ≥ 3 execuções completas após descartes; mediana com dispersão; ` +\n'
     '          (cell.classList.contains("ctrl")\n'
     '            ? "controle: define o envelope de referência (relógio de parede 3× a mediana)."\n'
     '            : "comparada ao harness zero e ao par pi / oh-my-pi por tarefa.");',
     '          `Célula (<b>${cell.dataset.a}</b>, ticket T${cell.dataset.t}, ${cell.dataset.tier}): n ≥ 3 execuções completas após descartes; mediana com dispersão; pareada com a célula do outro braço no mesmo ticket e nível.`;'),
], tolerant=False)
apply(Path("deck/src/slides/succ.ts"), [
    ("const diff = [0.6, 0.8, 0.9, 1.0, 1.1, 1.25, 1.4, 1.7];", "const diff = [0.6, 0.8, 0.9, 1.0, 1.1, 1.25, 1.4, 1.55, 1.7];"),
    ("const CRIT: Record<number, number> = { 8: 3, 7: 2, 6: 0 };", "const CRIT: Record<number, number> = { 9: 5, 8: 3, 7: 2, 6: 0 };"),
    ("    for (let i = 0; i < 8; i++) {\n      const y = 70 + i * 54;", "    for (let i = 0; i < 9; i++) {\n      const y = 64 + i * 49;"),
    ("Succ/Mtok por tarefa · A (âmbar) vs B (azul)", "Succ/Mtok por ticket · A (âmbar) vs B (azul)"),
], tolerant=False)
apply(Path("deck/src/slides/flow.ts"), [
    ("desfecho da tarefa · proxy reverso conta cada requisição · estocástica, n ≥ 3 por célula",
     "desfecho do ticket · proxy reverso conta cada requisição · estocástica, n ≥ 3 por célula"),
], tolerant=False)

# --- notes.ts: same notes as dist, as a TS array ---------------------------------
notes_src = slides.NOTES_NEW.replace("const NOTES=[\n", "").rstrip("\n")
notes_ts = Path("deck/src/notes.ts")
text = notes_ts.read_text(encoding="utf-8")
a = text.index("export const NOTES: string[] = [")
text = text[:a] + "export const NOTES: string[] = [\n" + notes_src + "\n];\n"
notes_ts.write_text(text, encoding="utf-8")
print("deck/src/notes.ts: rewritten")
