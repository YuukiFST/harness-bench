"""Prose edits applied to dist/projeto-pcc.docx on 2026-09-14 (fourth pass).

Coherence audit of docx, deck and roteiro. Two paragraphs change: the title
page [11] said "Projeto de Conclusão de Curso"; the author confirmed the
work is a research project for the Metodologia Científica course. The
structure paragraph [47] still announced a "suíte de tarefas", a term of
the retired ticket design; the current design has a product and a
specification. Paragraph indices are the ones `tools/docx_prose.py dump`
printed before this edit.

Usage:
    python tools/pcc_edits_2026-09-14d.py > /tmp/edits.json
    python tools/docx_prose.py apply dist/projeto-pcc.docx /tmp/edits.json
"""

import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

P11 = ("Projeto de pesquisa apresentado ao Departamento de Área de Informática do Instituto Federal de "
"Educação, Ciência e Tecnologia de Mato Grosso, Campus Octayde Jorge da Silva, na disciplina de "
"Metodologia Científica do curso de Sistemas para Internet.")

P47 = ("Este trabalho está organizado em seis seções. Esta introdução apresenta a justificativa, o tema, o "
"problema, os objetivos, a metodologia e as hipóteses. A seção 2 posiciona o trabalho na literatura e "
"delimita as pendências que ele se propõe a resolver. A seção 3 descreve o material e o método: "
"classificação da pesquisa, camadas de medição, braços, produto e especificação, limites, tratamento "
"estatístico e limitações. A seção 4 apresenta o orçamento, a seção 5 o cronograma, e a seção 6 reúne as "
"referências.")

print(json.dumps({"paragraphs": {"11": P11, "47": P47}}, ensure_ascii=False, indent=2))
