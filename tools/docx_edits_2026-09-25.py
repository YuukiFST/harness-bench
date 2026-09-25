"""Edit of dist/projeto-de-pesquisa.docx, 2026-09-25: fixes from the reference check
(wiki/queries/2026-09-25-verificacao-referencias-projeto.md) on the text of 9c0fe11.

- [44] 9c0fe11 left "paga pagando também" and a last clause without a verb
  ("e a conta de tokens fora do harness"); the Finn gloss the author added stays.
- [68] Zhang et al. p. 4: "HV is often comparable to or larger than MV"; "often" was missing.
- [68] Lin et al. never says the human-written harnesses of Table 1 ran on GPT-5.4: §4.1 fixes
  GPT-5.4 only for AHE's own three agents, and only Table 2's caption says "all four columns run
  on GPT-5.4". "sobre o GPT-5.4" goes; the numbers and the benchmark stay.
- [69] 9c0fe11 dropped "imposto do harness" from [44], so "o imposto" had no antecedent.
- [76] Earendil (2026) never says Pi is open source; Pan et al. (2026) does ("Pi, a minimal,
  open-source harness") and the OpenCode repository does ("The open source coding agent", MIT).
- [77] The Finn map (#1) has 24 decision tickets since 2026-09-16 (#2-#25, "Part of #1"), not 21.
- [83] "comum em ambos" -> "comum aos dois".

Run once, after 9c0fe11: python tools/docx_edits_2026-09-25.py
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
    ("44", "Quem paga por tokens paga pagando também essa diferença.", "Quem paga por tokens paga também essa diferença."),
    ("44", "o Finn, um SaaS voltado para o setor financeiro das empresas, e ele será construído com o OpenCode e com o Pi, sobre o mesmo modelo e a mesma especificação, e a conta de tokens fora do *harness*.",
     "o Finn, um SaaS voltado para o setor financeiro das empresas, com o OpenCode e com o Pi, sobre o mesmo modelo e a mesma especificação, e conta os tokens fora do *harness*."),
    ("68", "*harnesses* escritos por humanos sobre o GPT-5.4 vão de", "*harnesses* escritos por humanos vão de"),
    ("68", "a variação de desempenho devida ao *harness* é comparável ou maior",
     "a variação de desempenho devida ao *harness* é frequentemente comparável ou maior"),
    ("69", "o imposto pode começar na primeira requisição", "o imposto do *harness* pode começar na primeira requisição"),
    ("76", "Os dois são de código aberto.", "Os dois são de código aberto (Opencode, 2026a; Pan *et al.*, 2026)."),
    ("77", "decidido em 21 *tickets*", "decidido em 24 *tickets*"),
    ("83", "O pareamento remove a dificuldade comum em ambos *coding agents *(Miller, 2024).",
     "O pareamento remove a dificuldade comum aos dois *coding agents* (Miller, 2024)."),
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
