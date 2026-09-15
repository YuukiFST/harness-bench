"""Prose edits applied to dist/projeto-de-pesquisa.docx on 2026-09-15.

After the subtitle change (tools/docx_edits_2026-09-15b.py) the general
objective [33] and H1 [45] still read as if OpenCode and pi were the object of
study. Both now state the theme first (the difference attributable to the
harness, model fixed, same product) and name OpenCode, pi and Finn as the arms
and the product that instantiate it. Indices are the ones
`tools/docx_prose.py dump` printed before this edit.

Usage:
    python tools/docx_prose.py dump dist/projeto-de-pesquisa.docx > .tmp/prose.txt
    python tools/docx_edits_2026-09-15c.py > .tmp/edits.json
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


assert para(33).startswith("Medir, com o modelo de linguagem mantido fixo, a diferença de tokens consumidos e de taxa de sucesso entre o OpenCode e o pi")
assert para(45).startswith("H1: entre o OpenCode e o pi executando o mesmo modelo")

P33 = ("Medir, com o modelo de linguagem mantido fixo, a diferença de tokens consumidos e de taxa de sucesso "
       "atribuível ao *harness* na construção do mesmo produto de software a partir da mesma especificação, "
       "tomando como braços dois *harnesses* de código aberto, o OpenCode e o pi, separando a parte dessa "
       "diferença que vem da carga fixa por requisição, e entregar o resultado como critério de escolha "
       "reproduzível pelo desenvolvedor.")

P45 = ("H1: entre dois *harnesses* executando o mesmo modelo, o OpenCode e o pi, a diferença de tokens gastos "
       "para construir o mesmo produto, o Finn, a partir da mesma especificação é de ordem prática relevante "
       "para quem paga a conta, comparável à diferença obtida ao se trocar de modelo sob um *harness* fixo. "
       "H1 será refutada se os intervalos de tokens por construção dos dois braços se sobrepuserem e o teste "
       "pareado por unidade não apontar diferença.")

print(json.dumps({"paragraphs": {"33": P33, "45": P45}}, ensure_ascii=False, indent=2))
