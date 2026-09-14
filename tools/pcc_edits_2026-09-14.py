"""Prose edits applied to dist/projeto-pcc.docx on 2026-09-14.

The experiment changes object: instead of a DeepSWE suite run through harness
zero, pi, oh-my-pi and third-party harnesses, the project now builds the same
SaaS (Finn, github.com/YuukiFST/Finn) twice, once with OpenCode and once with
pi, over the same model, and counts the tokens each harness spends per ticket.
Everything that belonged to the previous design (harness zero, the pi/oh-my-pi
fork pair, DeepSWE, Pier) leaves the text. Paragraph indices are the ones
`tools/docx_prose.py dump` printed against 64553fb.

Usage:
    python tools/pcc_edits_2026-09-14.py > /tmp/edits.json
    python tools/docx_prose.py apply dist/projeto-pcc.docx /tmp/edits.json
"""

import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

P = {}
INSERT = {}

TITLE = ("O HARNESS COMO DECISÃO DO DESENVOLVEDOR: TOKENS E TAXA DE SUCESSO DO OPENCODE "
"E DO PI NA CONSTRUÇÃO DE UM MESMO SAAS SOB UM MESMO MODELO")
P[5] = TITLE
P[10] = TITLE

# --- 1 INTRODUÇÃO -----------------------------------------------------------
P[26] = ("Agentes de codificação como o Codex e o Claude Code são ferramenta de trabalho do "
"desenvolvedor. Cada um é um *harness*, a camada de software ao redor do modelo, e ela muda "
"o custo com o modelo fixo. No FrontierHarness (Runta, 2026), doze configurações de nove "
"*harnesses* sobre o mesmo modelo ficam entre 50,0% e 66,7% de aprovação, e o custo por "
"tarefa concluída vai de US$ 1,05 a US$ 18,34, uma razão de 17,5x calculada pelo autor deste "
"projeto. Dois dos *harnesses* medidos ali são de código aberto e rodam sem interface: o pi "
"conclui 60,0% das tarefas a US$ 2,43 por tarefa concluída e o OpenCode 50,0% a US$ 3,24.")

P[27] = ("Quem paga essa conta é o desenvolvedor, na assinatura pessoal, e a empresa que adota a "
"ferramenta em escala; conhecer o *harness* virou parte do ofício. As comparações publicadas "
"usam suítes de tarefas isoladas, e não dizem quanto custa entregar um produto inteiro com "
"uma ferramenta em vez de outra. Este projeto medirá esse custo construindo o mesmo produto "
"duas vezes: o Finn, um SaaS de financeiro por voz, será construído com o OpenCode e com o "
"pi, sobre o mesmo modelo, *ticket* a *ticket*, e os tokens de cada braço serão contados "
"fora do *harness*. O resultado será um critério de escolha para o desenvolvedor e para a "
"empresa.")

P[29] = ("A escolha do *harness* como decisão de engenharia do desenvolvedor e da empresa: seu "
"efeito sobre os tokens consumidos e sobre a taxa de sucesso de agentes de codificação na "
"construção de um mesmo produto de software, mantido fixo o modelo de linguagem.")

P[31] = ("Para o desenvolvedor ou a empresa que já escolheu o modelo, quantos tokens a mais ou a "
"menos custa construir o mesmo software com um *harness* em vez de outro? E quanto dessa "
"diferença vem da carga fixa que cada *harness* envia em toda requisição, de modo que seja "
"possível agir sobre ela?")

P[33] = ("Medir, com o modelo de linguagem mantido fixo, a diferença de tokens consumidos e de taxa "
"de sucesso entre o OpenCode e o pi na construção do mesmo SaaS, *ticket* a *ticket*, "
"separando a parte dessa diferença que vem da carga fixa por requisição, e entregar o "
"resultado como critério de escolha reproduzível pelo desenvolvedor.")

