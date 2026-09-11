"""Dump and rewrite the prose of a .docx without a generator.

`tools/build_pcc.py` stopped reproducing `dist/projeto-pcc.docx` at cd30dbe
(docs/research/estrutura-do-projeto-e-revisao-do-pcc.md §3.7), so the document
is edited in place. This script is the editing surface: `dump` prints every
non-empty paragraph as `[index] text` with `*italic*` / `**bold**` markup, and
`apply` rewrites the paragraphs named in a JSON file using the same markup.

Usage:
    python tools/docx_prose.py dump dist/projeto-pcc.docx > /tmp/prose.txt
    python tools/docx_prose.py apply dist/projeto-pcc.docx edits.json

edits.json:
    {
      "paragraphs": {"26": "New *text* here.", "67": null},   # null deletes
      "insert_after": {"185": "New paragraph, styled like paragraph 185."},
      "delete_tables_containing": ["oh-my-pi 17.2.10"]
    }

Each rewritten paragraph keeps its own paragraph properties and the run
properties of its first run; only the italic and bold flags change per chunk.
`[[FN]]` inserts a reference to footnote id 2, the ABNT divergence note.
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

PARA = re.compile(r"<w:p[ >].*?</w:p>", re.S)
TABLE = re.compile(r"<w:tbl>.*?</w:tbl>", re.S)
RUN_TEXT = re.compile(r"<w:t(?: [^>]*)?>(.*?)</w:t>", re.S)
RUN = re.compile(r"<w:r>.*?</w:r>", re.S)
RPR = re.compile(r"<w:rPr>.*?</w:rPr>", re.S)
MARKUP = re.compile(r"(\*\*.+?\*\*|\*.+?\*|\[\[FN\]\])")
FOOTNOTE_ID = 2


def _para_markup(para: str) -> str:
    """Paragraph XML -> text with *italic* and **bold** markers per run."""
    out = []
    for run in RUN.findall(para):
        text = html.unescape("".join(RUN_TEXT.findall(run)))
        if not text:
            if "footnoteReference" in run:
                out.append("[[FN]]")
            continue
        rpr = RPR.search(run)
        props = rpr.group(0) if rpr else ""
        italic = "<w:i/>" in props or '<w:i w:val="1"/>' in props
        bold = "<w:b/>" in props or '<w:b w:val="1"/>' in props
        if italic:
            text = f"*{text}*"
        if bold:
            text = f"**{text}**"
        out.append(text)
    return "".join(out)


def dump(docx: Path) -> None:
    # Windows consoles default to cp1252, which cannot print "≥" or curly quotes.
    sys.stdout.reconfigure(encoding="utf-8")
    with zipfile.ZipFile(docx) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    for i, para in enumerate(PARA.findall(xml)):
        text = _para_markup(para)
        if text.strip():
            print(f"[{i}] {text}")


def _set_flag(rpr: str, tag: str, on: bool) -> str:
    rpr = re.sub(rf"<w:{tag}(?: [^>]*)?/>", "", rpr)
    flag = f"<w:{tag}/>" if on else f'<w:{tag} w:val="0"/>'
    # rFonts must stay first inside rPr; the flag goes right after it.
    # A run without rFonts (paragraphs [52], [60] on 2026-09-11) used to lose
    # the flag entirely, so the whole paragraph came out plain.
    if "<w:rFonts" in rpr:
        return re.sub(r"(<w:rFonts[^>]*/>)", rf"\1{flag}", rpr, count=1)
    if rpr == "<w:rPr/>":
        return f"<w:rPr>{flag}</w:rPr>"
    return rpr.replace("<w:rPr>", f"<w:rPr>{flag}", 1)


def _render(para: str, markup: str) -> str:
    ppr = re.search(r"<w:pPr>.*?</w:pPr>", para, re.S)
    first = RUN.search(para)
    if first is None:
        raise ValueError("paragraph has no run to copy properties from")
    rpr = RPR.search(first.group(0))
    base = rpr.group(0) if rpr else "<w:rPr/>"
    runs = []
    for chunk in MARKUP.split(markup):
        if not chunk:
            continue
        if chunk == "[[FN]]":
            fn_rpr = re.sub(r"</w:rPr>", '<w:vertAlign w:val="superscript"/></w:rPr>', base)
            runs.append(f'<w:r>{fn_rpr}<w:footnoteReference w:id="{FOOTNOTE_ID}"/></w:r>')
            continue
        bold = chunk.startswith("**") and chunk.endswith("**")
        italic = not bold and chunk.startswith("*") and chunk.endswith("*")
        text = chunk[2:-2] if bold else chunk[1:-1] if italic else chunk
        props = _set_flag(_set_flag(base, "i", italic), "b", bold)
        escaped = html.escape(text, quote=False)
        runs.append(f'<w:r>{props}<w:t xml:space="preserve">{escaped}</w:t></w:r>')
    return f"<w:p>{ppr.group(0) if ppr else ''}{''.join(runs)}</w:p>"


def apply(docx: Path, edits_path: Path) -> None:
    edits = json.loads(edits_path.read_text(encoding="utf-8"))
    with zipfile.ZipFile(docx) as z:
        xml = z.read("word/document.xml").decode("utf-8")

    paras = PARA.findall(xml)
    changes = {int(k): v for k, v in edits.get("paragraphs", {}).items()}
    inserts = {int(k): v for k, v in edits.get("insert_after", {}).items()}
    # Walk backwards so earlier offsets stay valid after each splice.
    for idx in sorted(set(changes) | set(inserts), reverse=True):
        old = paras[idx]
        new = old
        if idx in changes:
            new = "" if changes[idx] is None else _render(old, changes[idx])
        if idx in inserts:
            new += _render(old, inserts[idx])
        start = xml.index(old)
        xml = xml[:start] + new + xml[start + len(old):]

    for needle in edits.get("delete_tables_containing", []):
        hits = [t for t in TABLE.findall(xml) if needle in html.unescape(t)]
        if len(hits) != 1:
            raise ValueError(f"{needle!r} matches {len(hits)} tables, expected 1")
        xml = xml.replace(hits[0], "", 1)

    _rewrite_zip(docx, {"word/document.xml": xml.encode("utf-8")})
    print(f"applied {len(changes)} edits and {len(inserts)} inserts to {docx}")


def _rewrite_zip(docx: Path, replacements: dict[str, bytes]) -> None:
    fd, name = tempfile.mkstemp(suffix=".docx")
    os.close(fd)  # Windows refuses to move a file whose descriptor is still open
    tmp = Path(name)
    with zipfile.ZipFile(docx) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            payload = replacements.get(item.filename, src.read(item.filename))
            dst.writestr(item, payload)
    shutil.move(str(tmp), str(docx))


def main(argv: list[str]) -> None:
    if len(argv) >= 2 and argv[0] == "dump":
        dump(Path(argv[1]))
    elif len(argv) == 3 and argv[0] == "apply":
        apply(Path(argv[1]), Path(argv[2]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
