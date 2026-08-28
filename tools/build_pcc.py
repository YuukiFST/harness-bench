"""Build dist/projeto-pcc.docx — the IFMT Projeto de Conclusão de Curso.

Structure, page budget and reduction ladder come from docs/spec/14-document-outline.md,
which is the binding specification. The spine (tema, problema, H1/H2, objetivos) is
quoted verbatim from the resolution comment of issue #9 and is never rewritten here.

Every quantitative figure in this file traces to a run or to a closed ticket:
Layer 1 numbers come from docs/spec/41-layer1-request-shape.md (measured 2026-08-28),
protocol numbers from docs/spec/11-experimental-protocol.md, control scope from
docs/spec/12-harness-zero-scope.md. Numbers that do not exist yet are emitted as
``[A MEDIR — #NN]`` markers rather than guessed, and the build prints what is left.

Usage:
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
CHARS_PER_LINE = 92          # 12 pt Times New Roman justified over 16 cm
LINES_PER_PAGE = 39          # 24.7 cm of text height at 1.5 line spacing


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


def table(doc, rows, *, size=10, header=True, widths=None):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = True
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
    _account("", lines=0.85 * len(rows))
    return t


# --------------------------------------------------------------------------
# footnotes — python-docx has no API for these, so the part is built by hand
# --------------------------------------------------------------------------

FOOTNOTE_ID = 2
FOOTNOTE_TEXT = (
    "Os exemplos de referência do template departamental precedem as edições vigentes "
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
      <w:pPr><w:jc w:val="both"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>
        <w:vertAlign w:val="superscript"/><w:sz w:val="20"/></w:rPr><w:footnoteRef/></w:r>
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
        for tag, attrs, text in (
            ("w:fldChar", {"w:fldCharType": "begin"}, None),
            ("w:instrText", {"xml:space": "preserve"}, " PAGE "),
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

TITULO = (
    "HARNESSES DE AGENTES DE CODIFICAÇÃO: O IMPACTO DO PROJETO DO HARNESS "
    "SOBRE O CUSTO E O DESEMPENHO DE UM MODELO DE LINGUAGEM MANTIDO FIXO"
)

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
    "AKITA, Fabio. **Novo LLM Benchmark**: refiz todos os testes! 30 jul. 2026. "
    "Disponível em: https://akitaonrails.com/2026/07/30/novo-llm-benchmark-refiz-todos-os-testes/. "
    "Acesso em: 28 ago. 2026.",

    "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6023**: informação e documentação — "
    "referências — elaboração. 3. ed. Rio de Janeiro: ABNT, 2025.",

    "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 10520**: informação e documentação — "
    "citações em documentos — apresentação. Rio de Janeiro: ABNT, 2023.",

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

    "LIN, Jiahang; LIU, Shichun; PAN, Chengjun; LIN, Lizhi; DOU, Shihan; XI, Zhiheng; "
    "HUANG, Xuanjing; YAN, Hang; HAN, Zhenhua; GUI, Tao; JIANG, Yu-Gang. **Agentic harness "
    "engineering**: observability-driven automatic evolution of coding-agent harnesses. "
    "arXiv:2604.25850, 2026. *Preprint*, não revisado por pares. Disponível em: "
    "https://arxiv.org/abs/2604.25850. Acesso em: 28 ago. 2026.",

    "NING, Xuying; TIEU, Katherine; FU, Dongqi; WEI, Tianxin; LI, Zihao et al. **Code as agent "
    "harness**. arXiv:2605.18747, 2026. *Preprint*, não revisado por pares. Disponível em: "
    "https://arxiv.org/abs/2605.18747. Acesso em: 28 ago. 2026.",

    "OPENCODE. **Zen**. 2026. Documentação do produto. Disponível em: "
    "https://opencode.ai/docs/zen/. Acesso em: 28 ago. 2026.",

    "PRODANOV, Cleber Cristiano; FREITAS, Ernani Cesar de. **Metodologia do trabalho "
    "científico**: métodos e técnicas da pesquisa e do trabalho acadêmico. 2. ed. "
    "Novo Hamburgo: Feevale, 2013. Disponível em: https://www.feevale.br/Comum/midias/"
    "0163c988-1f5d-496f-b118-a6e009a7a2f9/E-book%20Metodologia%20do%20Trabalho%20Cientifico.pdf. "
    "Acesso em: 28 ago. 2026.",

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
    _style_run(p.add_run("[NOME COMPLETO]"), size=14, bold=True)

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
    body(doc,
         "A escolha do modelo de linguagem domina a discussão sobre agentes de codificação, "
         "mas não é o único fator sob controle de quem os usa. Na Tabela 1 de Lin et al. "
         "(2026)[[FN]], três *harnesses* construídos por equipes humanas sobre o mesmo modelo, "
         "congelado e no mesmo *benchmark*, obtêm 47,2%, 62,9% e 71,9% de pass@1 — uma "
         "dispersão de 24,7 pontos percentuais atribuível exclusivamente ao *harness*, faixa "
         "comparável à que se obtém trocando o próprio modelo sob um *harness* fixo. O estudo "
         "da Databricks relatado por Earendil (2026) registra variação superior a 2x no custo "
         "por tarefa entre *harnesses*, com qualidade igual ou melhor.")
    body(doc,
         "Este projeto já mediu o mesmo efeito com a linhagem do *harness* mantida fixa: na "
         "primeira requisição de uma mesma tarefa, o oh-my-pi — *fork* direto do pi — envia "
         "11,4x os bytes do seu próprio ascendente, 64.945 contra 5.676, antes que o modelo "
         "gere um único token. A pergunta prática que daí decorre é direta: você está mesmo "
         "extraindo o máximo do modelo que está pagando para usar?")

    label(doc, "Tema")
    body(doc,
         "*Harnesses* de agentes de codificação: o impacto do projeto do *harness* sobre o "
         "custo e o desempenho de um modelo de linguagem mantido fixo.")

    label(doc, "Problema")
    body(doc,
         "Mantido fixo o modelo de linguagem, quanto do custo em tokens e da taxa de sucesso "
         "de um agente de codificação é determinado pelo projeto do *harness* — e é possível "
         "atribuir essa variação a decisões específicas de projeto, em vez de ao conjunto "
         "indistinto de diferenças entre implementações independentes?")

    label(doc, "Hipótese")
    body(doc,
         "**H1** — Entre *harnesses* distintos executando o mesmo modelo, a diferença de custo "
         "por tarefa concluída é de ordem prática relevante, comparável à diferença obtida ao "
         "se trocar de modelo sob um *harness* fixo. H1 é refutada se os intervalos de "
         "Succ/Mtok dos braços se sobrepuserem ao longo de toda a suíte.")
    body(doc,
         "**H2** — Essa diferença persiste entre um *harness* e um *fork* direto dele, o que "
         "indicaria que ela é produzida por decisões de projeto isoláveis — prompt de sistema, "
         "número e tamanho dos esquemas de ferramenta, política de compactação de contexto — e "
         "não apenas pelo acúmulo de diferenças entre bases de código independentes. H2 é "
         "refutada se pi e oh-my-pi não diferirem significativamente em Succ/Mtok, apesar dos "
         "11,4x de diferença na carga da primeira requisição medidos neste projeto. Esse "
         "desfecho é possível e seria, ele próprio, um achado a reportar: 11,4x de carga não "
         "implicam resultado pior, pois o oh-my-pi pode recuperar o custo concluindo a tarefa "
         "em menos passos.")

    label(doc, "Objetivo geral")
    body(doc,
         "Medir, com o modelo de linguagem mantido fixo, o efeito do projeto do *harness* "
         "sobre o custo em tokens e a taxa de sucesso de agentes de codificação, isolando "
         "decisões específicas de projeto por meio da comparação entre um *harness* e um "
         "*fork* direto dele.")

    label(doc, "Objetivos específicos")
    for item in (
        "a) Construir um instrumento de medição externo aos *harnesses*, capaz de contabilizar "
        "de forma idêntica, para todos eles, o número de requisições ao modelo, os tokens de "
        "entrada e de saída e a latência por requisição.",
        "b) Definir uma suíte de tarefas de programação com objetivos numerados e crédito "
        "parcial, acompanhada de um oráculo automatizado independente dos testes produzidos "
        "pelo próprio agente.",
        "c) Implementar um *harness* mínimo de referência, em laço ReAct, como controle "
        "científico do experimento.",
        "d) Executar a mesma suíte, com o mesmo modelo, em todos os *harnesses* avaliados, "
        "repetindo cada condição e reportando dispersão.",
        "e) Repetir o experimento em um segundo modelo, verificando se a ordenação entre "
        "*harnesses* se mantém ou se inverte.",
        "f) Quantificar a divergência entre o custo relatado por cada *harness* e o custo "
        "efetivamente medido no instrumento externo.",
        "g) Publicar o *runner*, os dados brutos e os scripts de análise, de modo que o "
        "experimento possa ser reexecutado a custo monetário zero.",
    ):
        bullet(doc, item)

    body(doc,
         "Este trabalho está organizado em seis seções. Esta introdução apresenta a "
         "justificativa, o tema, o problema, as hipóteses e os objetivos. A seção 2 posiciona "
         "o trabalho na literatura e delimita as pendências que ele se propõe a resolver. A "
         "seção 3 descreve o material e o método — classificação da pesquisa, camadas de "
         "medição, braços, suíte de tarefas, limites, tratamento estatístico, resultados "
         "preliminares do instrumento e limitações. A seção 4 apresenta o orçamento, a seção 5 "
         "o cronograma, e a seção 6 reúne as referências.")


def build_referencial(doc):
    heading(doc, "2 REFERENCIAL TEÓRICO")

    body(doc,
         "Adota-se a definição de Ning et al. (2026): um *agent harness* é a camada de "
         "software que envolve um modelo de linguagem com ferramentas, APIs, *sandboxes*, "
         "memória, validadores, fronteiras de permissão, laços de execução e canais de "
         "realimentação, convertendo um modelo sem estado em um agente capaz de executar "
         "tarefas de longo horizonte (tradução nossa). Os mesmos autores separam as "
         "capacidades internas do modelo, a infraestrutura de *harness* provida pelo sistema e "
         "os artefatos de código criados pelo agente; o recorte deste trabalho é o do meio, "
         "com as capacidades internas mantidas constantes. Os braços vão de um laço ReAct "
         "mínimo (Yao et al., 2022) a implementações com planejamento, compactação de contexto "
         "e subagentes.")

    body(doc,
         "A afirmação genérica de que o *harness* importa já está estabelecida, e este "
         "trabalho se posiciona em relação a ela em vez de redescobri-la. Quatro fontes a "
         "sustentam, duas delas de prática profissional. Lin et al. (2026) medem 24,7 pontos "
         "percentuais de dispersão entre *harnesses* humanos sobre um modelo congelado, contra "
         "linhas de base de 36,5% a 56,2% obtidas trocando o modelo sob *harness* fixo — "
         "dispersões da mesma ordem de grandeza. Zhang et al. (2026) enunciam a *Binding "
         "Constraint Thesis*: em tarefas de longo horizonte, o *harness* determina o "
         "desempenho mais que o modelo que ele encapsula. Somam-se o HarnessRank (2026), "
         "placar com método de medição documentado, e o estudo da Databricks relatado por "
         "Earendil (2026), com variação de custo por tarefa superior a 2x a qualidade igual ou "
         "melhor.")

    body(doc,
         "A primeira pendência é de atribuição: toda comparação publicada contrasta "
         "*harnesses* de equipes diferentes sobre fundações diferentes, e a dispersão medida "
         "agrega, sem separá-los, o projeto do prompt, o das ferramentas, a gestão de contexto "
         "e o desenho do laço. Ning et al. (2026) nomeiam a lacuna em §5.2.3 e pedem, em "
         "§5.2.7, métricas que isolem componentes do *harness*. O par pi / oh-my-pi responde a "
         "§5.2.7: o oh-my-pi é um *fork* direto do pi, o que mantém a linhagem fixa e faz "
         "variar apenas as modificações.")

    body(doc,
         "A segunda pendência é de instrumentação: o que um *harness* relata sobre o próprio "
         "custo diverge do que ele gasta. Cada implementação omite do relatório um conjunto "
         "diferente de chamadas reais ao modelo, e um *benchmark* de produção subestimou custo "
         "em 40 a 90 vezes durante meses por essa classe de erro (Akita, 2026). Daí a medição "
         "ficar em um proxy externo; quantificar a divergência é o objetivo específico (f).")

    body(doc,
         "A métrica primária é Succ/Mtok — sucesso por milhão de tokens —, adotada de Lin et "
         "al. (2026). Sobre ela pesa uma ressalva permanente: o efeito de um *harness* é "
         "específico do modelo e pode inverter de sinal — uma única mudança de *scaffolding* "
         "moveu escores em +67, −39, −22 e +1 pontos em quatro modelos (Akita, 2026). Por isso "
         "o desenho carrega dois níveis de modelo e enuncia as conclusões por nível, nunca de "
         "forma global.")


def build_material(doc):
    heading(doc, "3 MATERIAL E MÉTODO")

    body(doc,
         "Quanto à finalidade, esta é uma pesquisa **aplicada**: seu produto é uma decisão de "
         "engenharia que um desenvolvedor pode tomar hoje. Quanto à abordagem, é "
         "**quali-quantitativa**: as medidas de custo e de sucesso são quantitativas, e a "
         "atribuição de cada diferença a uma decisão de projeto do *harness* é qualitativa. "
         "Quanto aos objetivos, é **exploratória**, porque a comparação com linhagem de "
         "*harness* fixa não tem precedente publicado. Quanto aos procedimentos, é "
         "**experimental**: há variável independente manipulada — o *harness* —, variáveis "
         "controladas — modelo, tarefa e limites — e um grupo de controle (Gil, 2022; "
         "Prodanov; Freitas, 2013).")

    body(doc,
         "A medição ocorre em duas camadas, reportadas separadamente e nunca combinadas em um "
         "único número. A Camada 1 mede a forma da requisição contra um endpoint simulado que "
         "jamais encaminha nada ao modelo: não consome cota, é determinística e nomeia o "
         "mecanismo. A Camada 2 mede o desfecho das tarefas contra o modelo real: consome "
         "cota, é estocástica e mostra o efeito. Um *harness* que envia 11,4x os bytes não é, "
         "por isso, 11,4x pior — fundir as duas camadas afirmaria essa implicação.")

    body(doc,
         "O conjunto de braços é provisório até o fechamento das verificações de "
         "confiabilidade (#23) e é citado aqui como tal: o *harness* zero, o conjunto de "
         "implementações de terceiros e o par de destaque pi / oh-my-pi. O *harness* zero é o "
         "controle científico e o único braço que este projeto escreve — um laço observar/agir "
         "com três ferramentas (leitura de arquivo, escrita de arquivo e execução de "
         "comandos), sem planejamento, compactação de contexto, repetição automática de "
         "requisições ou qualquer chamada auxiliar ao modelo, mantido abaixo de 400 linhas de "
         "Python por um portão de integração contínua. Ele responde quanto qualquer *harness* "
         "acrescenta sobre o laço mais cru capaz de concluir a tarefa.")

    body(doc,
         "A suíte é composta por 8 tarefas Python do DeepSWE (Huang et al., 2026), congeladas "
         "na adoção e fixadas por *commit* e por *hash* SHA-256 de cada tarefa. São tarefas de "
         "implementação de longo horizonte sobre repositórios reais: o *benchmark* completo "
         "tem 113 tarefas sobre 91 repositórios, com soluções de referência de 526 a 847 "
         "linhas em 3 a 17 arquivos — outra ordem de grandeza ante o SWE-bench (Jimenez et "
         "al., 2023). A pontuação é o crédito parcial, a fração de testes aprovados, e não o "
         "resultado binário: modelos da classe *flash* marcaram de 0% a 36% na primeira versão "
         "do *benchmark*, e um escore binário leria zero para todos os braços, sem discriminar "
         "nenhum.")

    body(doc,
         "São dois níveis de modelo, ambos gratuitos e no mesmo gateway, reportados "
         "separadamente e jamais promediados: um primário e um de robustez. O segundo existe "
         "porque o efeito do *harness* é específico do modelo; se a ordenação entre braços se "
         "inverter entre os níveis, a inversão é o resultado, e não ruído a suavizar.")

    body(doc,
         "O instrumento de medição é um proxy reverso interposto entre cada braço e o gateway, "
         "que força a emissão do relatório de uso em cada requisição. Os tokens são contados "
         "no proxy, sobre os bytes efetivamente transmitidos, com um único tokenizador "
         "divulgado para todos os braços e níveis — nunca a partir do relatório do próprio "
         "*harness* nem da contagem do gateway, que inclui conteúdo injetado que nenhum braço "
         "enviou: um deslocamento aditivo por requisição não se cancela em uma razão e "
         "cobraria de cada braço um excedente proporcional ao número de passos, que é "
         "justamente um comportamento sob teste. As contagens do gateway permanecem "
         "registradas para verificação cruzada e para o cálculo de custo, e a divergência "
         "entre elas e as do proxy é reportada por braço.")

    body(doc,
         "Um único limite é imposto, idêntico para todos os braços: um relógio de parede, cujo "
         "valor será três vezes a mediana que o *harness* zero gastar nas tarefas-piloto "
         "[A MEDIR — #39]. O número de passos não é limitado, porque um teto de passos é ele "
         "próprio uma decisão de projeto de *harness* e apagaria a diferença sob teste. O "
         "comprimento máximo de saída é forçado idêntico pelo proxy. Os parâmetros de "
         "amostragem são registrados e reportados, mas não normalizados: o gateway os aceita e "
         "não os honra, de modo que afirmar igualdade criaria a aparência de um controle "
         "inexistente. O isolamento de ambiente é um portão que falha fechado, e não um item "
         "de conferência.")

    body(doc,
         "Cada célula do experimento — a tripla (braço, tarefa, nível) — recebe n ≥ 3 "
         "execuções completas, contadas após os descartes. Os resultados saem como mediana com "
         "dispersão, nunca como estimativa pontual, porque requisições byte-idênticas variam "
         "materialmente em tokens de saída neste nível gratuito. Quando a cota não comportar a "
         "matriz, reduz-se a cobertura e nunca as repetições: a ameaça é a variância.")

    body(doc,
         "A comparação é pareada por tarefa e usa o teste de Wilcoxon dos postos sinalizados "
         "sobre o Succ/Mtok por tarefa, bilateral, com α = 0,05 — não paramétrico porque oito "
         "pares não sustentam suposição distribucional, e pareado porque a dificuldade da "
         "tarefa é o maior fator de perturbação do desenho. Com n = 3 e 8 tarefas, a diferença "
         "mínima detectável é de cerca de 0,81σ. As predições são pré-registradas por nível de "
         "modelo, e um resultado nulo para H2 é achado reportável, não experimento fracassado.")

    body(doc,
         "Cada execução recebe exatamente uma classe. Aquela cujo agente não cumpriu a tarefa "
         "é um resultado, entra na estatística e recebe escore zero; nesse grupo, o estouro do "
         "relógio de parede é resultado e nunca motivo de nova tentativa, porque repetir "
         "converte uma indisponibilidade do serviço em diferença aparente entre *harnesses*. "
         "Aquela cuja medição é inconfiável é descartada, registrada como tal e jamais "
         "reparada ou repetida. Códigos de saída não classificam desfecho, porque não o "
         "discriminam.")

    label(doc, "Resultados preliminares do instrumento (Camada 1)")

    body(doc,
         "O instrumento da Camada 1 está construído e executado, com os dados brutos no "
         "repositório público do projeto (YuukiFST, 2026). Na primeira requisição da tarefa "
         "*probe*, em ambiente isolado, medida em 28 de agosto de 2026, os braços diferem por "
         "uma ordem de grandeza antes que o modelo gere qualquer token (Tabela 1): com a "
         "linhagem mantida fixa, o oh-my-pi envia 11,4x os bytes totais do pi, 13,5x os bytes "
         "de esquemas de ferramenta, 10,2x os de prompt de sistema, 2,75x o número de esquemas "
         "e 13,6x os tokens — uma medição anterior, com código independente e prompt "
         "diferente, obtivera 10,8x. Dois achados da mesma execução superam a razão em "
         "importância: os três braços reenviam o histórico completo a cada passo, com "
         "incremento constante de 555, 625 e 698 bytes (pi, oh-my-pi e OpenCode), sem "
         "compactar nem truncar em cinco passos, de modo que o custo relativo já está definido "
         "antes de o laço começar; e o OpenCode gasta por sessão uma chamada auxiliar de 2.526 "
         "bytes que seria cobrada em um nível pago e não aparece no seu próprio relatório — o "
         "objetivo (f) observado, e não argumentado. O delta de estado ambiente do pi nesta "
         "máquina é de 0 bytes, propriedade da máquina tanto quanto do *harness*, a ser "
         "remedida onde o experimento correrá.")

    caption(doc, "Tabela 1 – Primeira requisição por braço, perfil isolado, tarefa probe "
                 "(28 ago. 2026)")
    table(doc, LAYER1_TABLE, size=9)
    caption(doc, "Fonte: elaborado pelo autor (2026).", above=False)

    label(doc, "Limitações e ameaças à validade")

    body(doc,
         "Cinco limitações são declaradas de partida, em vez de defendidas depois. O efeito de "
         "um *harness* é específico do modelo e pode inverter de sinal, o que restringe "
         "qualquer conclusão ao nível de modelo em que foi obtida; o objetivo (e) existe para "
         "testar isso. A transferência para modelos pequenos fica deliberadamente em aberto e "
         "é registrada como trabalho futuro, pela razão que Ning et al. (2026, §5.2.3) "
         "nomeiam: o único modelo pequeno viável havia sido treinado dentro de um dos braços, "
         "o que invalidaria a medição de destaque em vez de apenas limitá-la. Os valores "
         "absolutos não são comparáveis ao placar público do DeepSWE, porque toda linha de "
         "base publicada usa um *harness* de ferramenta única; a comparação aqui é entre os "
         "próprios braços. O custo em dinheiro é um contrafactual de ordem de grandeza sobre "
         "tarifas pagas publicadas, rotulado como tal onde apareça. Por fim, os resultados "
         "preliminares da Camada 1 valem para uma tarefa, uma máquina e três braços — o "
         "controle ainda não figura na tabela — e a Camada 2 ainda não produziu resultado "
         "algum.")


def build_orcamento(doc):
    heading(doc, "4 ORÇAMENTO")

    caption(doc, "Tabela 2 – Orçamento do projeto")
    table(doc, ORCAMENTO_TABLE, size=11, widths=[Cm(11.5), Cm(4.5)])
    caption(doc, "Fonte: elaborado pelo autor (2026).", above=False)

    body(doc,
         "O total em dinheiro é zero, e o limite que restringe o experimento não é financeiro: "
         "é a cota — cerca de 10 requisições a cada 6 minutos no nível gratuito (Opencode, "
         "2026) contra 60 a 270 requisições ao modelo por tarefa do DeepSWE (Huang et al., "
         "2026) —, razão pela qual a matriz é executada em lotes distribuídos ao longo de dias "
         "e o custo monetário aparece apenas como contrafactual de ordem de grandeza sobre as "
         "tarifas pagas publicadas. O Docker é obrigatório, porque o executor falha sem ele "
         "(Datacurve, 2026), e a GPU da estação é irrelevante para todo resultado reportado.")


def build_cronograma(doc):
    heading(doc, "5 CRONOGRAMA")

    body(doc,
         "A cadência é de um lote da matriz por dia, porque a cota gratuita é o limite "
         "vinculante; um calendário que se estende por semanas é consequência do desenho e não "
         "atraso. A folga está onde está o risco — na execução da matriz e nos portões de "
         "confiabilidade dos braços —, e não na escrita. Os meses são numerados de forma "
         "relativa porque a data de entrega ainda não está confirmada: [A DEFINIR — #7].")

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
        pf.space_after = Pt(6)
        pf.first_line_indent = Cm(0)
        _add_marked_runs(p, entry)
        _account(re.sub(r"\*\*|\*", "", entry), factor=0.67, extra=0.34)


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
    found, seen = [], set()
    pattern = re.compile(r"\[[^\[\]]{2,60}\]")
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
    print("Páginas estimadas por seção (capa e sumário fora da contagem):")
    for name in SECTION_ORDER:
        print(f"  {name:<24} {pages[name]:>5.2f}  (inicia na página {starts[name]})")
    print(f"  {'TOTAL':<24} {total:>5.2f}   (alvo 6,4; teto 7,0)")
    if total > 7.0:
        print("  AVISO: acima de 7 páginas — aplicar a escada de redução do doc 14 §5.")
    print()

    markers = collect_markers(doc)
    print(f"Marcadores restantes ({len(markers)}):")
    for m in markers:
        print(f"  {m}")


if __name__ == "__main__":
    main()
