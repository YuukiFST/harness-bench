"""Slides do deck explicativo, um `<section class="slide">` por função.

Texto e números vêm só do projeto (dist/projeto-de-pesquisa.docx); cada slide de evidência
traz o denominador na linha de fonte. Notas do apresentador ficam em `<div class="notes">` e
aparecem com a tecla N; os índices [n] referem-se ao dump do .docx via
`python tools/docx_prose.py dump dist/projeto-de-pesquisa.docx` (versão do autor de 2026-09-24,
com tools/docx_edits_2026-09-24.py a 24f aplicados).
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
    SPEC_FLOW,
    UNIT_LABELS,
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
    sub_html = f'<p class="slide__subtitle">{sub}</p>' if sub else ""
    inner = (
        f'<span class="slide__number" aria-hidden="true">{num}</span>'
        f'<div class="reveal"><p class="divider-kicker">{kicker}</p><h2 class="slide__heading">{heading}</h2>'
        f'{sub_html}</div>{toc_html}'
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
<p class="title-sub">Tokens e taxa de sucesso com o mesmo modelo</p>
<div class="title-rule"></div>
<p class="title-who"><b>Fausto Yuuki T. A. Freire</b> · Orientadora: Profa. Inara Silva<br>
<span class="slide__subtitle">Projeto de pesquisa · Metodologia Científica · Cuiabá, 2026</span></p>
</div>"""
    notes = "<b>Capa [21]–[24].</b> Título: «O harness no custo e no desempenho de agentes de codificação: tokens e taxa de sucesso com o mesmo modelo» [22]. Projeto de pesquisa da disciplina de Metodologia Científica, curso de Sistemas para Internet, IFMT Campus Octayde Jorge da Silva [23]."
    return sec("title", "Capa", inner, notes)


def s_justificativa() -> str:
    inner = head("Justificativa", "Mesmo modelo, quase o mesmo sucesso, <em>cerca do dobro</em> do custo",
                 "HarnessTax (Pan <em>et al.</em>, 2026): sete modelos em três <em>harnesses</em>; no SWE-bench Lite, o Claude Fable 5 no Claude Code e no Pi")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1.3fr 1fr;align-items:stretch">
{figure(pair_bars(HARNESSTAX, "o Claude Code custa cerca do dobro por tentativa", "Claude Fable 5 · SWE-bench Lite · Pan et al. (2026)"), "Os mesmos números do projeto [43]: 97,8 % contra 96,7 % de sucesso, US$ 1,33 contra US$ 0,67 por tentativa.")}
<div class="cards" style="grid-template-columns:1fr;align-content:center">
<div class="card reveal"><span class="card__k">O que Pan <em>et al.</em> concluíram</span>A escolha do <em>harness</em> influencia notavelmente o custo.</div>
<div class="card card--hi reveal"><span class="card__k">Imposto do <em>harness</em></span>Quem paga por tokens paga também essa diferença.</div>
</div>
</div>"""
    inner += source("Pan <em>et al.</em> (2026), HarnessTax, Universidade da Califórnia em Berkeley; publicação de blogue de pesquisa, não revisada por pares. Projeto, §1 [43]–[44].")
    notes = "<b>Justificativa [43]–[44].</b> Um coding agent tem duas partes: o modelo de linguagem e o harness, o software ao redor dele que monta o contexto, expõe as ferramentas e conduz a execução [43]. Pan et al. (2026) avaliaram sete modelos em três harnesses e concluíram que a escolha do harness influencia notavelmente o custo; no SWE-bench Lite, o Claude Fable 5 resolve 97,8% no Claude Code e 96,7% no Pi, a US$ 1,33 contra US$ 0,67 por tentativa [43]. «Imposto do harness» é o termo dos autores, usado em [69]."
    return sec("chart", "Justificativa: o imposto do harness", inner, notes)


def s_tema() -> str:
    inner = head("Justificativa e tema", "O que falta medir: o <em>harness</em> num produto inteiro",
                 "as medições publicadas usam tarefas isoladas; os próprios autores pedem fluxos reais de desenvolvimento [44]")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">O limite das medições</span>Tarefas isoladas de <em>benchmarks</em> que os modelos podem ter visto no treino. O próximo passo, segundo os autores, é medir o <em>harness</em> em fluxos reais, com tarefas de várias sessões.</div>
<div class="card reveal"><span class="card__k">Tema</span>O efeito do <em>harness</em> sobre o custo e o desempenho de um modelo de linguagem fixo na construção de um produto de software completo.</div>
<div class="card card--hi reveal" style="grid-column:1/-1"><span class="card__k">O que este projeto faz [44]</span>Constrói o mesmo produto, o Finn, com o OpenCode e com o Pi, sobre o mesmo modelo e a mesma especificação, e conta os tokens fora do <em>harness</em>.</div>
</div>"""
    inner += source("Projeto, §1: justificativa [44], tema [46].")
    notes = "<b>Justificativa [44], tema [46].</b> Ler o tema na íntegra. Se perguntarem por que não deixar o OpenCode construir e gerar a especificação para o Pi: entrada desigual; a especificação sai do Finn de referência do autor e é a mesma para os dois coding agents [77]."
    return sec("content", "Justificativa e tema", inner, notes)