P[35] = ("1) construir um instrumento de medição externo aos *harnesses*, capaz de contabilizar de "
"forma idêntica, para os dois, o número de requisições ao modelo, os tokens de entrada e de "
"saída e a latência por requisição;")
P[36] = ("2) decompor a construção do Finn em *tickets* com testes de aceitação escritos pelo autor "
"antes da execução, independentes dos testes que o próprio agente produzir;")
P[37] = ("3) preparar, para cada *ticket*, um espaço de trabalho congelado e idêntico para os dois "
"braços, a partir de um estado de referência escrito pelo autor;")
P[38] = ("4) executar cada *ticket* nos dois *harnesses*, com o mesmo modelo e o mesmo *prompt*, "
"repetindo cada condição e reportando dispersão;")
P[39] = ("5) repetir o experimento em um segundo modelo, verificando se a ordenação entre os dois "
"*harnesses* se mantém ou se inverte;")
P[40] = ("6) quantificar a divergência entre os tokens relatados por cada *harness* e os tokens "
"medidos no instrumento externo, que são o que o desenvolvedor paga;")
P[41] = ("7) publicar o executor, os *prompts*, os testes de aceitação, os dados brutos e os "
"scripts de análise, com um procedimento que o desenvolvedor reexecute na própria máquina a "
"custo monetário zero.")

P[43] = ("A pesquisa é aplicada, quali-quantitativa, exploratória e experimental, e o método é "
"dedutivo, com hipóteses declaradas antes da coleta. Os dados serão coletados por um "
"instrumento próprio, um *proxy* reverso interposto entre cada *harness* e o modelo, que "
"contará requisições, tokens e latência da mesma forma para os dois braços. A suíte será a "
"construção do Finn dividida em nove *tickets*; cada par de braço e *ticket* será executado "
"ao menos três vezes, e a comparação será feita por teste pareado sobre os tokens por "
"*ticket* concluído e sobre o Succ/Mtok de cada *ticket*. Espera-se obter a diferença de "
"tokens e de taxa de sucesso atribuível ao *harness*, em forma utilizável por quem escolhe a "
"ferramenta. A seção 3 detalha material, método e tratamento estatístico.")

P[45] = ("H1: entre o OpenCode e o pi executando o mesmo modelo, a diferença de tokens por "
"*ticket* concluído é de ordem prática relevante para quem paga a conta, comparável à "
"diferença obtida ao se trocar de modelo sob um *harness* fixo. H1 será refutada se os "
"intervalos de tokens por *ticket* concluído dos dois braços se sobrepuserem ao longo de "
"toda a suíte.")

P[46] = ("H2: a carga fixa que cada *harness* envia em toda requisição (*prompt* de sistema e "
"esquemas de ferramenta, medidos na Camada 1) explica a maior parte dessa diferença, e o "
"número de passos que cada um leva para concluir o *ticket* explica a parte menor. H2 será "
"refutada se o número de passos explicar a maior parte da diferença de tokens. Esse desfecho "
"é possível e seria um achado a reportar, já que o *harness* com mais ferramentas pode "
"compensar a carga extra concluindo o *ticket* em menos passos.")

# --- 2 REFERENCIAL TEÓRICO --------------------------------------------------
P[49] = ("Segundo Ning et al. (2026, §2, tradução nossa), um *harness* “converte um modelo de "
"linguagem sem estado em um agente funcional ao ancorar suas saídas em execução externa, "
"estado persistente e realimentação verificável”. Wang et al. (2026) descrevem a mesma "
"camada pelo que ela faz: monta os *prompts*, gerencia o estado, invoca as ferramentas e "
"coordena o laço. É ela que muda quando o desenvolvedor troca de ferramenta e mantém o "
"modelo, e os dois braços deste projeto ficam em pontos distantes dessa camada: o pi é um "
"laço próximo do ReAct mínimo (Yao et al., 2022), com quatro ferramentas, e o OpenCode traz "
"planejamento, compactação, subagentes e permissões. Lin et al. (2026) delimitam o que, "
"exatamente, essa camada contém:")

