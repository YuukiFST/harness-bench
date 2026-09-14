"""Aligns dist/roteiro-apresentacao.html with the 17-slide deck (2026-09-14).

Follows the redesign of tools/slides_edits_2026-09-14e.py: each arm builds
the whole Finn from one frozen specification in nine units, in one
workspace; the primary metric is tokens per construction, paired per unit;
a cell is (braço, nível). "ticket", "estado de referência" and "tokens por
ticket concluído" leave the script; slide numbers follow the deck; the
Hypotheses slide is described with its external sources (Runta, Earendil)
and the Layer 1 numbers move to the question bank of that slide; three new
sections cover the slides the script never had (Finn, Como o projeto
funciona, Referências).

Every pair is an exact, single-occurrence replacement. Pairs already applied
are skipped, so the script can be rerun.

Usage:
    python tools/roteiro_edits_2026-09-14.py
"""

from pathlib import Path

PATH = Path("dist/roteiro-apresentacao.html")

PAIRS: list[tuple[str, str]] = [
    # --- header -------------------------------------------------------------
    (
        "Companheiro de <code>dist/apresentacao-pcc.html</code> (14 slides).",
        "Companheiro de <code>dist/apresentacao-pcc/index.html</code> (17 slides).",
    ),
    (
        "Cada slide traz um tempo sugerido; a soma dá 12 min. Se a banca der 10 min, corte os slides 5 e 11 pela metade. Se der 15, alongue o 3 e o 10.",
        "Cada slide traz um tempo sugerido; a soma dá cerca de 18 min, então já ensaie com cortes. Se a banca der 10 min, pule os slides 7 e 16 e corte o 13 pela metade. Se der 15, pule só o 16.",
    ),
    (
        "o deck só cita autores no slide 7 (linha do tempo). Nos outros slides a fonte fica na sua boca.",
        "o deck cita autores na tela nos slides 3, 8, 9 (linha do tempo), 10, 13 e 16. Nos outros slides a fonte fica na sua boca.",
    ),
    # --- pitch --------------------------------------------------------------
    (
        "constrói o mesmo produto, o Finn, duas vezes, com OpenCode e com pi, ticket a ticket, sobre o mesmo modelo,",
        "constrói o mesmo produto, o Finn, duas vezes, com OpenCode e com pi, a partir da mesma especificação, unidade a unidade, sobre o mesmo modelo,",
    ),
    (
        "Camada 2: os tickets do Finn contra o modelo real, via <em>proxy</em> reverso, n ≥ 3 por célula. Nove tickets técnicos, espaço de trabalho congelado por SHA-256, testes de aceitação escritos por mim. Métrica: tokens por ticket concluído e Succ/Mtok. Estatística: Wilcoxon pareado por ticket.",
        "Camada 2: a construção do Finn contra o modelo real, via <em>proxy</em> reverso, n ≥ 3 construções por célula. Uma especificação em nove unidades, congelada por SHA-256, espaço de trabalho inicial vazio, testes de aceitação escritos por mim. Métrica: tokens por construção, ao lado da fração de testes aprovados, e Succ/Mtok. Estatística: Wilcoxon pareado por unidade.",
    ),
    (
        "Efeito específico do modelo, um produto numa pilha só, estado de referência escrito por mim, sem placar público.",
        "Efeito específico do modelo, um produto numa pilha só, especificação escrita por mim e cada braço carregando os próprios erros de uma unidade à seguinte, sem placar público.",
    ),
    # --- glossary -----------------------------------------------------------
    (
        "<dt>ticket</dt><dd>Uma unidade de trabalho do Finn com testes de aceitação. Nove técnicos entram no experimento.</dd>",
        "<dt>unidade</dt><dd>Uma parte da especificação do Finn, com testes de aceitação próprios. Nove, em ordem de dependência (U1 a U9); cada uma veio de uma <em>issue</em> técnica.</dd>",
    ),
    (
        "<dt>estado de referência</dt><dd>O ponto de partida de cada ticket, escrito por mim depois do ticket anterior. O que o agente produziu não entra no ticket seguinte.</dd>",
        "<dt>especificação</dt><dd>Documento único, escrito por mim antes de qualquer execução a partir das <em>issues</em> do Finn e congelado por SHA-256: produto, pilha, restrições e as nove unidades.</dd>\n"
        "  <dt>espaço de trabalho inicial</dt><dd>O diretório de onde uma construção parte: só a especificação e a pilha. Daí em diante o espaço é do braço; o que ele construiu numa unidade é o ponto de partida da seguinte, e eu não escrevo código.</dd>\n"
        "  <dt>construção</dt><dd>Uma execução de um braço, num nível, que constrói o produto inteiro, unidade a unidade, uma invocação do <em>harness</em> por unidade.</dd>",
    ),
    (
        "Escore = fração aprovada; ticket concluído quando todos passam.</dd>",
        "Escore = fração aprovada; unidade concluída quando todos os seus testes passam, construção concluída quando todos passam ao fim.</dd>",
    ),
    (
        "<dt>célula</dt><dd>Braço × ticket × nível de modelo. Cada célula recebe n ≥ 3 execuções válidas.</dd>",
        "<dt>célula</dt><dd>Um par (braço, nível de modelo). Cada célula recebe n ≥ 3 construções válidas.</dd>",
    ),
    (
        "<dt>execução não concluída</dt><dd>O agente não fechou o ticket. É resultado: entra com a fração aprovada. Estouro do relógio incluído.</dd>",
        "<dt>unidade não concluída</dt><dd>O agente não concluiu a unidade. É resultado: entra com a fração aprovada e a construção segue para a unidade seguinte. Estouro do relógio incluído.</dd>",
    ),
    (
        "<dt>execução descartada</dt><dd>Medição inconfiável. Registrada, sem reparo nem repetição.",
        "<dt>construção descartada</dt><dd>Medição inconfiável em alguma unidade descarta a construção. Registrada, sem reparo nem repetição.",
    ),
    (
        "Pareado por ticket porque a dificuldade do ticket é o maior fator de perturbação.",
        "Pareado por unidade porque a dificuldade da unidade é o maior fator de perturbação.",
    ),
    (
        "Com n = 3 por célula e 9 tickets, ≈ 0,76σ.",
        "Com n = 3 por célula e 9 unidades, ≈ 0,76σ.",
    ),
    # --- slide 2 -------------------------------------------------------------
    (
        "A evidência revisada por pares do efeito do <em>harness</em> está no slide 7: SWE-agent (NeurIPS 2024).",
        "A evidência revisada por pares do efeito do <em>harness</em> está no slide 9: SWE-agent (NeurIPS 2024).",
    ),
    # --- slide 4 -------------------------------------------------------------
    (
        "Objetivo geral: medir a diferença de tokens e de sucesso entre OpenCode e pi construindo o Finn, ticket a ticket; separar",
        "Objetivo geral: medir a diferença de tokens e de sucesso entre OpenCode e pi construindo o mesmo SaaS a partir da mesma especificação; separar",
    ),
    # --- new slides 5 and 6, inserted before the objectives card -------------
    (
        '<div class="card slide"><span class="n">5</span>\n<h3>Sete objetivos específicos</h3>',
        '<div class="card slide"><span class="n">5</span>\n'
        "<h3>Finn: o produto</h3>\n"
        '<p class="meta"><b>60 s</b> · <kbd>→</kbd> revela os cartões; o <em>pipeline</em> e as nove unidades ficam na tela</p>\n'
        '<div class="blk"><b>Fale</b><div class="say">\n'
        "<p>Antes de usar o Finn como suíte, o que ele é. Um financeiro por voz para pequenas empresas. O dono fala pelo WhatsApp ou pelo aplicativo e recebe lançamento, relatório e aviso no celular. Multiempresa num banco só.</p>\n"
        "<p>Tudo isso já está decidido: 21 <em>issues</em> fechadas por mim antes do experimento. Os agentes não escolhem nada disso. O <em>pipeline</em> de voz tem sete passos na <em>issue</em> #14; aqui executar e negar aparecem juntos. Toda escrita confirma antes de valer. Custo zero por padrão: Whisper local, IA por API atrás de <em>flag</em>, desligada.</p>\n"
        "<p>As nove <em>issues</em> técnicas, #14 a #22, viram as nove unidades de uma especificação única, congelada por hash, cada uma com testes de aceitação meus. É um produto de verdade, com pilha fixa. As comparações publicadas usam suítes de tarefas soltas.</p>\n"
        "</div></div>\n"
        '<div class="blk"><b>Números</b><div class="num">\n'
        "<div><b>21 <em>issues</em></b><small>#1 mapa; #2–#10 produto; #11–#22 técnicas</small></div>\n"
        "<div><b>9 unidades</b><small>U1 tenant · U2 governança · U3 <em>flags</em> · U4 <em>pipeline</em> de voz · U5 confirmação · U6 log · U7 relatório · U8 agendador · U9 cobrança</small></div>\n"
        "</div></div>\n"
        '<div class="blk"><b>Fontes</b><ul class="src">\n'
        "<li><b>YuukiFST (2026a)</b>, github.com/YuukiFST/Finn. Cada decisão de produto tem número de <em>issue</em>; citar o número se perguntarem.</li>\n"
        "</ul></div>\n"
        '<div class="blk"><b>Se perguntarem</b><ul class="q">\n'
        '<li><b>"Por que o seu próprio produto?"</b>Porque as decisões já estão tomadas e registradas, então a especificação sai das <em>issues</em> e não da minha cabeça durante o experimento. E porque conheço a pilha o bastante para escrever os testes de aceitação.</li>\n'
        "</ul></div>\n"
        "</div>\n"
        "\n"
        '<div class="card slide"><span class="n">6</span>\n'
        "<h3>Como o projeto funciona</h3>\n"
        '<p class="meta"><b>60 s</b> · <kbd>→</kbd> revela os quatro cartões e a justificativa</p>\n'
        '<div class="blk"><b>Fale</b><div class="say">\n'
        "<p>A visão geral, em quatro passos. Uma especificação: o Finn descrito em nove unidades a partir das <em>issues</em>, cada uma com testes de aceitação meus. Dois <em>harnesses</em>: OpenCode e pi recebem a mesma especificação, os mesmos <em>prompts</em>, o mesmo espaço de trabalho vazio e o mesmo modelo, e constroem o produto do zero, unidade a unidade.</p>\n"
        "<p>Um contador externo: um <em>proxy</em> entre o <em>harness</em> e o modelo conta requisições, tokens e latência da mesma forma para os dois; n ≥ 3 construções por célula. Um critério: tokens por construção, ao lado da fração de testes aprovados, e Succ/Mtok, comparados por teste pareado por unidade; a Camada 1 separa a parte que é carga fixa.</p>\n"
        "<p>Isso justifica o tema. Quem paga é o desenvolvedor, na assinatura, e a empresa, em escala; conhecer o <em>harness</em> virou parte do ofício. As comparações publicadas usam tarefas isoladas. Este projeto mede o custo de entregar um produto inteiro.</p>\n"
        "</div></div>\n"
        '<div class="blk"><b>Se perguntarem</b><ul class="q">\n'
        '<li><b>"Por que não deixar o OpenCode construir e gerar a especificação para o pi?"</b>Entrada desigual. O pi receberia um documento destilado de um sistema pronto, e a diferença deixaria de ser atribuível ao <em>harness</em>. Por isso a especificação é minha, vem das <em>issues</em> e é a mesma para os dois.</li>\n'
        "</ul></div>\n"
        "</div>\n"
        "\n"
        '<div class="card slide"><span class="n">7</span>\n<h3>Sete objetivos específicos</h3>',
    ),
    # --- slide 7 (objectives) --------------------------------------------------
    (
        "Dois: o Finn dividido em tickets, com testes de aceitação meus, independentes dos testes do agente. Três: espaço de trabalho congelado e idêntico por ticket. Quatro: cada ticket nos dois <em>harnesses</em>, mesmo modelo, mesmo <em>prompt</em>, com repetição e dispersão.",
        "Dois: a especificação do Finn em nove unidades, com testes de aceitação meus, independentes dos testes do agente. Três: espaço de trabalho inicial idêntico, só a especificação e a pilha. Quatro: construção completa nos dois <em>harnesses</em>, unidade a unidade, mesmo modelo, mesmos <em>prompts</em>, com repetição e dispersão.",
    ),
    # --- slide 8 (hypotheses) ---------------------------------------------------
    (
        '<div class="card slide"><span class="n">6</span>\n<h3>Hipóteses H1 e H2</h3>\n<p class="meta"><b>75 s</b> · gráfico da Camada 1 anima ao entrar</p>',
        '<div class="card slide"><span class="n">8</span>\n<h3>Hipóteses H1 e H2</h3>\n<p class="meta"><b>75 s</b> · painel da direita só com fontes externas; as barras do FrontierHarness crescem ao entrar</p>',
    ),
    (
        "<p>H1: entre OpenCode e pi, no mesmo modelo, a diferença de tokens por ticket concluído é relevante para quem paga, comparável a trocar de modelo. Refutada se os intervalos dos dois braços se sobrepuserem em toda a suíte.</p>",
        "<p>H1: entre OpenCode e pi, no mesmo modelo, a diferença de tokens para construir o Finn a partir da mesma especificação é relevante para quem paga, comparável a trocar de modelo. Refutada se os intervalos de tokens por construção se sobrepuserem e o teste pareado por unidade não apontar diferença.</p>",
    ),
    (
        "um <em>harness</em> com mais ferramentas pode compensar a carga extra fechando o ticket em menos passos.</p>",
        "um <em>harness</em> com mais ferramentas pode compensar a carga extra concluindo a unidade em menos passos.</p>",
    ),
    (
        "<p>O gráfico é a Camada 1, já medida: primeira requisição da mesma tarefa, contra <em>endpoint</em> simulado. pi, 5.676 bytes e 1.228 tokens; OpenCode, 29.997 bytes e 6.659 tokens. Cinco vezes, na primeira requisição. Crescimento por passo, 555 contra 698 bytes. Isso é o que H2 quer explicar.</p>",
        "<p>O painel usa só fontes externas. Para H1, as duas linhas do FrontierHarness: pi 60,0 % a US$ 2,43 por tarefa aprovada; OpenCode 50,0 % a US$ 3,24. Mesmo modelo, e o OpenCode paga 1,33× por tarefa aprovada e aprova 10 pontos a menos; as duas contas são minhas. Para H2, o Earendil: o pi tem 4 ferramentas, <em>prompt</em> de sistema e definições abaixo de 1.000 tokens; e a Databricks, citada pelo Earendil, mediu «3x less context per turn», com custo por tarefa acima de 2× e qualidade igual. Isso é o que H2 quer explicar, agora com a minha medição.</p>",
    ),
    (
        '<div><b>5.676 vs 29.997 bytes</b><small>primeira requisição, pi vs OpenCode, 5,3×</small></div>\n'
        '<div><b>1.228 vs 6.659 tokens</b><small>mesma requisição, tokenizador cl100k_base, 5,4×</small></div>\n'
        '<div><b>555 vs 698 bytes/passo</b><small>crescimento por passo, <code>step_growth.csv</code></small></div>\n'
        '<div><b>n = 1</b><small>Camada 1 é determinística: mesma entrada, mesma saída</small></div>',
        '<div><b>1,33×</b><small>US$ 3,24 ÷ US$ 2,43, custo por tarefa aprovada, OpenCode sobre pi; cálculo do autor</small></div>\n'
        '<div><b>10 pp</b><small>60,0 % − 50,0 % de aprovação, pi sobre OpenCode; cálculo do autor</small></div>\n'
        '<div><b>Kimi K3 · 30 tarefas · n = 1</b><small>via Fireworks; pi v0.84.2, OpenCode v1.18.19; FrontierHarness, 1 set. 2026</small></div>\n'
        '<div><b>&lt; 1.000 tokens</b><small><em>prompt</em> de sistema e definições das 4 ferramentas do pi (Earendil, 2026)</small></div>\n'
        '<div><b>3× menos contexto por turno</b><small>Databricks apud Earendil (2026); custo por tarefa &gt; 2×</small></div>',
    ),
    (
        "<li>Medição própria, 28 ago. 2026, <code>layer1/data/first_request.csv</code> e <code>step_growth.csv</code>. Esses números não estão no texto do projeto (o projeto descreve o que será feito); estão no repositório.</li>",
        '<li><b>Runta (2026)</b>, FrontierHarness, blogue institucional de 1 set. 2026; versões dos braços no repositório do <em>eval</em>. <b>Earendil (2026)</b>, "Pi, minimal and performant", blogue institucional de 4 ago. 2026; a medição da Databricks é citação de segunda mão (apud). Nenhum dos dois é revisado por pares.</li>',
    ),
    (
        '<li><b>"Cinco vezes mais bytes não já responde a pergunta?"</b>Não. Mais bytes por requisição não significam, por si, resultado pior. Se o OpenCode fecha o ticket em menos passos, a conta pode virar. É exatamente o que H2 testa.</li>',
        '<li><b>"Você tem número próprio da carga fixa?"</b>Tenho, da Camada 1, medida em 28 ago. 2026 contra <em>endpoint</em> simulado, <code>layer1/data/first_request.csv</code> e <code>step_growth.csv</code>: primeira requisição de 5.676 bytes e 1.228 tokens no pi contra 29.997 bytes e 6.659 tokens no OpenCode, 5,3×; crescimento por passo de 555 contra 698 bytes. Saiu do slide porque o projeto descreve o que será feito; está no repositório.</li>\n'
        '<li><b>"Três vezes menos contexto não já responde a pergunta?"</b>Não. Mais bytes por requisição não significam, por si, resultado pior. Se o OpenCode conclui a unidade em menos passos, a conta pode virar. É exatamente o que H2 testa.</li>',
    ),
    # --- slide 9 (timeline) -----------------------------------------------------
    (
        '<div class="card slide"><span class="n">7</span>\n<h3>Referencial teórico (linha do tempo)</h3>',
        '<div class="card slide"><span class="n">9</span>\n<h3>Referencial teórico (linha do tempo)</h3>',
    ),
    (
        "Eu comparo na construção de um produto completo, ticket a ticket, com estado de referência controlado, e decomponho",
        "Eu comparo na construção de um produto completo, a partir de uma especificação única, unidade a unidade, com o mesmo espaço de trabalho inicial, e decomponho",
    ),
    # --- slide 10 (classification) ------------------------------------------------
    (
        '<div class="card slide"><span class="n">8</span>\n<h3>Classificação da pesquisa e uso de IA</h3>',
        '<div class="card slide"><span class="n">10</span>\n<h3>Classificação da pesquisa e uso de IA</h3>',
    ),
    (
        "Objetivos: exploratória, porque comparar dois <em>harnesses</em> construindo o mesmo produto completo não tem precedente publicado. Procedimentos: experimental; variável independente, o <em>harness</em>; controladas, modelo, ticket, espaço de trabalho e limites.",
        "Objetivos: exploratória, porque comparar dois <em>harnesses</em> construindo o mesmo produto completo do zero, a partir da mesma especificação, não tem precedente publicado. Procedimentos: experimental; variável independente, o <em>harness</em>; controladas, modelo, especificação, espaço de trabalho inicial e limites.",
    ),
    (
        "Ferramenta: Claude Code. Finalidade: um <em>LLM Wiki</em> no repositório para levantar e organizar fontes.",
        "Ferramenta: Claude Code. Finalidade: síntese e conferência de fontes, num <em>LLM Wiki</em> no repositório, padrão de Karpathy (2026).",
    ),
    (
        "<b>Brasil (2026)</b>: Portaria CNPq nº 2.664, de 6 de março de 2026, Política de Integridade.</li>",
        "<b>Brasil (2026)</b>: Portaria CNPq nº 2.664, de 6 de março de 2026, Política de Integridade. <b>Karpathy (2026)</b>: <em>gist</em> \"LLM Wiki\", o padrão que o repositório instancia.</li>",
    ),
    # --- slide 11 (method) ---------------------------------------------------------
    (
        '<div class="card slide"><span class="n">9</span>\n<h3>Método: duas camadas de medição</h3>',
        '<div class="card slide"><span class="n">11</span>\n<h3>Método: duas camadas de medição</h3>',
    ),
    (
        "<p>Camada 2: o desfecho. Os tickets rodam contra o modelo real, através de um <em>proxy</em> reverso. Estocástica, consome cota, n ≥ 3 por célula.</p>",
        "<p>Camada 2: o desfecho. A construção do produto roda contra o modelo real, através de um <em>proxy</em> reverso. Estocástica, consome cota, n ≥ 3 construções por célula.</p>",
    ),
    (
        "Limite único: relógio de parede, 3× a maior mediana dos braços nos tickets-piloto.",
        "Limite único: relógio de parede por unidade, 3× a maior mediana dos braços nas unidades-piloto.",
    ),
    (
        "Calibrada nos tickets-piloto, antes da matriz.",
        "Calibrada nas unidades-piloto, antes da matriz.",
    ),
    # --- slide 12 (matrix) ---------------------------------------------------------
    (
        '<div class="card slide"><span class="n">10</span>\n<h3>Braços e matriz experimental</h3>\n<p class="meta"><b>90 s</b> · clique numa célula ou <kbd>Tab</kbd>; <kbd>→</kbd> preenche a matriz</p>',
        '<div class="card slide"><span class="n">12</span>\n<h3>Braços e matriz experimental</h3>\n<p class="meta"><b>90 s</b> · clique numa unidade ou navegue com <kbd>Tab</kbd>; <kbd>→</kbd> preenche a matriz</p>',
    ),
    (
        "com 21 tickets fechados antes do experimento. Nove técnicos entram: tenant, governança, <em>flags</em>, <em>pipeline</em> de voz, confirmação, log, relatório, agendador, cobrança.",
        "com 21 tickets fechados antes do experimento. Os nove técnicos viram as nove unidades da especificação, em ordem de dependência: tenant, governança, <em>flags</em>, <em>pipeline</em> de voz, confirmação, log, relatório, agendador, cobrança.",
    ),
    (
        "<p>A matriz é braço × ticket × nível de modelo. Cada célula, n ≥ 3 execuções válidas. O espaço de trabalho é congelado por SHA-256 a cada ticket; o estado de referência é escrito por mim depois do ticket anterior, então o que o agente produziu não entra no seguinte. Escore: fração dos meus testes de aceitação, que o agente não vê.</p>",
        "<p>A matriz é braço × nível de modelo, com as nove unidades dentro de cada construção. Cada célula, n ≥ 3 construções válidas. A especificação é congelada por SHA-256; o espaço de trabalho inicial é vazio, e o que o agente construiu numa unidade é o ponto de partida da seguinte. Eu não escrevo código depois do início. Escore: fração dos meus testes de aceitação, que o agente não vê, rodados sobre uma cópia do espaço ao fim de cada unidade.</p>",
    ),
    (
        "<p>Duas classes de execução. Não concluída: o agente não fechou o ticket; é resultado, entra com a fração aprovada, estouro de relógio incluído. Descartada: medição inconfiável; registrada, sem reparo nem repetição.",
        "<p>Duas classes. Unidade não concluída: o agente não a concluiu; é resultado, entra com a fração aprovada e a construção segue, estouro de relógio incluído. Construção descartada: medição inconfiável em alguma unidade; registrada, sem reparo nem repetição.",
    ),
    (
        "<div><b>2 × 9 × 2</b><small>braços × tickets × níveis de modelo = 36 células</small></div>\n"
        "<div><b>n ≥ 3</b><small>execuções válidas por célula, após descartes; ≥ 108 execuções</small></div>\n"
        "<div><b>21 tickets</b><small>fechados no Finn antes do experimento; 9 técnicos entram (#14–#22)</small></div>",
        "<div><b>2 × 2</b><small>braços × níveis de modelo = 4 células; 9 unidades por construção</small></div>\n"
        "<div><b>n ≥ 3</b><small>construções válidas por célula, após descartes; ≥ 12 construções</small></div>\n"
        "<div><b>21 tickets</b><small>fechados no Finn antes do experimento; os 9 técnicos (#14–#22) viram as unidades</small></div>",
    ),
    (
        '<li><b>"O estado de referência é seu. Isso não enviesa?"</b>Enviesa igual para os dois braços: o mesmo estado entra nos dois, e a comparação é pareada por ticket.',
        '<li><b>"A especificação é sua. Isso não enviesa?"</b>Enviesa igual para os dois braços: a mesma entrada e o mesmo início vazio para os dois, e a comparação é pareada por unidade.',
    ),
    (
        '<li><b>"E se os dois braços falharem num ticket?"</b>Entra como não concluído nos dois, com a fração aprovada. O par continua válido para o Wilcoxon.</li>',
        '<li><b>"E se os dois braços falharem numa unidade?"</b>Entra como não concluída nos dois, com a fração aprovada, e as duas construções seguem. O par continua válido para o Wilcoxon.</li>',
    ),
    (
        '<li><b>"Por que esses nove tickets?"</b>São as issues técnicas #14–#22, cada uma com um resultado que um teste de aceitação decide.',
        '<li><b>"Por que essas nove unidades?"</b>São as issues técnicas #14–#22, cada uma com um resultado que um teste de aceitação decide.',
    ),
    (
        "As issues #1–#13 são o mapa, as decisões do dono do produto e as decisões de base que os tickets já assumem.</li>",
        "As issues #1–#13 são o mapa, as decisões do dono do produto e as decisões de base que as unidades já assumem.</li>",
    ),
    # --- slide 13 (Succ/Mtok) ---------------------------------------------------------
    (
        '<div class="card slide"><span class="n">11</span>\n<h3>Succ/Mtok e teste pareado</h3>',
        '<div class="card slide"><span class="n">13</span>\n<h3>Succ/Mtok e teste pareado</h3>',
    ),
    (
        "<p>Duas medidas. Tokens por ticket concluído, contados no <em>proxy</em>. E Succ/Mtok,",
        "<p>Duas medidas. Tokens por construção, contados no <em>proxy</em>, sempre ao lado da fração final de testes aprovados: um braço que falha barato não pode parecer o mais barato. E Succ/Mtok,",
    ),
    (
        "<p>Estatística: Wilcoxon dos postos sinalizados, bilateral, α = 0,05, pareado por ticket. Não paramétrico, porque nove pares não sustentam suposição de distribuição. Pareado, porque a dificuldade do ticket é o maior fator de perturbação. Com n = 3 por célula e nove tickets,",
        "<p>Estatística: Wilcoxon dos postos sinalizados, bilateral, α = 0,05, pareado por unidade, sobre os tokens por unidade e o Succ/Mtok por unidade. Não paramétrico, porque nove pares não sustentam suposição de distribuição. Pareado, porque a dificuldade da unidade é o maior fator de perturbação. Com n = 3 por célula e nove unidades,",
    ),
    (
        "<div><b>MDE ≈ 0,76σ</b><small>n = 3 por célula, 9 tickets, Wilcoxon bilateral, α = 0,05</small></div>",
        "<div><b>MDE ≈ 0,76σ</b><small>n = 3 por célula, 9 unidades, Wilcoxon bilateral, α = 0,05</small></div>",
    ),
    # --- slide 14 (limitations) --------------------------------------------------------
    (
        '<div class="card slide"><span class="n">12</span>\n<h3>Limitações e ameaças à validade</h3>',
        '<div class="card slide"><span class="n">14</span>\n<h3>Limitações e ameaças à validade</h3>',
    ),
    (
        "Estado de referência humano: mitigado pelo mesmo estado para os dois braços e comparação pareada. Sem placar público: suíte própria, válido só braço contra braço.</p>",
        "Especificação humana e trajetória própria: eu escrevo a especificação, e cada braço carrega os próprios erros de uma unidade à seguinte; mitigado pela mesma entrada e pelo mesmo início vazio para os dois, com comparação pareada por unidade. Sem placar público: suíte própria, válido só braço contra braço; custo em dinheiro só como contrafactual rotulado.</p>",
    ),
    # --- slide 15 (budget) ---------------------------------------------------------------
    (
        '<div class="card slide"><span class="n">13</span>\n<h3>Orçamento e cronograma</h3>',
        '<div class="card slide"><span class="n">15</span>\n<h3>Orçamento e cronograma</h3>',
    ),
    (
        "Outubro e novembro, instrumento e estados de referência dos tickets. Dezembro e janeiro, a matriz. Janeiro, análise. A folga está concentrada onde a cota manda: na matriz e nos estados de referência.</p>",
        "Outubro e novembro, instrumento, especificação e testes de aceitação. Dezembro e janeiro, a matriz. Janeiro, análise. A folga está concentrada onde a cota manda: na matriz e na escrita da especificação e dos testes.</p>",
    ),
    # --- new slide 16 and slide 17 (close) -------------------------------------------------
    (
        '<div class="card slide"><span class="n">14</span>\n<h3>Fecho</h3>\n<p class="meta"><b>20 s</b></p>\n<div class="blk"><b>Fale</b><div class="say">\n'
        "<p>A pergunta que o projeto responde: quantos tokens a mais custa construir o mesmo SaaS com um <em>harness</em> em vez de outro, e quanto disso é carga fixa. O produto é um critério de escolha que um desenvolvedor ou uma empresa pode aplicar. Tudo fica público nos dois repositórios. Obrigado. Perguntas?</p>",
        '<div class="card slide"><span class="n">16</span>\n'
        "<h3>Referências citadas nos slides</h3>\n"
        '<p class="meta"><b>20 s</b> · sem interação; pular se faltar tempo</p>\n'
        '<div class="blk"><b>Fale</b><div class="say">\n'
        "<p>As dezoito referências que apareceram nos slides, em ABNT abreviado, todas sobre o <em>harness</em>. O projeto tem 20; ficam de fora aqui duas citadas só no texto. Os <em>preprints</em> estão marcados.</p>\n"
        "</div></div>\n"
        '<div class="blk"><b>Se perguntarem</b><ul class="q">\n'
        '<li><b>"Quais são as duas que faltam?"</b>HarnessRank e Opencode Zen (2026b), citadas só no texto.</li>\n'
        '<li><b>"Cadê as normas ABNT e os manuais de metodologia?"</b>Saíram da lista em 14 de setembro: a lista só tem fontes sobre o <em>harness</em>. A formatação segue a ABNT mesmo assim, e a classificação da pesquisa fica sem manual citado.</li>\n'
        "</ul></div>\n"
        "</div>\n"
        "\n"
        '<div class="card slide"><span class="n">17</span>\n<h3>Fecho</h3>\n<p class="meta"><b>20 s</b></p>\n<div class="blk"><b>Fale</b><div class="say">\n'
        "<p>A tela pergunta: quanto pesa, para o desenvolvedor que já escolheu o modelo, conhecer o <em>harness</em> antes de pagar por ele? O projeto responde em tokens: quantos a mais custa construir o mesmo SaaS com um <em>harness</em> em vez de outro, e quanto disso é carga fixa. O produto é um critério de escolha que um desenvolvedor ou uma empresa pode aplicar. Tudo fica público nos dois repositórios, harness-bench e Finn. Obrigado. Perguntas?</p>",
    ),
    # --- question bank ----------------------------------------------------------------------
    (
        "Controladas: modelo, ticket, espaço de trabalho, limites de tempo e saída. Dependentes: tokens por ticket concluído, fração de testes aprovada, Succ/Mtok.</li>",
        "Controladas: modelo, especificação, espaço de trabalho inicial, limites de tempo e saída. Dependentes: tokens por construção, fração de testes aprovada, Succ/Mtok.</li>",
    ),
    (
        "Os testes de aceitação ficam fora do espaço de trabalho congelado. O agente recebe o <em>prompt</em> com a decisão, as restrições e a pilha; os testes rodam depois, sobre o resultado.</li>",
        "Os testes de aceitação ficam fora do espaço de trabalho. O agente recebe a especificação e o <em>prompt</em> da unidade; os testes rodam depois, sobre uma cópia do espaço ao fim de cada unidade.</li>",
    ),
    (
        "Declarado conforme a Portaria CNPq 2.664/2026: Claude Code, para levantar e organizar fontes num <em>LLM Wiki</em>.",
        "Declarado conforme a Portaria CNPq 2.664/2026: Claude Code, para síntese e conferência de fontes num <em>LLM Wiki</em>, padrão de Karpathy (2026).",
    ),
    # --- numbers table -------------------------------------------------------------------------
    (
        '<tr><td class="r">9</td><td>tickets técnicos do Finn no experimento</td><td>de 21 fechados; issues #14–#22</td><td>YuukiFST (2026a)</td></tr>\n'
        '<tr><td class="r">n ≥ 3</td><td>execuções válidas por célula</td><td>2 braços × 9 tickets × 2 níveis = 36 células</td><td>projeto, §3</td></tr>\n'
        '<tr><td class="r">3×</td><td>limite de relógio de parede</td><td>maior mediana dos braços nos tickets-piloto</td><td>projeto, §3</td></tr>\n'
        '<tr><td class="r">≈ 0,76σ</td><td>diferença mínima detectável</td><td>n = 3, 9 tickets, Wilcoxon bilateral, α = 0,05</td><td>projeto, §3</td></tr>',
        '<tr><td class="r">1,33× / 10 pp</td><td>OpenCode paga mais por tarefa aprovada e aprova menos que o pi</td><td>idem; cálculo do autor</td><td>Runta (2026)</td></tr>\n'
        '<tr><td class="r">&lt; 1.000 tokens</td><td><em>prompt</em> de sistema e definições das 4 ferramentas do pi</td><td>blogue, 4 ago. 2026</td><td>Earendil (2026)</td></tr>\n'
        '<tr><td class="r">3× / &gt; 2×</td><td>menos contexto por turno / custo por tarefa, pi vs outro <em>harness</em></td><td>medição da Databricks, citada de segunda mão</td><td>Databricks apud Earendil (2026)</td></tr>\n'
        '<tr><td class="r">9</td><td>unidades da especificação do Finn</td><td>de 21 tickets fechados; issues #14–#22</td><td>YuukiFST (2026a)</td></tr>\n'
        '<tr><td class="r">n ≥ 3</td><td>construções válidas por célula</td><td>2 braços × 2 níveis = 4 células; 9 unidades por construção</td><td>projeto, §3</td></tr>\n'
        '<tr><td class="r">3×</td><td>limite de relógio de parede por unidade</td><td>maior mediana dos braços nas unidades-piloto</td><td>projeto, §3</td></tr>\n'
        '<tr><td class="r">≈ 0,76σ</td><td>diferença mínima detectável</td><td>n = 3, 9 unidades, Wilcoxon bilateral, α = 0,05</td><td>projeto, §3</td></tr>',
    ),
    # --- checklist -----------------------------------------------------------------------------
    (
        "<li>Abrir <code>dist/apresentacao-pcc.html</code> no Chrome; testar <kbd>→</kbd>, <kbd>F</kbd>, <kbd>0</kbd>–<kbd>5</kbd> no slide 3, clique nos nós do slide 7.</li>",
        "<li>Abrir <code>dist/apresentacao-pcc/index.html</code> no Chrome; testar <kbd>→</kbd>, <kbd>F</kbd>, <kbd>0</kbd>–<kbd>5</kbd> no slide 3, clique nos nós do slide 9.</li>",
    ),
    (
        "<li>Fontes Archivo/Fraunces carregam pela rede; sem internet o deck cai para Segoe UI/Georgia. Aceitável; testar antes.</li>",
        "<li>Fontes Space Grotesk/Inter vêm embutidas no deck; não dependem de internet. Testar mesmo assim.</li>",
    ),
    (
        "<li>Ensaiar o slide 7 com o cronômetro: é o mais longo (2 min) e o único com nomes de autores.</li>",
        "<li>Ensaiar o slide 9 com o cronômetro: é o mais longo (2 min) e o que mais tem nomes de autores.</li>",
    ),
    (
        "<li>Se a banca cortar tempo: pular o slide 5 (objetivos estão implícitos no 9 e 10) e fazer o 11 sem mover os controles.</li>",
        "<li>Se a banca cortar tempo: pular o 7 (objetivos estão implícitos no 11 e 12) e o 16, e fazer o 13 sem mover os controles.</li>",
    ),
    # --- 2026-09-14, later: references outside the theme left the project --------
    (
        "<li><b>Gil (2022)</b> e <b>Prodanov e Freitas (2013)</b>: manuais usados para classificar. <b>Brasil (2026)</b>: Portaria CNPq nº 2.664",
        "<li>A classificação segue sem manual citado: as referências do projeto são só sobre o <em>harness</em>. <b>Brasil (2026)</b>: Portaria CNPq nº 2.664",
    ),
]


def apply(path: Path, pairs: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    done = 0
    for old, new in pairs:
        if new in text:
            continue
        hits = text.count(old)
        if hits != 1:
            raise SystemExit(f"{path}: expected 1 match, found {hits}:\n{old[:120]}")
        text = text.replace(old, new)
        done += 1
    path.write_text(text, encoding="utf-8")
    print(f"{path}: {done} replacements")


if __name__ == "__main__":
    apply(PATH, PAIRS)
