"""Remove o aparato de citacao de dist/apresentacao-pcc.html (pedido do autor, 2026-09-14).

O deck fica so com o projeto, o tema e o efeito do harness no custo: sai o
slide de referencias, saem as citacoes autor-ano no corpo dos slides e a linha
do tempo mantem autor-ano: o autor quer dizer de onde veio cada afirmacao. As notas do apresentador
(tecla N) nao sao tocadas. Cada par deve casar exatamente uma vez.

Uso (depois de slides_edits_2026-09-14.py e slides_h3_2026-09-14.py):
    python tools/slides_refs_2026-09-14.py
"""
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "dist" / "apresentacao-pcc.html"

R: list[tuple[str, str]] = [
    # slide 2: barras
    (
        "<small>FrontierHarness (Runta, 2026): 12 configurações",
        "<small>FrontierHarness: 12 configurações",
    ),
    (
        " Razão 17,5× calculada pelo autor. Blogue institucional, não revisado por pares.</div>",
        " Razão 17,5× calculada pelo autor.</div>",
    ),
    # rótulo do último nó ("FrontierHarness") estourava o viewBox: ancora nas pontas
    (
        'text-anchor="middle" fill="#8b98a8" font-size="20">${n[1]',
        "text-anchor=\"${i===0?'start':(i===TL.length-1?'end':'middle')}\" fill=\"#8b98a8\" font-size=\"20\">${n[1]",
    ),
    # slide 8: classificação
    (
        "<small>Gil (2022); Prodanov e Freitas (2013) · → revela cada eixo</small>",
        "<small>→ revela cada eixo</small>",
    ),
    (
        "Portaria CNPq nº 2.664/2026 (Brasil, 2026)</div>",
        "Portaria CNPq nº 2.664/2026</div>",
    ),
    (
        '  <div class="denom">Projeto, §3, parágrafos de classificação e de declaração do método (YuukiFST, 2026; Brasil, 2026).</div>\n',
        "",
    ),
    # slide 10: matriz
    ('<div class="denom">Finn (YuukiFST, 2026a): SaaS', '<div class="denom">Finn: SaaS'),
    # slide 11: Succ/Mtok
    (
        ' <span class="mute">(Lin <em>et al.</em>, 2026, Eq. 2)</span></div>',
        "</div>",
    ),
    # slide 15: fecho
    (
        "github.com/YuukiFST/harness-bench (YuukiFST, 2026b) e github.com/YuukiFST/Finn (YuukiFST, 2026a).",
        "github.com/YuukiFST/harness-bench e github.com/YuukiFST/Finn.",
    ),
]

REFS_SLIDE_START = '<section class="slide" data-title="Referências citadas nos slides">'
REFS_SLIDE_END = "<!-- "  # próximo comentário de slide (fecho)
REFS_JS_START = "// ---------- slide 13: referências ----------"
REFS_JS_END = "// ---------- início ----------"
REFS_NOTE_START = "`<b>Referências [166]–[190].</b>"


def cut(html: str, start: str, end: str) -> str:
    a = html.index(start)
    b = html.index(end, a)
    assert html.count(start) == 1, start
    return html[:a] + html[b:]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    for old, new in R:
        n = html.count(old)
        if n != 1:
            raise SystemExit(f"esperado 1, achado {n}: {old[:80]!r}")
        html = html.replace(old, new)
    html = cut(html, REFS_SLIDE_START, REFS_SLIDE_END)
    html = cut(html, REFS_JS_START, REFS_JS_END)
    # nota do slide removido: a entrada inteira, até a próxima linha de nota
    a = html.index(REFS_NOTE_START)
    b = html.index("\n", a) + 1
    html = html[:a] + html[b:]
    HTML.write_text(html, encoding="utf-8", newline="\n")
    print(f"applied {len(R)} replacements, removed references slide, JS and note")


if __name__ == "__main__":
    main()
