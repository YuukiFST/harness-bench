"""Slides do deck explicativo, um `<section class="slide">` por função.

Texto e números vêm do projeto (dist/projeto-de-pesquisa.docx, deck/src/content.ts) e das
páginas de fonte da wiki; cada slide de evidência traz o denominador na linha de fonte.
Notas do apresentador ficam em `<div class="notes">` e aparecem com a tecla N; os índices [n]
referem-se ao dump do .docx via `python tools/docx_prose.py dump`.
"""

from __future__ import annotations

from charts import (
    dumbbell,
    fmt,
    fmt_int,
    frontier_scatter,
    harness_anatomy,
    hbars,
    layers_flow,
    pair_bars,
    title_decor,
    vbars,
)
from content import (
    ALIER,
    CLASS_AXES,
    FINN_PIPELINE,
    FRONTIER,
    GANTT,
    GANTT_MONTHS,
    HAL,
    LAYER1,
    LEE,
    LIN_SWE,
    LIN_T1,
    OBJECTIVES,
    REFS,
    TIMELINE_A,
    TIMELINE_B,
    UNITS,
)


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


def divider(num: str, kicker: str, heading: str, sub: str) -> str:
    inner = (
        f'<span class="slide__number" aria-hidden="true">{num}</span>'
        f'<div class="reveal"><p class="divider-kicker">{kicker}</p><h2 class="slide__heading">{heading}</h2>'
        f'<p class="slide__subtitle">{sub}</p></div>'
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


# ---------------------------------------------------------------- capa e problema

def s_capa() -> str:
    inner = f"""
<div class="title-decor">{title_decor()}</div>
<div class="reveal">
<p class="title-inst">Instituto Federal de Mato Grosso · Campus Octayde Jorge da Silva · Sistemas para Internet</p>
<h1 class="slide__display">Como o <em>harness</em> altera o custo e o desempenho do modelo</h1>
<div class="title-rule"></div>
<p class="title-who"><b>Fausto Yuuki T. A. Freire</b> · Orientadora: Profa. Inara Silva<br>
<span class="slide__subtitle">Projeto de pesquisa · Metodologia Científica · Cuiabá, 2026</span></p>
</div>"""
    notes = "<b>Capa.</b> Título, autor e orientadora [21][22][24]. Projeto de pesquisa da disciplina de Metodologia Científica, curso de Sistemas para Internet, IFMT Campus Octayde Jorge da Silva [23]. Deck explicativo: mesma fala, gráficos das fontes do projeto."
    return sec("title", "Capa", inner, notes)


def s_kpis() -> str:
    inner = head("O problema em uma tela", "Mesmo modelo, custo por tarefa aprovada de <em>US$ 1,05 a US$ 18,34</em>",
                 "FrontierHarness (Runta, 2026): 12 configurações de 9 <em>harnesses</em>, modelo Kimi K3, 30 tarefas, 1 tentativa por célula, set. 2026")
    inner += """
<div class="kpis">
<div class="kpi reveal"><div class="kpi__v">12</div><div class="kpi__l">configurações</div><div class="kpi__d">9 <em>harnesses</em> sobre o mesmo modelo, mesmas 30 tarefas, mesmo gateway</div></div>
<div class="kpi reveal"><div class="kpi__v kpi__v--long">50,0–66,7 %</div><div class="kpi__l">taxa de aprovação</div><div class="kpi__d">17 pontos percentuais entre a pior e a melhor configuração</div></div>
<div class="kpi reveal"><div class="kpi__v kpi__v--long">US$ 1,05–18,34</div><div class="kpi__l">custo por tarefa aprovada</div><div class="kpi__d">mediana por configuração; o modelo não mudou, só o <em>harness</em></div></div>
<div class="kpi reveal"><div class="kpi__v">5,6×</div><div class="kpi__l">mesmo pass, outro custo</div><div class="kpi__d">Claude Code e DSH Creator aprovam as mesmas 19 tarefas; razão declarada no post</div></div>
</div>
<div class="cards c2">
<div class="card card--pi reveal"><span class="card__k">pi · braço deste projeto</span><span class="card__v num">60,0 % · US$ 2,43</span><span class="mute">4 ferramentas, prompt de sistema abaixo de 1.000 tokens (Earendil, 2026)</span></div>
<div class="card card--oc reveal"><span class="card__k">OpenCode · braço deste projeto</span><span class="card__v num">50,0 % · US$ 3,24</span><span class="mute">planejamento, compactação, subagentes e permissões</span></div>
</div>"""
    inner += source("Runta (2026), blogue institucional, não revisado por pares; tabela «Pass Rate / Median Cost Per Pass». Quem paga é o desenvolvedor, na assinatura, e a empresa, em escala [44].")
    notes = "<b>Justificativa [43].</b> «No FrontierHarness (Runta, 2026), doze configurações de nove harnesses sobre o mesmo modelo ficam entre 50,0% e 66,7% de aprovação, e o custo por tarefa concluída vai de US$ 1,05 a US$ 18,34.» Os dois braços deste projeto estão no mesmo post: pi 60,0% a US$ 2,43, OpenCode 50,0% a US$ 3,24 [43]. Também [69]: Codex 66,7% a US$ 3,47; Claude Code 63,3% a US$ 18,34 (5,3x). Quem paga é o desenvolvedor e a empresa [44]."
    return sec("dashboard", "O problema em números", inner, notes)


def s_frontier() -> str:
    inner = head("A mesma tabela, em duas dimensões", "Passar e passar barato são habilidades separadas",
                 "cada ponto é um <em>harness</em> (ou configuração) sobre o mesmo Kimi K3; para a direita, mais caro; para cima, mais tarefas aprovadas")
    inner += figure(frontier_scatter(FRONTIER),
                    "<b>Leitura:</b> Claude Code e DSH Creator aprovam as mesmas 19 tarefas (63,3 %); um custa US$ 3,28 por aprovação, o outro US$ 18,34. "
                    "pi (teal) e OpenCode (ferrugem) são os dois braços deste projeto. Fonte: Runta (2026), tabela do post, 12 configurações, Kimi K3 via Fireworks, 30 tarefas, 1 tentativa por célula, versões pi v0.84.2 e OpenCode v1.18.19 no repositório do eval.")
    notes = "Ler o gráfico: eixo x custo mediano por tarefa aprovada; eixo y taxa de aprovação. Claude Code é o ponto isolado à direita: mesmo pass do DSH Creator, 5,6x o custo (o post diz 5,6x contra DSH Creator; 5,3x contra Codex é conta do autor). Os 12 valores estão no post; o deck original mostrava 7. Caveat do post: o resultado do Claude Code pode refletir interação harness-modelo-gateway (cache), não o harness sozinho."
    return sec("chart", "FrontierHarness: custo × aprovação", inner, notes)


# ---------------------------------------------------------------- harness

def s_anatomy() -> str:
    inner = head("Definição", "O que é um <em>harness</em>",
                 "tudo o que fica entre o modelo e o mundo: componentes externos ao modelo e editáveis (Lin <em>et al.</em>, 2026, §1)")
    inner += f"""
<div class="slide__inner">
<div class="slide__aside reveal">{harness_anatomy()}</div>
<div>
<ul class="slide__bullets">
<li class="reveal"><b>Ning <em>et al.</em> (2026, §2)</b> · um <em>harness</em> «converte um modelo de linguagem sem estado em um agente funcional ao ancorar suas saídas em execução externa, estado persistente e realimentação verificável».</li>
<li class="reveal"><b>Wang <em>et al.</em> (2026)</b> · monta os <em>prompts</em>, gerencia o estado, invoca as ferramentas e coordena o laço.</li>
<li class="reveal"><b>Lee <em>et al.</em> (2026, §3)</b> · «um programa com estado que envolve um modelo de linguagem e determina que contexto o modelo vê a cada passo».</li>
<li class="reveal"><b>Neste projeto</b> · o modelo é fixo em todos os braços; o <em>proxy</em> fica fora do <em>harness</em> e é o instrumento [80].</li>
</ul>
</div>
</div>"""
    inner += source("Lin <em>et al.</em> (2026, §1); Ning <em>et al.</em> (2026, §2); Wang <em>et al.</em> (2026); Lee <em>et al.</em> (2026, §3). Todos <em>preprints</em>, não revisados por pares.")
    notes = "<b>Referencial [66][67].</b> Ning et al. (2026, §2): definição citada. Wang et al. (2026): monta os prompts, gerencia o estado, invoca as ferramentas e coordena o laço. Lin et al. (2026, §1): prompt de sistema, ferramentas, middleware de contexto; «conjunto de componentes externos ao modelo e editáveis». [66]: os dois braços ficam em pontos distantes dessa camada: pi perto do ReAct mínimo com quatro ferramentas; OpenCode com planejamento, compactação, subagentes e permissões. O proxy externo é o instrumento [80], fora do harness."
    return sec("content", "O que é um harness", inner, notes)


def s_components() -> str:
    inner = head("Componentes", "Quatro peças editáveis, dois braços em pontos distantes",
                 "o pi fica perto do laço ReAct mínimo; o OpenCode carrega planejamento, compactação, subagentes e permissões [66]")
    rows = [
        ("Prompt de sistema", "Molda o estilo de trabalho. Viaja inteiro em toda requisição.", "2.499 bytes", "9.738 bytes", "Lin <em>et al.</em> (2026, §1); layer1/data"),
        ("Ferramentas", "Expõem sistema de arquivos e shell ao modelo. Esquemas viajam a cada requisição.", "4 esquemas", "9 esquemas", "Lin <em>et al.</em> (2026, §1); layer1/data"),
        ("Middleware de contexto", "Controla contexto, execução e recuperação: compactação, memória, permissões, verificação.", "não tem, por decisão", "tem", "Lin <em>et al.</em> (2026, §1); Ning <em>et al.</em> (2026, §2); Earendil (2026)"),
        ("Laço de execução", "Monta <em>prompts</em>, gerencia estado, invoca ferramentas, coordena o laço.", "ReAct mínimo", "planejamento e subagentes", "Wang <em>et al.</em> (2026); Yao <em>et al.</em> (2022)"),
        ("Proxy externo", "Fora do <em>harness</em>: instrumento do projeto. Conta requisições, tokens e latência igual para os dois braços.", "o mesmo", "o mesmo", "Projeto, §3 [80]; objetivo 1"),
    ]
    trs = "".join(
        f'<tr><td class="k">{k}</td><td>{d}</td><td class="n pi">{p}</td><td class="n oc">{o}</td><td class="mute" style="font-size:0.8em">{s}</td></tr>'
        for k, d, p, o, s in rows
    )
    inner += f"""
<div class="table-wrap reveal"><table class="data">
<thead><tr><th>componente</th><th>o que faz</th><th class="n"><span class="tag tag--pi">pi</span></th><th class="n"><span class="tag tag--oc">OpenCode</span></th><th>fonte</th></tr></thead>
<tbody>{trs}</tbody></table></div>"""
    inner += source("Bytes e esquemas: layer1/data/first_request.csv, 28 ago. 2026, pi 0.80.10 e OpenCode 1.17.9, primeira requisição contra endpoint simulado (Camada 1). pi sem MCP, subagentes ou modo de plano por decisão do projeto pi (Earendil, 2026).")
    notes = "Números de bytes e esquemas: layer1/data/first_request.csv (pi 2.499 bytes de prompt de sistema e 4 esquemas; OpenCode 9.738 e 9). O middleware do pi: o README do pi declara sem MCP, sem subagentes, sem plan mode (Earendil, 2026). Essa tabela é o mapa que a Camada 1 (seção 3) mede."
    return sec("table", "Componentes do harness", inner, notes)


def s_layer1() -> str:
    sb, tb, tot, pt, sc = LAYER1["system_bytes"], LAYER1["tools_bytes"], LAYER1["total_bytes"], LAYER1["prompt_tokens"], LAYER1["schemas"]
    rows = [
        (f"prompt de sistema · pi", sb[0], "pi"), ("prompt de sistema · OpenCode", sb[1], "oc"),
        ("esquemas de ferramentas · pi", tb[0], "pi"), ("esquemas de ferramentas · OpenCode", tb[1], "oc"),
        ("requisição inteira · pi", tot[0], "pi"), ("requisição inteira · OpenCode", tot[1], "oc"),
    ]
    inner = head("Método · Camada 1, medição própria", "A carga fixa antes do primeiro token de conversa",
                 f"o que cada braço envia em toda requisição, medido contra um endpoint simulado: {fmt(tot[1]/tot[0])}× mais bytes e {fmt(pt[1]/pt[0])}× mais tokens de <em>prompt</em> no OpenCode")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:3fr 1.2fr;align-items:stretch">
{figure(hbars(rows, " bytes", dec=0, aria="Bytes por requisição: prompt de sistema, esquemas de ferramentas e requisição inteira, pi contra OpenCode", height_per_row=68), "Primeira requisição de cada braço, mesma tarefa, mesmo endpoint simulado; determinístico, sem cota. É a carga fixa por requisição de que H2 depende [76].")}
<div class="cards" style="grid-template-columns:1fr;align-content:center">
<div class="card card--pi reveal"><span class="card__k">pi 0.80.10</span><span class="card__v num">{fmt_int(pt[0])} tokens</span><span class="mute">{sc[0]} esquemas de ferramenta · {fmt_int(tot[0])} bytes</span></div>
<div class="card card--oc reveal"><span class="card__k">OpenCode 1.17.9</span><span class="card__v num">{fmt_int(pt[1])} tokens</span><span class="mute">{sc[1]} esquemas de ferramenta · {fmt_int(tot[1])} bytes</span></div>
<div class="card reveal"><span class="card__k">o que isso não diz</span>«A Camada 2 também diz quanto dessa carga por requisição pesa no resultado.» A Camada 2 mede se o <em>harness</em> com mais ferramentas compensa a carga concluindo em menos passos [76].</div>
</div>
</div>"""
    inner += source("layer1/data/first_request.csv, 28 ago. 2026 (YuukiFST, 2026c). Tokens de <em>prompt</em> contados pelo endpoint simulado com um único tokenizador. Precedente externo: Databricks apud Earendil (2026), «Pi sent about 3x less context per turn».")
    notes = "Camada 1 é medição própria, determinística, sem cota. Os valores estão no repositório (layer1/data). A razão 5,3x de bytes é conta sobre o CSV. Se perguntarem se isso já responde H2: não; H2 precisa do número de passos da Camada 2, porque o harness com mais ferramentas pode concluir a unidade em menos passos [63]."
    return sec("chart", "Camada 1: carga fixa medida", inner, notes)


# ---------------------------------------------------------------- tema, problema, objetivos

def s_tema() -> str:
    inner = head("Justificativa e tema", "Escolher o modelo deixou de bastar",
                 "os modelos avançam, e com eles os <em>harnesses</em> e as ferramentas feitas para agentes; o <em>harness</em> é a parte dessa escolha que ninguém mediu em um produto inteiro [44]")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">Justificativa</span>Os agentes de codificação avançam em duas frentes: o modelo e o <em>harness</em> em volta dele. Next.js, TanStack e Effect se adaptam ao trabalho de agentes. Quem paga é o desenvolvedor, na assinatura, e a empresa, em escala; as comparações publicadas usam tarefas isoladas.</div>
<div class="card reveal"><span class="card__k">Tema</span>O efeito do <em>harness</em> sobre o custo e o desempenho de um modelo de linguagem fixo: quantos tokens e que taxa de sucesso o mesmo modelo entrega ao construir o mesmo produto sob dois <em>harnesses</em>.</div>
<div class="card card--hi reveal" style="grid-column:1/-1"><span class="card__k">Como o projeto mede isso [44]</span>«Este projeto mede esse custo construindo o Finn duas vezes, com o OpenCode e com o pi, sobre o mesmo modelo e a mesma especificação, com os tokens contados fora do <em>harness</em>.»</div>
</div>"""
    inner += source("Projeto, §1: justificativa [43]–[44], tema [46].")
    notes = "<b>Justificativa [43]–[44], tema [46].</b> Ler o tema [46] na íntegra. Se perguntarem por que não deixar o OpenCode construir e gerar a especificação para o pi: entrada desigual; o pi receberia um documento destilado de um sistema pronto e a diferença deixaria de ser atribuível ao harness."
    return sec("content", "Justificativa e tema", inner, notes)


def s_problema() -> str:
    inner = """
<blockquote class="reveal">«Com o modelo já escolhido, <b>quanto mudam o custo em tokens e a taxa de sucesso</b> ao construir o mesmo software com um <em>harness</em> em vez de outro, e <b>quanto dessa diferença</b> vem da carga fixa que cada <em>harness</em> envia em toda requisição?»</blockquote>
<cite class="reveal">Problema de pesquisa · Projeto, §1 [48]</cite>"""
    notes = "<b>Problema [48].</b> Ler na íntegra. A segunda metade é H2; a primeira é H1. Objetivo geral [50]: medir a diferença de tokens e de sucesso atribuível ao harness construindo o mesmo produto a partir da mesma especificação, com OpenCode e pi como braços; separar a parte que vem da carga fixa; entregar critério reproduzível."
    return sec("quote", "Problema de pesquisa", inner, notes)


def s_objetivos() -> str:
    inner = head("Objetivos", "Um objetivo geral, sete específicos",
                 "medir a diferença de tokens e de sucesso atribuível ao <em>harness</em> construindo o mesmo produto, com OpenCode e pi como braços; separar a parte que vem da carga fixa; entregar critério reproduzível [50]")
    trs = "".join(
        f'<tr><td class="n" style="color:var(--accent);font-weight:600">{i+1}</td><td class="k">{k}</td><td>{d}</td></tr>'
        for i, (k, d) in enumerate(OBJECTIVES)
    )
    inner += f'<div class="table-wrap reveal"><table class="data"><tbody>{trs}</tbody></table></div>'
    inner += source("Projeto, §1, objetivos específicos [52]–[58]. O objetivo 5 existe porque o efeito do <em>harness</em> é específico do modelo e pode inverter (Kapoor <em>et al.</em>, 2025; Lin <em>et al.</em>, 2026).")
    notes = "<b>Objetivos específicos [52]–[58].</b> 1 instrumento externo idêntico; 2 especificação do Finn em nove unidades, testes de aceitação do autor independentes dos testes do agente; 3 espaço inicial idêntico, congelado por hash; 4 construção completa nos dois harnesses, unidade a unidade, mesmo modelo e prompts, repetição e dispersão; 5 segundo modelo, ordenação mantida ou invertida; 6 tokens relatados vs medidos; 7 publicar executor, prompts, testes, dados e scripts a custo zero."
    return sec("table", "Objetivos", inner, notes)


def s_hipoteses() -> str:
    pi = next(r for r in FRONTIER if r[3] == "pi")
    oc = next(r for r in FRONTIER if r[3] == "oc")
    inner = head("Hipóteses", "H1: a diferença é relevante para quem paga. H2: a maior parte é carga fixa",
                 "as duas com critério de refutação declarado antes da coleta [62][63]")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1.1fr 1fr">
<div class="cards" style="grid-template-columns:1fr">
<div class="card card--hi reveal"><span class="card__k">H1</span>Entre dois <em>harnesses</em> no mesmo modelo (OpenCode e pi), a diferença de tokens para construir o mesmo produto (Finn) a partir da mesma especificação é relevante para quem paga, comparável a trocar de modelo.<br><span class="mute">Refutada se os intervalos de tokens por construção se sobrepuserem e o teste pareado por unidade não apontar diferença.</span></div>
<div class="card card--hi reveal"><span class="card__k">H2</span>A carga fixa por requisição (<em>prompt</em> de sistema e esquemas, Camada 1) explica a maior parte da diferença; o número de passos, a parte menor.<br><span class="mute">Refutada se o número de passos explicar a maior parte: o <em>harness</em> com mais ferramentas pode compensar a carga concluindo a unidade em menos passos.</span></div>
</div>
{figure(pair_bars((pi[1], pi[2]), (oc[1], oc[2])), "Ponto externo para H1: os dois braços no mesmo protocolo do FrontierHarness (Runta, 2026). Para H2: pi com 4 ferramentas e prompt abaixo de 1.000 tokens (Earendil, 2026); Databricks apud Earendil (2026), custo por tarefa acima de 2× em alguns casos com qualidade igual.")}
</div>"""
    inner += source("H1: Runta (2026), blogue institucional, 1 set. 2026; Kimi K3 via Fireworks, 30 tarefas, 1 tentativa por célula; 1,33× e 10 pp calculados pelo autor. H2: Earendil (2026), blogue institucional, 4 ago. 2026.")
    notes = "<b>Hipóteses [62][63].</b> H1 refutada se os intervalos de tokens por construção se sobrepuserem e o teste pareado por unidade não apontar diferença. H2 refutada se o número de passos explicar a maior parte, «desfecho possível e reportável». Painel da direita é fonte externa; a Camada 1 (medição própria) está na seção 3, depois das duas camadas."
    return sec("content", "Hipóteses H1 e H2", inner, notes)


# ---------------------------------------------------------------- referencial

def timeline_cards(items: list[tuple[str, str, str]], cols: int) -> str:
    cards = "".join(
        f'<div class="card reveal"><span class="card__k">{y}</span><span class="card__v" style="font-size:clamp(16px,1.7vw,24px)">{t}</span><span class="mute" style="font-size:0.9em">{c}</span></div>'
        for y, t, c in items
    )
    return f'<div class="cards c{cols}">{cards}</div>'


def s_timeline_a() -> str:
    inner = head("Referencial teórico · 2022–2025", "A interface virou objeto de projeto; o custo ficou de fora da avaliação",
                 "quatro trabalhos que definem o laço, a interface e a lacuna de custo")
    inner += timeline_cards(TIMELINE_A, 4)
    inner += source("ReAct (ICLR 2023) e SWE-agent (NeurIPS 2024) têm revisão por pares; Kapoor <em>et al.</em> (2024, 2025) são <em>preprints</em>.")
    notes = "<b>Referencial [66]–[72], parte 1.</b> Yang 2024: interface modelo-ambiente como objeto de projeto. Kapoor 2024/2025: custo ignorado, comparações entre harnesses raras; Anthropic melhor com BrowserUse, OpenAI com SeeAct (efeito específico do modelo, base do objetivo 5)."
    return sec("content", "Referencial 2022–2025", inner, notes)


def s_timeline_b() -> str:
    inner = head("Referencial teórico · 2026", "O <em>harness</em> como alavanca de primeira classe",
                 "seis trabalhos do ano: definição, tese, otimização e o placar que motivou o projeto")
    inner += timeline_cards(TIMELINE_B, 3)
    inner += source("Todos <em>preprints</em> não revisados por pares, exceto o FrontierHarness (blogue institucional).")
    notes = "<b>Referencial, parte 2.</b> Lin 2026 Tabela 1: 47,2% a 71,9%, GPT-5.4, Terminal-Bench 2, 89 tarefas, 24,7 pp (cálculo do autor). Zhang 2026: Binding Constraint Thesis. Lee 2026 Tabela 7: 76,4% vs 74,7%. Ning 2026 §5.2.1/§5.2.7: lacuna de atribuição, pede métricas por componente; este projeto responde pelo lado da medição, separando carga fixa de conversa [70]. Runta 2026: cache 25,0% vs 67,8%."
    return sec("content", "Referencial 2026", inner, notes)


def s_ev_lin() -> str:
    inner = head("Evidência nas referências · 1", "Modelo congelado, <em>harness</em> humano trocado: 24,7 pontos",
                 "Lin <em>et al.</em> (2026): mesmo GPT-5.4, três <em>harnesses</em> escritos por humanos, mesmas 89 tarefas")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1fr 1fr;align-items:stretch">
{figure(vbars(LIN_T1, " %", 80, "pass@1 de três harnesses sobre GPT-5.4 no Terminal-Bench 2"), "<b>Tabela 1:</b> pass@1, GPT-5.4 fixo, Terminal-Bench 2, 89 tarefas, k = 2. A diferença de 24,7 pp é cálculo do autor sobre a tabela.")}
{figure(hbars(LIN_SWE, " mil tokens", dec=0, vmax=760, aria="Tokens por tarefa de quatro harnesses com acurácia empatada no SWE-bench-verified", height_per_row=92), "<b>Mesma acurácia, custo diferente:</b> 74,6 % a 75,6 % no SWE-bench-verified (500 tarefas, mesmo modelo) com 679 a 461 mil tokens por tarefa, cerca de 47 % de variação de custo. O <em>harness</em> evoluído (AHE) gasta menos para o mesmo resultado.")}
</div>"""
    inner += source("Lin <em>et al.</em> (2026), arXiv:2604.25850 v4, <em>preprint</em>. Sem desvio-padrão nem barras de erro; falhas de infraestrutura contam 0 no pass@1 e saem da média de tokens (Apêndice A). Succ/Mtok, a métrica adotada por este projeto, vem da Eq. 2 do mesmo artigo.")
    notes = "Lin et al. 2026 é a fonte da definição operacional, da Tabela 1 e do Succ/Mtok. Esquerda: OpenCode 47,2%, Terminus-2 62,9%, Codex 71,9%. Direita: acurácia empatada com 47% de variação de tokens; é o argumento de que custo e acurácia são eixos separados. Limitação declarada: campanha única, k = 2, sem variância; o projeto faz n ≥ 3 e reporta dispersão."
    return sec("chart", "Evidência: Lin et al. (2026)", inner, notes)


def s_ev_hal() -> str:
    inner = head("Evidência nas referências · 2", "Mesmo modelo, outro <em>scaffold</em>: 30 a 48 pontos",
                 "Kapoor <em>et al.</em> (2025), HAL: SWE-bench Verified Mini, 50 tarefas, SWE-Agent contra o agente generalista, execução única")
    inner += figure(dumbbell(HAL, "SWE-Agent", "HAL Generalist", "Taxa de resolução do mesmo modelo com dois scaffolds no SWE-bench Verified Mini"),
                    "<b>Tabela A19:</b> quatro modelos, o mesmo par de <em>scaffolds</em>; a queda vai de 30 pp (Claude 3.7 Sonnet High) a 48 pp (o4-mini Low). Execução única, sem intervalo de confiança: o próprio artigo avisa que dependeu de <em>single runs</em> na maior parte das avaliações.")
    inner += source("Kapoor <em>et al.</em> (2025), arXiv:2510.11977, <em>preprint</em>; 21.730 <em>rollouts</em>, 9 modelos × 9 <em>benchmarks</em>, ~US$ 40.000. Também: Online Mind2Web, SeeAct + GPT-5 US$ 171 contra Browser-Use + Claude US$ 1.577 (9×) para ~2 pp; Claude vai melhor com BrowserUse, OpenAI com SeeAct.")
    notes = "HAL é o precedente de que o scaffold move dezenas de pontos com o modelo fixo, e de que o efeito depende do modelo (BrowserUse × SeeAct). Ressalva permanente: execuções únicas. É a evidência real da inversão de sinal que o objetivo 5 existe para detectar; o deck original usava um gráfico ilustrativo aqui."
    return sec("chart", "Evidência: HAL (Kapoor et al., 2025)", inner, notes)


def s_ev_alier() -> str:
    inner = head("Evidência nas referências · 3", "Custo por tarefa concluída: o <em>scaffold</em> pesa mais que a interface",
                 "Alier Forment <em>et al.</em> (2026): uma tarefa de 6 operações GitHub, sete <em>scaffoldings</em>, custo condicionado à conclusão")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1.3fr 1fr;align-items:stretch">
{figure(hbars(ALIER, " tokens", dec=0, vmax=470000, aria="Mediana de tokens de entrada por run concluída: pi, qwen-code e Claude Code", height_per_row=96), "Mediana de tokens de entrada por <em>run</em> concluída, braço CLI (sem MCP): pi 14.660 a Claude Code 410.797, <b>28×</b>. Escala linear: a barra do pi é 3,6 % da do Claude Code. Fração concluída entre parênteses; mistura de modelos hospedados, uma tarefa, um domínio.")}
<div class="cards" style="grid-template-columns:1fr;align-content:center">
<div class="card reveal"><span class="card__k">A tese, verbatim</span>«When the running cost of an agent is at issue, the scaffolding chosen to drive the model is a larger factor than the interface through which that model is given tools.»</div>
<div class="card reveal"><span class="card__k">Modelo local fixo</span><span class="card__v num">139×</span>qwen3.6:27b: Tau CLI 17.416 a Codex MCP 2.418.828 tokens.</div>
<div class="card reveal"><span class="card__k">Limite de resolução</span>Diferença menor que ~2× não se distingue de variação entre <em>runs</em>. Custo da falha: 12,9 % do dinheiro em MCP não comprou trabalho concluído, contra 2,2 % em CLI.</div>
</div>
</div>"""
    inner += source("Alier Forment <em>et al.</em> (2026), arXiv:2608.08654, <em>preprint</em>; preços OpenRouter de 3 ago. 2026; verificação por estado do repositório, nunca auto-relato. As cinco regras (condicionar, separar, verificar, checar aderência, repetir) viram protocolo deste projeto.")
    notes = "Alier Forment 2026: sem MCP 5,0x a 28x mais barato; pi o mais barato da matriz [69]. A razão 20x do abstract mistura modelos; a de 28x é o braço CLI. Regras adotadas: custo condicionado à conclusão, conclusão reportada em separado, verificação por estado. Escala linear no gráfico: a barra do pi fica em 3,6 % da do Claude Code, e essa desproporção é o ponto."
    return sec("chart", "Evidência: Alier Forment et al. (2026)", inner, notes)


def s_ev_medicao() -> str:
    lee_rows = "".join(
        f'<tr><td class="k">{m}</td><td class="n" style="color:var(--accent);font-weight:600">{fmt(a)} %</td><td class="n">{fmt(b)} %<br><span class="mute" style="font-size:.78em">{base}</span></td></tr>'
        for m, a, b, base in LEE
    )
    inner = head("Evidência nas referências · 4", "Como a prática mede: regras que este projeto adota",
                 "um placar com modelo fixo (HarnessRank), o custo do cache (Runta) e a edição só do código do <em>harness</em> (Meta-Harness)")
    inner += f"""
<div class="cards c3" style="align-items:stretch">
<div class="card card--hi reveal"><span class="card__k">HarnessRank (2026) · harnessrank.net</span>
<ul class="card__steps">
<li>Mesmo <em>benchmark</em> (terminal-bench-2.1), mesmo modelo, mesmo esforço: «each score reflects the harness, not the model behind it».</li>
<li>Ordena por fração de tarefas resolvidas, média de várias <em>runs</em>, com dispersão; custo e tokens ao lado, sem mudar a ordem.</li>
<li>«A timeout is a result, not a do-over.» Só <em>runs</em> completas e limpas contam.</li>
<li>Eficiência em tokens <b>sem cache</b> por tarefa; custo só quando o provedor emite, nunca estimado.</li>
</ul>
<span class="mute" style="display:block;margin-top:8px;font-size:0.85em">Sem linhas publicadas até 15 set. 2026: entra como precedente de método, não de número.</span></div>
<div class="card reveal"><span class="card__k">Runta (2026) · o cache muda a conta</span>
<span class="card__v num">25,0 % vs 67,8 %</span>
Taxa de acerto de cache do Claude Code: 25,0 % ponderada por tokens contra 67,8 % na célula mediana. Na tarefa-exemplo, pi passa a US$ 2,50 em 90 turnos; Claude Code passa a US$ 64,36 em 381 turnos (26×).<br>
<span class="mute">Regra adotada: o <em>proxy</em> conta tokens sobre os bytes transmitidos, um tokenizador para os dois braços; o relatório do <em>gateway</em> fica como verificação cruzada (objetivo 6).</span></div>
<div class="card reveal"><span class="card__k">Lee <em>et al.</em> (2026) · decisões são isoláveis</span>
<div class="table-wrap" style="margin:6px 0 8px"><table class="data" style="font-size:0.9em"><thead><tr><th>modelo fixo</th><th class="n">Meta-Harness</th><th class="n">base</th></tr></thead><tbody>{lee_rows}</tbody></table></div>
<span class="mute">TerminalBench-2, 89 tarefas, sem repetições nem variância: pelo critério de ~2× de Alier Forment, +1,7 pp não se distingue de ruído. Por isso este projeto reporta dispersão.</span></div>
</div>"""
    inner += source("HarnessRank (2026), site, acesso em 28 ago. 2026, relido em 15 set. 2026; Runta (2026), blogue institucional; Lee <em>et al.</em> (2026), arXiv:2603.28052, <em>preprint</em>. Miller (2024) fundamenta o teste pareado e as barras de erro.")
    notes = "HarnessRank [69]: ordena por aprovação com modelo fixo e publica custo e tokens ao lado. Ainda sem linhas publicadas (conferido em 15 set. 2026), por isso é precedente de método: timeout como resultado, descarte documentado, tokens sem cache, custo reportado e não estimado. Runta: cache 25,0% ponderado vs 67,8% na célula mediana [72]. Lee 2026: 76,4% vs 74,7%, sem variância."
    return sec("content", "Evidência: regras de medição", inner, notes)


# ---------------------------------------------------------------- método

def s_como() -> str:
    steps = [
        ("01 · UMA ESPECIFICAÇÃO", "Finn, em 9 unidades", "SaaS de financeiro por voz descrito a partir das <em>issues</em>; cada unidade com testes de aceitação escritos pelo autor; congelada por SHA-256.", "spec.md · SHA-256"),
        ("02 · DOIS HARNESSES", "OpenCode e pi", "Mesma especificação, mesmos <em>prompts</em>, mesmo espaço de trabalho vazio, mesmo modelo; constroem do zero, unidade a unidade.", "opencode run · pi --mode json"),
        ("03 · UM CONTADOR EXTERNO", "Proxy reverso", "Entre o <em>harness</em> e o modelo: conta requisições, tokens e latência da mesma forma para os dois; n ≥ 3 construções por célula.", "proxy · um tokenizador"),
        ("04 · UM CRITÉRIO", "Tokens ao lado do sucesso", "Tokens por construção ao lado da fração de testes aprovados, e Succ/Mtok; teste pareado por unidade; a Camada 1 separa a carga fixa.", "Wilcoxon · Succ/Mtok"),
    ]
    inner = head("Como o projeto funciona", "O mesmo produto, construído duas vezes", "a ordem importa: especificação, dois braços do zero, <em>proxy</em>, critério")
    inner += pipeline(steps)
    inner += source("Projeto, §1 [44] e §3 [76]–[83]. Braços: OpenCode (Opencode, 2026a) e pi (Earendil, 2026), código aberto, sem interface. «O projeto escreve apenas o instrumento, os <em>prompts</em> e os testes de aceitação» [77].")
    notes = "<b>Como o projeto funciona [44][60][76][78].</b> Dizer em voz alta a ordem: especificação → dois braços do zero → proxy → critério. Camada 1 e Camada 2, matriz e limites vêm nos slides seguintes; aqui só a visão geral. Classificação e uso de IA já foram ditos, na ordem do projeto [74][75]."
    return sec("content", "Como o projeto funciona", inner, notes)


def s_finn() -> str:
    steps = [(str(i + 1), n, d, "") for i, (n, d) in enumerate(FINN_PIPELINE)]
    inner = head("O produto", "Finn: um SaaS de verdade, não um <em>benchmark</em> de tarefas soltas",
                 "financeiro por voz para pequenas empresas: o dono fala pelo WhatsApp ou pelo app e recebe lançamento, relatório e aviso no celular; multiempresa em um banco só")
    inner += pipeline(steps, {3: "pipeline__step--oc"})
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">Já decidido antes do experimento</span>21 <em>issues</em> fechadas pelo autor (#2–#22, sob o mapa #1) fixam produto e pilha: TypeScript, TanStack Start, tRPC, Drizzle, PostgreSQL, Vitest. Os agentes não escolhem nada disso.</div>
<div class="card reveal"><span class="card__k">Custo zero por padrão</span>Whisper local; IA por API atrás de <em>flag</em> por empresa, desligada (#4, #12, #17). Toda escrita confirma antes de valer (#5, #20). O <em>pipeline</em> de sete passos da <em>issue</em> #14 aparece com executar e negar juntos.</div>
</div>"""
    inner += source("Finn (YuukiFST, 2026b): github.com/YuukiFST/Finn. Decisões de produto nas <em>issues</em> #2–#10; decisões técnicas em #11–#22. Em ferrugem, o passo que a unidade U4 implementa.")
    notes = "<b>Finn (YuukiFST, 2026b) [78].</b> Apresentar o produto antes de usá-lo como suíte: SaaS de financeiro por voz para pequenas empresas, do próprio autor, especificado em 21 issues fechadas antes do experimento. Ponto a dizer: é um produto de verdade, com pilha fixa, não uma suíte de tarefas isoladas como as das comparações publicadas."
    return sec("content", "Finn: o produto", inner, notes)


def s_spec() -> str:
    cells = "".join(
        f'<div class="card reveal" style="text-align:center;padding:clamp(10px,1.6vh,18px) 8px{";border-top:3px solid var(--oc)" if u == "U4" else ";border-top:3px solid var(--accent)"}"><span class="card__k" style="margin:0">{u}</span><span class="card__v" style="font-size:clamp(15px,1.6vw,22px);margin:4px 0">{n}</span><span class="mute num" style="font-size:0.8em">issue {i}</span></div>'
        for u, n, i in UNITS
    )
    inner = head("A especificação", "Nove unidades em ordem de dependência, uma especificação congelada",
                 "as 9 <em>issues</em> técnicas (#14–#22) viram as 9 unidades; o agente carrega o próprio código de uma unidade à seguinte")
    inner += f'<div class="cards" style="grid-template-columns:repeat(9,minmax(0,1fr));gap:8px">{cells}</div>'
    inner += """
<div class="cards c3">
<div class="card reveal"><span class="card__k">Entrada idêntica</span>Os dois braços recebem os mesmos bytes e um espaço de trabalho com só a especificação e a pilha, congelado por hash. O autor não escreve código depois do início.</div>
<div class="card reveal"><span class="card__k">Escore</span>Fração dos testes de aceitação do autor, <em>held-out</em>, rodados sobre uma cópia do espaço ao fim de cada unidade. Unidade concluída quando todos os seus testes passam; construção concluída quando todos passam ao fim.</div>
<div class="card reveal"><span class="card__k">Executor</span>Invoca o <em>harness</em> uma vez por unidade, em ordem, com <em>prompt</em> idêntico; o que o agente construiu em uma unidade é o ponto de partida da seguinte.</div>
</div>"""
    inner += source("Projeto, §3 [78]. Ordem: #15 tenant, #16 governança, #17 flags, #14 pipeline de voz, #20 confirmação, #21 log, #19 relatório, #18 agendador, #22 cobrança.")
    notes = "<b>Suíte [78].</b> O autor escreve, antes de qualquer execução, uma especificação única congelada por SHA-256: produto, pilha, restrições gerais e nove unidades em ordem de dependência. Escore: fração dos testes de aceitação do autor, held-out. Unidades não são independentes: a seguinte parte do que o mesmo braço construiu; essa dependência é custo do harness e é reportada por unidade."
    return sec("content", "A especificação em 9 unidades", inner, notes)


def s_classificacao() -> str:
    trs = "".join(
        f'<tr><td class="k">{k}</td><td style="color:var(--accent);font-weight:600">{v}</td><td>{w}</td></tr>'
        for k, v, w in CLASS_AXES
    )
    inner = head("Classificação da pesquisa", "Aplicada, quanti + quali, exploratória, experimental, dedutiva",
                 "variável independente: o <em>harness</em>; controladas: modelo, especificação, espaço de trabalho inicial e limites")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1.4fr 1fr">
<div class="table-wrap reveal"><table class="data"><tbody>{trs}</tbody></table></div>
<div class="card card--hi reveal"><span class="card__k">Por que exploratória</span>A comparação de dois <em>harnesses</em> construindo o mesmo produto completo do zero, a partir da mesma especificação, não tem precedente publicado. O que já existe compara <em>harnesses</em> em suítes de tarefas isoladas.</div>
</div>"""
    inner += source("Projeto, §3, parágrafo de classificação [74]; sem manual de metodologia citado: as referências são só sobre o <em>harness</em>.")
    notes = "<b>Classificação [60][74].</b> Aplicada; quantitativa (tokens e sucesso) e qualitativa (atribuição à carga fixa ou aos passos); exploratória «porque a comparação de dois harnesses construindo o mesmo produto completo do zero, a partir da mesma especificação, não tem precedente publicado»; experimental, VI o harness; dedutiva."
    return sec("table", "Classificação da pesquisa", inner, notes)


def s_ia() -> str:
    inner = head("Uso de IA declarado", "Dois métodos, um papel: o autor decide e confere, o agente escreve",
                 "Portaria CNPq nº 2.664/2026 (Brasil, 2026) pede ferramenta e finalidade · ferramenta: Claude Code")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">Fontes · <em>LLM Wiki</em> (Karpathy, 2026)</span>
<ol class="card__steps">
<li><b>Fontes brutas</b> ficam guardadas sem alteração; o autor escolhe o que entra.</li>
<li><b>O agente escreve</b> uma página de síntese por fonte e liga entidades e conceitos.</li>
<li><b>Cada operação</b> entra num registro cronológico; contradições viram uma fila de revisão.</li>
<li><b>O autor confere</b> cada afirmação citada na obra original antes de entrar no texto.</li>
</ol>
<span class="mute" style="display:block;margin-top:8px">29 fontes ingeridas · 46 páginas · nenhuma frase do projeto escrita pelo agente</span></div>
<div class="card reveal"><span class="card__k">Especificação · Helmsman (YuukiFST, 2026a)</span>
<ol class="card__steps">
<li><b>Uma ideia vira um mapa</b> de decisões no rastreador de <em>issues</em>: 21 <em>tickets</em> sob um mapa.</li>
<li><b>O que o sistema faz</b>, só o autor responde: 9 <em>tickets</em> de produto, em conversa.</li>
<li><b>Como construir</b>, o agente decide sozinho: 12 <em>tickets</em> técnicos, cada um com alternativas e critério.</li>
<li><b>Fato externo</b> (preço de API, modelo de voz): subagentes de pesquisa antes de decidir, 3 <em>tickets</em>.</li>
</ol>
<span class="mute" style="display:block;margin-top:8px">Mapa fechado: nada a decidir · base da especificação congelada dos dois braços</span></div>
</div>"""
    inner += source("Finalidade declarada: entender o tema, buscar artigos e registrar as decisões de produto e de pilha do Finn antes do experimento. Projeto, §3 [75] (Karpathy, 2026; YuukiFST, 2026a, 2026c; Brasil, 2026).")
    notes = "<b>Uso de IA [75].</b> LLM Wiki instanciado no repositório (YuukiFST, 2026c). Helmsman: #2–#10 perguntas de produto que só o autor respondeu; #11–#22 decisões técnicas do agente, cada uma com alternativas, critério e o que trava para as seguintes; #11–#13 dependiam de fato externo e foram resolvidas por subagentes de pesquisa. O autor responde pelo texto final e por cada decisão de produto."
    return sec("content", "Uso de IA declarado", inner, notes)


def s_camadas() -> str:
    inner = head("Método · instrumento", "Duas camadas de medição, um <em>proxy</em>",
                 "Camada 1 dá a carga fixa por requisição (H2); Camada 2 dá tokens por construção ao lado do sucesso (H1)")
    inner += figure(layers_flow(), "")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">Camada 1</span>Forma da requisição contra endpoint simulado: esquemas, bytes de <em>prompt</em>, tokens por passo. Determinística, sem cota. «Fornece a carga fixa por requisição de que H2 depende.»</div>
<div class="card reveal"><span class="card__k">Camada 2</span>Construção do produto no modelo real via <em>proxy</em>. Estocástica, consome cota, n ≥ 3 por célula. Limite único: relógio de parede por unidade, 3× a maior mediana dos braços nas unidades-piloto; sem teto de passos, porque o teto seria decisão de projeto do <em>harness</em> [81].</div>
</div>"""
    inner += source("O <em>proxy</em> conta tokens sobre os bytes transmitidos, um só tokenizador para os dois braços; o <em>gateway</em> injeta conteúdo, deslocamento aditivo por requisição que não se cancela em razão, por isso o relatório do <em>gateway</em> fica para verificação cruzada [80].")
    notes = "<b>Método [76][80][81].</b> Camada 1: determinística, sem cota. Camada 2: estocástica, consome cota. «A Camada 2 também diz quanto dessa carga por requisição pesa no resultado.» Proxy reverso força o relatório de uso, conta tokens sobre os bytes transmitidos com um único tokenizador; o gateway injeta conteúdo, deslocamento aditivo que não se cancela em razão [80]. Limite único: relógio de parede por unidade [81]."
    return sec("chart", "Duas camadas de medição", inner, notes)


def s_matriz() -> str:
    units = "".join(f'<span class="u">{u}</span>' for u, _, _ in UNITS)

    def cell(arm: str, tier: str) -> str:
        return f'<div class="cell cell--{arm} reveal"><div class="units">{units}</div><span class="n">{tier} · n ≥ 3 construções após descartes</span></div>'

    inner = head("Método · matriz", "Braço × nível, nove unidades por construção",
                 "cada célula (braço, nível) recebe n ≥ 3 construções; dois níveis gratuitos no mesmo <em>gateway</em> (Opencode, 2026b)")
    inner += f"""
<div class="slide__inner" style="grid-template-columns:1.5fr 1fr;align-items:start">
<div>
<div class="matrix">
<div></div><div class="mh pi">pi</div><div class="mh oc">OpenCode</div>
<div class="mh">nível primário</div>{cell("pi", "primário")}{cell("oc", "primário")}
<div class="mh">nível de robustez</div>{cell("pi", "robustez")}{cell("oc", "robustez")}
</div>
<div class="card reveal" style="margin-top:12px"><span class="card__k">Cada unidade recebe uma classe</span><span class="tag tag--bad">não concluída</span> o agente não concluiu a unidade; é resultado, entra com a fração de testes aprovada e a construção segue (estouro do relógio incluído). <span class="tag tag--mute">descartada</span> medição inconfiável descarta a construção; registrada, sem reparo nem repetição. Classe lida do registro do <em>proxy</em>.</div>
</div>
<div class="cards" style="grid-template-columns:1fr">
<div class="card card--hi reveal"><span class="card__k">Braços</span>OpenCode e pi: código aberto, sem interface (<code>opencode run</code>, <code>pi --mode json</code>), URL base OpenAI-compatível. Nenhum <em>harness</em> escrito pelo projeto.</div>
<div class="card reveal"><span class="card__k">Segundo nível de modelo</span>Responde ao objetivo 5: a ordenação entre os braços se mantém ou inverte quando o modelo muda? Conclusões por nível.</div>
<div class="card reveal"><span class="card__k">Ameaça principal</span>Variância entre execuções no nível gratuito. Resposta: n ≥ 3, mediana com dispersão, reduzir cobertura antes de reduzir repetições [82].</div>
</div>
</div>"""
    inner += source("Projeto, §3: braços [77], células [82], classes [84]. Pilha fixa TypeScript, TanStack Start, tRPC, Drizzle, PostgreSQL, Vitest.")
    notes = "<b>Braços [77], células [82], classes [84].</b> Células (braço, nível) com n ≥ 3 construções; dois níveis gratuitos no mesmo gateway [79]. Classes: não concluída = resultado com a fração aprovada, a construção segue; descartada = medição inconfiável descarta a construção."
    return sec("content", "Braços e matriz experimental", inner, notes)


def s_estatistica() -> str:
    inner = head("Método · métrica e teste", "Succ/Mtok e Wilcoxon pareado por unidade",
                 "um braço que falha barato não pode parecer o mais barato: tokens sempre ao lado da fração de testes aprovados")
    inner += """
<div class="cards c3" style="align-items:stretch">
<div class="card card--hi reveal"><span class="card__k">Métrica</span><span class="card__v num" style="font-size:clamp(18px,2vw,28px)">Succ/Mtok = pass@1 × 10⁶ ÷ tokens por execução</span>Lin <em>et al.</em> (2026, Eq. 2). Medida principal: tokens por construção, contados no <em>proxy</em>, relatados ao lado da fração final de testes aprovados. Para H2: tokens decompostos em carga fixa (Camada 1 × passos) e conversa.</div>
<div class="card reveal"><span class="card__k">Teste</span><span class="card__v">Wilcoxon dos postos sinalizados</span>Bilateral, α = 0,05, pareado por unidade, sobre tokens por unidade e Succ/Mtok por unidade. Não paramétrico porque nove pares não sustentam suposição distribucional; pareado porque a dificuldade da unidade é o maior fator de perturbação (Miller, 2024).</div>
<div class="card reveal"><span class="card__k">Poder</span><span class="card__v num">MDE ≈ 0,76σ</span>Com n = 3 por célula e 9 unidades. Valor crítico de W para k = 9 pares, bilateral, α = 0,05: 5. Unidades não são independentes (a seguinte parte do que o mesmo braço construiu): essa dependência é custo do <em>harness</em> e é reportada por unidade.</div>
</div>"""
    inner += source("Projeto, §3 [72][83]. Miller (2024), arXiv:2411.00640, <em>preprint</em>: barras de erro e teste pareado em avaliações de modelos.")
    notes = "<b>Métrica e estatística [72][83].</b> Medida principal: tokens por construção, contados no proxy, sempre ao lado da fração final de testes aprovados. Wilcoxon bilateral, α = 0,05, pareado por unidade. MDE ≈ 0,76σ com n = 3 e 9 unidades. O deck original tinha uma simulação interativa aqui; este mostra só a regra."
    return sec("content", "Succ/Mtok e teste pareado", inner, notes)


def s_limitacoes() -> str:
    inner = head("Limitações e ameaças à validade", "Quatro declaradas de partida",
                 "a inversão de sinal com outro modelo é real na literatura (BrowserUse × SeeAct em Kapoor <em>et al.</em>, 2025); o segundo nível existe para detectá-la")
    inner += """
<div class="cards c2">
<div class="card reveal"><span class="card__k">Específico do modelo</span>O efeito pode inverter de sinal. Conclusões por nível; objetivo 5 testa isso. Lin <em>et al.</em> (2026): «the optimal harness is model-specific».</div>
<div class="card reveal"><span class="card__k">Um produto, uma pilha</span>O resultado vale para tarefas dessa família; outras pilhas ficam como trabalho futuro.</div>
<div class="card reveal"><span class="card__k">Especificação humana e trajetória própria</span>O autor escreve a especificação, e cada braço carrega os próprios erros de uma unidade à seguinte. Mitigação: mesma entrada e mesmo início vazio para os dois, comparação pareada por unidade.</div>
<div class="card reveal"><span class="card__k">Sem placar público</span>Suíte própria, válido só braço × braço; valores absolutos sem placar; dólares externos de outros modelos e níveis pagos entram como contrafactual rotulado.</div>
</div>"""
    inner += source("Projeto, §3 [86]; variância como principal ameaça [82]. Evidência de inversão: Kapoor <em>et al.</em> (2025), §4.1.")
    notes = "<b>Limitações [86].</b> Quatro declaradas: efeito específico do modelo (objetivo 5); um único produto sobre uma única pilha; especificação escrita pelo autor e cada braço carregando os próprios erros; valores absolutos sem placar público. Variância como principal ameaça [82]. A evidência real de inversão é Kapoor et al. (2025) [72]."
    return sec("content", "Limitações", inner, notes)


def s_orcamento() -> str:
    inner = head("Orçamento", "R$ 0,00 em dinheiro; a cota gratuita é o limite vinculante",
                 "Tabela 1 do projeto; folga concentrada na execução da matriz e na escrita da especificação e dos testes de aceitação")
    inner += """
<div class="kpis" style="grid-template-columns:repeat(3,minmax(0,1fr))">
<div class="kpi reveal"><div class="kpi__v">R$ 0,00</div><div class="kpi__l">inferência</div><div class="kpi__d">dois níveis gratuitos do mesmo <em>gateway</em>, OpenCode Zen (Opencode, 2026b)</div></div>
<div class="kpi reveal"><div class="kpi__v">R$ 0,00</div><div class="kpi__l"><em>harnesses</em> e ferramentas</div><div class="kpi__d">OpenCode e pi, código aberto; Node.js e PostgreSQL</div></div>
<div class="kpi reveal"><div class="kpi__v">R$ 0,00</div><div class="kpi__l">máquinas</div><div class="kpi__d">estação NixOS e estação Windows, já disponíveis</div></div>
</div>
<div class="card card--hi reveal"><span class="card__k">O que limita de fato</span>A cota gratuita: um lote da matriz por dia, ao longo de dias. Por isso o cronograma reserva dois meses para a matriz e a análise vem só depois.</div>"""
    inner += source("Projeto, §4, Tabela 1 [88]–[100].")
    notes = "<b>Orçamento [88]–[100]:</b> inferência R$ 0,00 (nível gratuito do gateway), harnesses e ferramentas R$ 0,00, máquinas R$ 0,00. Cota gratuita é o limite vinculante; lotes ao longo de dias."
    return sec("dashboard", "Orçamento", inner, notes)


def s_cronograma() -> str:
    hdr = '<div></div>' + "".join(f'<div class="gh">{m}</div>' for m in GANTT_MONTHS)
    rows = []
    for phase, months in GANTT:
        done = months[:2] == [1, 1] or phase.startswith("Revisão")
        cells = "".join(f'<div class="gc {"done" if (on and done) else ("on" if on else "")}"></div>' for on in months)
        rows.append(f'<div class="gp reveal">{phase}</div>{cells}')
    inner = head("Cronograma", "Ago. 2026 a jan. 2027",
                 "toda a escrita concluída em set. 2026 (teal); instrumento, especificação e testes em out–nov; matriz em dez–jan; análise em jan")
    inner += f'<div class="gantt">{hdr}{"".join(rows)}</div>'
    inner += source("Projeto, §5, Tabela 2 [102]–[180]. Experimentos práticos a partir de outubro; revisão final e apresentação em setembro.")
    notes = "<b>Cronograma [102]–[180]:</b> ago–set leitura, definição do tema e toda a escrita (concluída em set. 2026); out–nov instrumento, especificação e testes de aceitação; matriz dez–jan; análise em jan; revisão final e apresentação em set."
    return sec("content", "Cronograma", inner, notes)


# ---------------------------------------------------------------- referências e fecho

def s_refs() -> str:
    inner = head("Referências", "As 21 entradas da seção 6",
                 "formato ABNT abreviado; 18 sobre o <em>harness</em>, 3 sobre o método de trabalho declarado (Portaria CNPq, LLM Wiki, Helmsman)")
    inner += '<div class="refs reveal">' + "".join(f"<p>{r}</p>" for r in REFS) + "</div>"
    notes = "<b>Referências [183]–[203].</b> Lista completa com 21 entradas: 18 sobre o harness, 3 sobre o método de trabalho declarado; normas e manuais de metodologia saíram em 14 set. 2026. Preprints marcados. HarnessRank (2026) está na lista e é citado em §2 [69]."
    return sec("content", "Referências", inner, notes)


def s_fecho() -> str:
    inner = f"""
<div class="title-decor">{title_decor()}</div>
<div class="reveal">
<p class="slide__label">Pergunta que o projeto responde</p>
<h2 class="slide__display">Quanto pesa, para o desenvolvedor que já escolheu o modelo, conhecer o <em>harness</em> antes de pagar por ele?</h2>
<div class="title-rule"></div>
<p class="end-thanks">Obrigado. Perguntas?</p>
<p class="slide__subtitle">github.com/YuukiFST/harness-bench (YuukiFST, 2026c) · github.com/YuukiFST/Finn (YuukiFST, 2026b)</p>
</div>"""
    notes = "<b>Fecho.</b> Retomar o problema [48] e o produto [74]: um critério de escolha que um desenvolvedor ou uma empresa poderá aplicar. Repositórios YuukiFST/Finn [201] e YuukiFST/harness-bench [202]."
    return sec("end", "Fecho", inner, notes)


def all_slides() -> str:
    # Mesma ordem do projeto (dist/projeto-de-pesquisa.docx): 1 Introdução, 2 Referencial teórico,
    # 3 Material e método, 4 Orçamento, 5 Cronograma, 6 Referências. Dentro de cada seção, a ordem
    # dos parágrafos [n] do dump (tools/docx_prose.py dump).
    parts = [
        s_capa(),
        divider("01", "Seção 1", "Introdução", "O <em>harness</em> muda o que o mesmo modelo custa e entrega: por que isso importa, a pergunta que abre e o que o projeto promete medir."),
        s_kpis(),
        s_frontier(),
        s_tema(),
        s_problema(),
        s_objetivos(),
        s_hipoteses(),
        divider("02", "Seção 2", "Referencial teórico", "O que é um <em>harness</em>, dez trabalhos em quatro anos e as duas pendências que o projeto responde: atribuição e instrumentação."),
        s_anatomy(),
        s_components(),
        s_timeline_a(),
        s_timeline_b(),
        s_ev_lin(),
        s_ev_hal(),
        s_ev_alier(),
        s_ev_medicao(),
        divider("03", "Seção 3", "Material e método", "Classificação, uso de IA declarado, duas camadas de medição, o produto, a matriz, a estatística e as limitações."),
        s_classificacao(),
        s_ia(),
        s_como(),
        s_camadas(),
        s_layer1(),
        s_finn(),
        s_spec(),
        s_matriz(),
        s_estatistica(),
        s_limitacoes(),
        divider("04", "Seções 4, 5 e 6", "Orçamento, cronograma e referências", "R$ 0,00 em dinheiro, calendário de agosto a janeiro e 21 entradas, todas sobre o <em>harness</em> ou sobre o método declarado."),
        s_orcamento(),
        s_cronograma(),
        s_refs(),
        s_fecho(),
    ]
    return "\n".join(parts)
