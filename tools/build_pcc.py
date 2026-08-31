"""Build dist/projeto-pcc.docx — the IFMT Projeto de Conclusão de Curso.

Structure, page budget and reduction ladder come from docs/spec/14-document-outline.md,
which is the binding specification. The spine (tema, problema, H1/H2, objetivos) is
quoted verbatim from the resolution comment of issue #9 and is never rewritten here.

Every quantitative figure in this file traces to a run or to a closed ticket:
Layer 1 numbers come from `41-layer1-request-shape.md` (measured 2026-08-28),
protocol numbers from `11-experimental-protocol.md`, control scope from
`12-harness-zero-scope.md`. Those four specs live on their own branches until
PRs #42, #45, #46 and #47 land, so they are not under `docs/spec/` here yet; the
script reads none of them at runtime. Numbers that do not exist yet are emitted
as ``[A MEDIR ...]`` markers rather than guessed, and the build prints what is
left, including any bare ticket reference that leaked into the body text.

Usage:
    python -m pip install -r tools/requirements.txt
    python tools/build_pcc.py
"""

from __future__ import annotations

import math
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.packuri import PackURI
from docx.opc.part import Part
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "dist" / "projeto-pcc.docx"

FONT = "Times New Roman"
BODY_PT = 12
HEADING_PT = 14
INDENT = Cm(1.25)

# Page-budget bookkeeping, in units of one 12 pt line at 1.5 spacing. Filled while
# the document is written so the build reports an estimate instead of asserting one.
_SECTION_LINES: dict[str, float] = {}
_current_section = "capa"

# Text-area geometry for the estimate: A4 minus the 3/2/3/2 cm margins.
# 12 pt Times New Roman averages ~5.8 pt per character, so a 16 cm (453 pt)
# measure holds ~79 characters, not the ~92 an em-width estimate suggests.
CHARS_PER_LINE = 79
LINES_PER_PAGE = 39          # 24.7 cm of text height at 1.5 line spacing

# The template caps the justificativa at 12 lines and doc 14 §3.1 calls it the
# hardest constraint in the document, so the build asserts it rather than hoping.
JUSTIFICATIVA_MAX_LINES = 12

# Length the document is allowed to reach. The 7-page figure doc 14 §5 was
# written against was a guess; the author settled it at 10 (#49), so the
# reduction ladder is a tidiness tool now rather than a gate.
PAGES_MAX = 10.0


# --------------------------------------------------------------------------
# low-level helpers
# --------------------------------------------------------------------------

def _account(text: str, *, lines: float = 0.0, factor: float = 1.0,
             extra: float = 0.0) -> None:
    """Charge a paragraph to the section being written.

    A paragraph always occupies whole lines, so the char count is rounded up;
    `factor` scales a line to the body line height (single spacing is ~0.67 of
    1.5 spacing) and `extra` adds the paragraph's vertical spacing.
    """
    used = lines if lines else max(1, math.ceil(len(text) / CHARS_PER_LINE)) * factor
    _SECTION_LINES[_current_section] = _SECTION_LINES.get(_current_section, 0.0) + used + extra


