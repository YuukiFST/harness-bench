"""Rewrite dist/apresentacao-pcc.html for the Finn experiment (2026-09-14).

Exact-string replacements over the single-file deck, mirroring
tools/pcc_edits_2026-09-14.py: the arms become OpenCode and pi, the suite
becomes the nine technical tickets of Finn, and the Camada 1 figure compares
pi with OpenCode using layer1/data (28 ago. 2026). Every pair must match
exactly once; the script aborts otherwise so a silent miss cannot ship.

Usage:
    python tools/slides_edits_2026-09-14.py
"""

from pathlib import Path

HTML = Path("dist/apresentacao-pcc.html")

R: list[tuple[str, str]] = []

# --- capa -------------------------------------------------------------------
R.append((
    "custo por tarefa concluída e taxa de sucesso de agentes de codificação sob um mesmo modelo</div>",
    "tokens e taxa de sucesso do OpenCode e do pi na construção de um mesmo SaaS sob um mesmo modelo</div>",
))

# --- slide 2: barras --------------------------------------------------------
R.append((
    "o gráfico mostra as 7 com valor no texto do post. Razão 17,5× calculada pelo autor. Blogue institucional, não revisado por pares.</div>",
    "o gráfico mostra as 7 com valor no texto do post; Pi e OpenCode, em âmbar, são os dois braços deste projeto. Razão 17,5× calculada pelo autor. Blogue institucional, não revisado por pares.</div>",
))
R.append((
    "r.innerHTML=`<div>${n}</div>",
    "r.innerHTML=`<div${n==='Pi'||n==='OpenCode'?' class=\"acc\" style=\"font-weight:700\"':''}>${n}</div>",
))

# --- slide 3: harness 3D ----------------------------------------------------
R.append((
    "Molda o estilo de trabalho. Na Camada 1, pi envia 2.499 bytes; oh-my-pi, 25.395 (10,2×).",
    "Molda o estilo de trabalho. Na Camada 1, pi envia 2.499 bytes; OpenCode, 9.738 (3,9×).",
))
R.append((
    "Esquemas viajam a cada requisição: 4 no pi, 11 no oh-my-pi.",
    "Esquemas viajam a cada requisição: 4 no pi, 9 no OpenCode.",
))
R.append((
    "Conta requisições, tokens e latência igual para todos os braços.',src:'Projeto, §3 [63]; objetivo 1'",
    "Conta requisições, tokens e latência igual para os dois braços.',src:'Projeto, §3 [63]; objetivo 1'",
))

# --- slide 4: justificativa, tema, problema, objetivo geral ------------------
R.append((
    "As comparações publicadas contrastam equipes diferentes e não dizem qual decisão de projeto pesa.</div>",
    "As comparações publicadas usam tarefas isoladas e não dizem quanto custa entregar um produto inteiro com uma ferramenta em vez de outra.</div>",
))
R.append((
    "a escolha do <em>harness</em> como decisão de engenharia: efeito sobre custo por tarefa concluída e taxa de sucesso, modelo fixo.</div>",
    "a escolha do <em>harness</em> como decisão de engenharia: efeito sobre tokens consumidos e taxa de sucesso na construção de um mesmo produto, modelo fixo.</div>",
))
R.append((
    "com o modelo já escolhido, quanto do custo e do sucesso vem do <em>harness</em>? Quais decisões de projeto explicam a diferença?</div>",
    "com o modelo já escolhido, quantos tokens a mais ou a menos custa construir o mesmo software com um <em>harness</em> em vez de outro? Quanto vem da carga fixa por requisição?</div>",
))
R.append((
    "medir esse efeito, isolar decisões pela comparação <em>harness</em> × <em>fork</em> direto, entregar critério de escolha reproduzível.</div>",
    "medir a diferença de tokens e de sucesso entre OpenCode e pi construindo o Finn, <em>ticket</em> a <em>ticket</em>; separar a parte que vem da carga fixa; entregar critério reproduzível.</div>",
))

