# -*- coding: utf-8 -*-
"""Build the class deliverable from dist/projeto-pcc.docx.

The assignment is a partial delivery: the template filled with the introducao,
the referencial teorico carrying four citations, and the references those
citations need. Sections 3, 4 and 5 of the full project are out of scope, so
they are dropped here rather than written twice, and the reference list keeps
only what the remaining text cites -- Aula 3: "Fazer as referencias de todos os
trabalhos que foram citados no seu projeto".

Derived from the full document instead of generated from scratch, so cover,
folha de rosto, margins, header, fonts and spacing are byte-identical to what
the template already produced.
"""
import html
import re
import shutil
import zipfile
from pathlib import Path

SRC = Path(r"C:\Users\Desenvolvimento\Desktop\harness-bench\dist\projeto-pcc.docx")
DST = Path(r"C:\Users\Desenvolvimento\Desktop\harness-bench\dist\atividade-introducao-e-citacoes.docx")
WORK = Path(r"C:\Users\Desenvolvimento\Desktop\pcc-patch\work-atividade")

ELEMENT = re.compile(r"<w:p/>|<w:p>.*?</w:p>|<w:tbl>.*?</w:tbl>|<w:sectPr.*?</w:sectPr>", re.S)

# Reference entries whose only in-text citation lived in sections 3, 4 or 5.
DROP_REFS = (
    "DATACURVE.",
    "GIL, Antonio Carlos.",
    "HUANG, Wenqi;",
    "JIMENEZ, Carlos E.;",
    "LIU, Nelson F.;",
    "MILLER, Evan.",
    "OPENCODE. Zen.",
    "PRODANOV, Cleber Cristiano;",
    "YUUKIFST.",
)

SUMARIO = [
    ("1 INTRODU\u00c7\u00c3O", "1"),
    ("2 REFERENCIAL TE\u00d3RICO", "3"),
    ("3 REFER\u00caNCIAS", "4"),
]

FONTS = ('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
         'w:cs="Times New Roman"/>')


def sumario_p(title, page):
    return (
        "<w:p><w:pPr><w:tabs><w:tab w:pos=\"9071\" w:val=\"right\"/></w:tabs>"
        '<w:spacing w:line="360" w:lineRule="auto" w:after="0"/>'
        '<w:ind w:firstLine="0"/></w:pPr>'
        "<w:r><w:rPr>" + FONTS + '<w:b w:val="0"/><w:i w:val="0"/>'
        '<w:sz w:val="24"/></w:rPr>'
        "<w:t>" + html.escape(title) + "</w:t><w:tab/>"
        "<w:t>" + page + "</w:t></w:r></w:p>"
    )


def text_of(el):
    # `<w:t[^>]*>` also matches `<w:tabs>`, which silently turns a sumario line
    # into markup soup and makes every index_of() below land on the wrong element.
    return html.unescape("".join(re.findall(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", el, re.S)))


def main():
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    with zipfile.ZipFile(SRC) as z:
        names = z.namelist()
        z.extractall(WORK)

    xml_path = WORK / "word" / "document.xml"
    xml = xml_path.read_text(encoding="utf-8")
    start = xml.index("<w:body>") + len("<w:body>")
    end = xml.index("</w:body>")
    head, body, tail = xml[:start], xml[start:end], xml[end:]

    els = ELEMENT.findall(body)
    assert "".join(els) == body, "body holds something this script would drop"

    def index_of(prefix, start=0):
        for i in range(start, len(els)):
            if text_of(els[i]).startswith(prefix):
                return i
        raise AssertionError(prefix)

    i_sumario = index_of("SUM\u00c1RIO")
    i_sum_first = index_of("1 INTRODU\u00c7\u00c3O")          # sumario line, not the heading
    i_sum_last = index_of("6 REFER\u00caNCIAS")
    # Searched past the sumario, whose lines carry the same headings.
    i_mat = index_of("3 MATERIAL E M\u00c9TODO", i_sum_last + 1)
    i_refs = index_of("6 REFER\u00caNCIAS", i_mat)
    assert i_sumario < i_sum_first < i_sum_last < i_mat < i_refs

    keep = []
    for i, el in enumerate(els):
        if i_sum_first <= i <= i_sum_last:
            continue                                   # old sumario, rebuilt below
        if i_mat <= i < i_refs:
            continue                                   # sections 3, 4 and 5
        if i == i_refs:
            keep.append(el.replace("6 REFER\u00caNCIAS", "3 REFER\u00caNCIAS"))
            continue
        if i > i_refs and text_of(el).startswith(DROP_REFS):
            continue
        keep.append(el)
        if i == i_sumario:
            keep.extend(sumario_p(t, p) for t, p in SUMARIO)

    new_body = "".join(keep)
    xml_path.write_text(head + new_body + tail, encoding="utf-8")

    with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as z:
        for name in names:
            z.write(WORK / name, name)

    kept = [text_of(e)[:60] for e in keep]
    print("elements: %d -> %d" % (len(els), len(keep)))
    for line in kept:
        if line.strip():
            print("  " + line)


if __name__ == "__main__":
    main()
