"""Slides do deck explicativo, um `<section class="slide">` por função.

Texto e números vêm só do projeto (dist/projeto-de-pesquisa.docx); cada slide de evidência
traz o denominador na linha de fonte. Notas do apresentador ficam em `<div class="notes">` e
aparecem com a tecla N; os índices [n] referem-se ao dump do .docx via
`python tools/docx_prose.py dump dist/projeto-de-pesquisa.docx` (versão de 2026-09-23).
"""

from __future__ import annotations

import re

from charts import (
    harness_anatomy,
    layers_flow,
    pair_bars,
    title_decor,
    vbars,
)
from content import (
    CLASS_AXES,
    FINN_PIPELINE,
    GANTT,
    GANTT_MONTHS,
    HARNESSTAX,
    LIN_T1,
    OBJECTIVES,
    REFS,
    UNITS,
)


EN_TERMS = re.compile(r"\b(harness(?:es)?|proxy)\b")
HEAD_OPEN = '<div class="slide__head reveal">'
SOURCE_OPEN = '<p class="slide__source reveal">'


def sec(kind: str, title: str, inner: str, notes: str = "", extra_cls: str = "") -> str:
    """Embrulha o miolo (entre cabeçalho e linha de fonte) em .slide__mid, que centra verticalmente."""
    cls = f"slide slide--{kind} {extra_cls}".strip()
    n = f'<div class="notes">{notes}</div>' if notes else ""
    if inner.startswith(HEAD_OPEN):
        head_end = inner.index("</div>", len(HEAD_OPEN)) + len("</div>")
        src_start = inner.rfind(SOURCE_OPEN)
        if src_start == -1:
            src_start = len(inner)
        inner = inner[:head_end] + '<div class="slide__mid">' + inner[head_end:src_start] + "</div>" + inner[src_start:]
    return f'<section class="{cls}" data-title="{title}">\n{inner}\n{n}\n</section>\n'


def head(label: str, heading: str, sub: str = "") -> str:
    s = f'<p class="slide__subtitle">{sub}</p>' if sub else ""
    return f'<div class="slide__head reveal"><p class="slide__label">{label}</p><h2 class="slide__heading">{heading}</h2>{s}</div>'


def source(text: str) -> str:
    return f'<p class="slide__source reveal">{text}</p>'


def divider(num: str, kicker: str, heading: str, sub: str, toc: list[str] | None = None) -> str:
    """Abertura de seção; `toc` lista os títulos dos slides da seção (preenchido por all_slides)."""
    items = "".join(f"<li>{EN_TERMS.sub(r'<em>\1</em>', t)}</li>" for t in (toc or []))
    toc_html = f'<ol class="divider-toc reveal">{items}</ol>' if items else ""
    inner = (
        f'<span class="slide__number" aria-hidden="true">{num}</span>'
        f'<div class="reveal"><p class="divider-kicker">{kicker}</p><h2 class="slide__heading">{heading}</h2>'
        f'<p class="slide__subtitle">{sub}</p></div>{toc_html}'
    )
    return sec("divider", f"{num} · {heading}", inner)


def figure(svg: str, caption: str) -> str:
    return f'<figure class="chart reveal">{svg}<figcaption>{caption}</figcaption></figure>'


ARROW = '<div class="pipeline__arrow"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M5 12h14m-4-4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'


def pipeline(steps: list[tuple[str, str, str, str]], cls_by_index: dict[int, str] | None = None) -> str:
    cls_by_index = cls_by_index or {}
    parts = []
    for i, (num, name, desc, file) in enumerate(steps):
        extra = f" {cls_by_index[i]}" if i in cls_by_index else ""
        f = f'<div class="pipeline__file">{file}</div>' if file else ""
        parts.append(f'<div class="pipeline__step{extra}"><div class="pipeline__num">{num}</div><div class="pipeline__name">{name}</div><div class="pipeline__desc">{desc}</div>{f}</div>')
    return '<div class="pipeline reveal">' + ARROW.join(parts) + "</div>"


# ---------------------------------------------------------------- capa e introdução

def s_capa() -> str:
    inner = f"""
<div class="title-decor">{title_decor()}</div>
<div class="reveal">
<p class="title-inst">Instituto Federal de Mato Grosso · Campus Octayde Jorge da Silva · Sistemas para Internet</p>
<h1 class="slide__display">O <em>harness</em> no custo e no desempenho de agentes de codificação</h1>
<p class="title-sub">Tokens e taxa de sucesso com o modelo fixo</p>
<div class="title-rule"></div>
<p class="title-who"><b>Fausto Yuuki T. A. Freire</b> · Orientadora: Profa. Inara Silva<br>
<span class="slide__subtitle">Projeto de pesquisa · Metodologia Científica · Cuiabá, 2026</span></p>
</div>"""
    notes = "<b>Capa [21]–[24].</b> Título: «O harness no custo e no desempenho de agentes de codificação: tokens e taxa de sucesso com o modelo fixo» [22]. Projeto de pesquisa da disciplina de Metodologia Científica, curso de Sistemas para Internet, IFMT Campus Octayde Jorge da Silva [23]."
    return sec("title", "Capa", inner, notes)