def s_problema() -> str:
    inner = """
<span class="quote-mark" aria-hidden="true">“</span>
<blockquote class="reveal">«Com o mesmo modelo, <b>quanto a escolha do <em>harness</em> influencia o custo e a taxa de sucesso</b> na construção do mesmo software?»</blockquote>
<cite class="reveal">Problema de pesquisa · Projeto, §1 [48]</cite>"""
    notes = "<b>Problema [48].</b> Ler na íntegra. H1 responde a ele; H2 e o objetivo geral acrescentam a parcela da carga fixa. Objetivo geral [50]: medir, com o mesmo modelo, a diferença de tokens e de taxa de sucesso atribuível ao harness na construção do mesmo produto a partir da mesma especificação, com o OpenCode e o Pi como coding agents, e separar a parcela que vem da carga fixa por requisição."
    return sec("quote", "Problema de pesquisa", inner, notes)


def s_objetivos() -> str:
    inner = head("Objetivos", "Um objetivo geral, seis específicos",
                 "medir, com o mesmo modelo, a diferença de tokens e de sucesso atribuível ao <em>harness</em>, com o OpenCode e o Pi como <em>coding agents</em>, e separar a parcela da carga fixa por requisição [50]")
    trs = "".join(
        f'<tr><td class="n">{i+1}</td><td class="k">{k}</td><td class="d">{d}</td></tr>'
        for i, (k, d) in enumerate(OBJECTIVES)
    )
    inner += f'<div class="table-wrap reveal"><table class="data"><tbody>{trs}</tbody></table></div>'
    inner += source("Projeto, §1: objetivo geral [50], objetivos específicos [52]–[57].")
    notes = "<b>Objetivos específicos [52]–[57].</b> 1 construir o proxy que conta requisições, tokens e latência por coding agent; 2 construir o Finn de referência e extrair dele a especificação e os testes; 3 construir o Finn nos dois harnesses, com o mesmo modelo, prompt e espaço inicial; 4 repetir em um segundo modelo e verificar se a ordenação dos coding agents se mantém; 5 comparar os tokens relatados por cada harness com os medidos no proxy; 6 publicar executor, prompts, testes, dados e scripts de análise."
    return sec("table", "Objetivos", inner, notes)


def s_hipoteses() -> str:
    inner = head("Hipóteses", "H1: o <em>harness</em> muda mais o custo do que o sucesso. H2: a maior parte é carga fixa",
                 "as duas com critério de refutação declarado [61][62]")
    inner += """
<div class="cards c2" style="align-items:stretch">
<div class="card card--hi reveal"><span class="card__k">H1</span>Com o modelo fixo, os tokens por unidade diferem entre o OpenCode e o Pi, e a fração de testes aprovados fica igual.<br><span class="mute">Refutada se o teste pareado não apontar diferença de tokens ou se as medianas da fração final de testes aprovados diferirem entre os <em>coding agents</em>.</span></div>
<div class="card card--hi reveal"><span class="card__k">H2</span>A carga fixa por requisição (<em>system prompt</em> e esquemas de ferramenta) explica a maior parte da diferença de tokens; o número de passos, a menor.<br><span class="mute">Refutada se os passos ou o conteúdo da conversa explicarem a maior parte.</span></div>
</div>"""
    inner += source("Projeto, §1, hipóteses [61]–[62].")
    notes = "<b>Hipóteses [61][62].</b> H1: com o modelo fixo, o harness muda mais o custo do que o sucesso; refutada se o teste pareado não apontar diferença de tokens ou se as medianas da fração final de testes aprovados diferirem entre os coding agents. H2: carga fixa contra passos e conversa; refutada se os passos ou o conteúdo da conversa explicarem a maior parte. As predições são registradas antes da coleta [83]."
    return sec("content", "Hipóteses H1 e H2", inner, notes)