P[52] = ("A interface entre modelo e ambiente é objeto de projeto desde Yang et al. (2024). Na "
"Tabela 1 de Lin et al. (2026), *harnesses* escritos por humanos sobre um modelo congelado "
"(GPT-5.4, Terminal-Bench 2, 89 tarefas) vão de 47,2% de aprovação no OpenCode a 71,9% no "
"Codex, uma diferença de 24,7 pontos percentuais calculada pelo autor deste projeto. Zhang "
"et al. (2026) enunciam a Binding Constraint Thesis: em tarefas de longo horizonte com "
"modelos de fronteira comparáveis, a parcela do desempenho que vem do *harness* é "
"frequentemente comparável ou maior que a que vem do modelo, e pode dominá-la. Em Alier "
"Forment et al. (2026), os dois *scaffoldings* sem suporte a MCP saíram de 5,0x a 28x mais "
"baratos que os cinco que o suportam, e o pi foi o mais barato da matriz. Somam-se três "
"fontes não revisadas por pares. O HarnessRank (2026) ordena *harnesses* por taxa de "
"aprovação com modelo fixo e publica custo e tokens ao lado, sem que eles alterem a ordem. O "
"FrontierHarness (Runta, 2026) compara, sobre o mesmo modelo, as ferramentas que o "
"desenvolvedor encontra no mercado: o Codex conclui 66,7% das tarefas a US$ 3,47 por tarefa "
"concluída e o Claude Code 63,3% a US$ 18,34, ou seja, 5,3x mais caro para uma taxa próxima "
"(cálculo do autor deste projeto). O estudo da Databricks registra custo por tarefa variando "
"mais de 2x em alguns casos, sem mudança de qualidade (Databricks, 2026 apud Earendil, "
"2026).")

P[53] = ("A primeira pendência é de atribuição. Toda comparação publicada contrasta *harnesses* "
"sobre suítes de tarefas isoladas e curtas, e a dispersão medida agrega *prompt*, "
"ferramentas, gestão de contexto e desenho do laço sem separá-los. O desenvolvedor sabe qual "
"ferramenta ganhou, mas não o que a fez ganhar, nem quanto essa diferença custa ao longo de "
"um produto inteiro. Ning et al. (2026) nomeiam a lacuna em §5.2.1 e pedem, em §5.2.7, "
"“métricas que isolem componentes do *harness*” (Ning et al., 2026, tradução nossa). Lee et "
"al. (2026) mostram que essas decisões são isoláveis: uma busca automática que edita só o "
"código do *harness*, com o modelo fixo, chegou a 76,4% de aprovação no TerminalBench-2 (89 "
"tarefas, Claude Opus 4.6), contra 74,7% do Terminus-KIRA, o *harness* escrito à mão de que "
"a busca partiu (Lee et al., 2026, Tabela 7). Este projeto responderá a §5.2.7 pelo lado da "
"medição: separará, em cada requisição, a carga fixa do *harness* (*prompt* de sistema e "
"esquemas de ferramenta) do conteúdo da conversa, e medirá quanto dessa carga chega ao "
"resultado ao longo de um produto completo.")

P[54] = ("A segunda pendência é de instrumentação, e atinge o desenvolvedor diretamente, porque ele "
"decide pelo relatório da própria ferramenta. O que um *harness* relata sobre o próprio custo "
"diverge do que ele gasta, e cada um omite um conjunto diferente de chamadas reais ao "
"modelo. Kapoor et al. (2024) mostram que a avaliação de agentes ignora o custo e por isso "
"erra sobre a origem dos ganhos, e Kapoor et al. (2025) registram que as avaliações "
"raramente relatam custo e que comparações entre *harnesses* são raras. Por isso a medição "
"ocorrerá em um *proxy* externo, e o objetivo (6) quantificará essa divergência.")

P[55] = ("As métricas serão os tokens por *ticket* concluído, contados no *proxy*, e o Succ/Mtok "
"(sucesso por milhão de tokens), de Lin et al. (2026), a razão que interessa a quem paga a "
"conta. Sobre elas pesa uma ressalva permanente, a de que o efeito é específico do modelo e "
"pode inverter de sinal. No Holistic Agent Leaderboard, os modelos da Anthropic vão melhor "
"com o BrowserUse e os da OpenAI com o SeeAct sobre o mesmo *benchmark* (Kapoor et al., "
"2025), e o FrontierHarness registra, para o Claude Code, aproveitamento de *cache* de 25,0% "
"ponderado por tokens contra 67,8% na célula mediana do mesmo *harness* (Runta, 2026). Por "
"isso o desenho carregará dois níveis de modelo, e as conclusões serão enunciadas por nível.")

