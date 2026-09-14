"""Prose edits applied to dist/projeto-pcc.docx on 2026-09-14 (third pass).

The experiment changes unit of analysis: instead of isolated tickets run from
author-written reference states, each arm builds the whole Finn from scratch,
from one frozen specification in nine units, in one workspace, and the tokens
per construction are compared (paired per unit). Reference states leave the
text; tickets become units of the specification. Paragraph indices are the
ones `tools/docx_prose.py dump` printed after tools/pcc_edits_2026-09-14b.py.

Usage:
    python tools/pcc_edits_2026-09-14c.py > /tmp/edits.json
    python tools/docx_prose.py apply dist/projeto-pcc.docx /tmp/edits.json
"""

import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

P = {}

# --- 1 INTRODUÇÃO -----------------------------------------------------------
P[27] = ("Quem paga essa conta é o desenvolvedor, na assinatura pessoal, e a empresa que adota a "
"ferramenta em escala; conhecer o *harness* virou parte do ofício. As comparações publicadas "
"usam suítes de tarefas isoladas, e não dizem quanto custa entregar um produto inteiro com "
"uma ferramenta em vez de outra. Este projeto medirá esse custo construindo o mesmo produto "
"duas vezes, do zero: o Finn, um SaaS de financeiro por voz, será construído com o OpenCode e "
"com o pi, sobre o mesmo modelo e a partir da mesma especificação, e os tokens que cada braço "
"gastar até entregar o produto serão contados fora do *harness*. O resultado será um critério "
"de escolha para o desenvolvedor e para a empresa.")

P[33] = ("Medir, com o modelo de linguagem mantido fixo, a diferença de tokens consumidos e de taxa "
"de sucesso entre o OpenCode e o pi na construção do mesmo SaaS a partir da mesma "
"especificação, separando a parte dessa diferença que vem da carga fixa por requisição, e "
"entregar o resultado como critério de escolha reproduzível pelo desenvolvedor.")

P[36] = ("2) escrever a especificação do Finn em nove unidades, a partir das decisões já registradas "
"no repositório do produto, com testes de aceitação escritos pelo autor antes da execução, "
"independentes dos testes que o próprio agente produzir;")

P[37] = ("3) preparar um espaço de trabalho inicial idêntico para os dois braços, contendo apenas a "
"especificação e a pilha fixada, congelado por hash;")

P[38] = ("4) executar a construção completa do Finn nos dois *harnesses*, unidade a unidade, com o "
"mesmo modelo e os mesmos *prompts*, repetindo cada condição e reportando dispersão;")

P[43] = ("A pesquisa é aplicada, quali-quantitativa, exploratória e experimental, e o método é "
"dedutivo, com hipóteses declaradas antes da coleta. Os dados serão coletados por um "
"instrumento próprio, um *proxy* reverso interposto entre cada *harness* e o modelo, que "
"contará requisições, tokens e latência da mesma forma para os dois braços. Cada braço "
"construirá o Finn do zero, a partir de uma especificação única dividida em nove unidades, "
"ao menos três vezes; a comparação será feita sobre os tokens por construção, relatados ao "
"lado da fração de testes de aceitação aprovados, e por teste pareado sobre os tokens de cada "
"unidade. Espera-se obter a diferença de tokens e de taxa de sucesso atribuível ao *harness*, "
"em forma utilizável por quem escolhe a ferramenta. A seção 3 detalha material, método e "
"tratamento estatístico.")

P[45] = ("H1: entre o OpenCode e o pi executando o mesmo modelo, a diferença de tokens gastos para "
"construir o Finn a partir da mesma especificação é de ordem prática relevante para quem paga "
"a conta, comparável à diferença obtida ao se trocar de modelo sob um *harness* fixo. H1 será "
"refutada se os intervalos de tokens por construção dos dois braços se sobrepuserem e o teste "
"pareado por unidade não apontar diferença.")

P[46] = ("H2: a carga fixa que cada *harness* envia em toda requisição (*prompt* de sistema e esquemas "
"de ferramenta, medidos na Camada 1) explica a maior parte dessa diferença, e o número de "
"passos que cada um leva para concluir cada unidade explica a parte menor. H2 será refutada se "
"o número de passos explicar a maior parte da diferença de tokens. Esse desfecho é possível e "
"seria um achado a reportar, já que o *harness* com mais ferramentas pode compensar a carga "
"extra concluindo a unidade em menos passos.")