# ---------------------------------------------------------------- referencial

def s_anatomy() -> str:
    inner = head("Definição", "O que é um <em>harness</em>",
                 "os componentes externos ao modelo e editáveis que o cercam (Lin <em>et al.</em>, 2026, p. 1)")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1fr 1.15fr">
<div class="slide__aside reveal">{harness_anatomy()}</div>
<div>
<ul class="slide__bullets">
<li class="reveal"><b>Ning <em>et al.</em> (2026, p. 7)</b> · um <em>harness</em> «converte um modelo de linguagem sem estado em um agente funcional ao ancorar suas saídas em execução externa, estado persistente e realimentação verificável».</li>
<li class="reveal"><b>Lin <em>et al.</em> (2026, p. 1)</b> · o <em>system prompt</em>, as ferramentas que expõem o sistema de arquivos e o shell, e o <em>middleware</em> que controla contexto, execução e recuperação.</li>
<li class="reveal"><b>Neste projeto</b> · só esse conjunto varia. O Pi envia quatro ferramentas e um <em>system prompt</em> curto; o OpenCode, mais ferramentas, subagentes e permissões (Earendil, 2026; Opencode, 2026a).</li>
</ul>
</div>
</div>"""
    inner += source("Ning <em>et al.</em> (2026, p. 7); Lin <em>et al.</em> (2026, p. 1). <em>Preprints</em>, não revisados por pares. Projeto, §2 [65]–[67].")
    notes = "<b>Referencial [65]–[67].</b> Ning et al. (2026, p. 7): definição citada [65]. Lin et al. (2026, p. 1): citação longa [66], o conjunto de componentes externos ao modelo e editáveis. [67]: só esse conjunto varia entre os coding agents; o Pi envia quatro ferramentas e um system prompt curto, o OpenCode mais ferramentas, subagentes e permissões (Earendil, 2026; Opencode, 2026a). O proxy fica fora do harness e conta igual para os dois coding agents [59]."
    return sec("content", "O que é um harness", inner, notes)


def s_sucesso() -> str:
    inner = head("Referencial · sucesso", "O <em>harness</em> muda o sucesso? As fontes divergem",
                 "por isso este projeto mede sucesso e custo juntos [68]")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1fr 1fr;align-items:stretch">
{figure(vbars(LIN_T1, " %", 80, "Aprovação de harnesses escritos por humanos no Terminal-Bench 2"), "<b>Lin <em>et al.</em> (2026), Tabela 1:</b> <em>harnesses</em> escritos por humanos, Terminal-Bench 2.")}
<div class="cards" style="grid-template-columns:1fr;align-content:center">
<div class="card reveal"><span class="card__k">Zhang <em>et al.</em> (2026)</span>Em tarefas longas e entre modelos de fronteira comparáveis, a variação de desempenho devida ao <em>harness</em> é frequentemente comparável ou maior que a devida ao modelo.</div>
<div class="card reveal"><span class="card__k">Pan <em>et al.</em> (2026) · SWE-bench Lite</span><span class="card__v num">efeito médio de ±2 % no sucesso</span>O Claude Code custou, em média, cerca de 2,0 vezes o Pi.</div>
</div>
</div>"""
    inner += source("Lin <em>et al.</em> (2026) e Zhang <em>et al.</em> (2026), <em>preprints</em>; Pan <em>et al.</em> (2026), blogue de pesquisa. Projeto, §2 [68].")
    notes = "<b>Referencial [68].</b> Lin et al. (2026), Tabela 1: harnesses escritos por humanos vão de 47,2% no OpenCode a 71,9% no Codex, no Terminal-Bench 2. Zhang et al. (2026): em tarefas longas e entre modelos de fronteira comparáveis, a variação de desempenho devida ao harness é frequentemente comparável ou maior que a devida ao modelo. Pan et al. (2026) mediram outra coisa: efeito médio do harness sobre o sucesso dentro de ±2%, custo do Claude Code, em média, cerca de 2,0 vezes o do Pi. Como as fontes divergem sobre o sucesso, o projeto mede os dois."
    return sec("chart", "Sucesso: as fontes divergem", inner, notes)


