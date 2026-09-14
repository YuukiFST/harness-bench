"""Prose edits applied to dist/projeto-pcc.docx on 2026-09-11.

Three things change: the justificativa carries the market and company stake
(who uses coding agents at work, who pays), every sentence about work not yet
done moves to the future tense, and the Camada 1 pilot results leave the text,
because a projeto de pesquisa describes what will be done. Paragraph indices are
the ones `tools/docx_prose.py dump` printed against 9cc41e9.

Usage:
    python tools/pcc_edits_2026-09-11.py > /tmp/edits.json
    python tools/docx_prose.py apply dist/projeto-pcc.docx /tmp/edits.json
"""

import json
import math
import re
import sys

P = {}

# --- 1 INTRODUÇÃO -----------------------------------------------------------
P[26] = ("Agentes de codificação já são ferramenta de trabalho. Entre mais de 15.000 "
"desenvolvedores profissionais, 39% usavam o Claude Code no trabalho em 2026, 16% o Codex e "
"12% o Cursor (Bogdanov, 2026). Cada um é um *harness*, a camada de software em torno do "
"modelo, e ela muda a conta com o modelo fixo. No FrontierHarness (Runta, 2026), "
"nove *harnesses* sobre o mesmo modelo ficam entre 50,0% e 66,7% de aprovação, e o custo "
"por tarefa concluída varia 17x, de US$ 1,05 a US$ 18,34.")

P[27] = ("Quem paga essa conta é o desenvolvedor, na assinatura pessoal, e a empresa que adota a "
"ferramenta em escala; conhecer o *harness* virou parte do ofício. As comparações "
"publicadas contrastam ferramentas de equipes diferentes e não dizem qual decisão de "
"projeto pesa. Este projeto medirá esse efeito com a linhagem "
"fixa, comparando o pi com seu *fork* direto, o oh-my-pi, e dará ao desenvolvedor e à "
"empresa um critério de escolha, e à literatura a primeira comparação desse tipo.")

P[29] = ("A escolha do *harness* como decisão de engenharia do desenvolvedor e da empresa: seu "
"efeito sobre o custo por tarefa concluída e sobre a taxa de sucesso de agentes de "
"codificação, mantido fixo o modelo de linguagem.")

P[31] = ("Para o desenvolvedor ou a empresa que já escolheu o modelo, quanto do custo por tarefa "
"concluída e da taxa de sucesso do agente de codificação é determinado pelo *harness* "
"adotado? E quais decisões de projeto do *harness* respondem por essa diferença, de modo que "
"seja possível agir sobre elas?")

P[33] = ("Medir, com o modelo de linguagem mantido fixo, quanto o *harness* adotado determina o "
"custo por tarefa concluída e a taxa de sucesso de um agente de codificação, isolando "
"decisões específicas de projeto pela comparação entre um *harness* e um *fork* direto dele, "
"e entregar o resultado como critério de escolha reproduzível pelo desenvolvedor.")

P[43] = ("A pesquisa é aplicada, quali-quantitativa, exploratória e experimental, e o método é "
"dedutivo, porque parte de hipóteses declaradas e as submete a teste. Os dados serão "
"coletados por um instrumento próprio, um proxy reverso interposto entre cada *harness* e o "
"modelo, que contará requisições, tokens e latência da mesma forma para todos os braços. "
"Cada par de braço e tarefa será executado ao menos três vezes sobre uma suíte fixa do "
"DeepSWE, e a comparação será feita por teste pareado sobre o Succ/Mtok de cada tarefa. "
"Espera-se obter a diferença de custo por tarefa concluída e de taxa de sucesso atribuível "
"ao *harness*, em forma utilizável por quem escolhe a ferramenta. A seção 3 detalha "
"material, método e tratamento estatístico.")

