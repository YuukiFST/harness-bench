"""Prose edit applied to dist/projeto-pcc.docx on 2026-09-14 (second pass).

The §3 paragraph that declares the LLM Wiki method now names the pattern's
origin, Karpathy (2026), and the reference list gains that entry after the
two Kapoor entries. Off-theme; exception recorded in AGENTS.md on 2026-09-14.
Paragraph indices are the ones `tools/docx_prose.py dump` printed before
this edit.

Usage:
    python tools/pcc_edits_2026-09-14b.py > /tmp/edits.json
    python tools/docx_prose.py apply dist/projeto-pcc.docx /tmp/edits.json
"""

import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

P58 = ("O levantamento das fontes deste projeto foi feito com apoio de um *LLM Wiki*, padrão descrito por "
"Karpathy (2026) e mantido no repositório do projeto (YuukiFST, 2026b). Nesse arranjo, as fontes brutas ficam "
"guardadas sem alteração, um agente de codificação escreve as páginas de síntese, cada operação entra em um "
"registro cronológico e as dúvidas vão para uma fila de revisão. O autor curou as fontes e revisou cada síntese, "
"e cada afirmação citada neste texto foi conferida na obra original, com o trecho copiado ao lado do veredito. "
"A Portaria CNPq nº 2.664/2026 pede que o uso de inteligência artificial generativa seja declarado com a "
"ferramenta e a finalidade (Brasil, 2026). A ferramenta foi o Claude Code, e a finalidade foi que o agente "
"entendesse o tema do projeto e ajudasse a buscar mais artigos sobre o tema escolhido. O autor responde pelo "
"texto final.")

REF = ("KARPATHY, Andrej. LLM Wiki: a pattern for building personal knowledge bases using LLMs. 2026. Gist "
"(GitHub). Disponível em: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f. "
"Acesso em: 14 set. 2026.")

print(json.dumps({"paragraphs": {"58": P58}, "insert_after": {"176": REF}}, ensure_ascii=False, indent=2))