def s_pendencia_custo() -> str:
    inner = head("Referencial · primeira pendência", "De onde vem a diferença de custo?",
                 "Pan <em>et al.</em> apontam a primeira requisição como possível origem; Liu <em>et al.</em>, o resto da conversa [69]")
    inner += """
<div class="cards c2" style="align-items:stretch">
<div class="card reveal"><span class="card__k">Pan <em>et al.</em> (2026) · a primeira requisição</span><span class="card__v num">mais de 10× o contexto inicial</span>Nos sete modelos, o contexto inicial médio do Claude Code passa de dez vezes o do Pi; no Claude Fable 5 os turnos quase se igualam: 15,3 contra 15,4.</div>
<div class="card reveal"><span class="card__k">Liu <em>et al.</em> (2026) · SoL-Pi · a conversa</span><span class="card__v num">44,7 % a 49,0 % menos tokens</span>Mudando só a execução das ações, a compactação de contexto, o tratamento das observações e a leitura delegada, em relação ao Pi, com 93,7 % a 94,3 % da pontuação dele.</div>
<div class="card card--hi reveal" style="grid-column:1/-1"><span class="card__k">O que H2 testa</span>Ning <em>et al.</em> (2026, p. 66) pedem «métricas que isolem componentes do <em>harness</em>». H2 testa se pesa mais a carga fixa ou a conversa.</div>
</div>"""
    inner += source("Pan <em>et al.</em> (2026), blogue de pesquisa; Liu <em>et al.</em> (2026), arXiv:2609.20519, <em>preprint</em>; Ning <em>et al.</em> (2026), <em>preprint</em>. Projeto, §2 [69].")
    notes = "<b>Primeira pendência [69].</b> Pan: o imposto do harness pode começar na primeira requisição; nos sete modelos, o contexto inicial médio do Claude Code passa de dez vezes o do Pi, com 15,3 contra 15,4 turnos no Claude Fable 5. Liu (SoL-Pi): mudando só a execução das ações, a compactação, o tratamento das observações e a leitura delegada, de 44,7% a 49,0% menos tokens que o Pi, mantendo de 93,7% a 94,3% da pontuação dele. Ning (p. 66) pede métricas que isolem componentes; H2 responde a isso."
    return sec("content", "Primeira pendência: o custo", inner, notes)


def s_pendencia_medida() -> str:
    inner = head("Referencial · segunda pendência e métricas", "Contar do mesmo jeito nos dois <em>coding agents</em>",
                 "cada <em>harness</em> conta turnos e tokens do seu jeito; aqui a medição ocorre num <em>proxy</em> externo [70]")
    inner += """
<div class="cards c3" style="align-items:stretch">
<div class="card reveal"><span class="card__k">Instrumentação [70]</span>Pan <em>et al.</em> (2026) registram que a definição de turno varia entre os <em>harnesses</em>. O <em>proxy</em> é igual para os dois <em>coding agents</em>, e o objetivo (5) compara essa medida com o relato de cada <em>harness</em>.</div>
<div class="card reveal"><span class="card__k">Métricas [71]</span>Tokens por construção, ao lado da fração de testes aprovados, e o Succ/Mtok (sucessos por milhão de tokens) de Lin <em>et al.</em> (2026).</div>
<div class="card card--hi reveal"><span class="card__k">Dois níveis de modelo [71]</span>O efeito depende do modelo: em nove de doze comparações de Pan <em>et al.</em> (2026), o maior sucesso veio de um <em>harness</em> que não é o do fornecedor do modelo.</div>
</div>"""
    inner += source("Projeto, §2 [70]–[71].")
    notes = "<b>Segunda pendência [70] e métricas [71].</b> Cada harness conta turnos e tokens do seu jeito, e Pan et al. registram que a definição de turno varia; o proxy externo é igual para os dois coding agents e o objetivo (5) compara a medida com o relato. Métricas: tokens por construção ao lado da fração de testes aprovados, e o Succ/Mtok de Lin et al. Nove de doze comparações de Pan: o maior sucesso veio de um harness que não é o do fornecedor do modelo; daí os dois níveis de modelo."
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
    notes = "<b>Classificação [59][73].</b> Aplicada quanto à finalidade, quali-quantitativa quanto à abordagem, exploratória quanto aos objetivos, experimental quanto aos procedimentos e dedutiva quanto ao método. Exploratória porque não se encontrou comparação publicada de harnesses construindo o mesmo produto completo."
    return sec("table", "Classificação da pesquisa", inner, notes)


def s_ia() -> str:
    inner = head("Uso de IA declarado", "O Claude Code ajuda nas fontes e no Finn; o autor confere e responde",
                 "ferramenta declarada: Claude Code, no levantamento das fontes, nas decisões do Finn e na sua versão de referência [74]")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">Levantamento das fontes · <em>LLM Wiki</em> (Karpathy, 2026)</span>