def _style_run(run, *, size=BODY_PT, bold=False, italic=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    # Word ignores font.name for complex-script and east-asian ranges unless told twice.
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:cs"), FONT)
    return run


_MARKUP = re.compile(r"(\*\*.+?\*\*|\*.+?\*|\[\[FN\]\])")


def _add_marked_runs(paragraph, text, *, size=BODY_PT, base_bold=False, doc=None):
    """Render a small markup subset: **bold**, *italic*, [[FN]] footnote anchor."""
    for chunk in _MARKUP.split(text):
        if not chunk:
            continue
        if chunk == "[[FN]]":
            _add_footnote_reference(paragraph)
        elif chunk.startswith("**") and chunk.endswith("**"):
            _style_run(paragraph.add_run(chunk[2:-2]), size=size, bold=True)
        elif chunk.startswith("*") and chunk.endswith("*"):
            _style_run(paragraph.add_run(chunk[1:-1]), size=size, italic=True, bold=base_bold)
        else:
            _style_run(paragraph.add_run(chunk), size=size, bold=base_bold)


def body(doc, text, *, indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=BODY_PT,
         space_after=0, bold=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.first_line_indent = INDENT if indent else Cm(0)
    _add_marked_runs(p, text, size=size, base_bold=bold)
    _account(re.sub(r"\*\*|\*|\[\[FN\]\]", "", text))
    return p


def label(doc, text):
    """A bold, unnumbered label paragraph — the form the department template uses."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(6)
    pf.space_after = Pt(0)
    pf.first_line_indent = Cm(0)
    _style_run(p.add_run(text), bold=True)
    _account("", lines=1.3)
    return p


def heading(doc, text):
    global _current_section
    _current_section = text
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)
    pf.first_line_indent = Cm(0)
    pf.keep_with_next = True
    _style_run(p.add_run(text.upper()), size=HEADING_PT, bold=True)
    _account("", lines=2.0)
    return p


def bullet(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.left_indent = INDENT
    pf.first_line_indent = Cm(-0.0)
    _add_marked_runs(p, text)
    _account(re.sub(r"\*\*|\*", "", text))
    return p


def caption(doc, text, *, above=True):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.space_before = Pt(6 if above else 2)
    pf.space_after = Pt(2 if above else 6)
    pf.first_line_indent = Cm(0)
    pf.keep_with_next = above
    _style_run(p.add_run(text), size=10)
    _account("", lines=0.8)
    return p


TEXT_WIDTH_CM = 16.0         # A4 minus the 3 cm and 2 cm side margins
CM_PER_CHAR_AT_12PT = 0.2045  # ~5.8 pt per character


def _table_lines(rows, size, widths):
    """Lines a table really occupies, wrapping each cell against its column."""
    cols = len(rows[0])
    col_cm = ([w.cm for w in widths] if widths
              else [TEXT_WIDTH_CM / cols] * cols)
    cm_per_char = CM_PER_CHAR_AT_12PT * size / BODY_PT
    total = 0.0
    for row in rows:
        wrapped = 1
        for value, cm in zip(row, col_cm):
            text = re.sub(r"\*\*|\*", "", value)
            capacity = max(1, int((cm - 0.2) / cm_per_char))
            wrapped = max(wrapped, math.ceil(len(text) / capacity))
        # single-spaced rows at `size`, plus the 1 pt of cell padding each side
        total += wrapped * 0.67 * size / BODY_PT + 0.12
    return total


def table(doc, rows, *, size=10, header=True, widths=None):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Fixed layout, or Word recomputes column widths from content and the
    # explicit `widths` below become advisory only.
    t.autofit = widths is None
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            cell = t.cell(r, c)
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.first_line_indent = Cm(0)
            if c > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            _add_marked_runs(p, value, size=size, base_bold=(header and r == 0))
    if widths:
        for row in t.rows:
            for cell, w in zip(row.cells, widths):
                cell.width = w
    _account("", lines=_table_lines(rows, size, widths))
    return t


# --------------------------------------------------------------------------
# footnotes — python-docx has no API for these, so the part is built by hand
# --------------------------------------------------------------------------

FOOTNOTE_ID = 2
FOOTNOTE_TEXT = (
    "Os exemplos de referência do template departamental (Instituto Federal de Mato "
    "Grosso, 2022) precedem as edições vigentes "
    "da NBR 6023 e da NBR 10520, e o template diverge de si mesmo ao alternar entre "
    "“Acesso em:” e “Acessado em:” e ao envolver endereços eletrônicos em colchetes "
    "angulares. Onde há contradição interna, seguiu-se a edição vigente: NBR 6023:2025 "
    "na lista de referências, sem colchetes angulares e com “Acesso em:” em todas as "
    "entradas, e NBR 10520:2023 nas citações do corpo do texto, com o sobrenome em "
    "caixa-alta apenas na lista de referências."
)

_W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

FOOTNOTES_XML = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:footnotes {_W}>
  <w:footnote w:type="separator" w:id="-1">
    <w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
      <w:r><w:separator/></w:r></w:p>
  </w:footnote>
  <w:footnote w:type="continuationSeparator" w:id="0">
    <w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
      <w:r><w:continuationSeparator/></w:r></w:p>
  </w:footnote>
  <w:footnote w:id="{FOOTNOTE_ID}">
    <w:p>
      <!-- CT_PPrBase is an xsd:sequence: w:spacing (21) precedes w:jc (26).
           This part is hand-built, so python-docx's ordered inserters never run
           and a wrong order reaches Word as "unreadable content". -->
      <w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>
        <w:sz w:val="20"/><w:vertAlign w:val="superscript"/></w:rPr><w:footnoteRef/></w:r>
      <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>
        <w:sz w:val="20"/></w:rPr><w:t xml:space="preserve"> {FOOTNOTE_TEXT}</w:t></w:r>
    </w:p>
  </w:footnote>
</w:footnotes>
"""

FOOTNOTES_CT = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"
)


def _add_footnote_reference(paragraph):
    run = paragraph.add_run()
    _style_run(run)
    rpr = run._element.get_or_add_rPr()
    vert = OxmlElement("w:vertAlign")
    vert.set(qn("w:val"), "superscript")
    rpr.append(vert)
    ref = OxmlElement("w:footnoteReference")
    ref.set(qn("w:id"), str(FOOTNOTE_ID))
    run._element.append(ref)


def attach_footnotes(doc):
    part = Part(
        PackURI("/word/footnotes.xml"),
        FOOTNOTES_CT,
        FOOTNOTES_XML.encode("utf-8"),
        doc.part.package,
    )
    doc.part.relate_to(part, RT.FOOTNOTES)


# --------------------------------------------------------------------------
# page setup
# --------------------------------------------------------------------------

def setup_section(section, *, numbered_from=None):
    # python-docx defaults to US Letter; NBR 14724 and the template require A4.
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(3)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(3)
    section.right_margin = Cm(2)
    if numbered_from is not None:
        pg = OxmlElement("w:pgNumType")
        pg.set(qn("w:start"), str(numbered_from))
        section._sectPr.append(pg)
        header = section.header
        header.is_linked_to_previous = False
        p = header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = p.add_run()
        _style_run(run)
        # `separate` plus a cached result: Word recomputes the field on layout,
        # but LibreOffice and headless docx->pdf converters render whatever is
        # cached, and an empty header loses the page numbering the template wants.
        for tag, attrs, text in (
            ("w:fldChar", {"w:fldCharType": "begin"}, None),
            ("w:instrText", {"xml:space": "preserve"}, " PAGE "),
            ("w:fldChar", {"w:fldCharType": "separate"}, None),
            ("w:t", {}, "1"),
            ("w:fldChar", {"w:fldCharType": "end"}, None),
        ):
            el = OxmlElement(tag)
            for k, v in attrs.items():
                el.set(qn(k), v)
            if text is not None:
                el.text = text
            run._element.append(el)


def set_default_style(doc):
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(BODY_PT)
    style.element.rPr.rFonts.set(qn("w:cs"), FONT)


# --------------------------------------------------------------------------
# document content
# --------------------------------------------------------------------------

AUTOR = "FAUSTO YUUKI T.A FREIRE"

TITULO = (
    "HARNESSES DE AGENTES DE CODIFICAÇÃO: O IMPACTO DO PROJETO DO HARNESS "
    "SOBRE O CUSTO E O DESEMPENHO DE UM MODELO DE LINGUAGEM MANTIDO FIXO"
)

# Kept as data, not inline prose, because the template caps this at 12 lines and
# the build has to be able to count them. Order fixed by doc 14 §3.1: the
# published magnitude, then this project's own measurement, then the stake.
JUSTIFICATIVA = [
    "A escolha do modelo domina a discussão sobre agentes de codificação, mas não é o "
    "único fator sob controle de quem os usa. Na Tabela 1 de Lin *et al.* (2026)[[FN]], "
    "três *harnesses* humanos sobre o mesmo modelo congelado obtêm 47,2%, 62,9% e 71,9% "
    "de pass@1, uma dispersão de 24,7 pontos percentuais atribuível só ao *harness*. O "
    "estudo da Databricks relatado por Earendil (2026) registra variação superior a 2x "
    "no custo por tarefa, sem mudança de qualidade.",

    "Com a linhagem do *harness* fixa, a diferença aparece antes de o modelo gerar um "
    "token. Na primeira requisição da mesma tarefa, o oh-my-pi, *fork* direto do pi, "
    "envia 11,4x os bytes do próprio ascendente, 64.945 contra 5.676. Falta "
    "medir quanto dessa diferença de carga chega ao resultado final, porque é isso que "
    "determina quanto do modelo pago cada *harness* aproveita.",
]

LAYER1_TABLE = [
    ["Braço", "Esquemas de ferramenta", "Bytes de ferramentas", "Bytes de system",
     "Bytes totais", "Tokens"],
    ["oh-my-pi 17.2.10", "11", "39.273", "25.395", "64.945", "16.714"],
    ["opencode 1.17.9", "9", "20.007", "9.738", "29.997", "6.659"],
    ["pi 0.80.10", "4", "2.900", "2.499", "5.676", "1.228"],
]

ORCAMENTO_TABLE = [
    ["Item", "Custo"],
    ["Inferência dos modelos (dois níveis, nível gratuito do gateway)", "R$ 0,00"],
    ["Executor e benchmark (Pier e DeepSWE, licença Apache-2.0)", "R$ 0,00"],
    ["Máquinas (estação pessoal NixOS e estação pessoal Windows)", "R$ 0,00 — já disponíveis"],
    ["**Total**", "**R$ 0,00**"],
]

CRONOGRAMA_FASES = [
    ("LEITURA E LEVANTAMENTO BIBLIOGRÁFICO", "XX   "),
    ("DEFINIÇÃO DO TEMA, DO PROBLEMA E DAS HIPÓTESES", "XX   "),
    ("CONSTRUÇÃO DO INSTRUMENTO E DO HARNESS ZERO", " XX  "),
    ("ESCREVENDO INTRODUÇÃO", "  X  "),
    ("ESCREVENDO REFERENCIAL TEÓRICO", "  X  "),
    ("ESCREVENDO MATERIAL E MÉTODO", "  XX "),
    ("EXECUÇÃO DA MATRIZ DE EXPERIMENTOS", "   XX"),
    ("ANÁLISE DOS RESULTADOS", "    X"),
    ("ELABORANDO AS REFERÊNCIAS", "    X"),
    ("REVISÃO FINAL E PREPARAÇÃO DA APRESENTAÇÃO", "    X"),
]

REFERENCIAS = [
    "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6023**: informação e documentação — "
    "referências — elaboração. 3. ed. Rio de Janeiro: ABNT, 2025a.",

    "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 10520**: informação e documentação — "
    "citações em documentos — apresentação. Rio de Janeiro: ABNT, 2023.",

    # The norm that governs this document's own genre. Added after the audit found
    # the text claiming ABNT conformity while citing only the citation and
    # reference norms (#20).
    "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 15287**: informação e documentação — "
    "projeto de pesquisa — apresentação. 3. ed. Rio de Janeiro: ABNT, 2025b.",

    "DATACURVE. **Pier**: a Harbor fork built for DeepSWE. 2026. Repositório de código. "
    "Disponível em: https://github.com/datacurve-ai/pier. Acesso em: 28 ago. 2026.",

    "EARENDIL. **Pi, minimal and performant**. 2026. Publicação de blogue institucional. "
    "Disponível em: https://earendil.com/posts/pi-autoresearch-and-databricks/. "
    "Acesso em: 28 ago. 2026.",

    "GIL, Antonio Carlos. **Como elaborar projetos de pesquisa**. 7. ed. São Paulo: Atlas, 2022.",

    "HARNESSRANK. **HarnessRank**: coding-agent harness rankings. 2026. Disponível em: "
    "https://harnessrank.net/. Acesso em: 28 ago. 2026.",

    "HUANG, Wenqi; LEE, Charley; TNG, Leonard; GE, Serena. **DeepSWE**: measuring frontier "
    "coding agents on original, long-horizon engineering tasks. arXiv:2607.07946, 2026. "
    "*Preprint*, não revisado por pares. Disponível em: https://arxiv.org/abs/2607.07946. "
    "Acesso em: 28 ago. 2026.",

    "INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE MATO GROSSO. **Normas básicas e "
    "padrões para a elaboração do Projeto de Conclusão de Curso (PCC)**. Cuiabá: Campus "
    "Octayde Jorge da Silva, Departamento de Área de Informática, 2022.",

    "JIMENEZ, Carlos E.; YANG, John; WETTIG, Alexander; YAO, Shunyu; PEI, Kexin; PRESS, Ofir; "
    "NARASIMHAN, Karthik. **SWE-bench**: can language models resolve real-world GitHub issues? "
    "arXiv:2310.06770, 2023. Trabalho apresentado na International Conference on Learning "
    "Representations (ICLR), 2024. Disponível em: https://arxiv.org/abs/2310.06770. "
    "Acesso em: 28 ago. 2026.",

    "KAPOOR, Sayash; STROEBL, Benedikt; SIEGEL, Zachary S.; NADGIR, Nitya; "
    "NARAYANAN, Arvind. **AI agents that matter**. arXiv:2407.01502, 2024. "
    "*Preprint*, não revisado por pares. Disponível em: "
    "https://arxiv.org/abs/2407.01502. Acesso em: 28 ago. 2026.",

    "KAPOOR, Sayash *et al.* **Holistic Agent Leaderboard**: the missing "
    "infrastructure for AI agent evaluation. arXiv:2510.11977, 2025. *Preprint*, não "
    "revisado por pares. Disponível em: https://arxiv.org/abs/2510.11977. "
    "Acesso em: 28 ago. 2026.",

    "LIN, Jiahang; LIU, Shichun; PAN, Chengjun; LIN, Lizhi; DOU, Shihan; XI, Zhiheng; "
    "HUANG, Xuanjing; YAN, Hang; HAN, Zhenhua; GUI, Tao; JIANG, Yu-Gang. **Agentic harness "
    "engineering**: observability-driven automatic evolution of coding-agent harnesses. "
    "arXiv:2604.25850, 2026. *Preprint*, não revisado por pares. Disponível em: "
    "https://arxiv.org/abs/2604.25850. Acesso em: 28 ago. 2026.",

    "LIU, Nelson F.; LIN, Kevin; HEWITT, John; PARANJAPE, Ashwin; BEVILACQUA, Michele; "
    "PETRONI, Fabio; LIANG, Percy. **Lost in the middle**: how language models use long "
    "contexts. arXiv:2307.03172, 2023. Publicado em Transactions of the Association for "
    "Computational Linguistics (TACL). Disponível em: https://arxiv.org/abs/2307.03172. "
    "Acesso em: 28 ago. 2026.",

    "MILLER, Evan. **Adding error bars to evals**: a statistical approach to language "
    "model evaluations. arXiv:2411.00640, 2024. *Preprint*, não revisado por pares. "
    "Disponível em: https://arxiv.org/abs/2411.00640. Acesso em: 28 ago. 2026.",

    "NING, Xuying *et al.* **Code as agent "
    "harness**. arXiv:2605.18747, 2026. *Preprint*, não revisado por pares. Disponível em: "
    "https://arxiv.org/abs/2605.18747. Acesso em: 28 ago. 2026.",

    "OPENCODE. **Zen**. 2026. Documentação do produto. Disponível em: "
    "https://opencode.ai/docs/zen/. Acesso em: 28 ago. 2026.",

    "PRODANOV, Cleber Cristiano; FREITAS, Ernani Cesar de. **Metodologia do trabalho "
    "científico**: métodos e técnicas da pesquisa e do trabalho acadêmico. 2. ed. "
    "Novo Hamburgo: Feevale, 2013. Disponível em: https://www.feevale.br/Comum/midias/"
    "0163c988-1f5d-496f-b118-a6e009a7a2f9/E-book%20Metodologia%20do%20Trabalho%20Cientifico.pdf. "
    "Acesso em: 28 ago. 2026.",

    "YANG, John; JIMENEZ, Carlos E.; WETTIG, Alexander; LIERET, Kilian; YAO, Shunyu; "
    "NARASIMHAN, Karthik; PRESS, Ofir. **SWE-agent**: agent-computer interfaces enable "
    "automated software engineering. arXiv:2405.15793, 2024. Trabalho apresentado na "
    "Conference on Neural Information Processing Systems (NeurIPS), 2024. Disponível "
    "em: https://arxiv.org/abs/2405.15793. Acesso em: 28 ago. 2026.",

    "YAO, Shunyu; ZHAO, Jeffrey; YU, Dian; DU, Nan; SHAFRAN, Izhak; NARASIMHAN, Karthik; "
    "CAO, Yuan. **ReAct**: synergizing reasoning and acting in language models. "
    "arXiv:2210.03629, 2022. Trabalho apresentado na International Conference on Learning "
    "Representations (ICLR), 2023. Disponível em: https://arxiv.org/abs/2210.03629. "
    "Acesso em: 28 ago. 2026.",

    "YUUKIFST. **harness-bench**: runner, dados brutos e scripts de análise deste projeto. "
    "2026. Repositório de código. Disponível em: https://github.com/YuukiFST/harness-bench. "
    "Acesso em: 28 ago. 2026.",

    "ZHANG, Yunbei; WANG, Janet; GE, Yingqiang; XU, Weijie; HAMM, Jihun; REDDY, Chandan K. "
    "**Stop comparing LLM agents without disclosing the harness**. arXiv:2605.23950, 2026. "
    "*Preprint*, não revisado por pares. Disponível em: https://arxiv.org/abs/2605.23950. "
    "Acesso em: 28 ago. 2026.",
]


def build_cover(doc):
    for line in (
        "INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA",
        "DE MATO GROSSO - CAMPUS OCTAYDE JORGE DA SILVA",
        "DIRETORIA DE ENSINO",
        "DEPARTAMENTO DE ÁREA DE INFORMÁTICA",
    ):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        _style_run(p.add_run(line), size=12, bold=True)

    for _ in range(4):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    _style_run(p.add_run(AUTOR), size=14, bold=True)

    for _ in range(6):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_after = Pt(0)
    _style_run(p.add_run(TITULO), size=16, bold=True)

    for _ in range(8):
        doc.add_paragraph()

    for line in ("Cuiabá", "2026"):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        _style_run(p.add_run(line), size=12)


def build_folha_de_rosto(doc):
    """The one mandatory pre-textual element the template omits.

    NBR 15287:2025 makes the folha de rosto mandatory (4.2.1.1) and the capa
    optional (4.1.1); the template shows the opposite and says nothing about
    this page, so doc 14 §1 keeps both. Field order is the norm's: author,
    title, submission note naming the type and the entity, orientador, city,
    year.
    """
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    _style_run(p.add_run(AUTOR), size=12, bold=True)

    for _ in range(7):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_after = Pt(0)
    _style_run(p.add_run(TITULO), size=14, bold=True)

    for _ in range(4):
        doc.add_paragraph()

    # The submission note sits in the right half of the text block, single
    # spaced, which is the form every ABNT-following template in the course
    # material uses for it.
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(8.0)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.space_after = Pt(0)
    _style_run(p.add_run(
        "Projeto de Conclusão de Curso apresentado ao Departamento de Área de "
        "Informática do Instituto Federal de Educação, Ciência e Tecnologia de "
        "Mato Grosso, Campus Octayde Jorge da Silva, como requisito parcial "
        "para a conclusão do curso de Sistemas para Internet."), size=12)

    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(8.0)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.space_before = Pt(12)
    pf.space_after = Pt(0)
    _style_run(p.add_run("Orientadora: Profa. Inara Silva"), size=12)

    for _ in range(6):
        doc.add_paragraph()

    for line in ("Cuiabá", "2026"):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        _style_run(p.add_run(line), size=12)


def build_sumario(doc, start_pages):
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(24)
    _style_run(p.add_run("SUMÁRIO"), size=HEADING_PT, bold=True)

    entries = [
        ("1 INTRODUÇÃO", start_pages["1 INTRODUÇÃO"]),
        ("2 REFERENCIAL TEÓRICO", start_pages["2 REFERENCIAL TEÓRICO"]),
        ("3 MATERIAL E MÉTODO", start_pages["3 MATERIAL E MÉTODO"]),
        ("4 ORÇAMENTO", start_pages["4 ORÇAMENTO"]),
        ("5 CRONOGRAMA", start_pages["5 CRONOGRAMA"]),
        ("6 REFERÊNCIAS", start_pages["6 REFERÊNCIAS"]),
    ]
    for text, page in entries:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        pf.space_after = Pt(0)
        pf.first_line_indent = Cm(0)
        pf.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT)
        _style_run(p.add_run(f"{text}\t{page}"))