P[55] = "As métricas serão os tokens por construção, contados no *proxy* e relatados ao lado da fração de testes de aceitação aprovados, e o Succ/Mtok (sucesso por milhão de tokens), de Lin et al. (2026), a razão que interessa a quem paga a conta. Sobre elas pesa uma ressalva permanente, a de que o efeito é específico do modelo e pode inverter de sinal. No Holistic Agent Leaderboard, os modelos da Anthropic vão melhor com o BrowserUse e os da OpenAI com o SeeAct sobre o mesmo *benchmark* (Kapoor et al., 2025), e o FrontierHarness registra, para o Claude Code, aproveitamento de *cache* de 25,0% ponderado por tokens contra 67,8% na célula mediana do mesmo *harness* (Runta, 2026). Por isso o desenho carregará dois níveis de modelo, e as conclusões serão enunciadas por nível."

# --- 3 MATERIAL E MÉTODO ----------------------------------------------------
P[57] = ("Quanto à natureza, esta é uma pesquisa aplicada, e seu produto será um critério de escolha "
"que um desenvolvedor ou uma empresa poderá aplicar. Quanto à abordagem, combina o "
"quantitativo e o qualitativo. As medidas de tokens e de sucesso são quantitativas, e a "
"atribuição da diferença à carga fixa ou ao número de passos é qualitativa. Quanto aos "
"objetivos, é exploratória, porque a comparação de dois *harnesses* construindo o mesmo "
"produto completo do zero, a partir da mesma especificação, não tem precedente publicado. "
"Quanto aos procedimentos, é experimental, com variável independente manipulada (o "
"*harness*) e variáveis controladas (modelo, especificação, espaço de trabalho inicial e "
"limites). Quanto ao método, é dedutivo, porque parte de hipóteses declaradas antes da coleta "
"e as submete a teste (Gil, 2022; Prodanov; Freitas, 2013).")

P[59] = ("A medição ocorrerá em duas camadas, relatadas em separado. A Camada 1 medirá a forma da "
"requisição contra um *endpoint* simulado que não encaminha nada ao modelo: quantos esquemas "
"de ferramenta, quantos bytes de *prompt* de sistema e quantos tokens cada braço envia na "
"primeira requisição e a cada passo seguinte. Essa camada não consome cota, é determinística "
"e fornece a carga fixa por requisição de que H2 depende. A Camada 2 medirá a construção do "
"produto contra o modelo real, consome cota e é estocástica. Mais bytes por requisição não "
"significam, por si, resultado pior; a Camada 2 dirá quanto dessa carga chega ao resultado.")

P[61] = ("O produto será o Finn, um SaaS multiempresa em que a empresa cliente fala com o próprio "
"financeiro por voz e recebe lançamento, relatório e aviso no celular (YuukiFST, 2026a). As "
"decisões de produto e de pilha foram registradas antes deste experimento em 21 *tickets* "
"fechados no repositório. A partir deles o autor escreverá, antes de qualquer execução, uma "
"especificação única, congelada por hash SHA-256: um documento com o produto, a pilha fixada "
"pelo dono (TypeScript, TanStack Start, tRPC, Drizzle ORM, PostgreSQL, Vitest) e as "
"restrições gerais, e nove unidades, uma por *ticket* técnico, em ordem de dependência: "
"separação por empresa, governança, *flags* por empresa, *pipeline* de voz, confirmação da "
"transcrição, registro de auditoria, relatório, agendador e cobrança. Cada braço recebe os "
"mesmos bytes e constrói o produto do zero em um único espaço de trabalho: o executor invoca "
"o *harness* uma vez por unidade, em ordem, com um *prompt* idêntico para os dois braços, e o "
"que o agente construiu em uma unidade é o ponto de partida da seguinte. O autor não escreve "
"código algum no espaço de trabalho depois do início. Essa é a diferença para o desenho "
"anterior, que partia de estados de referência escritos pelo autor a cada *ticket*: aqui a "
"entrada dos dois braços é a mesma, ou seja, a diferença de tokens fica atribuível ao "
"*harness*. A pontuação será a fração dos testes de aceitação aprovados; esses testes são "
"escritos pelo autor antes da execução, ficam fora do espaço de trabalho, rodam sobre uma "
"cópia dele ao fim de cada unidade e nunca são os testes que o agente escreve, já que um "
"modelo que alucina uma API também escreve testes que simulam a alucinação. Uma unidade conta "
"como concluída quando todos os seus testes passam, e a construção, quando todos os testes de "
"todas as unidades passam ao fim.")