<ol class="card__steps">
<li><b>Levantamento</b> organizado pelo método <em>LLM Wiki</em> no repositório do projeto (YuukiFST, 2026c).</li>
<li><b>O autor confere</b> cada afirmação citada na obra.</li>
</ol></div>
<div class="card reveal"><span class="card__k">Finn · Helmsman (YuukiFST, 2026a)</span>
<ol class="card__steps">
<li><b>O Finn</b> foi decidido em 24 <em>tickets</em>, mapeados com o Helmsman.</li>
<li><b>O que o sistema faz</b>: o autor decide e responde pelas decisões de produto.</li>
<li><b>Versão de referência</b> do Finn, da qual sai a especificação dos dois <em>coding agents</em>.</li>
</ol></div>
</div>"""
    inner += source("Projeto, §3 [74] e [77] (Karpathy, 2026; YuukiFST, 2026a, 2026c).")
    notes = "<b>Uso de IA [74].</b> Declara-se o uso do Claude Code no levantamento das fontes, organizado pelo método LLM Wiki de Karpathy (2026) no repositório do projeto (YuukiFST, 2026c), nas decisões do Finn, mapeadas com o Helmsman (YuukiFST, 2026a), e na sua versão de referência. O autor conferiu cada afirmação citada na obra e responde pelo texto e pelas decisões de produto. Os 24 tickets estão em [77]."
    return sec("content", "Uso de IA declarado", inner, notes)


def s_como() -> str:
    steps = [
        ("01 · UMA ESPECIFICAÇÃO", "Do Finn de referência", "O autor constrói o Finn antes. Dele sai a especificação, congelada por SHA-256, com uma unidade por etapa.", "congelada · SHA-256"),
        ("02 · DOIS HARNESSES", "OpenCode e Pi", "Mesmo modelo, mesmo <em>prompt</em>, mesmo espaço de trabalho inicial; cada <em>coding agent</em> constrói do zero.", "opencode run · pi --mode json"),
        ("03 · UM CONTADOR EXTERNO", "<em>Proxy</em> reverso", "Entre o <em>harness</em> e o modelo, guarda requisições, latência e os tokens que o <em>gateway</em> informa, da mesma forma para os dois.", "proxy · usage do gateway"),
        ("04 · UM CRITÉRIO", "Tokens ao lado do sucesso", "Tokens e Succ/Mtok no Wilcoxon pareado por unidade; a fração de testes aprovados sempre ao lado.", "Wilcoxon · Succ/Mtok"),
    ]
    inner = head("Como o projeto funciona", "O mesmo produto, construído duas vezes", "cada <em>coding agent</em> constrói o Finn do zero ao menos três vezes [59]")
    inner += pipeline(steps)
    inner += source("Projeto, §1 [59] e §3 [75]–[83]. Coding agents: OpenCode (Opencode, 2026a) e Pi (Earendil, 2026). Nenhum código do autor entra no espaço de trabalho [77].")
    notes = "<b>Como o projeto funciona [59][75]–[83].</b> Dizer a ordem: especificação, dois coding agents do zero, proxy, critério. Camadas, matriz e limite vêm nos slides seguintes."
    return sec("content", "Como o projeto funciona", inner, notes)


def s_camadas() -> str:
    inner = head("Método · instrumento", "Duas camadas de medição, um <em>proxy</em>",
                 "a Camada 1 mede a carga fixa de cada <em>coding agent</em> sem tarefa; a Camada 2 mede a construção contra o modelo real [75]")
    inner += figure(layers_flow(), "")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">Camada 1</span>Contra um <em>endpoint</em> simulado, mede os esquemas de ferramenta, o <em>system prompt</em> e os tokens de cada requisição.</div>
<div class="card reveal"><span class="card__k">Limite único</span>Tempo de relógio por unidade, de três vezes a maior mediana dos <em>coding agents</em> nas unidades-piloto. Sem teto de passos: um teto seria decisão de projeto de <em>harness</em> [81].</div>
</div>"""
    inner += source("O <em>proxy</em> guarda os tokens que o <em>gateway</em> informa em cada resposta, com o cache à parte, e separa em cada requisição a carga fixa do resto da conversa; a contagem do <em>harness</em> serve só para verificação cruzada [80].")
    notes = "<b>Método [75][80][81].</b> Camada 1: endpoint simulado, esquemas, system prompt e tokens por requisição; é a carga fixa de cada coding agent sem tarefa. Camada 2: construção contra o modelo real. O proxy guarda os tokens que o gateway informa, com o cache à parte, e separa a carga fixa do resto da conversa em cada requisição, para H2 [80]. Limite único: três vezes a maior mediana dos coding agents nas unidades-piloto; o número de passos fica livre [81]."
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
<div class="card card--hi reveal"><span class="card__k">Decidido em 24 <em>tickets</em></span>A especificação, tirada da versão de referência, traz o produto, a pilha, a interface dos testes e as funcionalidades em JSON.</div>"""
    inner += source("Finn (YuukiFST, 2026b): github.com/YuukiFST/Finn. Fluxo de voz: Finn, <em>issue</em> #14 (produto, não unidade). Projeto, §3 [77].")
    notes = "<b>Finn (YuukiFST, 2026b) [77].</b> SaaS multiempresa de financeiro por voz, decidido em 24 tickets. Da versão de referência sai a especificação: produto, pilha, interface dos testes e funcionalidades em JSON, no formato de Young (2025). Ponto a dizer: as medições publicadas usam tarefas isoladas [44]; aqui o agente constrói um produto inteiro."
    return sec("content", "Finn: o produto", inner, notes)


def s_spec() -> str:
    cells = "".join(
        f'<div class="units-tape__u"><span class="units-tape__id">{k}</span><span class="units-tape__n">{n}</span><span class="units-tape__i">{d}</span></div>'
        for k, n, d in SPEC_FLOW
    )
    inner = head("A especificação", "A especificação sai do Finn de referência",
                 "cada unidade parte do que o agente construiu na anterior [77]")
    inner += f'<div class="units-tape units-tape--flow reveal">{cells}</div>'
    inner += """