def build_introducao(doc):
    heading(doc, "1 INTRODUÇÃO")

    label(doc, "Justificativa")
    for paragraph in JUSTIFICATIVA:
        body(doc, paragraph)

    label(doc, "Tema")
    body(doc,
         "*Harnesses* de agentes de codificação: o impacto do projeto do *harness* sobre o "
         "custo e o desempenho de um modelo de linguagem mantido fixo.")

    label(doc, "Problema")
    body(doc,
         "Mantido fixo o modelo de linguagem, quanto do custo em tokens e da taxa de sucesso "
         "de um agente de codificação é determinado pelo projeto do *harness*? E é possível "
         "atribuir essa variação a decisões específicas de projeto, em vez de ao conjunto "
         "indistinto de diferenças entre implementações independentes?")

    label(doc, "Objetivo geral")
    body(doc,
         "Medir, com o modelo de linguagem mantido fixo, o efeito do projeto do *harness* "
         "sobre o custo em tokens e a taxa de sucesso de agentes de codificação, isolando "
         "decisões específicas de projeto por meio da comparação entre um *harness* e um "
         "*fork* direto dele.")

    label(doc, "Objetivos específicos")
    for item in (
        "1) construir um instrumento de medição externo aos *harnesses*, capaz de contabilizar "
        "de forma idêntica, para todos eles, o número de requisições ao modelo, os tokens de "
        "entrada e de saída e a latência por requisição;",
        "2) definir uma suíte de tarefas de programação com objetivos numerados e crédito "
        "parcial, acompanhada de um oráculo automatizado independente dos testes produzidos "
        "pelo próprio agente;",
        "3) implementar um *harness* mínimo de referência, em laço ReAct, como controle "
        "científico do experimento;",
        "4) executar a mesma suíte, com o mesmo modelo, em todos os *harnesses* avaliados, "
        "repetindo cada condição e reportando dispersão;",
        "5) repetir o experimento em um segundo modelo, verificando se a ordenação entre "
        "*harnesses* se mantém ou se inverte;",
        "6) quantificar a divergência entre o custo relatado por cada *harness* e o custo "
        "efetivamente medido no instrumento externo;",
        "7) publicar o *runner*, os dados brutos e os scripts de análise, de modo que o "
        "experimento possa ser reexecutado a custo monetário zero.",
    ):
        bullet(doc, item)

    # The aula 3 handout lists a short metodologia paragraph among the parts of
    # the introdução, ahead of the hipótese. Section 3 carries the full
    # treatment; this one only names what will be done.
    label(doc, "Metodologia")
    body(doc,
         "A pesquisa é aplicada, quali-quantitativa, exploratória e experimental, e o método "
         "é dedutivo, porque parte de hipóteses declaradas e as submete a teste. Os dados são "
         "coletados por um instrumento próprio, um proxy reverso interposto entre cada "
         "*harness* e o modelo, que conta requisições, tokens e latência da mesma forma para "
         "todos os braços. Cada par de braço e tarefa é executado ao menos três vezes sobre "
         "uma suíte fixa do DeepSWE, e a comparação é feita por teste pareado sobre o "
         "Succ/Mtok de cada tarefa. Espera-se obter a diferença de custo e de sucesso "
         "atribuível ao projeto do *harness*, com o modelo mantido fixo. A seção 3 detalha "
         "material, método e tratamento estatístico.")

    label(doc, "Hipótese")
    body(doc,
         "**H1** — Entre *harnesses* distintos executando o mesmo modelo, a diferença de custo "
         "por tarefa concluída é de ordem prática relevante, comparável à diferença obtida ao "
         "se trocar de modelo sob um *harness* fixo. H1 é refutada se os intervalos de "
         "Succ/Mtok dos braços se sobrepuserem ao longo de toda a suíte.")
    body(doc,
         "**H2** — Essa diferença persiste entre um *harness* e um *fork* direto dele, o que "
         "indicaria que ela é produzida por decisões de projeto isoláveis (prompt de sistema, "
         "número e tamanho dos esquemas de ferramenta, política de compactação de contexto), "
         "e não apenas pelo acúmulo de diferenças entre bases de código independentes. H2 é "
         "refutada se pi e oh-my-pi não diferirem significativamente em Succ/Mtok, apesar dos "
         "11,4x de diferença na carga da primeira requisição medidos neste projeto. Esse "
         "desfecho é possível e seria, ele próprio, um achado a reportar. Uma carga 11,4x maior "
         "não implica resultado pior, pois o oh-my-pi pode recuperar o custo concluindo a "
         "tarefa em menos passos.")

    body(doc,
         "Este trabalho segue as normas do curso (IFMT, 2022) e as da ABNT (2023, 2025a, "
         "2025b), e "
         "está organizado em seis seções. Esta introdução apresenta a justificativa, o tema, "
         "o problema, os objetivos, a metodologia e as hipóteses. A seção 2 posiciona o trabalho na "
         "literatura e delimita as pendências que ele se propõe a resolver. A "
         "seção 3 descreve o material e o método: classificação da pesquisa, camadas de "
         "medição, braços, suíte de tarefas, limites, tratamento estatístico, resultados "
         "preliminares do instrumento e limitações. A seção 4 apresenta o orçamento, a seção 5 "
         "o cronograma, e a seção 6 reúne as referências.")


