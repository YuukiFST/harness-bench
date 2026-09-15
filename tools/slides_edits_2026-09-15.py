"""Deck edits applied to deck/index.html and deck/src/*.ts on 2026-09-15.

Slide 10 mixed the research classification with the AI-use declaration and
had no room for the second method the author used (Helmsman). The AI card
moves to a new slide 11 that shows both methods, LLM Wiki and Helmsman, in
the author's words for a non-technical audience; slide 10 keeps the five
axes plus the exploratory sentence of [57]. Slide comments and the notes
array shift by one from the old slide 11 on. Reference letters follow
dist/projeto-de-pesquisa.docx after tools/docx_edits_2026-09-15.py.

Usage:
    python tools/slides_edits_2026-09-15.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

INDEX = Path("deck/index.html")
NOTES = Path("deck/src/notes.ts")
CONTENT = Path("deck/src/content.ts")

html = INDEX.read_text(encoding="utf-8")

# --- slide 10: classification only -------------------------------------------------
start = html.index('<section class="slide" id="s-class"')
end = html.index("<!-- 11 MÉTODO -->")
old_slide = html[start:end]

ai_start = old_slide.index('<div\n            class="card frag glass"')
slide10 = (
    old_slide[:ai_start]
    + """<div class="card frag glass" style="flex: 1; display: flex; align-items: center; padding: 40px 56px; margin-bottom: 70px">
            <div style="font-size: 34px; line-height: 1.45">
              <b class="acc">Por que exploratória.</b> A comparação de dois <em>harnesses</em> construindo o
              mesmo produto completo do zero, a partir da mesma especificação, não tem precedente publicado.
              O que já existe compara <em>harnesses</em> em suítes de tarefas isoladas.
            </div>
          </div>
          <div class="denom">Projeto, §3, parágrafo de classificação [57]; sem manual citado.</div>
        </section>
        """
)
slide10 = slide10.replace(
    'data-title="Classificação da pesquisa e uso de IA"', 'data-title="Classificação da pesquisa"'
)

# --- slide 11: AI use, two methods -------------------------------------------------------
slide11 = """<!-- 11 USO DE IA -->
        <section class="slide" id="s-ia" data-title="Uso de IA declarado: dois métodos">
          <h2>
            Uso de IA declarado<small
              >Portaria CNPq nº 2.664/2026 (Brasil, 2026): ferramenta e finalidade · ferramenta: Claude Code ·
              o autor decide, o agente escreve</small
            >
          </h2>
          <div class="row" style="gap: 34px; margin-bottom: 84px">
            <div class="card frag glass col ia">
              <div class="ia-head">
                <span class="ia-tag" style="background: rgba(59, 123, 214, 0.22); color: #9cc0f2">Fontes</span>
                <b><em>LLM Wiki</em></b>
                <span class="mute">padrão de Karpathy (2026), no repositório do projeto</span>
              </div>
              <ol class="ia-steps">
                <li><b>Fontes brutas</b> ficam guardadas sem alteração; o autor escolhe o que entra.</li>
                <li><b>O agente escreve</b> uma página de síntese por fonte e liga entidades e conceitos.</li>
                <li><b>Cada operação</b> entra num registro cronológico; contradições viram uma fila de revisão.</li>
                <li><b>O autor confere</b> cada afirmação citada na obra original antes de entrar no texto.</li>
              </ol>
              <div class="ia-foot">29 fontes ingeridas · 46 páginas · nenhuma frase do projeto escrita pelo agente</div>
            </div>
            <div class="card frag glass col ia">
              <div class="ia-head">
                <span class="ia-tag" style="background: rgba(123, 216, 143, 0.2); color: #a9e9b6">Especificação</span>
                <b>Helmsman</b>
                <span class="mute">rotina escrita pelo autor (YuukiFST, 2026a), mapa #1 do Finn</span>
              </div>
              <ol class="ia-steps">
                <li><b>Uma ideia vira um mapa</b> de decisões no rastreador de issues: 21 <em>tickets</em> sob um mapa.</li>
                <li><b>O que o sistema faz</b>, só o autor responde: 9 <em>tickets</em> de produto, em conversa.</li>
                <li><b>Como construir</b>, o agente decide sozinho: 12 <em>tickets</em> técnicos, cada um com alternativas e critério.</li>
                <li><b>Fato externo</b> (preço de API, modelo de voz): subagentes de pesquisa antes de decidir, 3 <em>tickets</em>.</li>
              </ol>
              <div class="ia-foot">Mapa fechado: nada a decidir · base da especificação congelada dos dois braços</div>
            </div>
          </div>
          <div class="denom">
            Finalidade declarada: entender o tema, buscar artigos e registrar as decisões de produto e de pilha do
            Finn antes do experimento. Projeto, §3 [58] (Karpathy, 2026; YuukiFST, 2026a, 2026c; Brasil, 2026).
          </div>
        </section>
        """

# --- shift slide comments before inserting the new slide 11 ---------------------------------
tail = html[end:]
for n in range(17, 10, -1):
    tail = tail.replace(f"<!-- {n} ", f"<!-- {n + 1} ", 1)

html = html[:start] + slide10 + slide11 + tail

# --- reference letters --------------------------------------------------------------------
html = html.replace("YuukiFST, 2026b", "YuukiFST, 2026c").replace("YuukiFST, 2026a", "YuukiFST, 2026b")
# the new slide cites 2026a for agent-dotfiles; restore it there
html = html.replace("(YuukiFST, 2026b), mapa #1 do Finn", "(YuukiFST, 2026a), mapa #1 do Finn")
html = html.replace("YuukiFST, 2026b, 2026c; Brasil, 2026", "YuukiFST, 2026a, 2026c; Brasil, 2026")
html = html.replace(
    """>formato ABNT abreviado; as 20 entradas do projeto, seção 6, todas sobre o
              <em>harness</em></small""",
    """>formato ABNT abreviado; as 21 entradas do projeto, seção 6: 18 sobre o
              <em>harness</em>, 3 sobre o método de trabalho declarado</small""",
)
INDEX.write_text(html, encoding="utf-8")

# --- notes ---------------------------------------------------------------------------------
notes = NOTES.read_text(encoding="utf-8")
old10 = notes[
    notes.index("  `<b>Classificação [43][57] e declaração de IA [58].</b>") : notes.index(
        "  `<b>Método [59][63][64].</b>"
    )
]
new10 = (
    "  `<b>Classificação [43][57].</b> [57]: aplicada; quantitativa (tokens e sucesso) e qualitativa "
    '(atribuição à carga fixa ou aos passos); exploratória "porque a comparação de dois harnesses construindo '
    'o mesmo produto completo do zero, a partir da mesma especificação, não tem precedente publicado"; '
    "experimental, VI o harness, controladas modelo, especificação, espaço de trabalho inicial e limites; "
    "dedutiva. Sem manual de metodologia citado: as referências são só sobre o harness.`,\n"
    "  `<b>Uso de IA [58].</b> Dois métodos, mesmo papel para o autor: ele decide e confere, o agente escreve. "
    "LLM Wiki, padrão de Karpathy (2026), instanciado no repositório (YuukiFST, 2026c): fontes brutas imutáveis, "
    "páginas de síntese pelo agente, registro cronológico, fila de revisão; cada citação conferida na obra "
    "original. Helmsman, rotina do autor (YuukiFST, 2026a): a ideia do Finn virou o mapa #1 com 21 tickets; "
    "#2–#10 são perguntas de produto que só o autor respondeu, em conversa; #11–#22 são decisões técnicas que o "
    "agente tomou sozinho, cada uma com alternativas, critério e o que trava para as seguintes; #11–#13 "
    "dependiam de fato externo (cobrança da Meta, Whisper em português, custo zero) e foram resolvidas por "
    "subagentes de pesquisa antes da decisão. Portaria CNPq 2.664/2026 pede ferramenta e finalidade (Brasil, "
    "2026): Claude Code; entender o tema, buscar artigos e registrar as decisões do Finn. O autor responde pelo "
    "texto final e por cada decisão de produto.`,\n"
)
notes = notes.replace(old10, new10)
notes = notes.replace("o Zen é citado no slide 15", "o Zen é citado no slide 16")
notes = notes.replace(
    "Lista completa com 20 entradas no projeto, todas sobre o <em>harness</em> (normas e manuais de metodologia saíram em 14 set. 2026).",
    "Lista completa com 21 entradas no projeto: 18 sobre o <em>harness</em>, 3 sobre o método de trabalho declarado (Portaria CNPq, LLM Wiki, Helmsman); normas e manuais de metodologia saíram em 14 set. 2026.",
)
notes = notes.replace("As mesmas 20 no slide", "As mesmas 21 no slide")
notes = notes.replace("Referências [166]–[185]", "Referências [166]–[186]")
notes = notes.replace(
    "YuukiFST/Finn [183] e YuukiFST/harness-bench [184]", "YuukiFST/Finn [184] e YuukiFST/harness-bench [185]"
)
notes = notes.replace("Finn (YuukiFST, 2026a)", "Finn (YuukiFST, 2026b)")
NOTES.write_text(notes, encoding="utf-8")

# --- refs in content.ts --------------------------------------------------------------------
content = CONTENT.read_text(encoding="utf-8")
content = content.replace("ordem dos 17 slides", "ordem dos 18 slides")
old_refs = (
    '  "YUUKIFST. <b>Finn</b>: SaaS universal de financeiro por voz. 2026a. Repositório de código.",\n'
    '  "YUUKIFST. <b>harness-bench</b>: executor, prompts, testes de aceitação, dados brutos e scripts de análise deste projeto. 2026b. Repositório de código.",'
)
new_refs = (
    '  "YUUKIFST. <b>agent-dotfiles</b>: skill Helmsman, mapa de decisões para agentes de codificação. 2026a. Repositório de código.",\n'
    '  "YUUKIFST. <b>Finn</b>: SaaS universal de financeiro por voz. 2026b. Repositório de código.",\n'
    '  "YUUKIFST. <b>harness-bench</b>: executor, prompts, testes de aceitação, dados brutos e scripts de análise deste projeto. 2026c. Repositório de código.",'
)
assert old_refs in content
content = content.replace(old_refs, new_refs)
CONTENT.write_text(content, encoding="utf-8")
print("ok")