# --- slide 5: objetivos específicos -----------------------------------------
R.append((
    '<li class="frag"><b>2</b> Suíte com objetivos numerados e <em>oracle</em> próprio</li>',
    '<li class="frag"><b>2</b> Finn em <em>tickets</em> com testes de aceitação do autor</li>',
))
R.append((
    '<li class="frag"><b>3</b> <em>Harness</em> zero em laço ReAct (controle)</li>',
    '<li class="frag"><b>3</b> Espaço de trabalho congelado e idêntico por <em>ticket</em></li>',
))
R.append((
    '<li class="frag"><b>4</b> Mesma suíte, mesmo modelo, todos os braços, com repetição</li>',
    '<li class="frag"><b>4</b> Cada <em>ticket</em> nos dois <em>harnesses</em>, mesmo modelo e <em>prompt</em>, n ≥ 3</li>',
))
R.append((
    '<li class="frag"><b>6</b> Custo relatado × custo medido no <em>proxy</em></li>',
    '<li class="frag"><b>6</b> Tokens relatados × tokens medidos no <em>proxy</em></li>',
))
R.append((
    '<li class="frag"><b>7</b> Publicar <em>runner</em>, dados e scripts, custo zero</li>',
    '<li class="frag"><b>7</b> Publicar executor, <em>prompts</em>, testes, dados e scripts, custo zero</li>',
))

# --- slide 6: hipóteses -----------------------------------------------------
R.append((
    "entre <em>harnesses</em> distintos no mesmo modelo, a diferença de custo por tarefa é relevante para quem paga, comparável a trocar de modelo. <span class=\"mute\">Refutada se os intervalos de Succ/Mtok se sobrepuserem em toda a suíte.</span></div>",
    "entre OpenCode e pi no mesmo modelo, a diferença de tokens por <em>ticket</em> concluído é relevante para quem paga, comparável a trocar de modelo. <span class=\"mute\">Refutada se os intervalos de tokens por <em>ticket</em> se sobrepuserem em toda a suíte.</span></div>",
))
R.append((
    "a diferença persiste entre um <em>harness</em> e seu <em>fork</em> direto: decisões isoláveis, não acúmulo de bases distintas. <span class=\"mute\">Refutada se pi e oh-my-pi não diferirem em Succ/Mtok.</span></div>",
    "a carga fixa por requisição (<em>prompt</em> de sistema e esquemas, Camada 1) explica a maior parte da diferença; o número de passos, a parte menor. <span class=\"mute\">Refutada se o número de passos explicar a maior parte.</span></div>",
))
R.append((
    "Camada 1, medição própria: primeira requisição da mesma tarefa, endpoint simulado, n = 1 (determinístico), tokenizador cl100k_base, 28 ago. 2026. pi 0.80.10, oh-my-pi 17.2.10.</div>",
    "Camada 1, medição própria: primeira requisição da mesma tarefa, endpoint simulado, n = 1 (determinístico), tokenizador cl100k_base, 28 ago. 2026. pi 0.80.10, OpenCode 1.17.9.</div>",
))
R.append((
    "const L1={pi:{first:5676,tok:1228,schemas:4,steps:[5676,6231,6786,7341,7896]},omp:{first:64945,tok:16714,schemas:11,steps:[64945,65273,65898,66523,67148]}};",
    "const L1={pi:{first:5676,tok:1228,schemas:4,steps:[5676,6231,6786,7341,7896]},omp:{first:29997,tok:6659,schemas:9,steps:[29997,30695,31393,32091,32789]}};",
))
R.append((
    "// ---------- slide 6: pi → oh-my-pi (Camada 1, layer1/data) ----------",
    "// ---------- slide 6: pi vs OpenCode (Camada 1, layer1/data/first_request.csv e step_growth.csv) ----------",
))
R.append((
    '<line x1="345" y1="95" x2="440" y2="95" stroke="#f5b638" stroke-width="4" marker-end="url(#arr)"/><text x="392" y="70" text-anchor="middle" fill="#f5b638" font-size="20">fork</text>',
    '<text x="400" y="103" text-anchor="middle" fill="#8b98a8" font-size="26">vs</text>',
))
R.append((
    'font-size="34" font-weight="700">oh-my-pi</text>',
    'font-size="34" font-weight="700">OpenCode</text>',
))
R.append((
    '1ª requisição: <tspan fill="#f5b638" font-weight="700">11,4×</tspan> os bytes, <tspan fill="#f5b638" font-weight="700">13,6×</tspan> os tokens (16.714 vs 1.228)</text>',
    '1ª requisição: <tspan fill="#f5b638" font-weight="700">5,3×</tspan> os bytes, <tspan fill="#f5b638" font-weight="700">5,4×</tspan> os tokens (6.659 vs 1.228)</text>',
))
R.append((
    "const x0=90,y0=500,w=660,hh=240,max=70000;",
    "const x0=90,y0=500,w=660,hh=240,max=35000;",
))
R.append((
    "for(const v of[0,20000,40000,60000]){",
    "for(const v of[0,10000,20000,30000]){",
))
R.append((
    "${k==='pi'?'pi':'oh-my-pi'}</text>`;}",
    "${k==='pi'?'pi':'OpenCode'}</text>`;}",
))