<div class="cards c3">
<div class="card reveal"><span class="card__k">Executor</span>Chama o <em>harness</em> uma vez por unidade, com o mesmo <em>prompt</em> nos dois <em>coding agents</em>. Nenhum código do autor entra no espaço de trabalho.</div>
<div class="card reveal"><span class="card__k">Pontuação</span>Fração dos testes de aceitação aprovados, escritos pelo autor antes da execução e fora do espaço de trabalho. Os testes do agente não contam.</div>
<div class="card card--hi reveal"><span class="card__k">Validados na referência</span>Todos os testes devem passar antes na referência, no marco da etapa. A unidade é concluída quando todos os seus passam.</div>
</div>"""
    inner += source("Projeto, §3 [77]–[78]. O número de unidades sai das etapas da referência.")
    notes = "<b>Especificação [77] e pontuação [78].</b> O autor constrói antes uma versão de referência do Finn e marca no git o fim de cada etapa. Dela sai a especificação, congelada por SHA-256: produto, pilha, interface dos testes e funcionalidades em JSON, uma unidade por etapa, ao menos seis. Os testes de aceitação são escritos antes da execução, ficam fora do espaço de trabalho, rodam sobre uma cópia ao fim de cada unidade e devem passar antes na referência, no marco da etapa; os testes escritos pelo agente não contam."
    return sec("content", "A especificação e as unidades", inner, notes)


def s_matriz() -> str:
    units = "".join(f'<span class="u">{u}</span>' for u in UNIT_LABELS)

    def cell(arm: str, tier: str) -> str:
        return f'<div class="cell cell--{arm} reveal"><div class="units">{units}</div><span class="n">{tier} · ao menos 3 construções válidas</span></div>'

    inner = head("Método · matriz", "<em>Coding agent</em> × nível, ao menos seis unidades por construção",
                 "dois níveis de modelo, primário e de robustez, ambos gratuitos no mesmo <em>gateway</em> (Opencode, 2026b) [79]")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1.5fr 1fr;align-items:start">
<div>
<div class="matrix">
<div></div><div class="mh pi">Pi</div><div class="mh oc">OpenCode</div>
<div class="mh">nível primário</div>{cell("pi", "primário")}{cell("oc", "primário")}
<div class="mh">nível de robustez</div>{cell("pi", "robustez")}{cell("oc", "robustez")}
</div>
<div class="card reveal" style="margin-top:12px"><span class="tag tag--bad">não concluída</span> conta como resultado, com a fração de testes aprovados, e a construção segue. <span class="tag tag--mute">descartada</span> medição não confiável, como a troca do modelo servido no meio da coleta, descarta a construção inteira [84].</div>
</div>
<div class="cards" style="grid-template-columns:1fr">
<div class="card card--hi reveal"><span class="card__k"><em>Coding agents</em></span>OpenCode e Pi: código aberto; versões fixadas e registradas no repositório (YuukiFST, 2026c) [76].</div>
<div class="card reveal"><span class="card__k">Resultados por nível</span>Se a ordenação dos <em>coding agents</em> inverter de um nível para o outro, a inversão é reportada como resultado [79].</div>
</div>
</div>"""
    inner += source("Projeto, §3: coding agents [76], níveis [79], construções [82], classes [84]. Mediana e dispersão por célula [82].")
    notes = "<b>Coding agents [76], níveis [79], células [82], classes [84].</b> Cada combinação de coding agent e nível tem ao menos três construções completas válidas, relatadas em mediana e dispersão. Unidade não concluída conta como resultado; medição não confiável descarta a construção inteira."
    return sec("content", "Coding agents e matriz experimental", inner, notes)


