"""Fifth edit of dist/projeto-de-pesquisa.docx, 2026-09-24, at the author's request:
the token measurement is made explicit, and Tabela 2 loses November.

- [80] The count the comparison uses is the gateway's own usage record,
  captured at the proxy on every response, with cached input apart. It is the
  model's count, identical for both arms, and it includes the context a
  harness resends at every step. The previous text
  recounted the bytes with one tokenizer (cl100k_base, docs/spec/41), which is
  not the tokenizer of mimo-v2.5-free or hy3-free and cannot see the cache.
  The recount stays in the proxy for the H2 split, see docs/spec/11 §2.1.
- [80]/[83] H2 is measured per request: the proxy separates system prompt and
  tool schemas from the rest of each request, instead of multiplying the
  Layer 1 load by the step count, which assumed the fixed load never changes
  within a construction.
- [83] Wilcoxon stays on tokens and Succ/Mtok. The pass fraction is reported
  without a test: when both arms pass every test the differences are zero,
  Wilcoxon drops them and has no pairs left. The headline number is the ratio
  of the two arms' median tokens per construction.
- Page budget: the first wording pushed 6 REFERÊNCIAS to a tenth page, so
  [61] and [80] were shortened until Word counted 9 pages again.
- [61] H1's refutation rule follows [83]: success is compared on the final
  pass fraction, not on a test that cannot reject.
- [75] Layer 1 now shows the fixed load without a task; it no longer feeds H2.
- Tabela 2: the author moved "Finn de referência, proxy e testes" into
  October only, which leaves NOVEMBRO empty. Same fix as
  docx_edits_2026-09-24d.py: the empty column goes, the table keeps the
  9071-twip text block and the phase column takes the freed width.

Run once, after tools/docx_edits_2026-09-24d.py: python tools/docx_edits_2026-09-24e.py
"""
import json
import re
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
TEXT_W, MONTHS, MONTH_W = 9071, 3, 1220
PHASE_W = TEXT_W - MONTHS * MONTH_W
FINN_ROW = "FINN DE REFERÊNCIA, PROXY E TESTES"

EDITS = {
    "61": (
        "H1: com o modelo fixo, o *harness* muda mais o custo do que o sucesso. Os tokens por unidade "
        "diferem entre o OpenCode e o Pi, e a fração de testes aprovados fica igual. H1 será refutada se "
        "o teste pareado não apontar diferença de tokens ou se a fração final de testes aprovados diferir."
    ),
    "75": (
        "A medição terá duas camadas. A Camada 1 mede, contra um *endpoint* simulado, os esquemas de "
        "ferramenta, o *system prompt* e os tokens de cada requisição, ou seja, a carga fixa de cada braço "
        "sem tarefa. A Camada 2 mede a construção do produto contra o modelo real."
    ),
    "80": (
        "O *proxy* guardará os tokens que o *gateway* informa em cada resposta, com o cache à parte, e "
        "separará em cada requisição a carga fixa (*system prompt* e ferramentas) do resto da conversa, "
        "para H2. A contagem do *harness* serve só para verificação cruzada."
    ),
    "83": (
        "A comparação usará o teste de Wilcoxon dos postos sinalizados, bilateral, α = 0,05, sobre tokens "
        "e Succ/Mtok, pareado por unidade porque a dificuldade da unidade é a maior fonte de variação "
        "(Miller, 2024). O resultado principal será a razão entre as medianas de tokens por construção "
        "dos braços. A fração de testes aprovados será relatada sem teste, pois um empate em 100% não "
        "deixa diferença a testar. As predições serão registradas antes da coleta."
    ),
}
# Guards: each paragraph must still hold the text this script was written against.
EXPECT = {
    "61": "ou se apontar diferença de sucesso.",
    "75": "e fornece a carga fixa que H2 usa",
    "80": "com o mesmo tokenizador para os dois braços.",
    "83": "(Camada 1 vezes o número de passos) e conversa.",
}


def cell_text(cell: str) -> str:
    return re.sub(r"<[^>]+>", "", cell)


def cronograma(table: str) -> str:
    def row(r: str) -> str:
        cells = CELL.findall(r)
        if len(cells) != 5:
            raise SystemExit(f"row has {len(cells)} cells, expected 5")
        nov = cell_text(cells[4])
        if "X" in nov and FINN_ROW not in cell_text(cells[0]):
            raise SystemExit(f"november has an X outside the Finn row: {cell_text(cells[0])}")
        return r[: r.index("<w:tc>")] + "".join(cells[:4]) + r[r.rindex("</w:tc>") + len("</w:tc>"):]

    new = ROW.sub(lambda m: row(m.group(0)), table)
    grid = "<w:tblGrid>" + f'<w:gridCol w:w="{PHASE_W}"/>' + f'<w:gridCol w:w="{MONTH_W}"/>' * MONTHS
    new, n = GRID.subn(grid, new)
    if n not in (1, 2):
        raise SystemExit(f"tblGrid matched {n} times")
    return new


def prose() -> None:
    import subprocess

    dump = subprocess.run([sys.executable, "tools/docx_prose.py", "dump", str(DOCX)],
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout
    text = dict(re.findall(r"^\[(\d+)\] (.*)$", dump, re.M))
    for i, tail in EXPECT.items():
        if tail not in text[i]:
            raise SystemExit(f"[{i}] changed since this script was written")
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"paragraphs": EDITS}, f, ensure_ascii=False)
    apply(DOCX, Path(f.name))
    Path(f.name).unlink()


def main() -> None:
    prose()
    xml = zipfile.ZipFile(DOCX).read("word/document.xml").decode("utf-8")
    crono = [t for t in TABLE.findall(xml) if "NOVEMBRO" in t]
    if len(crono) != 1:
        raise SystemExit("expected one cronograma with NOVEMBRO")
    xml = xml.replace(crono[0], cronograma(crono[0]), 1)
    _rewrite_zip(DOCX, {"word/document.xml": xml.encode("utf-8")})


if __name__ == "__main__":
    main()