def build_referencial(doc):
    heading(doc, "2 REFERENCIAL TEÓRICO")

    body(doc,
         "Ning *et al.* (2026) definem *agent harness* como a camada de "
         "software que envolve um modelo de linguagem com ferramentas, APIs, *sandboxes*, "
         "memória, validadores, fronteiras de permissão, laços de execução e canais de "
         "realimentação, convertendo um modelo sem estado em um agente capaz de executar "
         "tarefas de longo horizonte. Os mesmos autores separam capacidades "
         "internas do modelo, infraestrutura de *harness* e artefatos de código criados pelo "
         "agente; o recorte aqui é o do meio, com as capacidades internas constantes. Os "
         "braços vão de um laço ReAct mínimo (Yao *et al.*, 2022) a implementações com "
         "planejamento, compactação e subagentes.")

    body(doc,
         "A interface entre modelo e ambiente é objeto de projeto desde Yang *et al.* (2024), "
         "cuja interface agente-computador sob medida rendeu o estado da arte do SWE-bench à "
         "época. O efeito do *harness* já está estabelecido na "
         "literatura. Lin *et al.* (2026) medem 24,7 pontos percentuais de dispersão entre "
         "*harnesses* humanos sobre um modelo congelado, contra os 19,7 pontos entre as "
         "quatro bases alternativas do mesmo *harness* semente (§ 4.3), dispersões da mesma "
         "ordem. Zhang *et al.* (2026) enunciam a *Binding Constraint Thesis*: em longo "
         "horizonte, o *harness* determina o desempenho mais que o modelo que encapsula. "
         "Somam-se duas fontes de prática: o HarnessRank (2026) e o estudo da Databricks "
         "relatado por Earendil (2026), com custo por tarefa variando mais de 2x sem "
         "mudança de qualidade.")

    body(doc,
         "A primeira pendência é de atribuição. Toda comparação publicada contrasta "
         "*harnesses* de equipes diferentes sobre fundações diferentes, e a dispersão medida "
         "agrega prompt, ferramentas, gestão de contexto e desenho do laço sem separá-los. "
         "Ning *et al.* (2026) nomeiam a lacuna em §5.2.1, onde as métricas de sucesso final "
         "confundem modelo e *harness*, e pedem em §5.2.7 métricas que isolem componentes. O "
         "par pi / oh-my-pi responde a §5.2.7: um *fork* direto mantém a linhagem fixa e faz "
         "variar apenas as modificações.")

    body(doc,
         "A segunda pendência é de instrumentação. O que um *harness* relata sobre o próprio "
         "custo diverge do que ele gasta, e cada um omite do relatório um conjunto diferente "
         "de chamadas reais ao modelo. Kapoor *et al.* (2024) mostram que a avaliação de "
         "agentes ignora o custo e por isso erra sobre a origem dos ganhos, e Kapoor *et al.* "
         "(2025) registram que as avaliações raramente relatam custo e que comparações entre "
         "*harnesses* são raras. Por isso a medição ocorre em proxy externo, "
         "e o objetivo (6) quantifica essa divergência.")

    body(doc,
         "A métrica primária é o Succ/Mtok (sucesso por milhão de tokens), de Lin *et al.* "
         "(2026). Sobre ela pesa uma ressalva permanente. O efeito é específico do modelo e "
         "pode inverter de sinal. No *Holistic Agent Leaderboard*, os modelos da Anthropic "
         "vão melhor com o BrowserUse e os da OpenAI com o SeeAct sobre o mesmo *benchmark* "
         "(Kapoor *et al.*, 2025). Por isso o desenho carrega "
         "dois níveis, e as conclusões são enunciadas por nível.")