def s_justificativa() -> str:
    inner = head("Justificativa", "Mesmo modelo, quase o mesmo sucesso, <em>cerca do dobro</em> do custo",
                 "HarnessTax (Pan <em>et al.</em>, 2026): sete modelos em três <em>harnesses</em>; no SWE-bench Lite, o Claude Fable 5 no Claude Code e no pi")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1.3fr 1fr;align-items:stretch">
{figure(pair_bars(HARNESSTAX, "o Claude Code custa cerca do dobro por tentativa", "Claude Fable 5 · SWE-bench Lite · Pan et al. (2026)"), "Os mesmos números do projeto [43]: 97,8 % contra 96,7 % de sucesso, US$ 1,33 contra US$ 0,67 por tentativa.")}
<div class="cards" style="grid-template-columns:1fr;align-content:center">
<div class="card reveal"><span class="card__k">O que Pan <em>et al.</em> concluíram</span>A escolha do <em>harness</em> quase não muda a taxa de sucesso, mas muda o custo.</div>
<div class="card card--hi reveal"><span class="card__k">Imposto do <em>harness</em></span>Quem paga por tokens paga também essa diferença.</div>
</div>
</div>"""
    inner += source("Pan <em>et al.</em> (2026), HarnessTax, Universidade da Califórnia em Berkeley; publicação de blogue de pesquisa, não revisada por pares. Projeto, §1 [43]–[44].")
    notes = "<b>Justificativa [43]–[44].</b> Um agente de codificação tem duas partes: o modelo e o harness, o software ao redor que monta o contexto, expõe as ferramentas e conduz a execução (Claude Code, Codex, OpenCode, pi) [43]. Pan et al. (2026): sete modelos em três harnesses; no SWE-bench Lite, Claude Fable 5 resolve 97,8% no Claude Code e 96,7% no pi, a US$ 1,33 contra US$ 0,67 por tentativa [43]. «Imposto do harness» é o termo dos autores [44]."
    return sec("chart", "Justificativa: o imposto do harness", inner, notes)


def s_tema() -> str:
    inner = head("Justificativa e tema", "O que falta medir: o <em>harness</em> num produto inteiro",
                 "as medições publicadas usam tarefas isoladas; os próprios autores pedem fluxos reais de desenvolvimento [44]")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">O limite das medições</span>Tarefas isoladas de <em>benchmarks</em> que os modelos podem ter visto no treino. O próximo passo, segundo os autores, é medir o <em>harness</em> em fluxos reais, com tarefas de várias sessões.</div>
<div class="card reveal"><span class="card__k">Tema</span>O efeito do <em>harness</em> sobre o custo e o desempenho de um modelo de linguagem fixo na construção de um produto de software completo.</div>
<div class="card card--hi reveal" style="grid-column:1/-1"><span class="card__k">O que este projeto faz [44]</span>Constrói o mesmo produto, o Finn, com o OpenCode e com o pi, sobre o mesmo modelo e a mesma especificação, e conta os tokens fora do <em>harness</em>.</div>
</div>"""
    inner += source("Projeto, §1: justificativa [44], tema [46].")
    notes = "<b>Justificativa [44], tema [46].</b> Ler o tema na íntegra. Se perguntarem por que não deixar o OpenCode construir e gerar a especificação para o pi: entrada desigual; a especificação é única e a mesma para os dois braços [77]."
    return sec("content", "Justificativa e tema", inner, notes)


def s_problema() -> str:
    inner = """
<span class="quote-mark" aria-hidden="true">“</span>
<blockquote class="reveal">«Com o modelo fixo, <b>quanto mudam o custo em tokens e a taxa de sucesso</b> ao construir o mesmo software com um <em>harness</em> em vez de outro, e <b>quanto da diferença de custo</b> vem da carga fixa que cada <em>harness</em> envia em toda requisição?»</blockquote>
<cite class="reveal">Problema de pesquisa · Projeto, §1 [48]</cite>"""
    notes = "<b>Problema [48].</b> Ler na íntegra. A primeira metade vira H1; a segunda, H2. Objetivo geral [50]: medir, com o modelo fixo, a diferença de tokens e de taxa de sucesso atribuível ao harness na construção do mesmo produto a partir da mesma especificação, com o OpenCode e o pi como braços, e separar a parcela que vem da carga fixa por requisição."
    return sec("quote", "Problema de pesquisa", inner, notes)


def s_objetivos() -> str:
    inner = head("Objetivos", "Um objetivo geral, seis específicos",
                 "medir, com o modelo fixo, a diferença de tokens e de sucesso atribuível ao <em>harness</em>, com o OpenCode e o pi como braços, e separar a parcela da carga fixa por requisição [50]")
    trs = "".join(
        f'<tr><td class="n">{i+1}</td><td class="k">{k}</td><td class="d">{d}</td></tr>'
        for i, (k, d) in enumerate(OBJECTIVES)
    )
    inner += f'<div class="table-wrap reveal"><table class="data"><tbody>{trs}</tbody></table></div>'
    inner += source("Projeto, §1: objetivo geral [50], objetivos específicos [52]–[57].")
    notes = "<b>Objetivos específicos [52]–[57].</b> 1 construir o proxy que conta requisições, tokens e latência por braço; 2 escrever a especificação do Finn em nove unidades, com testes de aceitação; 3 construir o Finn nos dois harnesses, com o mesmo modelo, prompt e espaço inicial; 4 repetir em um segundo modelo e verificar se a ordenação dos braços se mantém; 5 comparar os tokens relatados por cada harness com os medidos no proxy; 6 publicar executor, prompts, testes, dados e scripts de análise."
    return sec("table", "Objetivos", inner, notes)


