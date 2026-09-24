"""Third edit of dist/projeto-de-pesquisa.docx, 2026-09-24: the author names
the harness "Pi", as in its own title (Earendil, 2026: "Pi, minimal and
performant"), instead of "PI". Only the standalone word changes; API and
SoL-Pi are untouched. The reference list [181] onwards is not rewritten.

Run once, after tools/docx_edits_2026-09-24b.py: python tools/docx_edits_2026-09-24c.py
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from docx_prose import apply  # noqa: E402

DOCX = Path("dist/projeto-de-pesquisa.docx")
LAST_PROSE = 180  # 6 REFERÊNCIAS heading; entries after it keep their text.


def main() -> None:
    dump = subprocess.run([sys.executable, "tools/docx_prose.py", "dump", str(DOCX)],
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout
    edits: dict[str, str] = {}
    for line in dump.splitlines():
        m = re.match(r"\[(\d+)\] (.*)", line)
        if not m or int(m.group(1)) >= LAST_PROSE:
            continue
        new = re.sub(r"\b(PI|pi)\b", "Pi", m.group(2))
        if new != m.group(2):
            edits[m.group(1)] = new
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"paragraphs": edits}, f, ensure_ascii=False)
    apply(DOCX, Path(f.name))
    Path(f.name).unlink()


if __name__ == "__main__":
    main()