# --- 3 MATERIAL E MÉTODO ----------------------------------------------------
P[57] = ("Quanto à natureza, esta é uma pesquisa aplicada, e seu produto será um critério de "
"escolha que um desenvolvedor ou uma empresa poderá aplicar. Quanto à abordagem, combina o "
"quantitativo e o qualitativo. As medidas de tokens e de sucesso são quantitativas, e a "
"atribuição da diferença à carga fixa ou ao número de passos é qualitativa. Quanto aos "
"objetivos, é exploratória, porque a comparação de dois *harnesses* construindo o mesmo "
"produto completo, *ticket* a *ticket*, não tem precedente publicado. Quanto aos "
"procedimentos, é experimental, com variável independente manipulada (o *harness*) e "
"variáveis controladas (modelo, *ticket*, espaço de trabalho e limites). Quanto ao método, é "
"dedutivo, porque parte de hipóteses declaradas antes da coleta e as submete a teste (Gil, "
"2022; Prodanov; Freitas, 2013).")

P[58] = ("O levantamento das fontes deste projeto foi feito com apoio de um *LLM Wiki* mantido no "
"repositório do projeto (YuukiFST, 2026b). Nesse arranjo, as fontes brutas ficam guardadas "
"sem alteração, um agente de codificação escreve as páginas de síntese, cada operação entra "
"em um registro cronológico e as dúvidas vão para uma fila de revisão. O autor curou as "
"fontes e revisou cada síntese, e cada afirmação citada neste texto foi conferida na obra "
"original, com o trecho copiado ao lado do veredito. A Portaria CNPq nº 2.664/2026 pede que "
"o uso de inteligência artificial generativa seja declarado com a ferramenta e a finalidade "
"(Brasil, 2026). A ferramenta foi o Claude Code, e a finalidade foi que o agente entendesse "
"o tema do projeto e ajudasse a buscar mais artigos sobre o tema escolhido. O autor responde "
"pelo texto final.")

P[59] = ("A medição ocorrerá em duas camadas, relatadas em separado. A Camada 1 medirá a forma da "
"requisição contra um *endpoint* simulado que não encaminha nada ao modelo: quantos esquemas "
"de ferramenta, quantos bytes de *prompt* de sistema e quantos tokens cada braço envia na "
"primeira requisição e a cada passo seguinte. Essa camada não consome cota, é determinística "
"e fornece a carga fixa por requisição de que H2 depende. A Camada 2 medirá o desfecho dos "
"*tickets* contra o modelo real, consome cota e é estocástica. Mais bytes por requisição não "
"significam, por si, resultado pior; a Camada 2 dirá quanto dessa carga chega ao resultado.")

P[60] = ("Os braços serão dois: o OpenCode (Opencode, 2026a) e o pi (Earendil, 2026). Os dois "
"são de código aberto, rodam sem interface (opencode run e pi --mode json) e apontam para "
"uma URL base compatível com a API da OpenAI sem adaptação, o que os faz atravessar o *proxy* "
"de medição. Ficam em pontos distantes do espaço de projeto: o pi envia quatro ferramentas e "
"um *prompt* de sistema curto, sem subagentes nem permissões; o OpenCode envia mais esquemas "
"de ferramenta, um *prompt* de sistema maior, e traz subagentes, permissões e compactação de "
"contexto. As versões serão fixadas na adoção e registradas no repositório (YuukiFST, "
"2026b). Este projeto não escreve *harness* algum; escreve o instrumento, os *prompts* e os "
"testes de aceitação.")