def s_hipoteses() -> str:
    inner = head("Hipóteses", "H1: o <em>harness</em> muda mais o custo do que o sucesso. H2: a maior parte é carga fixa",
                 "as duas com critério de refutação declarado [61][62]")
    inner += """
<div class="cards c2" style="align-items:stretch">
<div class="card card--hi reveal"><span class="card__k">H1</span>Com o modelo fixo, os tokens por unidade diferem entre o OpenCode e o pi, e a fração de testes aprovados fica igual.<br><span class="mute">Refutada se o teste pareado não apontar diferença de tokens ou se apontar diferença de sucesso.</span></div>
<div class="card card--hi reveal"><span class="card__k">H2</span>A carga fixa por requisição (<em>prompt</em> de sistema e esquemas de ferramenta) explica a maior parte da diferença de tokens; o número de passos, a menor.<br><span class="mute">Refutada se os passos ou o conteúdo da conversa explicarem a maior parte.</span></div>
</div>"""
    inner += source("Projeto, §1, hipóteses [61]–[62].")
    notes = "<b>Hipóteses [61][62].</b> H1: com o modelo fixo, o harness muda mais o custo do que o sucesso; refutada se o teste pareado não apontar diferença de tokens ou se apontar diferença de sucesso. H2: carga fixa contra passos e conversa; refutada se os passos ou o conteúdo da conversa explicarem a maior parte. As predições são registradas antes da coleta [83]."
    return sec("content", "Hipóteses H1 e H2", inner, notes)


# ---------------------------------------------------------------- referencial

def s_anatomy() -> str:
    inner = head("Definição", "O que é um <em>harness</em>",
                 "os componentes externos ao modelo e editáveis que o cercam (Lin <em>et al.</em>, 2026, §1)")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1fr 1.15fr">
<div class="slide__aside reveal">{harness_anatomy()}</div>
<div>
<ul class="slide__bullets">
<li class="reveal"><b>Ning <em>et al.</em> (2026, §2)</b> · um <em>harness</em> «converte um modelo de linguagem sem estado em um agente funcional ao ancorar suas saídas em execução externa, estado persistente e realimentação verificável».</li>
<li class="reveal"><b>Lin <em>et al.</em> (2026, §1)</b> · o <em>prompt</em> de sistema, as ferramentas que expõem o sistema de arquivos e o shell, e o <em>middleware</em> que controla contexto, execução e recuperação.</li>
<li class="reveal"><b>Neste projeto</b> · só esse conjunto varia. O pi envia quatro ferramentas e um <em>prompt</em> curto; o OpenCode, mais ferramentas, um <em>prompt</em> maior, subagentes e permissões.</li>
</ul>
</div>
</div>"""
    inner += source("Ning <em>et al.</em> (2026, §2); Lin <em>et al.</em> (2026, §1). <em>Preprints</em>, não revisados por pares. Projeto, §2 [65]–[67].")
    notes = "<b>Referencial [65]–[67].</b> Ning et al. (2026, §2): definição citada [65]. Lin et al. (2026, §1): citação longa [66], o conjunto de componentes externos ao modelo e editáveis. [67]: só esse conjunto varia entre os braços; o pi envia quatro ferramentas e um prompt curto, o OpenCode mais ferramentas, prompt maior, subagentes e permissões. O proxy fica fora do harness e conta igual para os dois braços [59]."
    return sec("content", "O que é um harness", inner, notes)


def s_sucesso() -> str:
    inner = head("Referencial · sucesso", "O <em>harness</em> muda o sucesso? As fontes divergem",
                 "por isso este projeto mede sucesso e custo juntos [68]")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1fr 1fr;align-items:stretch">
{figure(vbars(LIN_T1, " %", 80, "Aprovação de harnesses escritos por humanos sobre o GPT-5.4 no Terminal-Bench 2"), "<b>Lin <em>et al.</em> (2026), Tabela 1:</b> <em>harnesses</em> escritos por humanos sobre o GPT-5.4, Terminal-Bench 2.")}
<div class="cards" style="grid-template-columns:1fr;align-content:center">
<div class="card reveal"><span class="card__k">Zhang <em>et al.</em> (2026)</span>Entre modelos de fronteira comparáveis, a parcela do desempenho que vem do <em>harness</em> é comparável ou maior que a do modelo.</div>
<div class="card reveal"><span class="card__k">Pan <em>et al.</em> (2026) · SWE-bench Lite</span><span class="card__v num">±2 % no sucesso</span>O Claude Code custou cerca de 2,0 vezes o pi.</div>
</div>
</div>"""
    inner += source("Lin <em>et al.</em> (2026) e Zhang <em>et al.</em> (2026), <em>preprints</em>; Pan <em>et al.</em> (2026), blogue de pesquisa. Projeto, §2 [68].")
    notes = "<b>Referencial [68].</b> Lin et al. (2026), Tabela 1: harnesses escritos por humanos sobre o GPT-5.4 vão de 47,2% no OpenCode a 71,9% no Codex, no Terminal-Bench 2. Zhang et al. (2026): parcela do harness comparável ou maior que a do modelo. Pan et al. (2026) mediram outra coisa: efeito médio do harness sobre o sucesso dentro de ±2%, custo do Claude Code cerca de 2,0 vezes o do pi. Como as fontes divergem sobre o sucesso, o projeto mede os dois."
    return sec("chart", "Sucesso: as fontes divergem", inner, notes)


