"""Tabela 2 (cronograma) of dist/projeto-de-pesquisa.docx, 2026-09-23.

The author moved "Execução da matriz de experimentos" (dez–jan) and "Análise dos
resultados" (jan) to October 2026. December and January are left without any X,
so their columns go, as in the course template, which lists only months with work
(files/Template projeto novo3.pdf, §5). The freed width goes to the four month
columns; the table keeps its total width.

docx_prose.py rewrites text only: it cannot move a table cell or delete a column,
so this pass edits the table XML directly, as set_sumario() does in docx_edits_2026-09-23.py.

Run once on the f0d5889 docx: python tools/docx_edits_2026-09-23b.py
"""
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from docx_prose import _rewrite_zip  # noqa: E402

DOCX = Path("dist/projeto-de-pesquisa.docx")
TABLE = re.compile(r"<w:tbl>.*?</w:tbl>", re.S)
ROW = re.compile(r"<w:tr[ >].*?</w:tr>", re.S)
CELL = re.compile(r"<w:tc>.*?</w:tc>", re.S)
GRID = re.compile(r"<w:tblGrid>(?:<w:gridCol w:w=\"\d+\"/>)+")
# Cell index per column: 0 phase, 1 ago, 2 set, 3 out, 4 nov, 5 dez, 6 jan.
OUT, DEZ, JAN = 3, 5, 6
MOVES = {"EXECUÇÃO DA MATRIZ DE EXPERIMENTOS": DEZ, "ANÁLISE DOS RESULTADOS": JAN}
PHASE_W, TABLE_W, MONTHS = 4309, 10021, 4


def edit_row(row: str) -> str:
    cells = CELL.findall(row)
    if len(cells) != 7:
        raise SystemExit(f"row has {len(cells)} cells, expected 7")
    for label, src in MOVES.items():
        if label in cells[0]:
            cells[OUT] = cells[src]
    head = row[: row.index("<w:tc>")]
    tail = row[row.rindex("</w:tc>") + len("</w:tc>"):]
    return head + "".join(cells[:DEZ]) + tail


def main() -> None:
    xml = zipfile.ZipFile(DOCX).read("word/document.xml").decode("utf-8")
    hits = [t for t in TABLE.findall(xml) if "JANEIRO" in t]
    if len(hits) != 1:
        raise SystemExit(f"cronograma table matched {len(hits)} times")
    old = hits[0]
    new = ROW.sub(lambda m: edit_row(m.group(0)), old)
    month_w = (TABLE_W - PHASE_W) // MONTHS
    grid = "<w:tblGrid>" + f'<w:gridCol w:w="{PHASE_W}"/>' + f'<w:gridCol w:w="{month_w}"/>' * MONTHS
    new, n = GRID.subn(grid, new)
    if n != 2:  # tblGrid and the tblGrid inside tblGridChange
        raise SystemExit(f"tblGrid matched {n} times, expected 2")
    if "DEZEMBRO" in new or "JANEIRO" in new:
        raise SystemExit("december or january column survived")
    _rewrite_zip(DOCX, {"word/document.xml": xml.replace(old, new, 1).encode("utf-8")})
    print(f"cronograma: {MONTHS} months, X moved to OUTUBRO")


if __name__ == "__main__":
    main()
