"""Script edits applied to dist/roteiro-apresentacao.html on 2026-09-15.

The deck gained slide 11 (AI use, two methods) and slide 10 lost the AI
paragraph, so the script gets a new card 11, card 10 shrinks to the
classification, every card from the old 11 on shifts by one, and the intro,
checklist and question bank follow. The deck output folder was renamed to
dist/apresentacao/. Companion of tools/slides_edits_2026-09-15.py.

Usage:
    python tools/roteiro_edits_2026-09-15.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PATH = Path("dist/roteiro-apresentacao.html")
s = PATH.read_text(encoding="utf-8")


def swap(old: str, new: str, count: int = 1) -> None:
    global s
    assert s.count(old) == count, (old[:60], s.count(old))
    s = s.replace(old, new)


# --- paths and counts -----------------------------------------------------------------------
swap("dist/apresentacao-pcc/index.html", "dist/apresentacao/index.html", 2)
swap("(17 slides)", "(18 slides)")
swap("a soma dá cerca de 18 min", "a soma dá cerca de 19 min")
swap(
    "pule os slides 7 e 16 e corte o 13 pela metade. Se der 15, pule só o 16.",
    "pule os slides 7 e 17 e corte o 14 pela metade. Se der 15, pule só o 17.",
)
swap(
    "nos slides 2, 3, 5, 6, 8, 9 (linha do tempo), 10, 12, 13, 15, 16 e 17.",
    "nos slides 2, 3, 5, 6, 8, 9 (linha do tempo), 11, 13, 14, 16, 17 e 18.",
)
swap(
    "pular o 7 (objetivos estão implícitos no 11 e 12) e o 16, e fazer o 13 sem mover os controles.",
    "pular o 7 (objetivos estão implícitos no 12 e 13) e o 17, e fazer o 14 sem mover os controles.",
)

# --- renumber cards 17..11 -> 18..12 ------------------------------------------------------------
for n in range(17, 10, -1):
    swap(f'<div class="card slide"><span class="n">{n}</span>', f'<div class="card slide"><span class="n">{n + 1}</span>')

# --- card 10: classification only ---------------------------------------------------------------
swap(
    "<h3>Classificação da pesquisa e uso de IA</h3>\n<p class=\"meta\"><b>60 s</b>",
    "<h3>Classificação da pesquisa</h3>\n<p class=\"meta\"><b>40 s</b>",
)
swap(
    "<p>Uso de IA declarado, conforme a Portaria CNPq 2.664 de 2026, que pede ferramenta e finalidade. "
    "Ferramenta: Claude Code. Finalidade: entender o tema do projeto e ajudar a buscar mais artigos, num "
    "<em>LLM Wiki</em> no repositório, padrão de Karpathy (2026). Eu curei as fontes, conferi cada citação "
    "na obra original e respondo pelo texto.</p>\n",
    "<p>Exploratória merece uma frase a mais: o que já existe compara <em>harnesses</em> em suítes de tarefas "
    "isoladas; ninguém publicou dois <em>harnesses</em> construindo o mesmo produto completo do zero.</p>\n",
)
swap(
    "<li>A classificação segue sem manual citado: as referências do projeto são só sobre o <em>harness</em>. "
    "<b>Brasil (2026)</b>: Portaria CNPq nº 2.664, de 6 de março de 2026, Política de Integridade. "
    "<b>Karpathy (2026)</b>: <em>gist</em> \"LLM Wiki\", o padrão que o repositório instancia.</li>",
    "<li>A classificação segue sem manual citado: as referências do projeto são sobre o <em>harness</em> e "
    "sobre o método de trabalho declarado no slide seguinte.</li>",
)
swap(
    "<li><b>\"O que a IA escreveu?\"</b>Nada do texto final. Ela leu fontes e montou resumos numa wiki; cada "
    "afirmação que entrou no projeto eu conferi no original.</li>",
    "<li><b>\"Por que não cita Gil ou Prodanov?\"</b>Porque a lista de referências fica no tema; a "
    "classificação é a da disciplina e não precisa de citação para se sustentar.</li>",
)

# --- new card 11 ---------------------------------------------------------------------------------
CARD11 = """<div class="card slide"><span class="n">11</span>
<h3>Uso de IA declarado: dois métodos</h3>
<p class="meta"><b>75 s</b> · <kbd>→</kbd> revela o cartão da esquerda, depois o da direita</p>
<div class="blk"><b>Fale</b><div class="say">
<p>A Portaria CNPq 2.664 de 2026 pede que o uso de IA generativa seja declarado com ferramenta e finalidade. A ferramenta foi o Claude Code. Usei dois métodos, e nos dois o papel é o mesmo: eu decido e confiro, o agente escreve.</p>
<p>Para as fontes, um <em>LLM Wiki</em>, padrão de Karpathy (2026). As fontes brutas ficam guardadas sem alteração; eu escolho o que entra. O agente escreve uma página de síntese por fonte e liga entidades e conceitos. Cada operação entra num registro cronológico, e quando duas fontes se contradizem, a dúvida vai para uma fila que eu resolvo. Cada afirmação que entrou no texto eu conferi na obra original. Foram 29 fontes e 46 páginas; nenhuma frase do projeto foi escrita pelo agente.</p>
<p>Para a especificação do Finn, o Helmsman, uma rotina que eu mesmo escrevi. A ideia solta vira um mapa de decisões no rastreador de issues: 21 <em>tickets</em> sob um mapa. Cada pergunta passa por um teste: muda o que a pessoa que usa o sistema vive, ou o que o negócio ganha? Se sim, é minha, e o agente só me pergunta isso, em conversa: foram 9. Se não, é dele: 12 decisões técnicas que ele tomou sozinho, cada uma registrada com as alternativas, o critério e o que trava para as seguintes. Quando a decisão dependia de um fato de fora, como a cobrança do WhatsApp ou o modelo de voz em português, o agente abriu subagentes de pesquisa, esperou o resultado e só então decidiu: 3 <em>tickets</em>. O mapa fechou sem nada a decidir, e é a base da especificação congelada que os dois braços recebem.</p>
</div></div>
<div class="blk"><b>Fontes</b><ul class="src">
<li><b>Brasil (2026)</b>: Portaria CNPq nº 2.664, de 6 de março de 2026, Política de Integridade; pede ferramenta e finalidade. <b>Karpathy (2026)</b>: <em>gist</em> "LLM Wiki", o padrão que o repositório (YuukiFST, 2026c) instancia. <b>YuukiFST (2026a)</b>: repositório agent-dotfiles, pasta <code>skills/helmsman</code>; o mapa do Finn é a issue #1 do repositório Finn (YuukiFST, 2026b), com os <em>tickets</em> #2–#22 fechados.</li>
</ul></div>
<div class="blk"><b>Se perguntarem</b><ul class="q">
<li><b>"O que a IA escreveu?"</b>Nada do texto final. Ela leu fontes e montou resumos numa wiki, e tomou decisões técnicas do Finn que eu revisei; cada afirmação que entrou no projeto eu conferi no original.</li>
<li><b>"O agente decidiu a pilha do Finn sozinho?"</b>Não. A pilha foi uma preferência minha registrada no mapa antes de qualquer <em>ticket</em>; o agente decidiu como usá-la, e cada decisão está aberta em uma issue com as alternativas rejeitadas.</li>
<li><b>"Isso não contamina o experimento?"</b>A especificação é a mesma para os dois braços, e as decisões foram tomadas antes de qualquer execução. O experimento mede o custo de construir a partir dela; o custo de escrevê-la fica fora da medida.</li>
</ul></div>
</div>