def s_pendencia_custo() -> str:
    inner = head("Referencial · primeira pendência", "De onde vem a diferença de custo?",
                 "Pan <em>et al.</em> apontam a primeira requisição; Liu <em>et al.</em>, o resto da conversa [69]")
    inner += """
<div class="cards c2" style="align-items:stretch">
<div class="card reveal"><span class="card__k">Pan <em>et al.</em> (2026) · a primeira requisição</span><span class="card__v num">mais de 10× o contexto inicial</span>O contexto inicial do Claude Code passa de dez vezes o do pi, com número de turnos parecido: 15,3 contra 15,4 no Claude Fable 5.</div>
<div class="card reveal"><span class="card__k">Liu <em>et al.</em> (2026) · SoL-Pi · a conversa</span><span class="card__v num">44,7 % a 49,0 % menos tokens</span>Mudando só a execução das ações, a compactação de contexto e o tratamento das observações, em relação ao pi, com 93,7 % a 94,3 % da pontuação dele.</div>
<div class="card card--hi reveal" style="grid-column:1/-1"><span class="card__k">O que H2 testa</span>Ning <em>et al.</em> (2026, §5.2.7) pedem «métricas que isolem componentes do <em>harness</em>». H2 testa se pesa mais a carga fixa ou a conversa.</div>
</div>"""
    inner += source("Pan <em>et al.</em> (2026), blogue de pesquisa; Liu <em>et al.</em> (2026), arXiv:2609.20519, <em>preprint</em>; Ning <em>et al.</em> (2026), <em>preprint</em>. Projeto, §2 [69].")
    notes = "<b>Primeira pendência [69].</b> Pan: o contexto inicial do Claude Code passa de dez vezes o do pi, com 15,3 contra 15,4 turnos no Claude Fable 5. Liu (SoL-Pi): mudando só a execução das ações, a compactação e o tratamento das observações, de 44,7% a 49,0% menos tokens que o pi, mantendo de 93,7% a 94,3% da pontuação dele. Ning (§5.2.7) pede métricas que isolem componentes; H2 responde a isso."
    return sec("content", "Primeira pendência: o custo", inner, notes)


def s_pendencia_medida() -> str:
    inner = head("Referencial · segunda pendência e métricas", "Contar do mesmo jeito nos dois braços",
                 "cada <em>harness</em> conta turnos e tokens do seu jeito; aqui a medição ocorre num <em>proxy</em> externo [70]")
    inner += """
<div class="cards c3" style="align-items:stretch">
<div class="card reveal"><span class="card__k">Instrumentação [70]</span>Pan <em>et al.</em> (2026) registram que a definição de turno varia entre os <em>harnesses</em>. O <em>proxy</em> é igual para os dois braços, e o objetivo (5) compara essa medida com o relato de cada <em>harness</em>.</div>
<div class="card reveal"><span class="card__k">Métricas [71]</span>Tokens por construção, ao lado da fração de testes aprovados, e o Succ/Mtok (sucessos por milhão de tokens) de Lin <em>et al.</em> (2026).</div>
<div class="card card--hi reveal"><span class="card__k">Dois níveis de modelo [71]</span>O efeito depende do modelo: em nove de doze comparações de Pan <em>et al.</em> (2026), o maior sucesso veio de um <em>harness</em> de outro fornecedor.</div>
</div>"""
    inner += source("Projeto, §2 [70]–[71].")
    notes = "<b>Segunda pendência [70] e métricas [71].</b> Cada harness conta turnos e tokens do seu jeito, e Pan et al. registram que a definição de turno varia; o proxy externo é igual para os dois braços e o objetivo (5) compara a medida com o relato. Métricas: tokens por construção ao lado da fração de testes aprovados, e o Succ/Mtok de Lin et al. Nove de doze comparações de Pan: o maior sucesso veio de um harness de outro fornecedor; daí os dois níveis de modelo."
    return sec("content", "Segunda pendência: a medida", inner, notes)


# ---------------------------------------------------------------- método

def s_classificacao() -> str:
    trs = "".join(
        f'<tr><td class="k">{k}</td><td class="v">{v}</td><td class="d">{w}</td></tr>'
        for k, v, w in CLASS_AXES
    )
    inner = head("Classificação da pesquisa", "Aplicada, quali-quantitativa, exploratória, experimental, dedutiva",
                 "o <em>harness</em> é a variável manipulada; modelo, especificação, espaço de trabalho inicial e limites ficam controlados")
    inner += f"""
<div class="table-wrap reveal"><table class="data"><tbody>{trs}</tbody></table></div>"""
    inner += source("Projeto, §1 [59] e §3 [73].")
    notes = "<b>Classificação [59][73].</b> Aplicada quanto à finalidade, quali-quantitativa quanto à abordagem, exploratória quanto aos objetivos, experimental quanto aos procedimentos e dedutiva quanto ao método. Exploratória porque não há comparação publicada de harnesses construindo o mesmo produto completo."
    return sec("table", "Classificação da pesquisa", inner, notes)