P[45] = ("H1 — Entre *harnesses* distintos executando o mesmo modelo, a diferença de custo por "
"tarefa concluída é de ordem prática relevante para quem paga a conta, comparável à "
"diferença obtida ao se trocar de modelo sob um *harness* fixo. H1 será refutada se os "
"intervalos de Succ/Mtok dos braços se sobrepuserem ao longo de toda a suíte.")

P[46] = ("H2 — Essa diferença persiste entre um *harness* e um *fork* direto dele, o que indicaria "
"que ela vem de decisões de projeto isoláveis (prompt de sistema, número e tamanho dos "
"esquemas de ferramenta, política de compactação de contexto), e não do acúmulo de "
"diferenças entre bases de código independentes. H2 será refutada se pi e oh-my-pi não "
"diferirem significativamente em Succ/Mtok, mesmo que a Camada 1 confirme que o *fork* "
"envia uma carga maior por requisição. Esse desfecho é possível e seria, ele próprio, um "
"achado a reportar, pois o oh-my-pi pode recuperar a carga extra concluindo a tarefa em "
"menos passos.")

P[47] = ("Este trabalho segue as normas do curso (IFMT, 2022) e as da ABNT (2023, 2025a, "
"2025b)[[FN]], e está organizado em seis seções. Esta introdução apresenta a justificativa, "
"o tema, o problema, os objetivos, a metodologia e as hipóteses. A seção 2 posiciona o "
"trabalho na literatura e delimita as pendências que ele se propõe a resolver. A seção 3 "
"descreve o material e o método: classificação da pesquisa, camadas de medição, braços, "
"suíte de tarefas, limites, tratamento estatístico e limitações. A seção 4 apresenta o "
"orçamento, a seção 5 o cronograma, e a seção 6 reúne as referências.")

# --- 2 REFERENCIAL TEÓRICO --------------------------------------------------
P[52] = ("A interface entre modelo e ambiente é objeto de projeto desde Yang *et al.* (2024). "
"Que o *harness* importa já está estabelecido. Lin *et al.* (2026) medem 24,7 pontos "
"percentuais de dispersão entre *harnesses* humanos sobre um modelo congelado, e Zhang "
"*et al.* (2026) enunciam a *Binding Constraint Thesis*, segundo a qual, em tarefas de longo "
"horizonte, o *harness* determina o desempenho mais que o modelo que encapsula. Em Alier "
"Forment *et al.* (2026), os dois *scaffoldings* sem suporte a MCP saíram de 5,0x a 28x mais "
"baratos que os cinco que o suportam. Somam-se três fontes não revisadas por pares. O "
"HarnessRank (2026) ordena *harnesses* por custo. O FrontierHarness (Runta, 2026) compara, "
"sobre o mesmo modelo, as ferramentas que o desenvolvedor encontra no mercado: o Codex "
"conclui 66,7% das tarefas a US$ 3,47 por tarefa concluída e o Claude Code 63,3% a "
"US$ 18,34, 5,3x mais caro para uma taxa próxima. O estudo da Databricks registra custo "
"por tarefa variando mais de 2x sem mudança de qualidade (Databricks, 2026 *apud* "
"Earendil, 2026).")

P[53] = ("A primeira pendência é de atribuição. Toda comparação publicada contrasta *harnesses* "
"de equipes diferentes sobre fundações diferentes, e a dispersão medida agrega prompt, "
"ferramentas, gestão de contexto e desenho do laço sem separá-los. O desenvolvedor sabe "
"qual ferramenta ganhou, mas não o que a fez ganhar. Ning *et al.* (2026) nomeiam a lacuna "
"em §5.2.1 e pedem, em §5.2.7, “métricas que isolem componentes do *harness*” (Ning *et "
"al.*, 2026, tradução nossa). Essas decisões são isoláveis. Lee *et al.* (2026) otimizam o "
"código do *harness* e ganham 7,7 pontos usando 4x menos tokens de contexto. O par pi / "
"oh-my-pi responderá a §5.2.7 pelo lado do controle, já que um *fork* direto mantém a "
"linhagem fixa e faz variar apenas as modificações.")