def s_estatistica() -> str:
    inner = head("Método · medição e teste", "Como os tokens são contados e comparados",
                 "medir, resumir, comparar e explicar, nesta ordem [71][80][83]")
    inner += """
<div class="cards c2" style="align-items:stretch">
<div class="card card--hi reveal"><span class="card__k">1 · Medir</span><span class="card__v">O <em>gateway</em> conta</span>O <em>proxy</em> guarda os tokens que o <em>gateway</em> informa em cada resposta (entrada, cache e saída) e soma por unidade e por construção [80].</div>
<div class="card reveal"><span class="card__k">2 · Resumir</span><span class="card__v">Tokens por construção</span>Mediana das construções de cada <em>coding agent</em> (ao menos três) [82]. Succ/Mtok: sucessos por milhão de tokens (Lin <em>et al.</em>, 2026) [71].</div>
<div class="card reveal"><span class="card__k">3 · Comparar</span><span class="card__v">Razão das medianas</span>Wilcoxon pareado por unidade, bilateral, α = 0,05, sobre tokens e Succ/Mtok (Miller, 2024). A fração de testes aprovados é relatada sem teste [83].</div>
<div class="card reveal"><span class="card__k">4 · Explicar (H2)</span><span class="card__v">Carga fixa e conversa</span>Em cada requisição, o <em>proxy</em> separa o <em>system prompt</em> e as ferramentas do resto da conversa [80].</div>
</div>"""
    inner += source("Projeto, §2 [71] e §3 [80], [83]. Miller (2024), arXiv:2411.00640, <em>preprint</em>. Predições registradas antes da coleta.")
    notes = "<b>Medição e estatística [71][80][83].</b> 1) O proxy guarda o usage do gateway em cada resposta: entrada, cache e saída; soma por unidade e por construção. A contagem do harness serve só para verificação cruzada. 2) Tokens por construção, mediana de três; Succ/Mtok = sucessos ÷ milhões de tokens. 3) Wilcoxon pareado por unidade sobre tokens e Succ/Mtok; o resultado principal é a razão entre as medianas de tokens por construção dos coding agents; a fração de testes aprovados vai sem teste, porque um empate em 100% não deixa diferença. 4) H2: em cada requisição, system prompt e ferramentas separados do resto da conversa. Predições registradas antes da coleta."
    return sec("content", "Como os tokens são contados e comparados", inner, notes)


def s_limitacoes() -> str:
    inner = head("Limitações e ameaças à validade", "Quatro limitações", "declaradas no projeto [86]")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">O efeito depende do modelo</span>As conclusões valem por nível de modelo.</div>
<div class="card reveal"><span class="card__k">Um produto, a solução do autor</span>O produto é um único SaaS, especificado a partir da solução do autor.</div>
<div class="card reveal"><span class="card__k">Unidades dependentes</span>Cada <em>coding agent</em> carrega os próprios erros de uma unidade à seguinte, e o Wilcoxon supõe independência. O valor-p será lido como indicativo, ao lado da diferença e da dispersão.</div>
<div class="card reveal"><span class="card__k">Nível gratuito</span>O <em>gateway</em> pode trocar o modelo ou cortar a cota durante a coleta.</div>
</div>"""
    inner += source("Projeto, §3, limitações e ameaças à validade [86].")
    notes = "<b>Limitações [86].</b> Quatro: o efeito do harness depende do modelo, então as conclusões valem por nível; um único SaaS, especificado a partir da solução do autor; as unidades não são independentes, embora o Wilcoxon suponha que sejam, então o valor-p vale como indicativo, ao lado da diferença e da dispersão; o nível gratuito do gateway pode trocar o modelo ou cortar a cota."
    return sec("content", "Limitações", inner, notes)


# ---------------------------------------------------------------- orçamento, cronograma, referências

def s_orcamento() -> str:
    inner = head("Orçamento", "R$ 0,00",
                 "Tabela 1 do projeto: inferência, <em>harnesses</em> e hardware sem custo")
    inner += """