# --- slide 7: linha do tempo ------------------------------------------------
R.append((
    "O laço observar/agir mínimo. É um <em>harness</em> legítimo, o mais raso; ponto de partida do <em>harness</em> zero.</p></div>",
    "O laço observar/agir mínimo. É um <em>harness</em> legítimo, o mais raso; o pi fica perto dele.</p></div>",
))
R.append((
    "['2022','Yao <em>et al.</em> · ReAct','O laço observar/agir mínimo. É um <em>harness</em> legítimo, o mais raso; ponto de partida do <em>harness</em> zero.'],",
    "['2022','Yao <em>et al.</em> · ReAct','O laço observar/agir mínimo. É um <em>harness</em> legítimo, o mais raso; o pi, com quatro ferramentas, fica perto dele.'],",
))

# --- slide 8: classificação -------------------------------------------------
R.append((
    '<span class="w">medir custo e sucesso; atribuir a decisão</span>',
    '<span class="w">medir tokens e sucesso; atribuir à carga fixa ou aos passos</span>',
))
R.append((
    '<span class="w">linhagem fixa sem precedente</span>',
    '<span class="w">mesmo produto completo, dois <em>harnesses</em>, sem precedente</span>',
))
R.append((
    '<span class="w">VI: <em>harness</em> · controladas: modelo, tarefa, limites · grupo de controle</span>',
    '<span class="w">VI: <em>harness</em> · controladas: modelo, <em>ticket</em>, espaço de trabalho, limites</span>',
))

# --- slide 9: duas camadas --------------------------------------------------
R.append((
    "Esquemas, bytes de prompt, tokens por passo. Determinística, sem cota.</div>",
    "Esquemas, bytes de prompt, tokens por passo. Determinística, sem cota. Dá a carga fixa de H2.</div>",
))
R.append((
    "desfecho das tarefas no modelo real via <em>proxy</em> reverso. Estocástica, consome cota, n ≥ 3.</div>",
    "desfecho dos <em>tickets</em> no modelo real via <em>proxy</em> reverso. Estocástica, consome cota, n ≥ 3.</div>",
))
R.append((
    "um só tokenizador para todos os braços; o relatório do <em>gateway</em> fica para verificação cruzada.</div>",
    "um só tokenizador para os dois braços; o relatório do <em>gateway</em> fica para verificação cruzada.</div>",
))
R.append((
    "desfecho da tarefa · proxy reverso conta cada requisição · estocástica, n ≥ 3 por célula",
    "desfecho do ticket · proxy reverso conta cada requisição · estocástica, n ≥ 3 por célula",
))