P[64] = ("Um único limite será imposto, idêntico para os dois braços. É um relógio de parede por "
"unidade, cujo valor será três vezes a maior mediana que os dois braços gastarem nas "
"unidades-piloto. O número de passos não será limitado, porque um teto de passos é ele "
"próprio uma decisão de projeto de *harness* e apagaria a diferença sob teste. O comprimento "
"máximo de saída será forçado idêntico pelo *proxy*. Os parâmetros de amostragem serão "
"registrados e relatados, mas não normalizados, já que o *gateway* os aceita sem os honrar, e "
"Miller (2024) desaconselha mexer na temperatura para reduzir variância. O isolamento de "
"ambiente será verificado por um portão que falha fechado.")

P[65] = ("Cada célula do experimento, o par (braço, nível), receberá n ≥ 3 construções completas, "
"contadas após os descartes, na função redutora de variância que Miller (2024) atribui à "
"reamostragem. Os resultados sairão como mediana com dispersão, porque requisições "
"byte-idênticas podem variar em tokens de saída em um nível gratuito, o que as unidades-piloto "
"vão medir. Quando a cota não comportar a matriz, a cobertura será reduzida antes das "
"repetições, já que a variância é a principal ameaça ao desenho.")

P[66] = ("A medida principal será o total de tokens por construção, sempre relatado ao lado da fração "
"final de testes aprovados, para que um braço que falhe barato não pareça o mais barato. A "
"comparação inferencial será pareada por unidade e usará o teste de Wilcoxon dos postos "
"sinalizados, bilateral, com α = 0,05, sobre duas medidas: os tokens de cada unidade e o "
"Succ/Mtok de cada unidade. O teste é não paramétrico porque nove pares não sustentam "
"suposição distribucional, e pareado porque a dificuldade da unidade é o maior fator de "
"perturbação do desenho, que é o que Miller (2024) recomenda ao preferir a diferença pareada "
"por questão à média agregada. As unidades não são independentes: a unidade seguinte parte do "
"que o mesmo braço construiu nas anteriores, então um erro cobra de novo mais adiante; essa "
"dependência é parte do custo do *harness* e será reportada por unidade, não corrigida. Com "
"n = 3 e 9 unidades, a diferença mínima detectável é de cerca de 0,76σ. Para H2, os tokens de "
"cada unidade serão decompostos em carga fixa (esquemas e *prompt* de sistema, medidos na "
"Camada 1, multiplicados pelo número de passos) e conteúdo da conversa, e a parcela de cada "
"uma na diferença entre braços será reportada por unidade e por construção. As predições serão "
"pré-registradas por nível de modelo, e um resultado nulo para H2 será um achado reportável.")

P[67] = ("Cada unidade de cada construção receberá exatamente uma classe. Aquela cujo agente não a "
"concluiu será um resultado, entrará na estatística com a fração de testes que aprovou, e a "
"construção segue para a unidade seguinte a partir do que ficou; nesse grupo, o estouro do "
"relógio de parede contará como resultado, já que repetir converteria uma indisponibilidade "
"do serviço em diferença aparente entre *harnesses*. Aquela cuja medição for inconfiável "
"descartará a construção inteira, registrada como tal, sem reparo nem repetição. A "
"classificação virá do registro do *proxy*, já que o código de saída não discrimina o "
"desfecho.")

P[69] = ("Quatro limitações são declaradas de partida. O efeito de um *harness* é específico do "
"modelo e pode inverter de sinal, o que restringe qualquer conclusão ao nível de modelo em que "
"for obtida; o objetivo (5) existe para testar isso. O produto é um único SaaS sobre uma única "
"pilha (TypeScript, TanStack Start, tRPC, Drizzle), então o resultado vale para tarefas dessa "
"família, e a transferência para outras pilhas fica registrada como trabalho futuro. A "
"especificação é escrita pelo autor, então carrega as escolhas de um humano, e cada braço "
"carrega os próprios erros de uma unidade para a seguinte; a mitigação é que os dois braços "
"recebem a mesma especificação e partem do mesmo espaço de trabalho vazio, e a comparação é "
"pareada por unidade. Os valores absolutos não serão comparáveis a placares públicos, porque o "
"produto é próprio, e os valores em dólar citados de fontes externas vêm de outros modelos e "
"de níveis pagos; a comparação válida aqui é entre os dois braços, e o custo em dinheiro será "
"um contrafactual de ordem de grandeza sobre tarifas pagas publicadas, rotulado como tal onde "
"apareça.")

