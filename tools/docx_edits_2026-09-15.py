"""Prose edits applied to dist/projeto-de-pesquisa.docx on 2026-09-15.

The AI-use paragraph [58] declared only the LLM Wiki. The author also charted
the Finn specification with Helmsman, a skill of their own, so [58] now names
both methods and the reference list gains the agent-dotfiles repository.
Same author, same year: ABNT letters follow title order, so agent-dotfiles is
2026a, Finn moves to 2026b and harness-bench to 2026c; [58], [60], [61],
[183] and [184] carry the new letters. Paragraph indices are the ones
`tools/docx_prose.py dump` printed before this edit.

Usage:
    python tools/docx_edits_2026-09-15.py > .tmp/edits.json
    python tools/docx_prose.py apply dist/projeto-de-pesquisa.docx .tmp/edits.json
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PROSE = Path(".tmp/prose.txt").read_text(encoding="utf-8").splitlines()


def para(i: int) -> str:
    prefix = f"[{i}] "
    line = next(l for l in PROSE if l.startswith(prefix))
    return line[len(prefix):]


P58 = ("Duas partes deste projeto foram feitas com apoio de um agente de codificação. O levantamento das "
"fontes usou um *LLM Wiki*, padrão descrito por Karpathy (2026) e mantido no repositório do projeto "
"(YuukiFST, 2026c). Nesse arranjo, as fontes brutas ficam guardadas sem alteração, o agente escreve as "
"páginas de síntese, cada operação entra em um registro cronológico e as dúvidas vão para uma fila de "
"revisão. O autor curou as fontes e revisou cada síntese, e cada afirmação citada neste texto foi conferida "
"na obra original, com o trecho copiado ao lado do veredito. A especificação do Finn usou o Helmsman, uma "
"rotina escrita pelo autor (YuukiFST, 2026a) que separa as perguntas de um projeto em dois grupos: o que o "
"sistema deve fazer, que só o autor responde, e como construir, que o agente decide sozinho e registra como "
"*ticket*, com as alternativas e o critério. Quando uma decisão depende de um fato externo, como o preço de "
"uma API, o agente dispara subagentes de pesquisa e só decide com o resultado em mãos. A Portaria CNPq nº "
"2.664/2026 pede que o uso de inteligência artificial generativa seja declarado com a ferramenta e a "
"finalidade (Brasil, 2026). A ferramenta foi o Claude Code, e a finalidade foi entender o tema do projeto, "
"buscar mais artigos sobre ele e registrar as decisões de produto e de pilha do Finn antes do experimento. "
"O autor responde pelo texto final e por cada decisão de produto.")

P60 = para(60).replace("(YuukiFST, 2026b)", "(YuukiFST, 2026c)")
P61 = para(61).replace("(YuukiFST, 2026a)", "(YuukiFST, 2026b)")
P183 = para(183).replace(" 2026a. ", " 2026b. ")
P184 = para(184).replace(" 2026b. ", " 2026c. ")
NEW = ("YUUKIFST. agent-dotfiles: skill Helmsman, mapa de decisões para agentes de codificação. 2026a. "
"Repositório de código. Disponível em: https://github.com/YuukiFST/agent-dotfiles/tree/main/skills/helmsman. "
"Acesso em: 15 set. 2026.")

assert P60 != para(60) and P61 != para(61) and P183 != para(183) and P184 != para(184)

print(json.dumps({
    "paragraphs": {"58": P58, "60": P60, "61": P61, "183": P183, "184": P184},
    "insert_after": {"182": NEW},
}, ensure_ascii=False, indent=2))
