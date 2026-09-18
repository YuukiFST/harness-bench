"""Align dist/apresentacao-explainer/index.html with the 2026-09-18 docx: new title,
theme (harness as the lever on a fixed model's cost and performance), problem
wording, one-line objectives, and the paragraph indices [n] in notes and source
lines, which moved by +17 after the author's Word edits.

Run once: python tools/slides_edits_2026-09-18.py
"""
import re
from pathlib import Path

DECK = Path("dist/apresentacao-explainer/index.html")
TITLE_HTML = "Como o <em>harness</em> altera o custo e o desempenho do modelo"
TITLE_TEXT = "Como o harness altera o custo e o desempenho do modelo"

REPLACEMENTS = [
    ("<title>O harness como decisão do desenvolvedor — deck explicativo</title>",
     f"<title>{TITLE_TEXT} — deck explicativo</title>"),
    ('<h1 class="slide__display">O <em>harness</em> como decisão do desenvolvedor</h1>',
     f'<h1 class="slide__display">{TITLE_HTML}</h1>'),
    ("Justificativa, tema, problema, objetivos e hipóteses. Mesmo modelo, mesmas tarefas",
     "Justificativa, tema, problema, objetivos, metodologia e hipóteses. Mesmo modelo, mesmas tarefas"),
    # Slide "Justificativa e tema"
    ('<h2 class="slide__heading">Conhecer o <em>harness</em> virou parte do ofício</h2><p class="slide__subtitle">as comparações publicadas usam tarefas isoladas e não dizem quanto custa entregar um produto inteiro com uma ferramenta em vez de outra [44]</p>',
     '<h2 class="slide__heading">Escolher o modelo deixou de bastar</h2><p class="slide__subtitle">os modelos avançam, e com eles os <em>harnesses</em> e as ferramentas feitas para agentes; o <em>harness</em> é a parte dessa escolha que ninguém mediu em um produto inteiro [44]</p>'),
    ('<span class="card__k">Justificativa</span>Quem paga é o desenvolvedor, na assinatura, e a empresa, em escala. Os placares publicados comparam <em>harnesses</em> em suítes de tarefas soltas; nenhum mede o custo de construir um produto completo com um <em>harness</em> em vez de outro.',
     '<span class="card__k">Justificativa</span>Os agentes de codificação avançam em duas frentes: o modelo e o <em>harness</em> em volta dele. Next.js, TanStack e Effect se adaptam ao trabalho de agentes. Quem paga é o desenvolvedor, na assinatura, e a empresa, em escala; as comparações publicadas usam tarefas isoladas.'),
    ('<span class="card__k">Tema</span>A escolha do <em>harness</em> como decisão de engenharia: efeito sobre tokens consumidos e taxa de sucesso na construção de um mesmo produto, com o modelo fixo.',
     '<span class="card__k">Tema</span>O efeito do <em>harness</em> sobre o custo e o desempenho de um modelo de linguagem fixo: quantos tokens e que taxa de sucesso o mesmo modelo entrega ao construir o mesmo produto sob dois <em>harnesses</em>.'),
    ('<span class="card__k">Como o projeto mede isso [44]</span>«Este projeto medirá esse custo construindo o mesmo produto duas vezes: o Finn, um SaaS de financeiro por voz, será construído com o OpenCode e com o pi, sobre o mesmo modelo e a partir da mesma especificação, e os tokens que cada braço gastar até entregar o produto serão contados fora do <em>harness</em>.»',
     '<span class="card__k">Como o projeto mede isso [44]</span>«Este projeto mede esse custo construindo o Finn duas vezes, com o OpenCode e com o pi, sobre o mesmo modelo e a mesma especificação, com os tokens contados fora do <em>harness</em>.»'),
    ('Projeto, §1: justificativa [43]–[44], tema [46].', 'Projeto, §1: justificativa [43]–[44], tema [46].'),
    ('<div class="notes"><b>Justificativa [44], tema [46].</b> Ler o trecho [44] na íntegra.',
     '<div class="notes"><b>Justificativa [43]–[44], tema [46].</b> Ler o tema [46] na íntegra.'),
    # Problem
    ('<blockquote class="reveal">Com o modelo já escolhido, <b>quantos tokens</b> a mais ou a menos custa construir o mesmo software com um <em>harness</em> em vez de outro? E <b>quanto dessa diferença</b> vem da carga fixa que cada <em>harness</em> envia em toda requisição?</blockquote>',
     '<blockquote class="reveal">Com o modelo já escolhido, <b>quanto mudam o custo em tokens e a taxa de sucesso</b> ao construir o mesmo software com um <em>harness</em> em vez de outro, e <b>quanto dessa diferença</b> vem da carga fixa que cada <em>harness</em> envia em toda requisição?</blockquote>'),
    ('<cite class="reveal">Problema de pesquisa · Projeto, §1 [48]</cite>', '<cite class="reveal">Problema de pesquisa · Projeto, §1 [48]</cite>'),
    ('<div class="notes"><b>Problema [48].</b> Ler na íntegra. A segunda pergunta é H2; a primeira é H1. Objetivo geral [50]:',
     '<div class="notes"><b>Problema [48].</b> Ler na íntegra. A segunda metade é H2; a primeira é H1. Objetivo geral [50]:'),
    # Objectives table rows follow the one-line objectives
    ('<td class="k">Instrumento externo</td><td>requisições, tokens, latência, idêntico para os dois braços</td>',
     '<td class="k">Instrumento externo</td><td>requisições, tokens e latência por braço</td>'),
    ('<td class="k">Espaço de trabalho inicial idêntico</td><td>só a especificação e a pilha, congelado por hash</td>',
     '<td class="k">Espaço de trabalho inicial idêntico</td><td>para os dois braços, congelado por hash</td>'),
    ('<td class="k">Construção completa nos dois <em>harnesses</em></td><td>mesmo modelo e <em>prompts</em>, n ≥ 3</td>',
     '<td class="k">Finn nos dois <em>harnesses</em></td><td>mesmo modelo e <em>prompts</em>, com repetição (n ≥ 3)</td>'),
    ('<td class="k">Tokens relatados × medidos</td><td>divergência entre relato do <em>harness</em> e <em>proxy</em></td>',
     '<td class="k">Tokens relatados × medidos</td><td>divergência entre o relato do <em>harness</em> e o instrumento</td>'),
    # Capa notes: the title-page paragraphs
    ("Título, autor e orientadora [4][5][12].", "Título, autor e orientadora [21][22][24]."),
    ("IFMT Campus Octayde Jorge da Silva [11].", "IFMT Campus Octayde Jorge da Silva [23]."),
]


def shift_indices(html: str) -> str:
    """[n] with n >= 26 in the slide markup (not the script) moves by +17."""
    cut = html.index("// Motor de leitura do deck")  # the deck engine; the one-liner in <head> stays
    body, script = html[:cut], html[cut:]

    def bump(m: re.Match) -> str:
        n = int(m.group(1))
        return f"[{n + 17}]" if n >= 26 else m.group(0)

    return re.sub(r"\[(\d+)\]", bump, body) + script


def main() -> None:
    html = shift_indices(DECK.read_text(encoding="utf-8"))
    for old, new in REPLACEMENTS:
        if old not in html:
            raise SystemExit(f"not found: {old[:80]}")
        html = html.replace(old, new, 1)
    DECK.write_text(html, encoding="utf-8")
    print("deck updated")


if __name__ == "__main__":
    main()
