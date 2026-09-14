"""Sixth pass on the decks (2026-09-14): references outside the theme leave.

Mirrors the removal in dist/projeto-pcc.docx of the ABNT norms, the IFMT
template, Gil (2022) and Prodanov and Freitas (2013): the classification
slide loses its handbook subtitle, the references slide drops the two
handbook entries and the project count goes from 24 to 20, and the notes
follow the new paragraph indices of the dump ([166]-[185] references,
Finn [183], harness-bench [184]).

Applies to dist/apresentacao-pcc.html (exact), deck/index.html (whitespace-
tolerant) and deck/src TypeScript (exact). Pairs already applied are
skipped, so the script can be rerun.

Usage:
    python tools/slides_edits_2026-09-14f.py
    cd deck && npx prettier --write index.html src && npm run build
"""

from pathlib import Path

_src = Path("tools/deck_edits_2026-09-14.py").read_text(encoding="utf-8")
_ns: dict = {}
exec(compile(_src.split("# --- index.html")[0], "deck_edits_helpers", "exec"), _ns)
_apply = _ns["apply"]
ws_pattern = _ns["ws_pattern"]


def apply(path: Path, pairs: list, tolerant: bool) -> None:
    text = path.read_text(encoding="utf-8")
    present = (lambda n: ws_pattern(n).search(text) is not None) if tolerant else (lambda n: n in text)
    todo = [(o, n) for o, n in pairs if not present(n)]
    if todo:
        _apply(path, todo, tolerant)
    else:
        print(f"{path}: nothing to do")


NOTES: list[tuple[str, str]] = [
    ("dedutiva (Gil, 2022; Prodanov; Freitas, 2013)", "dedutiva"),
    (
        "Repositórios YuukiFST/Finn [188] e YuukiFST/harness-bench [189]",
        "Repositórios YuukiFST/Finn [183] e YuukiFST/harness-bench [184]",
    ),
]

DECK_NOTES = NOTES + [
    (
        "<b>Referências [166]–[190].</b> Lista completa com 24 entradas no projeto. Preprints marcados. Aqui só as citadas nos slides: sem as três normas ABNT, IFMT (2022), HarnessRank e Opencode Zen (2026b), citadas só no texto do projeto.",
        "<b>Referências [166]–[185].</b> Lista completa com 20 entradas no projeto, todas sobre o <em>harness</em> (normas e manuais de metodologia saíram em 14 set. 2026). Preprints marcados. Aqui só as citadas nos slides: sem HarnessRank e Opencode Zen (2026b), citadas só no texto do projeto.",
    ),
]

DECK_MARKUP: list[tuple[str, str]] = [
    (
        "Classificação da pesquisa<small>Gil (2022); Prodanov e Freitas (2013) · → revela cada eixo</small>",
        "Classificação da pesquisa<small>→ revela cada eixo</small>",
    ),
    (
        "formato ABNT abreviado; lista completa com 24 entradas no projeto, seção 6",
        "formato ABNT abreviado; lista completa com 20 entradas no projeto, seção 6",
    ),
]

CONTENT: list[tuple[str, str]] = [
    (
        '  "GIL, A. C. <b>Como elaborar projetos de pesquisa</b>. 7. ed. São Paulo: Atlas, 2022.",\n',
        "",
    ),
    (
        '  "PRODANOV, C. C.; FREITAS, E. C. de. <b>Metodologia do trabalho científico</b>. 2. ed. Novo Hamburgo: Feevale, 2013.",\n',
        "",
    ),
]

apply(Path("dist/apresentacao-pcc.html"), NOTES, tolerant=False)
apply(Path("deck/index.html"), DECK_MARKUP, tolerant=True)
apply(Path("deck/src/notes.ts"), DECK_NOTES, tolerant=False)
# Deletions: "present" cannot be tested on an empty replacement, so test the old side.
_content = Path("deck/src/content.ts")
_todo = [(o, n) for o, n in CONTENT if o in _content.read_text(encoding="utf-8")]
if _todo:
    _apply(_content, _todo, tolerant=False)
else:
    print(f"{_content}: nothing to do")