"""
swap('<div class="card slide"><span class="n">12</span>\n<h3>Método: duas camadas de medição</h3>', CARD11 + '<div class="card slide"><span class="n">12</span>\n<h3>Método: duas camadas de medição</h3>')

# --- question bank --------------------------------------------------------------------------------
swap(
    "<li><b>\"Onde entra a IA generativa no seu trabalho?\"</b>Declarado conforme a Portaria CNPq 2.664/2026: "
    "Claude Code, para entender o tema e buscar mais artigos num <em>LLM Wiki</em>, padrão de Karpathy (2026). "
    "O texto e as citações são meus e conferidos no original.</li>",
    "<li><b>\"Onde entra a IA generativa no seu trabalho?\"</b>Declarado conforme a Portaria CNPq 2.664/2026: "
    "Claude Code, em dois métodos. Um <em>LLM Wiki</em> (Karpathy, 2026) para entender o tema e buscar artigos, "
    "e o Helmsman, rotina minha, para registrar as decisões do Finn antes do experimento: eu respondi o que o "
    "sistema faz, o agente decidiu como construir e pesquisou com subagentes o que dependia de fato externo. "
    "O texto e as citações são meus e conferidos no original.</li>",
)

PATH.write_text(s, encoding="utf-8")
print("ok")