def s_ia() -> str:
    inner = head("Uso de IA declarado", "O agente organiza e especifica; o autor confere e responde",
                 "Portaria CNPq nº 2.664/2026 (Brasil, 2026) · ferramenta declarada: Claude Code")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">Levantamento das fontes · <em>LLM Wiki</em> (Karpathy, 2026)</span>
<ol class="card__steps">
<li><b>Fontes brutas</b> ficam guardadas sem alteração no repositório (YuukiFST, 2026c).</li>
<li><b>O agente escreve</b> uma página de síntese por fonte e liga entidades e conceitos.</li>
<li><b>O autor confere</b> cada afirmação citada na obra original.</li>
</ol></div>
<div class="card reveal"><span class="card__k">Especificação do Finn · Helmsman (YuukiFST, 2026a)</span>
<ol class="card__steps">
<li><b>Produto e pilha</b> decididos antes do experimento, em 21 <em>tickets</em>.</li>
<li><b>O que o sistema faz</b>: o autor decide e responde pelas decisões de produto.</li>
<li><b>Resultado</b>: a especificação única, a mesma para os dois braços.</li>
</ol></div>
</div>"""
    inner += source("Projeto, §3 [74] e [77] (Brasil, 2026; Karpathy, 2026; YuukiFST, 2026a, 2026c).")
    notes = "<b>Uso de IA [74].</b> Conforme a Portaria CNPq nº 2.664/2026, declara-se o uso do Claude Code no levantamento das fontes, organizado pelo método LLM Wiki de Karpathy (2026) no repositório do projeto (YuukiFST, 2026c), e na especificação do Finn, feita com o Helmsman (YuukiFST, 2026a). O autor conferiu cada afirmação citada na obra original e responde pelo texto e pelas decisões de produto. Os 21 tickets estão em [77]."
    return sec("content", "Uso de IA declarado", inner, notes)


def s_como() -> str:
    steps = [
        ("01 · UMA ESPECIFICAÇÃO", "Finn, em 9 unidades", "Especificação única, congelada por SHA-256, com a pilha e nove unidades em ordem de dependência.", "congelada · SHA-256"),
        ("02 · DOIS HARNESSES", "OpenCode e pi", "Mesmo modelo, mesmo <em>prompt</em>, mesmo espaço de trabalho inicial; cada braço constrói do zero.", "opencode run · pi --mode json"),
        ("03 · UM CONTADOR EXTERNO", "<em>Proxy</em> reverso", "Entre o <em>harness</em> e o modelo: conta requisições, tokens e latência da mesma forma para os dois.", "proxy · um tokenizador"),
        ("04 · UM CRITÉRIO", "Tokens ao lado do sucesso", "Tokens, fração de testes aprovados e Succ/Mtok; Wilcoxon pareado por unidade.", "Wilcoxon · Succ/Mtok"),
    ]
    inner = head("Como o projeto funciona", "O mesmo produto, construído duas vezes", "cada braço constrói o Finn do zero, em nove unidades, ao menos três vezes [59]")
    inner += pipeline(steps)
    inner += source("Projeto, §1 [59] e §3 [75]–[83]. Braços: OpenCode (Opencode, 2026a) e pi (Earendil, 2026). O autor não escreve código no espaço de trabalho [77].")
    notes = "<b>Como o projeto funciona [59][75]–[83].</b> Dizer a ordem: especificação, dois braços do zero, proxy, critério. Camadas, matriz e limite vêm nos slides seguintes."
    return sec("content", "Como o projeto funciona", inner, notes)


def s_camadas() -> str:
    inner = head("Método · instrumento", "Duas camadas de medição, um <em>proxy</em>",
                 "a Camada 1 fornece a carga fixa que H2 usa; a Camada 2 mede a construção do produto contra o modelo real [75]")
    inner += figure(layers_flow(), "")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">Camada 1</span>Contra um <em>endpoint</em> simulado, mede os esquemas de ferramenta, o <em>prompt</em> de sistema e os tokens de cada requisição.</div>
<div class="card reveal"><span class="card__k">Limite único</span>Tempo de relógio por unidade, de três vezes a maior mediana dos braços nas unidades-piloto. Sem teto de passos: um teto seria decisão de projeto de <em>harness</em> [81].</div>
</div>"""
    inner += source("O <em>proxy</em> conta os tokens sobre os bytes transmitidos, com o mesmo tokenizador para os dois braços; as contagens do <em>harness</em> e do <em>gateway</em> servem só para verificação cruzada [80].")
    notes = "<b>Método [75][80][81].</b> Camada 1: endpoint simulado, esquemas, prompt de sistema e tokens por requisição; é a carga fixa de H2. Camada 2: construção do produto contra o modelo real. O proxy conta sobre os bytes transmitidos com o mesmo tokenizador [80]. Limite único: três vezes a maior mediana dos braços nas unidades-piloto; o número de passos fica livre [81]."
    return sec("chart", "Duas camadas de medição", inner, notes)