def build_material(doc):
    heading(doc, "3 MATERIAL E MÉTODO")

    body(doc,
         "Quanto à finalidade, esta é uma pesquisa **aplicada**: seu produto é uma decisão de "
         "engenharia que um desenvolvedor pode tomar hoje. Quanto à abordagem, é "
         "**quali-quantitativa**: as medidas de custo e de sucesso são quantitativas, e a "
         "atribuição de cada diferença a uma decisão de projeto do *harness* é qualitativa. "
         "Quanto aos objetivos, é **exploratória**, porque a comparação com linhagem de "
         "*harness* fixa não tem precedente publicado. Quanto aos procedimentos, é "
         "**experimental**: há variável independente manipulada (o *harness*), variáveis "
         "controladas (modelo, tarefa e limites) e um grupo de controle. Quanto ao método, é "
         "**dedutivo**, porque parte de hipóteses declaradas antes da coleta e as submete a "
         "teste (Gil, 2022; Prodanov; Freitas, 2013).")

    body(doc,
         "A medição ocorre em duas camadas, cada uma relatada em separado. "
         "A Camada 1 mede a forma da requisição contra um endpoint simulado que "
         "não encaminha nada ao modelo: não consome cota, é determinística e nomeia o "
         "mecanismo. A Camada 2 mede o desfecho das tarefas contra o modelo real: consome "
         "cota, é estocástica e mostra o efeito. Um *harness* que envia 11,4x os bytes não é, "
         "por isso, 11,4x pior.")

    body(doc,
         "O conjunto de braços é provisório até o fechamento das verificações de "
         "confiabilidade. São o *harness* zero, o conjunto de "
         "implementações de terceiros e o par de destaque pi / oh-my-pi. O executor não traz "
         "adaptador para pi nem para oh-my-pi (Datacurve, 2026); os dois, e o *harness* "
         "zero, são escritos neste projeto. O *harness* zero é o "
         "controle científico e o único braço que este projeto escreve: um laço observar/agir "
         "com três ferramentas (leitura de arquivo, escrita de arquivo e execução de "
         "comandos). Não tem planejamento, compactação de contexto, repetição automática de "
         "requisições nem qualquer chamada auxiliar ao modelo, e é mantido abaixo de 400 "
         "linhas de Python por um portão de integração contínua. Ele mede quanto qualquer "
         "*harness* acrescenta sobre o laço mais cru capaz de concluir a tarefa.")

    body(doc,
         "A suíte é composta por 8 tarefas Python do DeepSWE (Huang *et al.*, 2026), congeladas "
         "na adoção e fixadas por *commit* e por *hash* SHA-256 de cada tarefa. São tarefas de "
         "implementação de longo horizonte sobre repositórios reais: o *benchmark* completo "
         "tem 113 tarefas sobre 91 repositórios, com soluções de referência que tocam cerca "
         "de 5,5x mais código que as do SWE-Bench Pro, outra ordem de grandeza ante o "
         "SWE-bench (Jimenez *et al.*, 2023). A pontuação adotada aqui é o crédito parcial, a "
         "fração de testes aprovados do verificador de cada tarefa. É uma adaptação, porque "
         "o DeepSWE grada de forma binária e declara a ausência de crédito parcial como "
         "limitação (Huang *et al.*, 2026, §8); sem ela, um escore binário tenderia a ler zero "
         "para todos os braços neste nível de modelo [A VERIFICAR nas tarefas-piloto].")

    body(doc,
         "São dois níveis de modelo, um primário e um de robustez, ambos gratuitos e no "
         "mesmo gateway (Opencode, 2026) e relatados em separado. O "
         "segundo existe porque o efeito do *harness* é específico do modelo. Se a ordenação "
         "entre braços se inverter entre os níveis, a inversão é o resultado.")

    body(doc,
         "O instrumento de medição é um proxy reverso interposto entre cada braço e o gateway, "
         "que força a emissão do relatório de uso em cada requisição. Os tokens são contados "
         "no proxy, sobre os bytes efetivamente transmitidos, com um único tokenizador "
         "divulgado para todos os braços e níveis. A contagem vem do proxy, e não do "
         "relatório do *harness* nem do gateway, que inclui conteúdo injetado que nenhum "
         "braço enviou. "
         "Esse deslocamento aditivo por requisição não se cancela em uma razão e cobraria de "
         "cada braço um excedente proporcional ao número de passos, que é um dos "
         "comportamentos sob teste. As contagens do gateway permanecem "
         "registradas para verificação cruzada e para o cálculo de custo, e a divergência "
         "entre elas e as do proxy é reportada por braço.")

    body(doc,
         "Um único limite é imposto, idêntico para todos os braços. É um relógio de parede, "
         "cujo valor será três vezes a mediana que o *harness* zero gastar "
         "[A MEDIR nas tarefas-piloto]. O número de passos não é limitado, porque um teto de passos é ele "
         "próprio uma decisão de projeto de *harness* e apagaria a diferença sob teste. O "
         "comprimento máximo de saída é forçado idêntico pelo proxy. Os parâmetros de "
         "amostragem são registrados e relatados, mas não normalizados, já que o gateway os "
         "aceita sem os honrar, e Miller (2024) desaconselha mexer na temperatura para "
         "reduzir variância. O isolamento de ambiente é verificado por um portão que falha "
         "fechado.")

    body(doc,
         "Cada célula do experimento, a tripla (braço, tarefa, nível), recebe n ≥ 3 "
         "execuções completas, contadas após os descartes, na função redutora de variância "
         "que Miller (2024) atribui à reamostragem. Os resultados saem como "
         "mediana com dispersão, já que requisições byte-idênticas variam "
         "materialmente em tokens de saída neste nível gratuito. Quando a cota não comportar a "
         "matriz, reduz-se a cobertura antes das repetições, já que a variância é a principal "
         "ameaça ao desenho.")

    body(doc,
         "A comparação é pareada por tarefa e usa o teste de Wilcoxon dos postos sinalizados "
         "sobre o Succ/Mtok por tarefa, bilateral, com α = 0,05. O teste é não paramétrico "
         "porque oito pares não sustentam suposição distribucional, e pareado porque a "
         "dificuldade da tarefa é o maior fator de perturbação do desenho, que é o que Miller "
         "(2024) recomenda ao preferir a diferença pareada por questão à média agregada. "
         "Com n = 3 e 8 "
         "tarefas, a diferença mínima detectável é de cerca de 0,81σ. As predições são "
         "pré-registradas por nível de modelo, e um resultado nulo para H2 é um achado "
         "reportável.")

    body(doc,
         "Cada execução recebe exatamente uma classe. Aquela cujo agente não cumpriu a tarefa "
         "é um resultado, entra na estatística e recebe escore zero; nesse grupo, o estouro do "
         "relógio de parede conta como resultado, já que repetir converteria "
         "uma indisponibilidade do serviço em diferença aparente entre *harnesses*. "
         "Aquela cuja medição é inconfiável é descartada e registrada como tal, sem reparo "
         "nem repetição. A classificação vem do registro do proxy, e não do código de saída, "
         "que não discrimina desfecho.")

    label(doc, "Resultados preliminares do instrumento (Camada 1)")

    body(doc,
         "O instrumento da Camada 1 está construído e executado, com os dados brutos no "
         "repositório do projeto, cuja abertura é o objetivo (7) (YuukiFST, 2026). Na "
         "primeira requisição da tarefa "
         "*probe*, em ambiente isolado, medida em 28 de agosto de 2026, os braços diferem por "
         "uma ordem de grandeza antes que o modelo gere qualquer token (Tabela 1): com a "
         "linhagem mantida fixa, o oh-my-pi envia 11,4x os bytes totais do pi, 13,5x os bytes "
         "de esquemas de ferramenta, 10,2x os de prompt de sistema, 2,75x o número de esquemas "
         "e 13,6x os tokens. Uma medição anterior, com código independente e prompt "
         "diferente, obtivera 10,8x. A mesma execução produziu outros dois achados. Os três "
         "braços reenviam o histórico completo a cada passo, com incremento constante de 555, "
         "625 e 698 bytes (pi, oh-my-pi e OpenCode), sem compactar nem truncar em cinco "
         "passos. Além do custo, Liu *et al.* (2023) medem queda de desempenho quando a "
         "informação relevante fica no meio de um contexto longo. O "
         "OpenCode gasta por sessão uma chamada auxiliar de 2.526 bytes que seria cobrada em "
         "um nível pago e não aparece no seu próprio relatório, divergência que o "
         "objetivo (6) quantifica. O delta de estado ambiente do pi nesta "
         "máquina é de 0 bytes, propriedade da máquina tanto quanto do *harness*, a ser "
         "remedida onde o experimento correrá.")

    caption(doc, "Tabela 1 – Primeira requisição por braço, perfil isolado, tarefa probe "
                 "(28 ago. 2026)")
    table(doc, LAYER1_TABLE, size=9,
          widths=[Cm(3.2), Cm(2.7), Cm(2.6), Cm(2.5), Cm(2.5), Cm(2.5)])
    caption(doc, "Fonte: elaborado pelo autor (2026).", above=False)

    label(doc, "Limitações e ameaças à validade")

    body(doc,
         "Cinco limitações são declaradas de partida. O efeito de "
         "um *harness* é específico do modelo e pode inverter de sinal, o que restringe "
         "qualquer conclusão ao nível de modelo em que foi obtida; o objetivo (5) existe para "
         "testar isso. A transferência para modelos pequenos fica deliberadamente em aberto e "
         "é registrada como trabalho futuro, porque o único modelo pequeno viável havia sido "
         "treinado dentro de um dos braços, "
         "o que invalidaria a medição de destaque em vez de apenas limitá-la. Os valores "
         "absolutos não são comparáveis ao placar público do DeepSWE, porque toda linha de "
         "base publicada usa um *harness* de ferramenta única; a comparação aqui é entre os "
         "próprios braços. O custo em dinheiro é um contrafactual de ordem de grandeza sobre "
         "tarifas pagas publicadas, rotulado como tal onde apareça. Por fim, os resultados "
         "preliminares da Camada 1 valem para uma tarefa, uma máquina e três braços, já que o "
         "controle ainda não figura na tabela, e a Camada 2 ainda não produziu resultado "
         "algum.")