P[54] = ("A segunda pendência é de instrumentação, e atinge o desenvolvedor diretamente, porque "
"ele decide pelo relatório da própria ferramenta. O que um *harness* relata sobre o próprio "
"custo diverge do que ele gasta, e cada um omite um conjunto diferente de chamadas reais ao "
"modelo. Kapoor *et al.* (2024) mostram que a avaliação de agentes ignora o custo e por "
"isso erra sobre a origem dos ganhos, e Kapoor *et al.* (2025) registram que as avaliações "
"raramente relatam custo e que comparações entre *harnesses* são raras. Por isso a medição "
"ocorrerá em um proxy externo, e o objetivo (6) quantificará essa divergência.")

P[55] = ("A métrica primária será o Succ/Mtok (sucesso por milhão de tokens), de Lin *et al.* "
"(2026), a razão que interessa a quem paga a conta. Sobre ela pesa uma ressalva permanente, "
"a de que o efeito é específico do modelo e pode inverter de sinal. No *Holistic Agent "
"Leaderboard*, os modelos da Anthropic vão melhor com o BrowserUse e os da OpenAI com o "
"SeeAct sobre o mesmo *benchmark* (Kapoor *et al.*, 2025), e o FrontierHarness registra "
"aproveitamento de cache ponderado por tokens caindo a 25,0% contra uma mediana de 67,8% "
"(Runta, 2026). Por isso o desenho carregará dois níveis de modelo, e as conclusões serão "
"enunciadas por nível.")

# --- 3 MATERIAL E MÉTODO ----------------------------------------------------
P[57] = ("Quanto à finalidade, esta é uma pesquisa aplicada, e seu produto será um critério de "
"escolha que um desenvolvedor ou uma empresa poderá aplicar. Quanto à abordagem, é "
"quali-quantitativa. As medidas de custo e de sucesso são quantitativas, e a atribuição de "
"cada diferença a uma decisão de projeto do *harness* é qualitativa. Quanto aos objetivos, "
"é exploratória, porque a comparação com linhagem de *harness* fixa não tem precedente "
"publicado. Quanto aos procedimentos, é experimental, com variável independente manipulada "
"(o *harness*), variáveis controladas (modelo, tarefa e limites) e um grupo de controle. "
"Quanto ao método, é dedutivo, porque parte de hipóteses declaradas antes da coleta e as "
"submete a teste (Gil, 2022; Prodanov; Freitas, 2013).")

P[58] = ("A medição ocorrerá em duas camadas, cada uma relatada em separado. A Camada 1 medirá "
"a forma da requisição contra um endpoint simulado que não encaminha nada ao modelo. Ela "
"não consome cota, é determinística e nomeia o mecanismo, pois registra quantos esquemas de "
"ferramenta, quantos bytes de prompt de sistema e quantos tokens cada braço envia na "
"primeira requisição e a cada passo seguinte. A Camada 2 medirá o desfecho das tarefas "
"contra o modelo real. Ela consome cota, é estocástica e mostra o efeito. Um *harness* que "
"envia mais bytes por requisição não é, por isso, proporcionalmente pior, e a Camada 2 é "
"que dirá quanto dessa carga chega ao resultado.")

P[59] = ("O conjunto de braços é provisório até o fechamento das verificações de "
"confiabilidade. Serão o *harness* zero, o conjunto de implementações de terceiros e o par "
"de destaque pi / oh-my-pi. O executor não traz adaptador para pi nem para oh-my-pi "
"(Datacurve, 2026); os dois adaptadores, e o *harness* zero, serão escritos neste projeto e "
"publicados no repositório dele (YuukiFST, 2026). O *harness* zero será o controle "
"científico e o único braço que este projeto escreve: um laço observar/agir com três "
"ferramentas (leitura de arquivo, escrita de arquivo e execução de comandos). Não terá "
"planejamento, compactação de contexto, repetição automática de requisições nem qualquer "
"chamada auxiliar ao modelo, e será mantido abaixo de 400 linhas de Python por um portão de "
"integração contínua. Ele medirá quanto qualquer *harness* acrescenta sobre o laço mais cru "
"capaz de concluir a tarefa.")