# --- slide 10: braços e matriz ---------------------------------------------
R.append((
    "<h2>Braços e matriz (braço × tarefa × nível)<small>clique ou navegue com Tab em uma célula · cada célula recebe n ≥ 3 execuções após descartes</small></h2>",
    "<h2>Braços e matriz (braço × <em>ticket</em> × nível)<small>clique ou navegue com Tab em uma célula · cada célula recebe n ≥ 3 execuções após descartes</small></h2>",
))
R.append((
    '<div class="card hi" style="padding:20px 30px"><b class="acc"><em>Harness</em> zero</b> · controle. Laço observar/agir, 3 ferramentas, &lt; 400 linhas de Python, sem planejamento, compactação ou <em>retry</em>.</div>',
    '<div class="card hi" style="padding:20px 30px"><b class="acc">Braços</b> · OpenCode e pi: código aberto, sem interface (<code>opencode run</code>, <code>pi --mode json</code>), URL base OpenAI-compatível. Nenhum <em>harness</em> escrito pelo projeto.</div>',
))
R.append((
    '<div class="card" style="padding:20px 30px"><b class="acc">Suíte</b> · 8 tarefas Python do DeepSWE, fixadas por <em>commit</em> e SHA-256. Crédito parcial: fração de testes do verificador.</div>',
    '<div class="card" style="padding:20px 30px"><b class="acc">Suíte</b> · Finn, 9 <em>tickets</em> técnicos; espaço de trabalho congelado por SHA-256 a cada <em>ticket</em>. Escore: fração dos testes de aceitação do autor, <em>held-out</em>.</div>',
))
R.append((
    '<div class="card" style="padding:20px 30px"><b class="acc">Limite único</b> · relógio de parede 3× a mediana do <em>harness</em> zero nas tarefas-piloto. Sem teto de passos, já que o teto seria uma decisão de projeto do <em>harness</em>. Saída máxima idêntica via <em>proxy</em>.</div>',
    '<div class="card" style="padding:20px 30px"><b class="acc">Limite único</b> · relógio de parede 3× a maior mediana dos braços nos <em>tickets</em>-piloto. Sem teto de passos, já que o teto seria uma decisão de projeto do <em>harness</em>. Saída máxima idêntica via <em>proxy</em>.</div>',
))
R.append((
    '<div class="denom">DeepSWE (Huang <em>et al.</em>, 2026): 113 tarefas, 91 repositórios; soluções de referência com 668 linhas em média, contra 32,8 no SWE-bench. Braços provisórios até os portões de confiabilidade.</div>',
    '<div class="denom">Finn (YuukiFST, 2026a): SaaS multiempresa de financeiro por voz, 21 <em>tickets</em> fechados antes do experimento; pilha fixa TypeScript, TanStack Start, tRPC, Drizzle, PostgreSQL, Vitest. T1 tenant · T2 governança · T3 <em>flags</em> · T4 <em>pipeline</em> de voz · T5 confirmação · T6 log · T7 relatório · T8 agendador · T9 cobrança.</div>',
))
R.append((
    "const arms=['harness zero','pi','oh-my-pi','terceiros…'];const tasks=8,tiers=['nível primário','nível de robustez'];",
    "const arms=['OpenCode','pi'];const tasks=9,tiers=['nível primário','nível de robustez'];",
))
R.append((
    "m.style.gridTemplateColumns='190px repeat(8,1fr)';",
    "m.style.gridTemplateColumns='190px repeat(9,1fr)';",
))
R.append((
    "<div class=\"hdr\" style=\"justify-content:flex-end;padding-right:10px;color:${ai?'#e8edf2':'#f5b638'}\">${a}</div>`;for(let t=1;t<=tasks;t++)h+=`<button class=\"cell${ai?'':' ctrl'}\" data-a=\"${a}\" data-t=\"${t}\" data-tier=\"${tier}\" aria-label=\"${a}, tarefa ${t}, ${tier}\">n ≥ 3</button>`;});});",
    "<div class=\"hdr\" style=\"justify-content:flex-end;padding-right:10px;color:#e8edf2\">${a}</div>`;for(let t=1;t<=tasks;t++)h+=`<button class=\"cell\" data-a=\"${a}\" data-t=\"${t}\" data-tier=\"${tier}\" aria-label=\"${a}, ticket ${t}, ${tier}\">n ≥ 3</button>`;});});",
))
R.append((
    "`Célula (<b>${c.dataset.a}</b>, tarefa ${c.dataset.t}, ${c.dataset.tier}): n ≥ 3 execuções completas após descartes; mediana com dispersão; ${c.classList.contains('ctrl')?'controle: define o envelope de referência (relógio de parede 3× a mediana).':'comparada ao harness zero e ao par pi / oh-my-pi por tarefa.'}`",
    "`Célula (<b>${c.dataset.a}</b>, ticket T${c.dataset.t}, ${c.dataset.tier}): n ≥ 3 execuções completas após descartes; mediana com dispersão; pareada com a célula do outro braço no mesmo ticket e nível.`",
))

R.append((
    '<span style="color:var(--bad)">falhada</span>: agente não cumpriu; é resultado, escore zero (estouro do relógio incluído).',
    '<span style="color:var(--bad)">não concluída</span>: agente não concluiu o <em>ticket</em>; é resultado, entra com a fração de testes aprovada (estouro do relógio incluído).',
))