def s_finn() -> str:
    flow = "".join(
        f'<div class="flow__step"><div class="flow__dot">{i + 1}</div><div class="flow__name">{n}</div><div class="flow__desc">{d}</div></div>'
        for i, (n, d) in enumerate(FINN_PIPELINE)
    )
    inner = head("O produto", "Finn: um SaaS completo, com a pilha já decidida",
                 "SaaS multiempresa em que a empresa cliente fala com o próprio financeiro por voz e recebe lançamento, relatório e aviso no celular [77]")
    inner += f'<div class="flow reveal">{flow}</div>'
    inner += """
<div class="card card--hi reveal"><span class="card__k">Decidido antes do experimento</span>Produto e pilha em 21 <em>tickets</em>: TypeScript, TanStack Start, tRPC, Drizzle ORM, PostgreSQL, Vitest. Os agentes não escolhem nada disso.</div>"""
    inner += source("Finn (YuukiFST, 2026b): github.com/YuukiFST/Finn. Fluxo de voz da <em>issue</em> #14, que a unidade U4 implementa. Projeto, §3 [77].")
    notes = "<b>Finn (YuukiFST, 2026b) [77].</b> SaaS multiempresa de financeiro por voz. Produto e pilha foram decididos antes do experimento, em 21 tickets. Ponto a dizer: as medições publicadas usam tarefas isoladas [44]; aqui o agente constrói um produto inteiro."
    return sec("content", "Finn: o produto", inner, notes)


def s_spec() -> str:
    cells = "".join(
        f'<div class="units-tape__u"><span class="units-tape__id">{u}</span><span class="units-tape__n">{n}</span><span class="units-tape__i">issue {i}</span></div>'
        for u, n, i in UNITS
    )
    inner = head("A especificação", "Nove unidades em ordem de dependência, uma especificação congelada",
                 "cada unidade parte do que o agente construiu na anterior [77]")
    inner += f'<div class="units-tape reveal">{cells}</div>'
    inner += """
<div class="cards c3">
<div class="card reveal"><span class="card__k">Executor</span>Chama o <em>harness</em> uma vez por unidade, com o mesmo <em>prompt</em> nos dois braços. O autor não escreve código no espaço de trabalho.</div>
<div class="card reveal"><span class="card__k">Pontuação</span>Fração dos testes de aceitação aprovados. O autor escreve os testes antes da execução e os mantém fora do espaço de trabalho.</div>
<div class="card reveal"><span class="card__k">Unidade concluída</span>Quando todos os seus testes passam, rodados sobre uma cópia do espaço ao fim da unidade. Os testes do agente não contam.</div>
</div>"""
    inner += source("Projeto, §3 [77]–[78]. Ordem: #15 tenant, #16 governança, #17 flags, #14 pipeline de voz, #20 confirmação, #21 log, #19 relatório, #18 agendador, #22 cobrança.")
    notes = "<b>Especificação [77] e pontuação [78].</b> Especificação única, congelada por SHA-256, com a pilha e nove unidades em ordem de dependência. Os testes de aceitação são escritos antes da execução, ficam fora do espaço de trabalho e rodam sobre uma cópia ao fim de cada unidade; os testes escritos pelo agente não contam."
    return sec("content", "A especificação em 9 unidades", inner, notes)


def s_matriz() -> str:
    units = "".join(f'<span class="u">{u}</span>' for u, _, _ in UNITS)

    def cell(arm: str, tier: str) -> str:
        return f'<div class="cell cell--{arm} reveal"><div class="units">{units}</div><span class="n">{tier} · ao menos 3 construções válidas</span></div>'

    inner = head("Método · matriz", "Braço × nível, nove unidades por construção",
                 "dois níveis de modelo, primário e de robustez, ambos gratuitos no mesmo <em>gateway</em> (Opencode, 2026b) [79]")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1.5fr 1fr;align-items:start">
<div>
<div class="matrix">
<div></div><div class="mh pi">pi</div><div class="mh oc">OpenCode</div>
<div class="mh">nível primário</div>{cell("pi", "primário")}{cell("oc", "primário")}
<div class="mh">nível de robustez</div>{cell("pi", "robustez")}{cell("oc", "robustez")}
</div>
<div class="card reveal" style="margin-top:12px"><span class="tag tag--bad">não concluída</span> conta como resultado, com a fração de testes aprovada, e a construção segue. <span class="tag tag--mute">descartada</span> medição não confiável, como a troca do modelo servido no meio da coleta, descarta a construção inteira [84].</div>
</div>
<div class="cards" style="grid-template-columns:1fr">
<div class="card card--hi reveal"><span class="card__k">Braços</span>OpenCode e pi: código aberto, sem interface, URL base compatível com a API da OpenAI; versões fixadas no repositório [76].</div>
<div class="card reveal"><span class="card__k">Resultados por nível</span>Se a ordenação dos braços inverter de um nível para o outro, a inversão é reportada como resultado [79].</div>
</div>
</div>"""
    inner += source("Projeto, §3: braços [76], níveis [79], construções [82], classes [84]. Mediana e dispersão por célula [82].")
    notes = "<b>Braços [76], níveis [79], células [82], classes [84].</b> Cada combinação de braço e nível tem ao menos três construções completas válidas, relatadas em mediana e dispersão. Unidade não concluída conta como resultado; medição não confiável descarta a construção inteira."
    return sec("content", "Braços e matriz experimental", inner, notes)


def s_estatistica() -> str:
    inner = head("Método · métrica e teste", "Wilcoxon pareado por unidade, e a divisão que H2 pede",
                 "tokens sempre ao lado da fração de testes aprovados [71][83]")
    inner += """