<div class="slide__inner" style="grid-template-columns:1180px 1fr;align-items:end">
<div class="ledger reveal">
<div class="ledger__row"><span class="ledger__item">Inferência dos modelos<small>dois níveis, nível gratuito do <em>gateway</em> (Opencode, 2026b)</small></span><span class="ledger__dots"></span><span class="ledger__v">R$ 0,00</span></div>
<div class="ledger__row"><span class="ledger__item"><span><em>Harnesses</em> e ferramentas</span><small>código aberto</small></span><span class="ledger__dots"></span><span class="ledger__v">R$ 0,00</span></div>
<div class="ledger__row"><span class="ledger__item">Hardware<small>PC pessoal, NixOS</small></span><span class="ledger__dots"></span><span class="ledger__v">R$ 0,00</span></div>
<div class="ledger__row ledger__row--total"><span class="ledger__item">Total</span><span class="ledger__dots"></span><span class="ledger__v">R$ 0,00</span></div>
</div>
<div class="card card--hi reveal"><span class="card__k">O risco do custo zero</span>O nível gratuito do <em>gateway</em> pode trocar o modelo ou cortar a cota durante a coleta [86].</div>
</div>"""
    inner += source("Projeto, §4, Tabela 1 [88]–[99].")
    notes = "<b>Orçamento [88]–[99]:</b> inferência R$ 0,00 (dois níveis, nível gratuito do gateway), harnesses e ferramentas de código aberto R$ 0,00, hardware R$ 0,00 (PC pessoal, NixOS). O risco está nas limitações [86]."
    return sec("dashboard", "Orçamento", inner, notes)


def s_cronograma() -> str:
    hdr = '<div></div>' + "".join(f'<div class="gh">{m}</div>' for m in GANTT_MONTHS)
    rows = []
    for phase, months in GANTT:
        # Cor separa leitura/escrita (ago–set) das fases do experimento (out em diante); nenhum status novo.
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
    inner = head("Cronograma", "Agosto a outubro",
                 "leitura e escrita em ago–set; Finn de referência, <em>proxy</em>, testes, matriz e análise em out")
    inner += f'<div class="gantt reveal">{hdr}{"".join(rows)}</div>'
    inner += '<div class="gantt-legend reveal"><span><i></i>leitura, escrita e revisão</span><span><i class="run"></i><span>referência, <em>proxy</em>, testes, execução e análise</span></span></div>'
    inner += source("Projeto, §5, Tabela 2 [101]–[146]. Revisão final e apresentação em setembro.")
    notes = "<b>Cronograma [101]–[146]:</b> três meses, de agosto a outubro. Ago–set: leitura, tema e hipóteses, e toda a escrita. Out: Finn de referência, proxy e testes, execução da matriz e análise. Revisão final e apresentação em set."
    return sec("content", "Cronograma", inner, notes)


def s_refs() -> str:
    inner = head("Referências", f"As {len(REFS)} entradas da seção 6")
    inner += '<div class="refs reveal">' + "".join(f"<p>{r}</p>" for r in REFS) + "</div>"
    notes = "<b>Referências [147]–[161].</b> Lista completa da seção 6. Preprints e blogues marcados como não revisados por pares. As normas ABNT e os manuais de metodologia não entram: a lista fica no tema."
    return sec("content", "Referências", inner, notes)


def s_fecho() -> str:
    inner = f"""
<div class="title-decor">{title_decor()}</div>
<div class="reveal">
<p class="slide__label">Por que isso importa</p>
<h2 class="slide__display">Conhecer o modelo não basta: o <em>harness</em> tem grande influência no custo</h2>
<p class="title-sub">No mercado atual, quem desenvolve com agentes precisa entender os dois: o modelo que gera e o <em>harness</em> que o envolve</p>
<div class="title-rule"></div>
<p class="end-links">github.com/YuukiFST/harness-bench (YuukiFST, 2026c)<br>github.com/YuukiFST/Finn (YuukiFST, 2026b)</p>
</div>"""
    notes = "<b>Fecho.</b> H1 [61] testa se, com o modelo fixo, o harness muda mais o custo do que o sucesso (problema [48]); quem paga por tokens paga também essa diferença [44]. Na prática: escolher o modelo sem olhar o harness é orçar pela metade. Repositórios YuukiFST/Finn [159] e YuukiFST/harness-bench [160]."
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
        ("04", "Seções 4, 5 e 6", "Orçamento, cronograma e referências", "",
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