# --- slide 11: Succ/Mtok e Wilcoxon -----------------------------------------
R.append((
    '<div><div class="mute">Wilcoxon (8 pares)</div>',
    '<div><div class="mute">Wilcoxon (9 pares)</div>',
))
R.append((
    "Com n = 3 por célula e 8 tarefas, diferença mínima detectável ≈ 0,81σ.</div>",
    "Com n = 3 por célula e 9 <em>tickets</em>, diferença mínima detectável ≈ 0,76σ. O mesmo teste roda sobre os tokens por <em>ticket</em> concluído.</div>",
))
R.append((
    "const diff=[0.6,0.8,0.9,1.0,1.1,1.25,1.4,1.7]; // multiplicadores de dificuldade, ilustrativos",
    "const diff=[0.6,0.8,0.9,1.0,1.1,1.25,1.4,1.55,1.7]; // multiplicadores de dificuldade, ilustrativos",
))
R.append((
    "const CRIT={8:3,7:2,6:0}; // bilateral, α=0,05",
    "const CRIT={9:5,8:3,7:2,6:0}; // bilateral, α=0,05",
))
R.append((
    "for(let i=0;i<8;i++){const y=70+i*54;",
    "for(let i=0;i<9;i++){const y=64+i*49;",
))
R.append((
    '<text x="380" y="30" text-anchor="middle" fill="#8b98a8" font-size="22">Succ/Mtok por tarefa · A (âmbar) vs B (azul)</text>',
    '<text x="380" y="30" text-anchor="middle" fill="#8b98a8" font-size="22">Succ/Mtok por ticket · A (âmbar) vs B (azul)</text>',
))

# --- slide 12: limitações ---------------------------------------------------
R.append((
    '<b class="acc">Modelos pequenos</b> · fora do escopo: o único viável foi treinado dentro de um braço.</div>',
    '<b class="acc">Um produto, uma pilha</b> · o resultado vale para tarefas dessa família; outras pilhas ficam como trabalho futuro.</div>',
))
R.append((
    '<b class="acc">Sem comparação ao placar público</b> · linhas de base do DeepSWE usam <em>harness</em> de ferramenta única. Válido: braço × braço.</div>',
    '<b class="acc">Estado de referência humano</b> · o autor escreve o ponto de partida de cada <em>ticket</em>; mitigação: mesmo estado para os dois braços, comparação pareada.</div>',
))
R.append((
    '<b class="acc">Custo em dinheiro</b> · contrafactual de ordem de grandeza sobre tarifas pagas, rotulado como tal.</div>',
    '<b class="acc">Sem placar público</b> · suíte própria, válido só braço × braço; custo em dinheiro como contrafactual rotulado.</div>',
))

# --- slide 13: orçamento e cronograma ---------------------------------------
R.append((
    '<span class="mute">Executor e <em>benchmark</em> (Pier, DeepSWE; Apache-2.0)</span>',
    '<span class="mute"><em>Harnesses</em> e ferramentas (OpenCode, pi; Node.js, PostgreSQL)</span>',
))
R.append((
    "Escrita do projeto concluída em 11 set. 2026; experimentos práticos a partir de out. 2026.",
    "Escrita do projeto concluída em set. 2026; experimentos práticos a partir de out. 2026.",
))
R.append((
    "um lote da matriz por dia; folga concentrada na execução da matriz e nos portões de confiabilidade.</div>",
    "um lote da matriz por dia; folga concentrada na execução da matriz e nos estados de referência dos <em>tickets</em>.</div>",
))
R.append((
    " ['Construção do instrumento e do harness zero',[0,0,1,1,0,0]],",
    " ['Construção do instrumento e dos estados de referência',[0,0,1,1,0,0]],",
))