<div class="cards c3" style="align-items:stretch">
<div class="card card--hi reveal"><span class="card__k">Métricas</span><span class="card__v">Tokens, testes aprovados, Succ/Mtok</span>Succ/Mtok: sucessos por milhão de tokens (Lin <em>et al.</em>, 2026).</div>
<div class="card reveal"><span class="card__k">Teste</span><span class="card__v">Wilcoxon dos postos sinalizados</span>Bilateral, α = 0,05, pareado por unidade, porque a dificuldade da unidade é a maior fonte de variação (Miller, 2024).</div>
<div class="card reveal"><span class="card__k">Para H2</span><span class="card__v">carga fixa + conversa</span>Tokens de cada unidade divididos em carga fixa (Camada 1 vezes o número de passos) e conversa. Predições registradas antes da coleta.</div>
</div>"""
    inner += source("Projeto, §2 [71] e §3 [83]. Miller (2024), arXiv:2411.00640, <em>preprint</em>.")
    notes = "<b>Métrica e estatística [71][83].</b> Wilcoxon dos postos sinalizados, bilateral, α = 0,05, sobre tokens, fração de testes aprovados e Succ/Mtok, pareado por unidade porque a dificuldade da unidade é a maior fonte de variação (Miller, 2024). Para H2: carga fixa (Camada 1 vezes o número de passos) e conversa. Predições registradas antes da coleta."
    return sec("content", "Métrica e teste pareado", inner, notes)


def s_limitacoes() -> str:
    inner = head("Limitações e ameaças à validade", "Quatro limitações", "declaradas no projeto [86]")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">O efeito depende do modelo</span>As conclusões valem por nível de modelo.</div>
<div class="card reveal"><span class="card__k">Um produto, uma pilha</span>O produto é um único SaaS em uma única pilha.</div>
<div class="card reveal"><span class="card__k">Unidades dependentes</span>Cada braço carrega os próprios erros de uma unidade à seguinte, e o Wilcoxon supõe independência. O valor-p será lido como indicativo, ao lado da diferença e da dispersão.</div>
<div class="card reveal"><span class="card__k">Nível gratuito</span>O <em>gateway</em> pode trocar o modelo ou cortar a cota durante a coleta.</div>
</div>"""
    inner += source("Projeto, §3, limitações e ameaças à validade [86].")
    notes = "<b>Limitações [86].</b> Quatro: o efeito do harness depende do modelo, então as conclusões valem por nível; um único SaaS numa única pilha; as unidades não são independentes, embora o Wilcoxon suponha que sejam, então o valor-p vale como indicativo, ao lado da diferença e da dispersão; o nível gratuito do gateway pode trocar o modelo ou cortar a cota."
    return sec("content", "Limitações", inner, notes)


# ---------------------------------------------------------------- orçamento, cronograma, referências

def s_orcamento() -> str:
    inner = head("Orçamento", "R$ 0,00",
                 "Tabela 1 do projeto: inferência, <em>harnesses</em> e máquinas sem custo")
    inner += """
<div class="slide__inner" style="grid-template-columns:1180px 1fr;align-items:end">
<div class="ledger reveal">
<div class="ledger__row"><span class="ledger__item">Inferência dos modelos<small>dois níveis, nível gratuito do <em>gateway</em> (Opencode, 2026b)</small></span><span class="ledger__dots"></span><span class="ledger__v">R$ 0,00</span></div>
<div class="ledger__row"><span class="ledger__item"><span><em>Harnesses</em> e ferramentas</span><small>código aberto</small></span><span class="ledger__dots"></span><span class="ledger__v">R$ 0,00</span></div>
<div class="ledger__row"><span class="ledger__item">Máquinas<small>estação pessoal NixOS e estação pessoal Windows</small></span><span class="ledger__dots"></span><span class="ledger__v">R$ 0,00<small>já disponíveis</small></span></div>
<div class="ledger__row ledger__row--total"><span class="ledger__item">Total</span><span class="ledger__dots"></span><span class="ledger__v">R$ 0,00</span></div>
</div>
<div class="card card--hi reveal"><span class="card__k">O risco do custo zero</span>O nível gratuito do <em>gateway</em> pode trocar o modelo ou cortar a cota durante a coleta [86].</div>
</div>"""
    inner += source("Projeto, §4, Tabela 1 [88]–[99].")
    notes = "<b>Orçamento [88]–[99]:</b> inferência R$ 0,00 (dois níveis, nível gratuito do gateway), harnesses e ferramentas de código aberto R$ 0,00, máquinas R$ 0,00 (já disponíveis). O risco está nas limitações [86]."
    return sec("dashboard", "Orçamento", inner, notes)


