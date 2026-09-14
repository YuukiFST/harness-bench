"""Fifth pass on the deck (2026-09-14): construction from one specification.

Mirrors tools/pcc_edits_2026-09-14c.py. Each arm builds the whole Finn from
scratch, from the same frozen specification in nine units, in one workspace;
the comparison is on tokens per construction, paired per unit. Reference
states and isolated tickets leave the slides; "ticket" becomes "unidade" and
T1..T9 become U1..U9. The matrix keeps its 9 columns, now the units inside a
construction; a cell is (braço, nível) with n ≥ 3 constructions.

Applies to dist/apresentacao-pcc.html (exact), deck/index.html (whitespace-
tolerant) and the deck TypeScript (exact). Pairs already applied are skipped,
so the script can be rerun.

Usage:
    python tools/slides_edits_2026-09-14e.py
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


# --- markup shared by both decks (modulo wrapping and the "glass" class) -----
M: list[tuple[str, str]] = [
    (
        "medir a diferença de tokens e de sucesso entre OpenCode e pi construindo o mesmo SaaS, <em>ticket</em> a <em>ticket</em>; separar a parte que vem da carga fixa; entregar critério reproduzível.",
        "medir a diferença de tokens e de sucesso entre OpenCode e pi construindo o mesmo SaaS a partir da mesma especificação; separar a parte que vem da carga fixa; entregar critério reproduzível.",
    ),
    (
        "<b class=\"acc\">A suíte</b> · as 9 <em>issues</em> técnicas (#14–#22) viram os 9 <em>tickets</em> do experimento; cada um tem testes de aceitação escritos pelo autor.",
        "<b class=\"acc\">A especificação</b> · as 9 <em>issues</em> técnicas (#14–#22) viram as 9 unidades de uma especificação única, congelada por hash; cada unidade tem testes de aceitação escritos pelo autor.",
    ),
    (
        "Em âmbar, o <em>ticket</em> do <em>pipeline</em> desenhado acima.",
        "Em âmbar, a unidade do <em>pipeline</em> desenhado acima.",
    ),
    (
        "<b class=\"acc\">1 · Um produto</b> · Finn, SaaS de financeiro por voz, dividido em 9 <em>tickets</em> técnicos, cada um com testes de aceitação escritos pelo autor.",
        "<b class=\"acc\">1 · Uma especificação</b> · Finn, SaaS de financeiro por voz, descrito em 9 unidades a partir das <em>issues</em>, cada uma com testes de aceitação escritos pelo autor.",
    ),
    (
        "<b class=\"acc\">2 · Dois <em>harnesses</em></b> · OpenCode e pi recebem o mesmo <em>ticket</em>, o mesmo <em>prompt</em>, o mesmo espaço de trabalho congelado e o mesmo modelo.",
        "<b class=\"acc\">2 · Dois <em>harnesses</em></b> · OpenCode e pi recebem a mesma especificação, os mesmos <em>prompts</em>, o mesmo espaço de trabalho vazio e o mesmo modelo, e constroem o produto do zero, unidade a unidade.",
    ),
    (
        "<b class=\"acc\">4 · Um critério</b> · tokens por <em>ticket</em> concluído e Succ/Mtok, comparados por teste pareado; a Camada 1 separa a parte que é carga fixa por requisição.",
        "<b class=\"acc\">4 · Um critério</b> · tokens por construção, ao lado da fração de testes aprovados, e Succ/Mtok, comparados por teste pareado por unidade; a Camada 1 separa a parte que é carga fixa por requisição.",
    ),
    (
        "<b>2</b> Finn em <em>tickets</em> com testes de aceitação do autor",
        "<b>2</b> Especificação do Finn em 9 unidades, com testes de aceitação do autor",
    ),
    (
        "<b>3</b> Espaço de trabalho congelado e idêntico por <em>ticket</em>",
        "<b>3</b> Espaço de trabalho inicial idêntico: só a especificação e a pilha",
    ),
    (
        "<b>4</b> Cada <em>ticket</em> nos dois <em>harnesses</em>, mesmo modelo e <em>prompt</em>, n ≥ 3",
        "<b>4</b> Construção completa nos dois <em>harnesses</em>, mesmo modelo e <em>prompts</em>, n ≥ 3",
    ),
    (
        "<b class=\"acc\">H1</b> · entre OpenCode e pi no mesmo modelo, a diferença de tokens por <em>ticket</em> concluído é relevante para quem paga, comparável a trocar de modelo. <span class=\"mute\">Refutada se os intervalos de tokens por <em>ticket</em> se sobrepuserem em toda a suíte.</span>",
        "<b class=\"acc\">H1</b> · entre OpenCode e pi no mesmo modelo, a diferença de tokens para construir o Finn a partir da mesma especificação é relevante para quem paga, comparável a trocar de modelo. <span class=\"mute\">Refutada se os intervalos de tokens por construção se sobrepuserem e o teste pareado por unidade não apontar diferença.</span>",
    ),
    (
        "VI: <em>harness</em> · controladas: modelo, <em>ticket</em>, espaço de trabalho, limites",
        "VI: <em>harness</em> · controladas: modelo, especificação, espaço de trabalho inicial, limites",
    ),
    (
        "<b class=\"acc\">Camada 2</b> · desfecho dos <em>tickets</em> no modelo real via <em>proxy</em> reverso. Estocástica, consome cota, n ≥ 3.",
        "<b class=\"acc\">Camada 2</b> · construção do produto no modelo real via <em>proxy</em> reverso. Estocástica, consome cota, n ≥ 3.",
    ),
    (
        "Braços e matriz (braço × <em>ticket</em> × nível)<small>clique ou navegue com Tab em uma célula · cada célula recebe n ≥ 3 execuções após descartes</small>",
        "Braços e matriz (braço × nível, 9 unidades por construção)<small>clique ou navegue com Tab em uma unidade · cada célula (braço, nível) recebe n ≥ 3 construções após descartes</small>",
    ),
    (
        "<b class=\"acc\">Cada execução recebe uma classe</b> · <span style=\"color:var(--bad)\">não concluída</span>: agente não concluiu o <em>ticket</em>; é resultado, entra com a fração de testes aprovada (estouro do relógio incluído). <span class=\"mute\">descartada</span>: medição inconfiável; registrada, sem reparo nem repetição. Classe lida do registro do <em>proxy</em>.",
        "<b class=\"acc\">Cada unidade recebe uma classe</b> · <span style=\"color:var(--bad)\">não concluída</span>: agente não concluiu a unidade; é resultado, entra com a fração de testes aprovada e a construção segue (estouro do relógio incluído). <span class=\"mute\">descartada</span>: medição inconfiável descarta a construção; registrada, sem reparo nem repetição. Classe lida do registro do <em>proxy</em>.",
    ),
    (
        "<b class=\"acc\">Suíte</b> · Finn, 9 <em>tickets</em> técnicos; espaço de trabalho congelado por SHA-256 a cada <em>ticket</em>. Escore: fração dos testes de aceitação do autor, <em>held-out</em>.",
        "<b class=\"acc\">Especificação</b> · Finn em 9 unidades, congelada por SHA-256; espaço de trabalho inicial vazio, o agente carrega o próprio código de uma unidade à seguinte. Escore: fração dos testes de aceitação do autor, <em>held-out</em>.",
    ),
    (
        "relógio de parede 3× a maior mediana dos braços nos <em>tickets</em>-piloto.",
        "relógio de parede por unidade, 3× a maior mediana dos braços nas unidades-piloto.",
    ),
    (
        "Finn: SaaS multiempresa de financeiro por voz, 21 <em>tickets</em> fechados antes do experimento; pilha fixa TypeScript, TanStack Start, tRPC, Drizzle, PostgreSQL, Vitest. T1 tenant · T2 governança · T3 <em>flags</em> · T4 <em>pipeline</em> de voz · T5 confirmação · T6 log · T7 relatório · T8 agendador · T9 cobrança.",
        "Finn: SaaS multiempresa de financeiro por voz, 21 <em>tickets</em> fechados antes do experimento; pilha fixa TypeScript, TanStack Start, tRPC, Drizzle, PostgreSQL, Vitest. Unidades em ordem de dependência: U1 tenant · U2 governança · U3 <em>flags</em> · U4 <em>pipeline</em> de voz · U5 confirmação · U6 log · U7 relatório · U8 agendador · U9 cobrança.",
    ),
    (
        "Teste de Wilcoxon dos postos sinalizados, bilateral, α = 0,05, pareado por tarefa. Com n = 3 por célula e 9 <em>tickets</em>, diferença mínima detectável ≈ 0,76σ. O mesmo teste roda sobre os tokens por <em>ticket</em> concluído.",
        "Teste de Wilcoxon dos postos sinalizados, bilateral, α = 0,05, pareado por unidade. Com n = 3 por célula e 9 unidades, diferença mínima detectável ≈ 0,76σ. O mesmo teste roda sobre os tokens por unidade; a medida principal, tokens por construção, é relatada ao lado da fração de testes aprovados.",
    ),
    (
        "<b class=\"acc\">Estado de referência humano</b> · o autor escreve o ponto de partida de cada <em>ticket</em>; mitigação: mesmo estado para os dois braços, comparação pareada.",
        "<b class=\"acc\">Especificação humana e trajetória própria</b> · o autor escreve a especificação, e cada braço carrega os próprios erros de uma unidade à seguinte; mitigação: mesma entrada e mesmo início vazio para os dois, comparação pareada por unidade.",
    ),
    (
        "folga concentrada na execução da matriz e nos estados de referência dos <em>tickets</em>.",
        "folga concentrada na execução da matriz e na escrita da especificação e dos testes de aceitação.",
    ),
]

M.append((
    "conta requisições, tokens e latência da mesma forma para os dois; n ≥ 3 execuções por célula.",
    "conta requisições, tokens e latência da mesma forma para os dois; n ≥ 3 construções por célula.",
))

# T1..T9 chips of the Finn slide become U1..U9.
CHIPS = ["tenant", "governança", "flags", "pipeline de voz", "confirmação", "log", "relatório", "agendador", "cobrança"]
for i, name in enumerate(CHIPS, start=1):
    M.append((f"font-size:23px\">T{i} {name}</span>", f"font-size:23px\">U{i} {name}</span>"))

# --- speaker notes (identical text in both decks) ---------------------------
N: list[tuple[str, str]] = [
    (
        "será construído com o OpenCode e com o pi, sobre o mesmo modelo, ticket a ticket, e os tokens de cada braço serão contados fora do harness.\" Ler o problema",
        "será construído com o OpenCode e com o pi, sobre o mesmo modelo e a partir da mesma especificação, e os tokens que cada braço gastar até entregar o produto serão contados fora do harness.\" Ler o problema",
    ),
    (
        "será construído com o OpenCode e com o pi, sobre o mesmo modelo, ticket a ticket, e os tokens de cada braço serão contados fora do harness.\" Dizer em voz alta a ordem: produto → dois braços → proxy → critério.",
        "será construído com o OpenCode e com o pi, sobre o mesmo modelo e a partir da mesma especificação, e os tokens que cada braço gastar até entregar o produto serão contados fora do harness.\" Dizer em voz alta a ordem: especificação → dois braços do zero → proxy → critério. Se perguntarem por que não deixar o OpenCode construir e gerar a spec para o pi: entrada desigual, o pi receberia um documento destilado de um sistema pronto e a diferença deixaria de ser atribuível ao harness.",
    ),
    (
        "2 Finn em tickets com testes de aceitação do autor, independentes dos testes do agente; 3 espaço de trabalho congelado e idêntico por ticket, a partir de um estado de referência do autor; 4 cada ticket nos dois harnesses, mesmo modelo e prompt, repetição e dispersão;",
        "2 especificação do Finn em nove unidades, a partir das decisões do repositório, com testes de aceitação do autor independentes dos testes do agente; 3 espaço de trabalho inicial idêntico, só especificação e pilha, congelado por hash; 4 construção completa nos dois harnesses, unidade a unidade, mesmo modelo e prompts, repetição e dispersão;",
    ),
    (
        "H1 refutada se os intervalos de tokens por ticket concluído dos dois braços se sobrepuserem ao longo de toda a suíte.",
        "H1 refutada se os intervalos de tokens por construção dos dois braços se sobrepuserem e o teste pareado por unidade não apontar diferença.",
    ),
    (
        "compensar a carga extra concluindo o ticket em menos passos\".",
        "compensar a carga extra concluindo a unidade em menos passos\".",
    ),
    (
        "\"porque a comparação de dois harnesses construindo o mesmo produto completo, ticket a ticket, não tem precedente publicado\"; experimental, VI o harness, controladas modelo, ticket, espaço de trabalho e limites;",
        "\"porque a comparação de dois harnesses construindo o mesmo produto completo do zero, a partir da mesma especificação, não tem precedente publicado\"; experimental, VI o harness, controladas modelo, especificação, espaço de trabalho inicial e limites;",
    ),
    (
        "Camada 2: desfecho dos tickets contra o modelo real, estocástica, consome cota.",
        "Camada 2: construção do produto contra o modelo real, estocástica, consome cota.",
    ),
    (
        "Limite único: relógio de parede 3x a maior mediana dos braços nos tickets-piloto; sem teto de passos [64].",
        "Limite único: relógio de parede por unidade, 3x a maior mediana dos braços nas unidades-piloto; sem teto de passos [64].",
    ),
    (
        "[61]: Finn (YuukiFST, 2026a), 21 tickets fechados no repositório; os nove técnicos são as tarefas (#15 tenant, #16 governança, #17 flags, #14 pipeline de voz, #20 confirmação, #21 log, #19 relatório, #18 agendador, #22 cobrança). Prompt idêntico com decisão, restrições e pilha (TypeScript, TanStack Start, tRPC, Drizzle, PostgreSQL, Vitest). Espaço de trabalho congelado por SHA-256: estado de referência escrito pelo autor após o ticket anterior; o que o agente produziu não entra no seguinte. Escore: fração dos testes de aceitação do autor, held-out; ticket concluído quando todos passam. Células n ≥ 3 [65]; dois níveis gratuitos no mesmo gateway [62]. Classes [67]: não concluído = resultado com a fração aprovada; descartada = medição inconfiável.",
        "[61]: Finn (YuukiFST, 2026a), 21 tickets fechados no repositório; o autor escreve, antes de qualquer execução, uma especificação única congelada por SHA-256: produto, pilha (TypeScript, TanStack Start, tRPC, Drizzle, PostgreSQL, Vitest), restrições gerais e nove unidades em ordem de dependência (#15 tenant, #16 governança, #17 flags, #14 pipeline de voz, #20 confirmação, #21 log, #19 relatório, #18 agendador, #22 cobrança). Os dois braços recebem os mesmos bytes e constroem do zero em um único espaço de trabalho: o executor invoca o harness uma vez por unidade, em ordem, com prompt idêntico; o que o agente construiu em uma unidade é o ponto de partida da seguinte; o autor não escreve código depois do início. Escore: fração dos testes de aceitação do autor, held-out, rodados sobre uma cópia do espaço ao fim de cada unidade; unidade concluída quando todos os seus testes passam, construção concluída quando todos passam ao fim. Células (braço, nível) com n ≥ 3 construções [65]; dois níveis gratuitos no mesmo gateway [62]. Classes [67]: não concluída = resultado com a fração aprovada, a construção segue; descartada = medição inconfiável descarta a construção.",
    ),
    (
        "Tokens por ticket concluído, contados no proxy, e Succ/Mtok de Lin et al. (2026). Wilcoxon dos postos sinalizados, bilateral, α = 0,05, pareado por ticket, sobre as duas medidas; não paramétrico porque nove pares não sustentam suposição distribucional; pareado porque a dificuldade do ticket é o maior fator de perturbação (Miller, 2024). MDE ≈ 0,76σ com n = 3 e 9 tickets. Para H2: tokens decompostos em carga fixa (Camada 1 x passos) e conversa, parcela reportada por ticket. O painel é simulação: dificuldades dos 9 tickets são multiplicadores ilustrativos;",
        "Medida principal: tokens por construção, contados no proxy, sempre ao lado da fração final de testes aprovados (um braço que falha barato não pode parecer o mais barato); Succ/Mtok de Lin et al. (2026). Wilcoxon dos postos sinalizados, bilateral, α = 0,05, pareado por unidade, sobre tokens por unidade e Succ/Mtok por unidade; não paramétrico porque nove pares não sustentam suposição distribucional; pareado porque a dificuldade da unidade é o maior fator de perturbação (Miller, 2024). Unidades não são independentes: a seguinte parte do que o mesmo braço construiu; essa dependência é custo do harness e é reportada por unidade. MDE ≈ 0,76σ com n = 3 e 9 unidades. Para H2: tokens decompostos em carga fixa (Camada 1 x passos) e conversa, parcela reportada por unidade e por construção. O painel é simulação: dificuldades das 9 unidades são multiplicadores ilustrativos;",
    ),
    (
        "estado de referência escrito pelo autor (mitigação: mesmo estado para os dois braços, comparação pareada);",
        "especificação escrita pelo autor e cada braço carregando os próprios erros de uma unidade à seguinte (mitigação: mesma entrada e mesmo início vazio para os dois, comparação pareada por unidade);",
    ),
    (
        "out–nov instrumento e estados de referência dos tickets;",
        "out–nov instrumento, especificação e testes de aceitação;",
    ),
    (
        "Os 9 tickets técnicos (#14–#22) são as tarefas; os agentes recebem o mesmo estado de referência e o mesmo prompt, e o escore é a fração dos testes de aceitação do autor.",
        "Os 9 tickets técnicos (#14–#22) viram as 9 unidades de uma especificação única; os agentes recebem a mesma especificação, os mesmos prompts e o mesmo espaço vazio, constroem do zero, e o escore é a fração dos testes de aceitação do autor.",
    ),
]

# --- dist-only script strings --------------------------------------------------
D: list[tuple[str, str]] = [
    (
        "'desfecho do ticket · proxy reverso conta cada requisição · estocástica, n ≥ 3 por célula'",
        "'construção do produto · proxy reverso conta cada requisição · estocástica, n ≥ 3 por célula'",
    ),
    (
        "aria-label=\"${a}, ticket ${t}, ${tier}\"",
        "aria-label=\"${a}, unidade ${t}, ${tier}\"",
    ),
    (
        "h+=`<div class=\"hdr\">T${t}</div>`",
        "h+=`<div class=\"hdr\">U${t}</div>`",
    ),
    (
        "`Célula (<b>${c.dataset.a}</b>, ticket T${c.dataset.t}, ${c.dataset.tier}): n ≥ 3 execuções completas após descartes; mediana com dispersão; pareada com a célula do outro braço no mesmo ticket e nível.`",
        "`Célula (<b>${c.dataset.a}</b>, ${c.dataset.tier}), unidade U${c.dataset.t}: n ≥ 3 construções completas após descartes; tokens da unidade como mediana com dispersão; pareada com a mesma unidade do outro braço no mesmo nível.`",
    ),
    (
        "Succ/Mtok por ticket · A (âmbar) vs B (azul)",
        "Succ/Mtok por unidade · A (âmbar) vs B (azul)",
    ),
    (
        "['Construção do instrumento e dos estados de referência',[0,0,1,1,0,0]],",
        "['Instrumento, especificação e testes de aceitação',[0,0,1,1,0,0]],",
    ),
]

# --- deck TypeScript -------------------------------------------------------------
TS: dict[str, list[tuple[str, str]]] = {
    "deck/src/content.ts": [
        (
            '{ phase: "Construção do instrumento e dos estados de referência", months: [0, 0, 1, 1, 0, 0] },',
            '{ phase: "Instrumento, especificação e testes de aceitação", months: [0, 0, 1, 1, 0, 0] },',
        ),
        (
            'w: "VI: <em>harness</em> · controladas: modelo, <em>ticket</em>, espaço de trabalho, limites",',
            'w: "VI: <em>harness</em> · controladas: modelo, especificação, espaço de trabalho inicial, limites",',
        ),
        (
            '"<b>2</b> Finn em <em>tickets</em> com testes de aceitação do autor",',
            '"<b>2</b> Especificação do Finn em 9 unidades, com testes de aceitação do autor",',
        ),
        (
            '"<b>3</b> Espaço de trabalho congelado e idêntico por <em>ticket</em>",',
            '"<b>3</b> Espaço de trabalho inicial idêntico: só a especificação e a pilha",',
        ),
        (
            '"<b>4</b> Cada <em>ticket</em> nos dois <em>harnesses</em>, mesmo modelo e <em>prompt</em>, n ≥ 3",',
            '"<b>4</b> Construção completa nos dois <em>harnesses</em>, mesmo modelo e <em>prompts</em>, n ≥ 3",',
        ),
    ],
    "deck/src/slides/flow.ts": [
        (
            '"desfecho do ticket · proxy reverso conta cada requisição · estocástica, n ≥ 3 por célula"',
            '"construção do produto · proxy reverso conta cada requisição · estocástica, n ≥ 3 por célula"',
        ),
    ],
    "deck/src/slides/matrix.ts": [
        ('h += `<div class="hdr">T${t}</div>`;', 'h += `<div class="hdr">U${t}</div>`;'),
        ('aria-label="${a}, ticket ${t}, ${tier}"', 'aria-label="${a}, unidade ${t}, ${tier}"'),
        (
            "info.innerHTML = `Célula (<b>${cell.dataset.a}</b>, ticket T${cell.dataset.t}, ${cell.dataset.tier}): n ≥ 3 execuções completas após descartes; mediana com dispersão; pareada com a célula do outro braço no mesmo ticket e nível.`;",
            "info.innerHTML = `Célula (<b>${cell.dataset.a}</b>, ${cell.dataset.tier}), unidade U${cell.dataset.t}: n ≥ 3 construções completas após descartes; tokens da unidade como mediana com dispersão; pareada com a mesma unidade do outro braço no mesmo nível.`;",
        ),
    ],
    "deck/src/slides/succ.ts": [
        ("Succ/Mtok por ticket · A (âmbar) vs B (azul)", "Succ/Mtok por unidade · A (âmbar) vs B (azul)"),
        ('font-size="22">T${i + 1}</text>', 'font-size="22">U${i + 1}</text>'),
        ("<title>T${i + 1}: A ${A[i].toFixed(2)} vs B ${B[i].toFixed(2)}</title>", "<title>U${i + 1}: A ${A[i].toFixed(2)} vs B ${B[i].toFixed(2)}</title>"),
        ("<title>A · T${i + 1}: ${A[i].toFixed(2)}</title>", "<title>A · U${i + 1}: ${A[i].toFixed(2)}</title>"),
        ("<title>B · T${i + 1}: ${B[i].toFixed(2)}</title>", "<title>B · U${i + 1}: ${B[i].toFixed(2)}</title>"),
    ],
    "deck/src/notes.ts": N,
}

D += [
    ("font-size=\"22\">T${i+1}</text>", "font-size=\"22\">U${i+1}</text>"),
]

# The deck's objective items live both in content.ts and, as the initial
# markup, in index.html.
DECK_MARKUP = list(M)
DECK_MARKUP = [
    (o.replace('style="color:var(--bad)"', 'style="color: var(--bad)"'), n.replace('style="color:var(--bad)"', 'style="color: var(--bad)"'))
    for o, n in DECK_MARKUP
]
# The deck denom carries the citation.
DECK_MARKUP = [
    (o.replace("Finn: SaaS multiempresa", "Finn (YuukiFST, 2026a): SaaS multiempresa"), n.replace("Finn: SaaS multiempresa", "Finn (YuukiFST, 2026a): SaaS multiempresa"))
    for o, n in DECK_MARKUP
]
# Prettier glued "·<span" in the classes card.
DECK_MARKUP = [
    (o.replace("classe</b> · <span", "classe</b> ·<span"), n.replace("classe</b> · <span", "classe</b> ·<span"))
    for o, n in DECK_MARKUP
]
# Prettier breaks the chip attributes across lines; match the text alone.
DECK_MARKUP = [p for p in DECK_MARKUP if not p[0].startswith("font-size:23px")]
DECK_MARKUP += [(f">T{i} {name}</span", f">U{i} {name}</span") for i, name in enumerate(CHIPS, start=1)]

apply(Path("dist/apresentacao-pcc.html"), M + N + D, tolerant=False)
apply(Path("deck/index.html"), DECK_MARKUP, tolerant=True)
for path, pairs in TS.items():
    apply(Path(path), pairs, tolerant=False)
