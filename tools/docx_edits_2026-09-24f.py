"""Sixth edit of dist/projeto-de-pesquisa.docx, 2026-09-24: review against the course
handouts and against the cited sources (wiki/queries/2026-09-24-mapa-citacoes-projeto.md).

- [9], [22] Template: the title is "Negrito, Tamanho 16"; it was not bold. *HARNESS*
  goes italic like every other English technical term in the document.
- [18], [31] Aula 3, folha de rosto: "Cidade e estado".
- [61] H1's success clause follows docs/spec/11 §H1: the cell medians of the final
  acceptance fraction, not an undefined "difference" of a fraction [83] reports without a test.
- [65], [66], [69] Aula 5: a direct quote gives author, year and page. The arXiv PDFs are
  paginated: Ning §2 is p. 7, Ning §5.2.7 is p. 66, Lin §1 is p. 1. *harness* in the
  Lin quote goes italic.
- [48] "influenciar no" -> "influencia o"; "com um harness em vez de outro" repeated
  "a escolha do harness".
- [67] The Pi / OpenCode contrast had no citation. Earendil (2026) states Pi's four
  tools and a prompt plus tools under 1,000 tokens; the OpenCode README lists its agents,
  subagent and permissions. "Um prompt maior" came only from the author's own
  Layer 1 measurement and is dropped.
- [68] Zhang's claim is about variance, in long tasks, among comparable frontier models;
  Pan's 2.0x is a geometric mean across models.
- [69] Pan hedges ("can begin with the first model call") and names the cause (longer
  instructions, larger tool schemas; left out for the page budget); the 15.3/15.4 turns are Fable 5 only. Liu changed
  four mechanisms, not three: delegated reading was missing.
- [71] "harness de outro fornecedor" was ambiguous; Pan: an alternative to the model
  provider's own harness.
- [73] A negative claim cannot be cited; "não se encontrou" states what the survey found.
- [83] Miller recommends paired differences because questions share difficulty across
  the two systems; he never says difficulty is the largest source of variance.

Run once, after tools/docx_edits_2026-09-24e.py: python tools/docx_edits_2026-09-24f.py
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

# (paragraph, old substring, new substring); each old must occur exactly once.
SUBS = [
    ("18", "Cuiabá", "Cuiabá – MT"),
    ("31", "Cuiabá", "Cuiabá – MT"),
    ("48", "quanto a escolha do *harness* pode influenciar no custo e na taxa de sucesso ao construir o mesmo software com um *harness* em vez de outro?",
     "quanto a escolha do *harness* influencia o custo e a taxa de sucesso na construção do mesmo software?"),
    ("61", "ou se a fração final de testes aprovados diferir.", "ou se as medianas da fração final de testes aprovados diferirem entre os braços."),
    ("65", "Ning *et al.* (2026, §2, tradução nossa)", "Ning *et al.* (2026, p. 7, tradução nossa)"),
    ("66", "chamado coletivamente de harness do agente. (Lin *et al.*, 2026, §1, tradução nossa).",
     "chamado coletivamente de *harness* do agente. (Lin *et al.*, 2026, p. 1, tradução nossa)."),
    ("67", "O Pi envia quatro ferramentas e um *system prompt* curto, e o OpenCode envia mais ferramentas, um *prompt* maior, subagentes e permissões.",
     "O Pi envia quatro ferramentas e um *system prompt* curto (Earendil, 2026), e o OpenCode envia mais ferramentas, subagentes e permissões (Opencode, 2026a)."),
    ("68", "Zhang *et al.* (2026) sustentam que, entre modelos de fronteira comparáveis, a parcela do desempenho que vem do *harness* é comparável ou maior que a do modelo.",
     "Zhang *et al.* (2026) sustentam que, em tarefas longas e entre modelos de fronteira comparáveis, a variação de desempenho devida ao *harness* é comparável ou maior que a devida ao modelo."),
    ("68", "enquanto o Claude Code custou cerca de 2,0 vezes o Pi.", "enquanto o Claude Code custou, em média, cerca de 2,0 vezes o Pi."),
    ("69", "Pan *et al.* (2026) apontam a primeira requisição. O contexto inicial do Claude Code passa de dez vezes o do Pi, com número de turnos parecido (15,3 contra 15,4 no Claude Fable 5).",
     "Para Pan *et al.* (2026), o imposto pode começar na primeira requisição: nos sete modelos, o contexto inicial médio do Claude Code passa de dez vezes o do Pi, e no Claude Fable 5 os turnos quase se igualam (15,3 contra 15,4)."),
    ("69", "a compactação de contexto e o tratamento das observações,", "a compactação de contexto, o tratamento das observações e a leitura delegada,"),
    ("69", "Ning *et al.* (2026, §5.2.7, tradução nossa)", "Ning *et al.* (2026, p. 66, tradução nossa)"),
    ("71", "o maior sucesso veio de um *harness* de outro fornecedor.", "o maior sucesso veio de um *harness* que não é o do fornecedor do modelo."),
    ("73", "não há comparação publicada de *harnesses* construindo o mesmo produto completo.",
     "não se encontrou comparação publicada de *harnesses* construindo o mesmo produto completo."),
    ("83", "pareado por unidade porque a dificuldade da unidade é a maior fonte de variação (Miller, 2024).",
     "pareado por unidade. O pareamento remove a dificuldade comum aos dois braços (Miller, 2024)."),
]
TITLE = "O HARNESS NO CUSTO E NO DESEMPENHO DE AGENTES DE CODIFICAÇÃO: TOKENS E TAXA DE SUCESSO COM O MODELO FIXO"


def prose() -> None:
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


def title_run(rpr: str, italic: bool) -> str:
    rpr = rpr.replace('<w:b w:val="0"/><w:bCs w:val="0"/>', '<w:b w:val="1"/><w:bCs w:val="1"/>')
    if italic:
        rpr = rpr.replace('<w:i w:val="0"/><w:iCs w:val="0"/>', '<w:i w:val="1"/><w:iCs w:val="1"/>')
    return rpr


def title() -> None:
    """Bold title, *HARNESS* italic; docx_prose markup cannot express bold and italic at once."""
    xml = zipfile.ZipFile(DOCX).read("word/document.xml").decode("utf-8")
    run = re.compile(r'<w:r(?: [^>]*)?>(<w:rPr><w:b w:val="0"/><w:bCs w:val="0"/><w:i w:val="0"/><w:iCs w:val="0"/>'
                     r'<w:sz w:val="32"/><w:szCs w:val="32"/><w:rtl w:val="0"/></w:rPr>)'
                     rf'<w:t xml:space="preserve">{re.escape(TITLE)}</w:t></w:r>')
    head, tail = "O ", TITLE[len("O HARNESS"):]

    def repl(m: re.Match) -> str:
        rpr = m.group(1)
        return "".join(
            f'<w:r>{title_run(rpr, it)}<w:t xml:space="preserve">{t}</w:t></w:r>'
            for t, it in ((head, False), ("HARNESS", True), (tail, False)))

    xml, n = run.subn(repl, xml)
    if n != 2:
        raise SystemExit(f"title run matched {n} times, expected 2 (capa and folha de rosto)")
    _rewrite_zip(DOCX, {"word/document.xml": xml.encode("utf-8")})


def main() -> None:
    title()
    prose()


if __name__ == "__main__":
    main()
