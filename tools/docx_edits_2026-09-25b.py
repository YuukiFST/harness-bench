"""Humanizer pass on dist/projeto-de-pesquisa.docx, 2026-09-25, after tools/docx_edits_2026-09-25.py.

Detect pass over [43]-[86]: no "não X, mas Y" outside the Lin quote, no dashes, about one
colon per paragraph, and the four causal closers ([71], [73], [81], [83]) each answer a real
objection, so they stay. Two minimum edits:

- [44] The Finn gloss made "com o OpenCode e com o Pi" read as attached to "empresas";
  the product is named in its own sentence.
- [84] "a fração de testes aprovada" -> "aprovados", the term used in [78] and [83].
- [65], [74], [75] Three short cuts that give back the lines the fixes cost (page budget).

Run once: python tools/docx_edits_2026-09-25b.py
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from docx_prose import apply  # noqa: E402

DOCX = Path("dist/projeto-de-pesquisa.docx")

# (paragraph, old substring, new substring); each old must occur exactly once.
SUBS = [
    ("44", "Este projeto constrói o mesmo produto, o Finn, um SaaS voltado para o setor financeiro das empresas, com o OpenCode e com o Pi, sobre o mesmo modelo e a mesma especificação, e conta os tokens fora do *harness*.",
     "Este projeto constrói o mesmo produto com o OpenCode e com o Pi, sobre o mesmo modelo e a mesma especificação, e conta os tokens fora do *harness*. O produto é o Finn, um SaaS voltado para o setor financeiro das empresas."),
    ("84", "com a fração de testes aprovada,", "com a fração de testes aprovados,"),
    # Page budget: the fixes of docx_edits_2026-09-25.py cost three lines and pushed 6 REFERÊNCIAS
    # to p. 9 in Word. Each cut below removes a one-word last line.
    ("65", "Lin *et al.* (2026) delimitam o que essa camada contém:", "Lin *et al.* (2026) delimitam essa camada:"),
    ("74", "na obra original", "na obra"),
    ("75", "A Camada 2 mede a construção do produto contra o modelo real.", "A Camada 2 mede a construção contra o modelo real."),
]


def main() -> None:
    dump = subprocess.run([sys.executable, "tools/docx_prose.py", "dump", str(DOCX)],
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout
    text = dict(re.findall(r"^\[(\d+)\] (.*)$", dump, re.M))
    edits: dict[str, str] = {}
    for i, old, new in SUBS:
        cur = edits.get(i, text[i])
        if cur.count(old) != 1:
            raise SystemExit(f"[{i}] changed since this script was written: {old[:50]}")
        edits[i] = cur.replace(old, new)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"paragraphs": edits}, f, ensure_ascii=False)
    apply(DOCX, Path(f.name))
    Path(f.name).unlink()


if __name__ == "__main__":
    main()
