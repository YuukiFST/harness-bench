"""Fourth edit of dist/projeto-de-pesquisa.docx, 2026-09-24, on four defects
of the author's revision, fixed at the author's request:

- Tabelas 1 and 2 lost "Fonte: elaborado pelo autor (2026)." The course
  template puts the source under every table; the line goes back into the
  empty paragraph each table left behind, with the 10 pt run it had at 8341dfd.
- Tabela 2 is back to six months with DEZEMBRO and JANEIRO empty and 10021
  twips wide. Same fix as docx_edits_2026-09-23b.py and 23c.py: the empty
  columns go (the template lists only months with work), the table takes the
  9071-twip text block, side padding 2.85 pt, phase column 4191, months 1220,
  and every X at 9 pt.
- One term for one thing: [62] says "*system prompt*", the author's latest
  wording, so [66], [67] and [75] follow it instead of "prompt de sistema".
- [96] loses its trailing space.
Narrowing Tabela 2 brings 6 REFERÊNCIAS back to page 8 (Word: 9 pages), so
the sumário line returns from 6 to 5.

docx_prose.py rewrites text only, so the tables are edited in the XML, as in
set_sumario().

Run once, after tools/docx_edits_2026-09-24c.py: python tools/docx_edits_2026-09-24d.py
"""
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from docx_prose import _rewrite_zip, apply  # noqa: E402

DOCX = Path("dist/projeto-de-pesquisa.docx")
TABLE = re.compile(r"<w:tbl>.*?</w:tbl>", re.S)
ROW = re.compile(r"<w:tr[ >].*?</w:tr>", re.S)
CELL = re.compile(r"<w:tc>.*?</w:tc>", re.S)
GRID = re.compile(r"<w:tblGrid>(?:<w:gridCol w:w=\"\d+\"/>)+")
EMPTY_RUN = re.compile(r'(<w:r [^>]*>)<w:rPr><w:rtl w:val="0"/></w:rPr></w:r>')
FONTE_RPR = '<w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/><w:rtl w:val="0"/></w:rPr>'
FONTE = "Fonte: elaborado pelo autor (2026)."
TEXT_W, MONTHS, MONTH_W = 9071, 4, 1220
PHASE_W = TEXT_W - MONTHS * MONTH_W
CELL_MAR = '<w:tblCellMar><w:left w:w="57" w:type="dxa"/><w:right w:w="57" w:type="dxa"/></w:tblCellMar>'
BARE_X = '<w:rPr><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">X</w:t>'
SIZED_X = '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">X</w:t>'


def add_fonte(xml: str, table: str) -> str:
    end = xml.index(table) + len(table)
    para_end = xml.index("</w:p>", end)
    para = xml[end:para_end]
    if FONTE in para or "<w:t" in para:
        raise SystemExit("paragraph after the table is not empty")
    m = EMPTY_RUN.search(para)
    if not m:
        raise SystemExit("no empty run after the table")
    run = f'{m.group(1)}{FONTE_RPR}<w:t xml:space="preserve">{FONTE}</w:t></w:r>'
    para = para[: m.start()] + run + para[m.start():]
    return xml[:end] + para + xml[para_end:]


def cronograma(table: str) -> str:
    def row(r: str) -> str:
        cells = CELL.findall(r)
        if len(cells) != 7:
            raise SystemExit(f"row has {len(cells)} cells, expected 7")
        if any("X" in re.sub(r"<[^>]+>", "", c) for c in cells[5:]):
            raise SystemExit("december or january has an X")
        return r[: r.index("<w:tc>")] + "".join(cells[:5]) + r[r.rindex("</w:tc>") + len("</w:tc>"):]

    new = ROW.sub(lambda m: row(m.group(0)), table)
    new, n = re.subn(r'<w:tblW w:w="[\d.]+" w:type="dxa"/>', f'<w:tblW w:w="{TEXT_W}" w:type="dxa"/>', new)
    if n != 1:
        raise SystemExit(f"tblW matched {n} times")
    if "<w:tblCellMar>" not in new:
        new = new.replace('<w:tblLayout w:type="fixed"/>', '<w:tblLayout w:type="fixed"/>' + CELL_MAR, 1)
    grid = "<w:tblGrid>" + f'<w:gridCol w:w="{PHASE_W}"/>' + f'<w:gridCol w:w="{MONTH_W}"/>' * MONTHS
    new, n = GRID.subn(grid, new)
    if n not in (1, 2):
        raise SystemExit(f"tblGrid matched {n} times")
    return new.replace(BARE_X, SIZED_X)


def prose() -> None:
    dump = subprocess.run([sys.executable, "tools/docx_prose.py", "dump", str(DOCX)],
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout
    text = dict(re.findall(r"^\[(\d+)\] (.*)$", dump, re.M))
    edits = {}
    for i in ("66", "67", "75"):
        new = re.sub(r"(?:o |um )?\*?prompt\*? de sistema", lambda m: m.group(0).split("prompt")[0].replace("*", "") + "*system prompt*", text[i])
        if new == text[i]:
            raise SystemExit(f"[{i}] has no 'prompt de sistema'")
        edits[i] = new
    edits["96"] = text["96"].rstrip()
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"paragraphs": edits}, f, ensure_ascii=False)
    apply(DOCX, Path(f.name))
    Path(f.name).unlink()


def main() -> None:
    prose()
    xml = zipfile.ZipFile(DOCX).read("word/document.xml").decode("utf-8")
    tables = TABLE.findall(xml)
    orcamento = [t for t in tables if "Custo" in t]
    crono = [t for t in tables if "JANEIRO" in t]
    if len(orcamento) != 1 or len(crono) != 1:
        raise SystemExit("expected one budget table and one six-month cronograma")
    new_crono = cronograma(crono[0])
    xml = xml.replace(crono[0], new_crono, 1)
    xml = add_fonte(xml, orcamento[0])
    xml = add_fonte(xml, new_crono)
    xml, hits = re.subn(r'(<w:t xml:space="preserve">6 REFERÊNCIAS</w:t><w:tab/><w:t xml:space="preserve">)\d+(</w:t>)',
                        r"\g<1>5\g<2>", xml)
    if hits != 1:
        raise SystemExit(f"sumário line matched {hits} times")
    _rewrite_zip(DOCX, {"word/document.xml": xml.encode("utf-8")})


if __name__ == "__main__":
    main()