P[60] = ("A suíte será composta por 8 tarefas Python do DeepSWE (Huang *et al.*, 2026), "
"congeladas na adoção e fixadas por *commit* e por *hash* SHA-256 de cada tarefa. São "
"tarefas de implementação de longo horizonte sobre repositórios reais. O *benchmark* "
"completo tem 113 tarefas sobre 91 repositórios, com soluções de referência que tocam cerca "
"de 5,5x mais código que as do SWE-Bench Pro, outra ordem de grandeza ante o SWE-bench "
"(Jimenez *et al.*, 2023). A pontuação adotada será o crédito parcial, a fração de testes "
"aprovados do verificador de cada tarefa. É uma adaptação, porque o DeepSWE grada de forma "
"binária e declara a ausência de crédito parcial como limitação (Huang *et al.*, 2026, §8). "
"Sem ela, um escore binário tenderia a ler zero para todos os braços neste nível de modelo, "
"o que será confirmado nas tarefas-piloto.")

P[61] = ("Serão dois níveis de modelo, um primário e um de robustez, ambos gratuitos e no mesmo "
"gateway (Opencode, 2026), relatados em separado. O segundo existe porque o efeito do "
"*harness* é específico do modelo. Se a ordenação entre braços se inverter entre os níveis, "
"a inversão será o resultado a reportar.")

P[62] = ("O instrumento de medição será um proxy reverso interposto entre cada braço e o "
"gateway, que forçará a emissão do relatório de uso em cada requisição. Os tokens serão "
"contados no proxy, sobre os bytes efetivamente transmitidos, com um único tokenizador "
"divulgado para todos os braços e níveis. A contagem virá do proxy porque o relatório do "
"*harness* e o do gateway incluem conteúdo injetado que nenhum braço enviou. Esse "
"deslocamento aditivo por requisição não se cancela em uma razão e cobraria de cada braço "
"um excedente proporcional ao número de passos, que é um dos comportamentos sob teste. As "
"contagens do gateway permanecerão registradas para verificação cruzada e para o cálculo "
"de custo, e a divergência entre elas e as do proxy será reportada por braço.")

P[63] = ("Um único limite será imposto, idêntico para todos os braços. É um relógio de parede, "
"cujo valor será três vezes a mediana que o *harness* zero gastar nas tarefas-piloto. O "
"número de passos não será limitado, porque um teto de passos é ele próprio uma decisão de "
"projeto de *harness* e apagaria a diferença sob teste. O comprimento máximo de saída será "
"forçado idêntico pelo proxy. Os parâmetros de amostragem serão registrados e relatados, "
"mas não normalizados, já que o gateway os aceita sem os honrar, e Miller (2024) "
"desaconselha mexer na temperatura para reduzir variância. O isolamento de ambiente será "
"verificado por um portão que falha fechado.")

P[64] = ("Cada célula do experimento, a tripla (braço, tarefa, nível), receberá n ≥ 3 execuções "
"completas, contadas após os descartes, na função redutora de variância que Miller (2024) "
"atribui à reamostragem. Os resultados sairão como mediana com dispersão, porque "
"requisições byte-idênticas podem variar em tokens de saída em um nível gratuito, o que as "
"tarefas-piloto vão medir. Quando a cota não comportar a matriz, a cobertura será reduzida "
"antes das repetições, já que a variância é a principal ameaça ao desenho.")