P[61] = ("A suíte será a construção do Finn, um SaaS multiempresa em que a empresa cliente fala "
"com o próprio financeiro por voz e recebe lançamento, relatório e aviso no celular "
"(YuukiFST, 2026a). O produto foi especificado antes deste experimento em 21 *tickets* "
"fechados no repositório, com a decisão e as restrições de cada um. Os nove *tickets* "
"técnicos serão as tarefas: separação por empresa, governança, *flags* por empresa, "
"*pipeline* de voz, confirmação da transcrição, registro de auditoria, relatório, agendador "
"e cobrança. Cada *ticket* vira um *prompt* idêntico para os dois braços, com a decisão "
"registrada, as restrições e a pilha fixada pelo dono do produto (TypeScript, TanStack "
"Start, tRPC, Drizzle ORM, PostgreSQL, Vitest). Cada *ticket* parte de um espaço de "
"trabalho congelado: o estado de referência que o autor escreve após o *ticket* anterior, "
"fixado por hash SHA-256. O que um agente produziu em um *ticket* não entra no seguinte, "
"ou seja, toda célula é independente e os dois braços partem dos mesmos bytes. A pontuação "
"será a fração dos testes de aceitação aprovados; esses testes são escritos pelo autor "
"antes da execução, ficam fora do espaço de trabalho e nunca são os testes que o agente "
"escreve, já que um modelo que alucina uma API também escreve testes que simulam a "
"alucinação. Um *ticket* conta como concluído quando todos os seus testes passam.")

P[62] = ("Serão dois níveis de modelo, um primário e um de robustez, ambos gratuitos e no mesmo "
"*gateway* (Opencode, 2026b), relatados em separado. O segundo existe porque o efeito do "
"*harness* é específico do modelo. Se a ordenação entre os braços se inverter entre os "
"níveis, a inversão será o resultado a reportar.")

P[64] = ("Um único limite será imposto, idêntico para os dois braços. É um relógio de parede, "
"cujo valor será três vezes a maior mediana que os dois braços gastarem nos *tickets*-piloto. "
"O número de passos não será limitado, porque um teto de passos é ele próprio uma decisão de "
"projeto de *harness* e apagaria a diferença sob teste. O comprimento máximo de saída será "
"forçado idêntico pelo *proxy*. Os parâmetros de amostragem serão registrados e relatados, "
"mas não normalizados, já que o *gateway* os aceita sem os honrar, e Miller (2024) "
"desaconselha mexer na temperatura para reduzir variância. O isolamento de ambiente será "
"verificado por um portão que falha fechado.")

P[65] = ("Cada célula do experimento, a tripla (braço, *ticket*, nível), receberá n ≥ 3 execuções "
"completas, contadas após os descartes, na função redutora de variância que Miller (2024) "
"atribui à reamostragem. Os resultados sairão como mediana com dispersão, porque "
"requisições byte-idênticas podem variar em tokens de saída em um nível gratuito, o que os "
"*tickets*-piloto vão medir. Quando a cota não comportar a matriz, a cobertura será reduzida "
"antes das repetições, já que a variância é a principal ameaça ao desenho.")

P[66] = ("A comparação será pareada por *ticket* e usará o teste de Wilcoxon dos postos "
"sinalizados, bilateral, com α = 0,05, sobre duas medidas: os tokens por *ticket* concluído "
"e o Succ/Mtok por *ticket*. O teste é não paramétrico porque nove pares não sustentam "
"suposição distribucional, e pareado porque a dificuldade do *ticket* é o maior fator de "
"perturbação do desenho, que é o que Miller (2024) recomenda ao preferir a diferença pareada "
"por questão à média agregada. Com n = 3 e 9 *tickets*, a diferença mínima detectável é de "
"cerca de 0,76σ. Para H2, os tokens de cada execução serão decompostos em carga fixa "
"(esquemas e *prompt* de sistema, medidos na Camada 1, multiplicados pelo número de passos) "
"e conteúdo da conversa, e a parcela de cada uma na diferença entre braços será reportada "
"por *ticket*. As predições serão pré-registradas por nível de modelo, e um resultado nulo "
"para H2 será um achado reportável.")

P[67] = ("Cada execução receberá exatamente uma classe. Aquela cujo agente não concluiu o *ticket* "
"será um resultado, entrará na estatística com a fração de testes que aprovou; nesse grupo, o "
"estouro do relógio de parede contará como resultado, já que repetir converteria uma "
"indisponibilidade do serviço em diferença aparente entre *harnesses*. Aquela cuja medição for "
"inconfiável será descartada e registrada como tal, sem reparo nem repetição. A classificação "
"virá do registro do *proxy*, já que o código de saída não discrimina o desfecho.")