# --- slide 14: referências --------------------------------------------------
R.append((
    "lista completa com 25 entradas no projeto, seção 6</small></h2>",
    "lista completa com 24 entradas no projeto, seção 6</small></h2>",
))
R.append((
    " 'DATACURVE. <b>Pier</b>: a Harbor fork built for DeepSWE. 2026. Repositório de código.',\n",
    " 'EARENDIL. <b>Pi, minimal and performant</b>. 2026. Blogue institucional.',\n",
))
R.append((
    " 'HUANG, W. <em>et al.</em> <b>DeepSWE</b>: measuring frontier coding agents on original, long-horizon engineering tasks. arXiv:2607.07946, 2026. <em>Preprint</em>.',\n 'JIMENEZ, C. E. <em>et al.</em> <b>SWE-bench</b>: can language models resolve real-world GitHub issues? ICLR, 2024.',\n",
    "",
))
R.append((
    " 'NING, X. <em>et al.</em> <b>Code as agent harness</b>. arXiv:2605.18747, 2026. <em>Preprint</em>.',\n",
    " 'NING, X. <em>et al.</em> <b>Code as agent harness</b>. arXiv:2605.18747, 2026. <em>Preprint</em>.',\n 'OPENCODE. <b>OpenCode</b>: the open source coding agent. 2026a. Repositório de código.',\n",
))
R.append((
    " 'YUUKIFST. <b>harness-bench</b>: runner, dados brutos e scripts de análise deste projeto. 2026. Repositório de código.',\n",
    " 'YUUKIFST. <b>Finn</b>: SaaS universal de financeiro por voz. 2026a. Repositório de código.',\n 'YUUKIFST. <b>harness-bench</b>: executor, prompts, testes de aceitação, dados brutos e scripts de análise deste projeto. 2026b. Repositório de código.',\n",
))

# --- fecho ------------------------------------------------------------------
R.append((
    "Quanto do que o desenvolvedor paga por tarefa vem do <em>harness</em>, e de qual decisão de projeto?</h1>",
    "Quantos tokens a mais custa construir o mesmo SaaS com um <em>harness</em> em vez de outro, e quanto disso é carga fixa?</h1>",
))
R.append((
    "Repositório do projeto: github.com/YuukiFST/harness-bench (YuukiFST, 2026).</div>",
    "Repositórios: github.com/YuukiFST/harness-bench (YuukiFST, 2026b) e github.com/YuukiFST/Finn (YuukiFST, 2026a).</div>",
))

