"""Script edit applied to dist/roteiro-apresentacao.html on 2026-09-15.

The docx title changed its subtitle (tools/docx_edits_2026-09-15b.py): it now
delimits the theme instead of naming the tools. The spoken opening of the
script repeats the title, so it follows.

Usage:
    python tools/roteiro_edits_2026-09-15b.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PATH = Path("dist/roteiro-apresentacao.html")
s = PATH.read_text(encoding="utf-8")

OLD = ('O projeto se chama "O <em>harness</em> como decisão do desenvolvedor": tokens e taxa de sucesso '
       'do OpenCode e do pi construindo um mesmo SaaS sob um mesmo modelo.')
NEW = ('O projeto se chama "O <em>harness</em> como decisão do desenvolvedor": efeito sobre tokens e taxa '
       'de sucesso de agentes de codificação na construção de um mesmo produto com o modelo de linguagem fixo.')
assert s.count(OLD) == 1, s.count(OLD)
PATH.write_text(s.replace(OLD, NEW), encoding="utf-8")
print("ok")