def build_orcamento(doc):
    heading(doc, "4 ORÇAMENTO")

    caption(doc, "Tabela 2 – Orçamento do projeto")
    table(doc, ORCAMENTO_TABLE, size=11, widths=[Cm(11.5), Cm(4.5)])
    caption(doc, "Fonte: elaborado pelo autor (2026).", above=False)

    body(doc,
         "O total em dinheiro é zero, e o limite que restringe o experimento é a cota: cerca "
         "de 10 requisições a cada 6 minutos, medidas neste projeto, contra o número de "
         "requisições que uma tarefa do DeepSWE consome [A MEDIR nas tarefas-piloto]. Por isso "
         "a matriz é executada em lotes distribuídos ao longo de dias, e o custo monetário "
         "aparece apenas como contrafactual de ordem de grandeza sobre as tarifas pagas "
         "publicadas. O executor roda em docker ou modal, e este projeto usa docker "
         "(Datacurve, 2026); a GPU da estação é irrelevante para todo resultado reportado.")


def build_cronograma(doc):
    heading(doc, "5 CRONOGRAMA")

    body(doc,
         "A cadência é de um lote da matriz por dia, porque a cota gratuita é o limite "
         "vinculante, e por isso o calendário se estende por semanas. A "
         "folga está concentrada na execução da matriz e nos portões de confiabilidade dos "
         "braços, onde está o risco. Os meses são numerados de forma "
         "relativa porque a data de entrega ainda não está confirmada "
         "[A DEFINIR com o orientador].")

    rows = [["FASES", "MÊS 1", "MÊS 2", "MÊS 3", "MÊS 4", "MÊS 5"]]
    for fase, marks in CRONOGRAMA_FASES:
        rows.append([fase] + ["X" if ch == "X" else "" for ch in marks])

    caption(doc, "Tabela 3 – Cronograma de execução")
    table(doc, rows, size=9,
          widths=[Cm(7.6)] + [Cm(1.68)] * 5)
    caption(doc, "Fonte: elaborado pelo autor (2026).", above=False)