# --- notas do apresentador --------------------------------------------------
NOTES_OLD_START = "const NOTES=["
NOTES_OLD_END = "];\n\n// ---------- navegação ----------"
NOTES_NEW = r"""const NOTES=[
`<b>Capa.</b> Título, autor e orientadora [4][5][12]. Projeto de pesquisa da disciplina de Metodologia Científica, curso de Sistemas para Internet, IFMT Campus Octayde Jorge da Silva [11].`,
`<b>Justificativa [26].</b> "No FrontierHarness (Runta, 2026), doze configurações de nove harnesses sobre o mesmo modelo ficam entre 50,0% e 66,7% de aprovação, e o custo por tarefa concluída vai de US$ 1,05 a US$ 18,34, uma razão de 17,5x calculada pelo autor." Os dois braços deste projeto estão no mesmo post: pi 60,0% a US$ 2,43, OpenCode 50,0% a US$ 3,24 [26]. Também [52]: Codex 66,7% a US$ 3,47; Claude Code 63,3% a US$ 18,34 (5,3x). Os demais valores das barras vêm de wiki/sources/frontierharness-runta-2026.md, mesmo post; 30 tarefas e 1 tentativa por célula também. Quem paga é o desenvolvedor e a empresa [27].`,
`<b>Referencial [49][50].</b> Ning et al. (2026, §2): um harness "converte um modelo de linguagem sem estado em um agente funcional ao ancorar suas saídas em execução externa, estado persistente e realimentação verificável". Wang et al. (2026): monta os prompts, gerencia o estado, invoca as ferramentas e coordena o laço. Lin et al. (2026, §1): prompt de sistema, ferramentas, middleware de contexto; "conjunto de componentes externos ao modelo e editáveis". [49]: os dois braços ficam em pontos distantes dessa camada: pi perto do ReAct mínimo com quatro ferramentas; OpenCode com planejamento, compactação, subagentes e permissões. Números de bytes e esquemas: layer1/data/first_request.csv (pi 2.499 bytes de prompt de sistema e 4 esquemas; OpenCode 9.738 e 9). O proxy externo é o instrumento [63], fora do harness.`,
`<b>Justificativa [27], tema [29], problema [31], objetivo geral [33].</b> [27]: "Este projeto medirá esse custo construindo o mesmo produto duas vezes: o Finn, um SaaS de financeiro por voz, será construído com o OpenCode e com o pi, sobre o mesmo modelo, ticket a ticket, e os tokens de cada braço serão contados fora do harness." Ler o problema na íntegra [31]: "quantos tokens a mais ou a menos custa construir o mesmo software com um harness em vez de outro? E quanto dessa diferença vem da carga fixa que cada harness envia em toda requisição?"`,
`<b>Objetivos específicos [35]–[41].</b> 1 instrumento externo idêntico para os dois; 2 Finn em tickets com testes de aceitação do autor, independentes dos testes do agente; 3 espaço de trabalho congelado e idêntico por ticket, a partir de um estado de referência do autor; 4 cada ticket nos dois harnesses, mesmo modelo e prompt, repetição e dispersão; 5 segundo modelo, ordenação mantida ou invertida; 6 divergência tokens relatados vs medidos; 7 publicar executor, prompts, testes, dados e scripts a custo zero.`,
`<b>Hipóteses [45][46].</b> H1 refutada se os intervalos de tokens por ticket concluído dos dois braços se sobrepuserem ao longo de toda a suíte. H2: a carga fixa (prompt de sistema e esquemas, Camada 1) explica a maior parte da diferença; refutada se o número de passos explicar a maior parte, "desfecho possível e reportável, já que o harness com mais ferramentas pode compensar a carga extra concluindo o ticket em menos passos". Dados do gráfico: layer1/data/first_request.csv e step_growth.csv (pi 5.676 bytes / 1.228 tokens / 4 esquemas; OpenCode 29.997 bytes / 6.659 tokens / 9 esquemas; 5,3x em bytes, 5,4x em tokens; crescimento por passo 555 vs 698 bytes). Esses números não estão no projeto (proposta descreve o que será feito); estão no repositório.`,
`<b>Referencial [49]–[55].</b> Yang 2024: interface modelo-ambiente como objeto de projeto. Lin 2026 Tabela 1: 47,2% OpenCode a 71,9% Codex, GPT-5.4, Terminal-Bench 2, 89 tarefas, 24,7 pp (cálculo do autor). Zhang 2026: Binding Constraint Thesis. Alier Forment 2026: sem MCP 5,0x a 28x mais barato; pi o mais barato da matriz. HarnessRank: ordena por aprovação, custo ao lado. Databricks apud Earendil: >2x em alguns casos. Ning 2026 §5.2.1/§5.2.7: lacuna de atribuição, pede métricas por componente; este projeto responde pelo lado da medição, separando carga fixa de conversa em cada requisição [53]. Lee 2026 Tabela 7: 76,4% vs 74,7%. Kapoor 2024/2025: custo ignorado, comparações entre harnesses raras; Anthropic melhor com BrowserUse, OpenAI com SeeAct. Runta 2026: cache 25,0% vs 67,8%.`,
`<b>Classificação [43][57] e declaração de IA [58].</b> [57]: aplicada; quantitativa (tokens e sucesso) e qualitativa (atribuição à carga fixa ou aos passos); exploratória "porque a comparação de dois harnesses construindo o mesmo produto completo, ticket a ticket, não tem precedente publicado"; experimental, VI o harness, controladas modelo, ticket, espaço de trabalho e limites; dedutiva (Gil, 2022; Prodanov; Freitas, 2013). [58]: LLM Wiki no repositório (YuukiFST, 2026b); Portaria CNPq 2.664/2026 pede ferramenta e finalidade (Brasil, 2026); ferramenta Claude Code; o autor curou as fontes, conferiu cada citação na obra original e responde pelo texto final.`,
`<b>Método [59][63][64].</b> Camada 1: forma da requisição contra endpoint simulado; determinística, sem cota; "fornece a carga fixa por requisição de que H2 depende". Camada 2: desfecho dos tickets contra o modelo real, estocástica, consome cota. "Mais bytes por requisição não significam, por si, resultado pior." Proxy reverso força o relatório de uso, conta tokens sobre os bytes transmitidos com um único tokenizador; o gateway injeta conteúdo, deslocamento aditivo por requisição que não se cancela em razão [63]. Limite único: relógio de parede 3x a maior mediana dos braços nos tickets-piloto; sem teto de passos [64].`,
`<b>Braços [60], suíte [61], limite [64], células [65], classes [67].</b> [60]: OpenCode (Opencode, 2026a) e pi (Earendil, 2026); código aberto, headless (opencode run, pi --mode json), URL base OpenAI-compatível; "Este projeto não escreve harness algum; escreve o instrumento, os prompts e os testes de aceitação." [61]: Finn (YuukiFST, 2026a), 21 tickets fechados no repositório; os nove técnicos são as tarefas (#15 tenant, #16 governança, #17 flags, #14 pipeline de voz, #20 confirmação, #21 log, #19 relatório, #18 agendador, #22 cobrança). Prompt idêntico com decisão, restrições e pilha (TypeScript, TanStack Start, tRPC, Drizzle, PostgreSQL, Vitest). Espaço de trabalho congelado por SHA-256: estado de referência escrito pelo autor após o ticket anterior; o que o agente produziu não entra no seguinte. Escore: fração dos testes de aceitação do autor, held-out; ticket concluído quando todos passam. Células n ≥ 3 [65]; dois níveis gratuitos no mesmo gateway [62]. Classes [67]: não concluído = resultado com a fração aprovada; descartada = medição inconfiável.`,
`<b>Métrica e estatística [55][66].</b> Tokens por ticket concluído, contados no proxy, e Succ/Mtok de Lin et al. (2026). Wilcoxon dos postos sinalizados, bilateral, α = 0,05, pareado por ticket, sobre as duas medidas; não paramétrico porque nove pares não sustentam suposição distribucional; pareado porque a dificuldade do ticket é o maior fator de perturbação (Miller, 2024). MDE ≈ 0,76σ com n = 3 e 9 tickets. Para H2: tokens decompostos em carga fixa (Camada 1 x passos) e conversa, parcela reportada por ticket. O painel é simulação: dificuldades dos 9 tickets são multiplicadores ilustrativos; valor crítico de W para n = 9, bilateral, α = 0,05 é 5.`,
`<b>Limitações [69].</b> Quatro declaradas: efeito específico do modelo (pode inverter; objetivo 5); um único produto sobre uma única pilha (transferência como trabalho futuro); estado de referência escrito pelo autor (mitigação: mesmo estado para os dois braços, comparação pareada); valores absolutos sem placar público, dólares externos de outros modelos e níveis pagos, custo em dinheiro como contrafactual rotulado. Variância como principal ameaça [65]. O gráfico de barras do slide é ilustrativo; a evidência real de inversão é Kapoor et al. (2025) [55].`,
`<b>Orçamento [71]–[83]:</b> inferência R$ 0,00 (nível gratuito do gateway), harnesses e ferramentas R$ 0,00 (OpenCode e pi, código aberto; Node.js e PostgreSQL), máquinas R$ 0,00 (estação NixOS e estação Windows). Cota gratuita é o limite vinculante; lotes ao longo de dias. <b>Cronograma [85]–[163]:</b> ago–set leitura, definição do tema e toda a escrita (concluída em set. 2026); out–nov instrumento e estados de referência dos tickets; matriz dez–jan; análise em jan; revisão final e apresentação em set; experimentos práticos a partir de out.`,
`<b>Referências [166]–[190].</b> Lista completa com 24 entradas no projeto. Preprints marcados. Aqui só as citadas nos slides: sem as três normas ABNT, IFMT (2022), HarnessRank e Opencode Zen (2026b), citadas só no texto do projeto.`,
`<b>Fecho.</b> Retomar o problema [31] e o produto [57]: um critério de escolha que um desenvolvedor ou uma empresa poderá aplicar. Repositórios YuukiFST/Finn [188] e YuukiFST/harness-bench [189].`
"""


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    for old, new in R:
        n = html.count(old)
        if n != 1:
            raise SystemExit(f"expected 1 match, found {n}:\n{old[:120]}")
        html = html.replace(old, new)
    a = html.index(NOTES_OLD_START)
    b = html.index(NOTES_OLD_END)
    html = html[:a] + NOTES_NEW + html[b:]
    HTML.write_text(html, encoding="utf-8")
    print(f"applied {len(R)} replacements and rewrote NOTES in {HTML}")


if __name__ == "__main__":
    main()