P[69] = ("Quatro limitações são declaradas de partida. O efeito de um *harness* é específico do "
"modelo e pode inverter de sinal, o que restringe qualquer conclusão ao nível de modelo em "
"que for obtida; o objetivo (5) existe para testar isso. A suíte é um único produto sobre "
"uma única pilha (TypeScript, TanStack Start, tRPC, Drizzle), então o resultado vale para "
"tarefas dessa família, e a transferência para outras pilhas fica registrada como trabalho "
"futuro. O estado de referência de cada *ticket* é escrito pelo autor, então o espaço de "
"trabalho carrega o estilo de um humano; a mitigação é que os dois braços partem do mesmo "
"estado e a comparação é pareada. Os valores absolutos não serão comparáveis a placares "
"públicos, porque a suíte é própria, e os valores em dólar citados de fontes externas vêm de "
"outros modelos e de níveis pagos; a comparação válida aqui é entre os dois braços, e o "
"custo em dinheiro será um contrafactual de ordem de grandeza sobre tarifas pagas "
"publicadas, rotulado como tal onde apareça.")

# --- 4 ORÇAMENTO e 5 CRONOGRAMA ---------------------------------------------
P[76] = "*Harnesses* e ferramentas (OpenCode e pi, código aberto; Node.js e PostgreSQL)"
P[83] = ("O total em dinheiro é zero, e o limite que restringe o experimento será a cota do nível "
"gratuito do *gateway*, a ser medida nos *tickets*-piloto contra o número de requisições que "
"um *ticket* do Finn consome. Por isso a matriz será executada em lotes distribuídos ao longo "
"de dias, e o custo monetário aparecerá apenas como contrafactual de ordem de grandeza sobre "
"as tarifas pagas publicadas.")
P[85] = ("A cota gratuita deve ser o limite vinculante, então a cadência prevista é de um lote da "
"matriz por dia e o calendário se estende por semanas. A folga está concentrada na execução "
"da matriz e nos estados de referência dos *tickets*, onde está o risco. Os meses vão de "
"agosto de 2026 a janeiro de 2027. A escrita deste projeto foi concluída em setembro de "
"2026, mês de entrega, e os experimentos práticos ocorrem a partir de outubro.")
P[108] = "CONSTRUÇÃO DO INSTRUMENTO E DOS ESTADOS DE REFERÊNCIA"

# --- 6 REFERÊNCIAS ----------------------------------------------------------
P[171] = None  # Datacurve, Pier: executor do DeepSWE, fora da suíte nova
P[175] = None  # Huang et al., DeepSWE: suíte substituída pelo Finn
P[177] = None  # Jimenez et al., SWE-bench: citado só na comparação com o DeepSWE
P[184] = ("OPENCODE. Zen. 2026b. Documentação do produto. Disponível em: "
"https://opencode.ai/docs/zen/. Acesso em: 28 ago. 2026.")
INSERT[183] = ("OPENCODE. OpenCode: the open source coding agent. 2026a. Repositório de código. "
"Disponível em: https://github.com/anomalyco/opencode. Acesso em: 14 set. 2026.")
P[190] = ("YUUKIFST. harness-bench: executor, prompts, testes de aceitação, dados brutos e "
"scripts de análise deste projeto. 2026b. Repositório de código. Disponível em: "
"https://github.com/YuukiFST/harness-bench. Acesso em: 28 ago. 2026.")
INSERT[189] = ("YUUKIFST. Finn: SaaS universal de financeiro por voz. 2026a. Repositório de "
"código. Disponível em: https://github.com/YuukiFST/Finn. Acesso em: 14 set. 2026.")

json.dump(
    {"paragraphs": {str(k): v for k, v in P.items()},
     "insert_after": {str(k): v for k, v in INSERT.items()}},
    sys.stdout, ensure_ascii=False, indent=1,
)