def build_referencias(doc):
    heading(doc, "6 REFERÊNCIAS")
    for entry in REFERENCIAS:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        pf.space_before = Pt(0)
        # NBR 6023:2025 separates entries by one blank single-spaced line.
        pf.space_after = Pt(12)
        pf.first_line_indent = Cm(0)
        _add_marked_runs(p, entry)
        _account(re.sub(r"\*\*|\*", "", entry), factor=0.67, extra=0.67)


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

SECTION_ORDER = [
    "1 INTRODUÇÃO",
    "2 REFERENCIAL TEÓRICO",
    "3 MATERIAL E MÉTODO",
    "4 ORÇAMENTO",
    "5 CRONOGRAMA",
    "6 REFERÊNCIAS",
]


def estimate_pages() -> dict[str, float]:
    return {
        name: round(_SECTION_LINES.get(name, 0.0) / LINES_PER_PAGE, 2)
        for name in SECTION_ORDER
    }


def start_pages(pages: dict[str, float]) -> dict[str, int]:
    starts, cursor = {}, 0.0
    for name in SECTION_ORDER:
        starts[name] = int(math.floor(cursor)) + 1
        cursor += pages[name]
    return starts


def collect_markers(doc) -> list[str]:
    """Anything left in the body that a reader outside this repo cannot resolve.

    Square-bracketed placeholders, plus bare `(#NN)` ticket references, which
    are repo-internal and must not survive into a submitted document.
    """
    found, seen = [], set()
    pattern = re.compile(r"\[[^\[\]]{2,60}\]|\(#\d+\)")
    texts = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                texts.extend(p.text for p in cell.paragraphs)
    for text in texts:
        for m in pattern.findall(text):
            if m not in seen:
                seen.add(m)
                found.append(m)
    return found