P[65] = ("A comparação será pareada por tarefa e usará o teste de Wilcoxon dos postos "
"sinalizados sobre o Succ/Mtok por tarefa, bilateral, com α = 0,05. O teste é não "
"paramétrico porque oito pares não sustentam suposição distribucional, e pareado porque a "
"dificuldade da tarefa é o maior fator de perturbação do desenho, que é o que Miller (2024) "
"recomenda ao preferir a diferença pareada por questão à média agregada. Com n = 3 e 8 "
"tarefas, a diferença mínima detectável é de cerca de 0,81σ. As predições serão "
"pré-registradas por nível de modelo, e um resultado nulo para H2 será um achado "
"reportável.")

P[66] = ("Cada execução receberá exatamente uma classe. Aquela cujo agente não cumpriu a tarefa "
"será um resultado, entrará na estatística e receberá escore zero; nesse grupo, o estouro "
"do relógio de parede contará como resultado, já que repetir converteria uma "
"indisponibilidade do serviço em diferença aparente entre *harnesses*. Aquela cuja medição "
"for inconfiável será descartada e registrada como tal, sem reparo nem repetição. A "
"classificação virá do registro do proxy, que discrimina o desfecho; o código de saída não "
"o faz.")

# Resultados preliminares: label, paragraph, caption and source line; the table
# itself goes through delete_tables_containing.
for i in (67, 68, 69, 94):
    P[i] = None

P[96] = ("Quatro limitações são declaradas de partida. O efeito de um *harness* é específico do "
"modelo e pode inverter de sinal, o que restringe qualquer conclusão ao nível de modelo em "
"que for obtida; o objetivo (5) existe para testar isso. A transferência para modelos "
"pequenos fica deliberadamente em aberto e é registrada como trabalho futuro, porque o "
"único modelo pequeno viável havia sido treinado dentro de um dos braços, o que invalidaria "
"a medição de destaque em vez de apenas limitá-la. Os valores absolutos não serão "
"comparáveis ao placar público do DeepSWE, porque toda linha de base publicada usa um "
"*harness* de ferramenta única, e os valores em dólar citados de fontes externas vêm de "
"outros modelos e de níveis pagos; a comparação válida aqui é entre os próprios braços. O "
"custo em dinheiro será um contrafactual de ordem de grandeza sobre tarifas pagas "
"publicadas, rotulado como tal onde apareça.")

# --- 4 ORÇAMENTO / 5 CRONOGRAMA ---------------------------------------------
P[110] = ("O total em dinheiro é zero, e o limite que restringe o experimento será a cota do "
"nível gratuito do gateway, a ser medida nas tarefas-piloto contra o número de requisições "
"que uma tarefa do DeepSWE consome. Por isso a matriz será executada em lotes distribuídos "
"ao longo de dias, e o custo monetário aparecerá apenas como contrafactual de ordem de "
"grandeza sobre as tarifas pagas publicadas.")

P[112] = ("A cadência prevista é de um lote da matriz por dia, porque a cota gratuita deve ser o "
"limite vinculante, e por isso o calendário se estende por semanas. A folga está "
"concentrada na execução da matriz e nos portões de confiabilidade dos braços, onde está o "
"risco. Os meses vão de setembro de 2026, mês de entrega deste projeto, a janeiro de 2027.")

# New reference, alphabetical slot after ABNT NBR 15287 (paragraph 185).
INSERT = {185: ("BOGDANOV, Mikhail. **AI coding agents**: adoption trends. 2026. Publicação de "
"blogue institucional (JetBrains Research). Disponível em: "
"https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/. "
"Acesso em: 11 set. 2026.")}


def main() -> None:
    # Template caps the justificativa at 12 lines; legacy/build_pcc.py counts 79 chars per line.
    lines = sum(math.ceil(len(re.sub(r"\*", "", P[i])) / 79) for i in (26, 27))
    print(f"justificativa: {lines} linhas (max 12)", file=sys.stderr)
    sys.stdout.reconfigure(encoding="utf-8")
    json.dump({"paragraphs": {str(k): v for k, v in P.items()},
               "insert_after": {str(k): v for k, v in INSERT.items()},
               "delete_tables_containing": ["oh-my-pi 17.2.10"]},
              sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