# --- 4 ORÇAMENTO e 5 CRONOGRAMA --------------------------------------------
P[83] = ("O total em dinheiro é zero, e o limite que restringe o experimento será a cota do nível "
"gratuito do *gateway*, a ser medida nas unidades-piloto contra o número de requisições que "
"uma unidade do Finn consome. Por isso cada construção será executada em lotes distribuídos "
"ao longo de dias, retomada na fronteira entre unidades, e o custo monetário aparecerá apenas "
"como contrafactual de ordem de grandeza sobre as tarifas pagas publicadas.")

P[85] = ("A cota gratuita deve ser o limite vinculante, então a cadência prevista é de um lote da "
"matriz por dia e o calendário se estende por semanas. A folga está concentrada na execução "
"da matriz e na escrita da especificação e dos testes de aceitação, onde está o risco. Os "
"meses vão de agosto de 2026 a janeiro de 2027. A escrita deste projeto foi concluída em "
"setembro de 2026, mês de entrega, e os experimentos práticos ocorrem a partir de outubro.")

P[108] = "CONSTRUÇÃO DO INSTRUMENTO, DA ESPECIFICAÇÃO E DOS TESTES DE ACEITAÇÃO"


# Slop pass (2026-09-14): colon reveal in [61] and an "X, não Y" contrast in [66] rewritten as plain sentences.
P[61] = "O produto será o Finn, um SaaS multiempresa em que a empresa cliente fala com o próprio financeiro por voz e recebe lançamento, relatório e aviso no celular (YuukiFST, 2026a). As decisões de produto e de pilha foram registradas antes deste experimento em 21 *tickets* fechados no repositório. A partir deles o autor escreverá, antes de qualquer execução, uma especificação única, congelada por hash SHA-256: um documento com o produto, a pilha fixada pelo dono (TypeScript, TanStack Start, tRPC, Drizzle ORM, PostgreSQL, Vitest) e as restrições gerais, e nove unidades, uma por *ticket* técnico, em ordem de dependência: separação por empresa, governança, *flags* por empresa, *pipeline* de voz, confirmação da transcrição, registro de auditoria, relatório, agendador e cobrança. Cada braço recebe os mesmos bytes e constrói o produto do zero em um único espaço de trabalho: o executor invoca o *harness* uma vez por unidade, em ordem, com um *prompt* idêntico para os dois braços, e o que o agente construiu em uma unidade é o ponto de partida da seguinte. O autor não escreve código algum no espaço de trabalho depois do início. Os dois braços recebem a mesma entrada, e por isso a diferença de tokens fica atribuível ao *harness*. A pontuação será a fração dos testes de aceitação aprovados; esses testes são escritos pelo autor antes da execução, ficam fora do espaço de trabalho, rodam sobre uma cópia dele ao fim de cada unidade e nunca são os testes que o agente escreve, já que um modelo que alucina uma API também escreve testes que simulam a alucinação. Uma unidade conta como concluída quando todos os seus testes passam, e a construção, quando todos os testes de todas as unidades passam ao fim."
P[66] = "A medida principal será o total de tokens por construção, sempre relatado ao lado da fração final de testes aprovados, para que um braço que falhe barato não pareça o mais barato. A comparação inferencial será pareada por unidade e usará o teste de Wilcoxon dos postos sinalizados, bilateral, com α = 0,05, sobre duas medidas: os tokens de cada unidade e o Succ/Mtok de cada unidade. O teste é não paramétrico porque nove pares não sustentam suposição distribucional, e pareado porque a dificuldade da unidade é o maior fator de perturbação do desenho, que é o que Miller (2024) recomenda ao preferir a diferença pareada por questão à média agregada. As unidades não são independentes, já que a seguinte parte do que o mesmo braço construiu nas anteriores, e um erro cobra de novo mais adiante. Essa dependência é parte do custo do *harness* e será reportada por unidade. Com n = 3 e 9 unidades, a diferença mínima detectável é de cerca de 0,76σ. Para H2, os tokens de cada unidade serão decompostos em carga fixa (esquemas e *prompt* de sistema, medidos na Camada 1, multiplicados pelo número de passos) e conteúdo da conversa, e a parcela de cada uma na diferença entre braços será reportada por unidade e por construção. As predições serão pré-registradas por nível de modelo, e um resultado nulo para H2 será um achado reportável."

print(json.dumps({"paragraphs": {str(k): v for k, v in P.items()}}, ensure_ascii=False, indent=2))