def main() -> None:
    global _current_section

    # Pass 1: render the body into a throwaway document to learn its length,
    # so the sumário can carry real page numbers rather than a promise.
    _SECTION_LINES.clear()
    probe = Document()
    set_default_style(probe)
    setup_section(probe.sections[0])
    build_introducao(probe)
    build_referencial(probe)
    build_material(probe)
    build_orcamento(probe)
    build_cronograma(probe)
    build_referencias(probe)
    pages = estimate_pages()
    starts = start_pages(pages)

    # Pass 2: the real document.
    _SECTION_LINES.clear()
    _current_section = "capa"
    doc = Document()
    set_default_style(doc)
    setup_section(doc.sections[0])

    build_cover(doc)
    doc.add_page_break()
    build_folha_de_rosto(doc)
    doc.add_page_break()
    build_sumario(doc, starts)

    setup_section(doc.add_section(WD_SECTION.NEW_PAGE), numbered_from=1)

    build_introducao(doc)
    build_referencial(doc)
    build_material(doc)
    build_orcamento(doc)
    build_cronograma(doc)
    build_referencias(doc)

    attach_footnotes(doc)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)

    pages = estimate_pages()
    total = sum(pages.values())

    print(f"Gerado: {OUT}")
    print()

    justificativa_lines = sum(
        math.ceil(len(re.sub(r"\*\*|\*|\[\[FN\]\]", "", p)) / CHARS_PER_LINE)
        for p in JUSTIFICATIVA
    )
    status = "ok" if justificativa_lines <= JUSTIFICATIVA_MAX_LINES else "ACIMA DO LIMITE"
    print(f"Justificativa: {len(JUSTIFICATIVA)} parágrafos, "
          f"{justificativa_lines} linhas (máx. {JUSTIFICATIVA_MAX_LINES}) — {status}")
    print()
    print("Páginas estimadas por seção (capa e sumário fora da contagem):")
    for name in SECTION_ORDER:
        print(f"  {name:<24} {pages[name]:>5.2f}  (inicia na página {starts[name]})")
    print(f"  {'TOTAL':<24} {total:>5.2f}   (teto {PAGES_MAX:.0f},0)")
    if total > PAGES_MAX:
        print(f"  AVISO: acima de {PAGES_MAX:.0f} páginas — aplicar a escada de "
              "redução do doc 14 §5.")
    print()

    markers = collect_markers(doc)
    print(f"Marcadores restantes ({len(markers)}):")
    for m in markers:
        print(f"  {m}")


if __name__ == "__main__":
    main()
