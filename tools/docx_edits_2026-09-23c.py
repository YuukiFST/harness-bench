"""Tabela 2 (cronograma) layout of dist/projeto-de-pesquisa.docx, 2026-09-23.

Two defects older than the October move (docx_edits_2026-09-23b.py):
- the table was 10021 twips wide, wider than the 9071-twip text block
  (A4 11906 minus margins 1701 + 1134), so it stuck out past both margins;
  Tabela 1 already uses the text width. At that width the default 5.4 pt cell
  padding wrapped SETEMBRO and NOVEMBRO, so this table's side padding drops to
  2.85 pt (57 twips) and the phase column gives the months what the longest
  label (LEITURA E LEVANTAMENTO BIBLIOGRÁFICO) does not need.
- 8 of the 17 X marks had no size and rendered at the body size, larger than
  the 9 pt (sz 18) of every other cell in the table.

Run once on the 450954b docx: python tools/docx_edits_2026-09-23c.py
"""
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from docx_prose import _rewrite_zip  # noqa: E402

DOCX = Path("dist/projeto-de-pesquisa.docx")
TABLE = re.compile(r"<w:tbl>.*?</w:tbl>", re.S)
GRID = re.compile(r"<w:tblGrid>(?:<w:gridCol w:w=\"\d+\"/>)+")
TEXT_W, MONTHS = 9071, 4
MONTH_W = 1220
PHASE_W = TEXT_W - MONTHS * MONTH_W  # 4191
CELL_MAR = '<w:tblCellMar><w:left w:w="57" w:type="dxa"/><w:right w:w="57" w:type="dxa"/></w:tblCellMar>'
BARE_X = '<w:rPr><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">X</w:t>'
SIZED_X = '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">X</w:t>'


def main() -> None:
    xml = zipfile.ZipFile(DOCX).read("word/document.xml").decode("utf-8")
    hits = [t for t in TABLE.findall(xml) if "NOVEMBRO" in t]
    if len(hits) != 1:
        raise SystemExit(f"cronograma table matched {len(hits)} times")
    old = hits[0]
    new, n = re.subn(r'<w:tblW w:w="[\d.]+" w:type="dxa"/>', f'<w:tblW w:w="{TEXT_W}" w:type="dxa"/>', old)
    if n != 1:
        raise SystemExit(f"tblW matched {n} times")
    if "<w:tblCellMar>" in new:
        raise SystemExit("table already has cell margins")
    new = new.replace('<w:tblLayout w:type="fixed"/>', '<w:tblLayout w:type="fixed"/>' + CELL_MAR, 1)
    grid = "<w:tblGrid>" + f'<w:gridCol w:w="{PHASE_W}"/>' + f'<w:gridCol w:w="{MONTH_W}"/>' * MONTHS
    new, n = GRID.subn(grid, new)
    if n != 2:  # tblGrid and the tblGrid inside tblGridChange
        raise SystemExit(f"tblGrid matched {n} times, expected 2")
    bare = new.count(BARE_X)
    new = new.replace(BARE_X, SIZED_X)
    _rewrite_zip(DOCX, {"word/document.xml": xml.replace(old, new, 1).encode("utf-8")})
    print(f"cronograma: width {TEXT_W}, {bare} X marks set to 9 pt")


if __name__ == "__main__":
    main()