def s_cronograma() -> str:
    hdr = '<div></div>' + "".join(f'<div class="gh">{m}</div>' for m in GANTT_MONTHS)
    rows = []
    for phase, months in GANTT:
        # Cor separa leitura/escrita (ago–set) das fases do experimento (out–nov); nenhum status novo.
        run = any(months[2:])
        cells = []
        for j, on in enumerate(months):
            if not on:
                cells.append('<div class="gc"></div>')
                continue
            cls = ["gc", "on"]
            if j == 0 or not months[j - 1]:
                cls.append("start")
            if j == len(months) - 1 or not months[j + 1]:
                cls.append("end")
            if run:
                cls.append("run")
            cells.append(f'<div class="{" ".join(cls)}"></div>')
        rows.append(f'<div class="gp">{phase}</div>{"".join(cells)}')
    inner = head("Cronograma", "Ago. a nov. 2026",
                 "leitura e escrita em ago–set; <em>proxy</em> e testes em out–nov; matriz e análise em out")
    inner += f'<div class="gantt reveal">{hdr}{"".join(rows)}</div>'
    inner += '<div class="gantt-legend reveal"><span><i></i>leitura, escrita e revisão</span><span><i class="run"></i><span><em>proxy</em>, testes, execução e análise</span></span></div>'
    inner += source("Projeto, §5, Tabela 2 [101]–[157]. Revisão final e apresentação em setembro.")
    notes = "<b>Cronograma [101]–[157]:</b> ago–set leitura, tema e hipóteses, e toda a escrita; out–nov construção do proxy e dos testes; out execução da matriz e análise; revisão final e apresentação em set."
    return sec("content", "Cronograma", inner, notes)


def s_refs() -> str:
    inner = head("Referências", f"As {len(REFS)} entradas da seção 6",
                 "formato ABNT abreviado; endereços e datas de acesso na seção 6 do projeto")
    inner += '<div class="refs reveal">' + "".join(f"<p>{r}</p>" for r in REFS) + "</div>"
    notes = "<b>Referências [159]–[172].</b> Lista completa da seção 6. Preprints e blogues marcados como não revisados por pares. As normas ABNT e os manuais de metodologia não entram: a lista fica no tema."
    return sec("content", "Referências", inner, notes)


def s_fecho() -> str:
    inner = f"""
<div class="title-decor">{title_decor()}</div>
<div class="reveal">
<p class="slide__label">Pergunta que o projeto testa</p>
<h2 class="slide__display">Com o modelo fixo, o <em>harness</em> muda mais o custo do que o sucesso?</h2>
<div class="title-rule"></div>
<p class="end-thanks">Obrigado. Perguntas?</p>
<p class="end-links">github.com/YuukiFST/harness-bench (YuukiFST, 2026c)<br>github.com/YuukiFST/Finn (YuukiFST, 2026b)</p>
</div>"""
    notes = "<b>Fecho.</b> Retomar H1 [61] e o problema [48]: quanto mudam tokens e sucesso, e quanto da diferença de custo é carga fixa. Repositórios YuukiFST/Finn [170] e YuukiFST/harness-bench [171]."
    return sec("end", "Fecho", inner, notes)


DECK_SHORT = "O <em>harness</em> no custo e no desempenho"


def title_of(html: str) -> str:
    """Lê o data-title que sec() gravou; usado no índice das divisórias."""
    start = html.index('data-title="') + len('data-title="')
    return html[start:html.index('"', start)]


def with_folio(html: str, section: str, n: int, total: int) -> str:
    """Cabeço corrido (título curto + seção) e fólio n/total, como numa página impressa."""
    chrome = (
        f'<div class="folio-head" aria-hidden="true"><span>{DECK_SHORT}</span><span>{section}</span></div>'
        f'<div class="folio-num" aria-hidden="true">{n:02d}<span>/ {total}</span></div>'
    )
    cut = html.rindex("</section>")
    return html[:cut] + chrome + html[cut:]


def all_slides() -> str:
    # Mesma ordem do projeto (dist/projeto-de-pesquisa.docx): 1 Introdução, 2 Referencial teórico,
    # 3 Material e método, 4 Orçamento, 5 Cronograma, 6 Referências. Dentro de cada seção, a ordem
    # dos parágrafos [n] do dump (tools/docx_prose.py dump). A ordem e o total (27) casam com
    # dist/roteiro-apresentacao.html; mudar um exige mudar o outro.
    sections = [
        ("01", "Seção 1", "Introdução", "O mesmo modelo custa diferente conforme o <em>harness</em>: a justificativa, o problema, os objetivos e as hipóteses.",
         [s_justificativa(), s_tema(), s_problema(), s_objetivos(), s_hipoteses()]),
        ("02", "Seção 2", "Referencial teórico", "O que é um <em>harness</em>, o que as fontes dizem sobre sucesso e custo, e as duas pendências: de onde vem o custo e como medi-lo.",
         [s_anatomy(), s_sucesso(), s_pendencia_custo(), s_pendencia_medida()]),
        ("03", "Seção 3", "Material e método", "Classificação, uso de IA declarado, duas camadas de medição, o produto, a matriz, a estatística e as limitações.",
         [s_classificacao(), s_ia(), s_como(), s_camadas(), s_finn(), s_spec(), s_matriz(), s_estatistica(), s_limitacoes()]),
        ("04", "Seções 4, 5 e 6", "Orçamento, cronograma e referências", f"R$ 0,00, calendário de agosto a novembro e as {len(REFS)} referências da seção 6.",
         [s_orcamento(), s_cronograma(), s_refs()]),
    ]
    pages: list[tuple[str, str]] = [(s_capa(), "")]
    for num, kicker, heading, sub, body in sections:
        running = f"<b>{num}</b> · {heading}"
        pages.append((divider(num, kicker, heading, sub, [title_of(b) for b in body]), running))
        pages.extend((b, running) for b in body)
    pages.append((s_fecho(), ""))
    total = len(pages)
    return "\n".join(with_folio(html, running, n, total) for n, (html, running) in enumerate(pages, start=1))
