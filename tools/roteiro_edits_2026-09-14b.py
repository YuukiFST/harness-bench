"""Second pass on dist/roteiro-apresentacao.html (2026-09-14): coherence audit.

Mirrors tools/slides_edits_2026-09-14g.py and the docx: the list of slides
that cite authors on screen; the FrontierHarness bars are the 7 with a
value in the post; the proxy answer follows paragraph [63] (the additive
offset is why counting happens at the proxy); Finn's 21 issues are #2–#22
under the map #1; the declared purpose of Claude Code is the one of [58];
Wilcoxon pairs are k = 9 units, the quota limits n; the quota answer
follows the reduction ladder of docs/spec/11 §5.4 ([65]); the gateway is
cited; the references slide carries the 20 entries of the project.

Every pair is an exact, single-occurrence replacement. Pairs already applied
are skipped, so the script can be rerun.

Usage:
    python tools/roteiro_edits_2026-09-14b.py
"""

from pathlib import Path

PATH = Path("dist/roteiro-apresentacao.html")

PAIRS: list[tuple[str, str]] = [
    (
        "o deck cita autores na tela nos slides 3, 8, 9 (linha do tempo), 10, 13 e 16.",
        "o deck cita autores na tela nos slides 2, 3, 5, 6, 8, 9 (linha do tempo), 10, 12, 13, 15, 16 e 17.",
    ),
    (
        "o gráfico do slide mostra 7 delas, as que têm valor citado no texto do projeto.",
        "o gráfico do slide mostra 7 delas, as que têm valor no texto do post.",
    ),
    (
        "ele não se cancela em razão, por isso eu reporto diferença absoluta e também a razão.",
        "ele não se cancela em razão e cobraria de cada braço um excedente proporcional ao número de passos. Por isso a contagem é feita no <em>proxy</em>, sobre os bytes transmitidos, e o relatório do <em>gateway</em> fica só para verificação cruzada.",
    ),
    (
        "<small>#1 mapa; #2–#10 produto; #11–#22 técnicas</small>",
        "<small>#2–#22, sob o mapa #1: #2–#10 produto; #11–#22 técnicas</small>",
    ),
    (
        "Único slide com autores na tela.",
        "Slide com mais autores na tela.",
    ),
    (
        "<b>Miller (2024)</b>, barras de erro em avaliações, base para o teste pareado.</li>",
        "<b>Miller (2024)</b>, barras de erro em avaliações, base para o teste pareado; <b>HarnessRank (2026)</b>, ordena <em>harnesses</em> por aprovação com modelo fixo e publica custo ao lado.</li>",
    ),
    (
        "Finalidade: síntese e conferência de fontes, num <em>LLM Wiki</em> no repositório, padrão de Karpathy (2026).",
        "Finalidade: entender o tema do projeto e ajudar a buscar mais artigos, num <em>LLM Wiki</em> no repositório, padrão de Karpathy (2026).",
    ),
    (
        "Claude Code, para síntese e conferência de fontes num <em>LLM Wiki</em>, padrão de Karpathy (2026).",
        "Claude Code, para entender o tema e buscar mais artigos num <em>LLM Wiki</em>, padrão de Karpathy (2026).",
    ),
    (
        "<small>n = 9 pares, bilateral, α = 0,05</small>",
        "<small>k = 9 pares (as nove unidades), bilateral, α = 0,05</small>",
    ),
    (
        "É o que a cota gratuita permite com n ≥ 3. O MDE está declarado;",
        "Nove pares são as nove unidades do Finn; a cota limita o n por célula, não os pares. O MDE está declarado;",
    ),
    (
        "Resposta: n ≥ 3, mediana com dispersão, e cobertura da matriz antes de repetições.",
        "Resposta: n ≥ 3, mediana com dispersão, e reduzir cobertura antes de reduzir repetições.",
    ),
    (
        "Cobertura primeiro: todas as células com n = 1, depois n = 2, depois n = 3. Se parar antes, o que existe é reportado com o n que tem.",
        "Repetições primeiro: n = 3 no nível primário, nas nove unidades. Se a cota não comportar a matriz, o nível de robustez é truncado após a unidade 6; se ainda não couber, sai inteiro e é reportado como não executado. Nunca abaixo de n = 3.",
    ),
    (
        "Inferência nos dois níveis gratuitos do <em>gateway</em>, o OpenCode Zen.",
        "Inferência nos dois níveis gratuitos do <em>gateway</em>, o OpenCode Zen (Opencode, 2026b).",
    ),
    (
        "<h3>Referências citadas nos slides</h3>",
        "<h3>Referências</h3>",
    ),
    (
        "As dezoito referências que apareceram nos slides, em ABNT abreviado, todas sobre o <em>harness</em>. O projeto tem 20; ficam de fora aqui duas citadas só no texto.",
        "As vinte referências do projeto, em ABNT abreviado, todas sobre o <em>harness</em>; a mesma lista da seção 6.",
    ),
    (
        '<li><b>"Quais são as duas que faltam?"</b>HarnessRank e Opencode Zen (2026b), citadas só no texto.</li>',
        '<li><b>"Todas essas aparecem nos slides?"</b>Dezesseis na tela. Alier Forment, Miller, HarnessRank e Opencode (2026a) estão no texto do projeto e na minha fala dos slides 9, 12 e 13.</li>',
    ),
]

# no-ai-slop pass on the sentences above: active voice in the author's mouth,
# no "X, não Y" contrast.
PAIRS += [
    (
        "Por isso a contagem é feita no <em>proxy</em>, sobre os bytes transmitidos, e o relatório do <em>gateway</em> fica só para verificação cruzada.",
        "Por isso eu conto no <em>proxy</em>, sobre os bytes transmitidos, e o relatório do <em>gateway</em> fica só para verificação cruzada.",
    ),
    (
        "Nove pares são as nove unidades do Finn; a cota limita o n por célula, não os pares. O MDE está declarado;",
        "Nove pares são as nove unidades do Finn. A cota limita o n por célula. O MDE está declarado;",
    ),
    (
        "Se a cota não comportar a matriz, o nível de robustez é truncado após a unidade 6; se ainda não couber, sai inteiro e é reportado como não executado. Nunca abaixo de n = 3.",
        "Se a cota não comportar a matriz, eu trunco o nível de robustez após a unidade 6; se ainda não couber, tiro esse nível inteiro e reporto como não executado. Nunca abaixo de n = 3.",
    ),
]

text = PATH.read_text(encoding="utf-8")
# A pair is done when its old side is gone (the slop pass below rewrites some new sides).
todo = [(o, n) for o, n in PAIRS if o in text]
for old, new in todo:
    if text.count(old) != 1:
        raise SystemExit(f"{PATH}: expected 1 match, found {text.count(old)}:\n{old[:120]}")
    text = text.replace(old, new)
PATH.write_text(text, encoding="utf-8")
print(f"{PATH}: {len(todo)} replacements")
