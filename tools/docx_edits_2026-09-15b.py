"""Title edit applied to dist/projeto-de-pesquisa.docx on 2026-09-15.

The subtitle named the method (OpenCode, pi, a SaaS, "sob um mesmo modelo")
instead of delimiting the theme, so the cover read as a study of two tools.
The new subtitle mirrors the theme paragraph [29]: the effect of the harness
on tokens and success rate of coding agents building the same product with
the language model held fixed. Tools, product and arms stay in the objectives
and in section 3. Paragraphs [5] (cover) and [10] (folha de rosto) carry the
title; indices are the ones `tools/docx_prose.py dump` printed before this edit.

Usage:
    python tools/docx_prose.py dump dist/projeto-de-pesquisa.docx > .tmp/prose.txt
    python tools/docx_edits_2026-09-15b.py > .tmp/edits.json
    python tools/docx_prose.py apply dist/projeto-de-pesquisa.docx .tmp/edits.json
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PROSE = Path(".tmp/prose.txt").read_text(encoding="utf-8").splitlines()

OLD = ("O HARNESS COMO DECISÃO DO DESENVOLVEDOR: TOKENS E TAXA DE SUCESSO DO OPENCODE E DO PI "
       "NA CONSTRUÇÃO DE UM MESMO SAAS SOB UM MESMO MODELO")
NEW = ("O HARNESS COMO DECISÃO DO DESENVOLVEDOR: EFEITO SOBRE TOKENS E TAXA DE SUCESSO DE AGENTES "
       "DE CODIFICAÇÃO NA CONSTRUÇÃO DE UM MESMO PRODUTO COM O MODELO DE LINGUAGEM FIXO")

edits = {}
for line in PROSE:
    idx, _, text = line.partition("] ")
    if text == OLD:
        edits[idx.lstrip("[")] = NEW
assert sorted(edits) == ["10", "5"], edits

print(json.dumps({"paragraphs": edits}, ensure_ascii=False, indent=2))
