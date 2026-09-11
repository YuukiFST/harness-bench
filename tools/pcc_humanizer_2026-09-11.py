"""Humanizer pass over dist/projeto-pcc.docx, 2026-09-11.

Second pass after pcc_edits_2026-09-11.py, following .claude/skills/humanizer:
staged one-liners merged into the sentence they announced, parallel triads and
repeated openings in the Camada 1/2 paragraph rewritten, "X, e não Y" tails cut
where the negative half carried nothing, em dashes on the hypothesis labels
replaced, and one doubled causal closer flattened. Claims, numbers and
citations are unchanged. Indices are from `docx_prose.py dump` after the first
pass.

Usage:
    python tools/pcc_humanizer_2026-09-11.py > /tmp/humanize.json
    python tools/docx_prose.py apply dist/projeto-pcc.docx /tmp/humanize.json
"""

import json
import math
import re
import sys

P = {}

P[26] = ("Agentes de codificação são ferramenta de trabalho. Entre mais de 15.000 "
"desenvolvedores profissionais, 39% usavam o Claude Code no trabalho em 2026, 16% o Codex e "
"12% o Cursor (Bogdanov, 2026). Cada um é um *harness*, a camada de software ao redor do "
"modelo, e ela muda o custo com o modelo fixo. No FrontierHarness (Runta, 2026), nove "
"*harnesses* sobre o mesmo modelo ficam entre 50,0% e 66,7% de aprovação, e o custo por "
"tarefa concluída varia 17x (US$ 1,05 a US$ 18,34).")

P[27] = ("Quem paga essa conta é o desenvolvedor, na assinatura pessoal, e a empresa que adota a "
"ferramenta em escala; conhecer o *harness* virou parte do ofício. As comparações "
"publicadas contrastam ferramentas de equipes diferentes e não dizem qual decisão de "
"projeto pesa. Este projeto medirá esse efeito com a linhagem fixa, comparando o pi com seu "
"*fork* direto, o oh-my-pi, e dará ao desenvolvedor e à empresa um critério de escolha, e à "
"literatura a primeira comparação desse tipo.")

P[43] = ("A pesquisa é aplicada, quali-quantitativa, exploratória e experimental, e o método é "
"dedutivo, com hipóteses declaradas antes da coleta. Os dados serão coletados por um "
"instrumento próprio, um proxy reverso interposto entre cada *harness* e o modelo, que "
"contará requisições, tokens e latência da mesma forma para todos os braços. Cada par de "
"braço e tarefa será executado ao menos três vezes sobre uma suíte fixa do DeepSWE, e a "
"comparação será feita por teste pareado sobre o Succ/Mtok de cada tarefa. Espera-se obter "
"a diferença de custo por tarefa concluída e de taxa de sucesso atribuível ao *harness*, em "
"forma utilizável por quem escolhe a ferramenta. A seção 3 detalha material, método e "
"tratamento estatístico.")

P[45] = ("H1: entre *harnesses* distintos executando o mesmo modelo, a diferença de custo por "
"tarefa concluída é de ordem prática relevante para quem paga a conta, comparável à "
"diferença obtida ao se trocar de modelo sob um *harness* fixo. H1 será refutada se os "
"intervalos de Succ/Mtok dos braços se sobrepuserem ao longo de toda a suíte.")

P[46] = ("H2: essa diferença persiste entre um *harness* e um *fork* direto dele, o que indicaria "
"que ela vem de decisões de projeto isoláveis (prompt de sistema, número e tamanho dos "
"esquemas de ferramenta, política de compactação de contexto), e não do acúmulo de "
"diferenças entre bases de código independentes. H2 será refutada se pi e oh-my-pi não "
"diferirem significativamente em Succ/Mtok, mesmo que a Camada 1 confirme que o *fork* "
"envia uma carga maior por requisição. Esse desfecho é possível e seria um achado a "
"reportar, já que o oh-my-pi pode compensar a carga extra concluindo a tarefa em menos "
"passos.")

P[52] = ("A interface entre modelo e ambiente é objeto de projeto desde Yang *et al.* (2024). "
"Lin *et al.* (2026) medem 24,7 pontos percentuais de dispersão entre *harnesses* humanos "
"sobre um modelo congelado, e Zhang *et al.* (2026) enunciam a *Binding Constraint "
"Thesis*, segundo a qual, em tarefas de longo horizonte, o *harness* determina o "
"desempenho mais que o modelo que encapsula. Em Alier Forment *et al.* (2026), os dois "
"*scaffoldings* sem suporte a MCP saíram de 5,0x a 28x mais baratos que os cinco que o "
"suportam. Somam-se três fontes não revisadas por pares. O HarnessRank (2026) ordena "
"*harnesses* por custo. O FrontierHarness (Runta, 2026) compara, sobre o mesmo modelo, as "
"ferramentas que o desenvolvedor encontra no mercado: o Codex conclui 66,7% das tarefas a "
"US$ 3,47 por tarefa concluída e o Claude Code 63,3% a US$ 18,34, 5,3x mais caro para uma "
"taxa próxima. O estudo da Databricks registra custo por tarefa variando mais de 2x sem "
"mudança de qualidade (Databricks, 2026 *apud* Earendil, 2026).")

P[53] = ("A primeira pendência é de atribuição. Toda comparação publicada contrasta *harnesses* "
"de equipes diferentes sobre fundações diferentes, e a dispersão medida agrega prompt, "
"ferramentas, gestão de contexto e desenho do laço sem separá-los. O desenvolvedor sabe "
"qual ferramenta ganhou, mas não o que a fez ganhar. Ning *et al.* (2026) nomeiam a lacuna "
"em §5.2.1 e pedem, em §5.2.7, “métricas que isolem componentes do *harness*” (Ning *et "
"al.*, 2026, tradução nossa). Lee *et al.* (2026) mostram que essas decisões são "
"isoláveis ao otimizar o código do *harness* e ganhar 7,7 pontos usando 4x menos tokens de "
"contexto. O par pi / oh-my-pi responderá a §5.2.7 pelo lado do controle, já que um *fork* "
"direto mantém a linhagem fixa e faz variar apenas as modificações.")

P[58] = ("A medição ocorrerá em duas camadas, relatadas em separado. A Camada 1 medirá a forma "
"da requisição contra um endpoint simulado que não encaminha nada ao modelo: quantos "
"esquemas de ferramenta, quantos bytes de prompt de sistema e quantos tokens cada braço "
"envia na primeira requisição e a cada passo seguinte. Essa camada não consome cota e é "
"determinística. A Camada 2 medirá o desfecho das tarefas contra o modelo real, consome "
"cota e é estocástica. Mais bytes por requisição não significam, por si, resultado pior; a "
"Camada 2 dirá quanto dessa carga chega ao resultado.")

P[59] = ("O conjunto de braços é provisório até o fechamento das verificações de "
"confiabilidade. Serão o *harness* zero, o conjunto de implementações de terceiros e o par "
"de destaque pi / oh-my-pi. O executor não traz adaptador para pi nem para oh-my-pi "
"(Datacurve, 2026); os dois adaptadores, e o *harness* zero, serão escritos neste projeto e "
"publicados no repositório dele (YuukiFST, 2026). O *harness* zero será o controle "
"científico e o único *harness* que este projeto escreve: um laço observar/agir com três "
"ferramentas (leitura de arquivo, escrita de arquivo e execução de comandos). Não terá "
"planejamento, compactação de contexto, repetição automática de requisições nem qualquer "
"chamada auxiliar ao modelo, e será mantido abaixo de 400 linhas de Python por um portão de "
"integração contínua. Ele medirá quanto qualquer *harness* acrescenta sobre o laço mais cru "
"capaz de concluir a tarefa.")

P[66] = ("Cada execução receberá exatamente uma classe. Aquela cujo agente não cumpriu a tarefa "
"será um resultado, entrará na estatística e receberá escore zero; nesse grupo, o estouro "
"do relógio de parede contará como resultado, já que repetir converteria uma "
"indisponibilidade do serviço em diferença aparente entre *harnesses*. Aquela cuja medição "
"for inconfiável será descartada e registrada como tal, sem reparo nem repetição. A "
"classificação virá do registro do proxy, já que o código de saída não discrimina o "
"desfecho.")

P[68] = ("Quatro limitações são declaradas de partida. O efeito de um *harness* é específico do "
"modelo e pode inverter de sinal, o que restringe qualquer conclusão ao nível de modelo em "
"que for obtida; o objetivo (5) existe para testar isso. A transferência para modelos "
"pequenos fica deliberadamente em aberto e é registrada como trabalho futuro, porque o "
"único modelo pequeno viável havia sido treinado dentro de um dos braços, o que invalidaria "
"a medição de destaque. Os valores absolutos não serão comparáveis ao placar público do "
"DeepSWE, porque toda linha de base publicada usa um *harness* de ferramenta única, e os "
"valores em dólar citados de fontes externas vêm de outros modelos e de níveis pagos; a "
"comparação válida aqui é entre os próprios braços. O custo em dinheiro será um "
"contrafactual de ordem de grandeza sobre tarifas pagas publicadas, rotulado como tal onde "
"apareça.")

P[84] = ("A cota gratuita deve ser o limite vinculante, então a cadência prevista é de um lote "
"da matriz por dia e o calendário se estende por semanas. A folga está concentrada na "
"execução da matriz e nos portões de confiabilidade dos braços, onde está o risco. Os "
"meses vão de setembro de 2026, mês de entrega deste projeto, a janeiro de 2027.")


def main() -> None:
    lines = sum(math.ceil(len(re.sub(r"\*", "", P[i])) / 79) for i in (26, 27))
    print(f"justificativa: {lines} linhas (max 12)", file=sys.stderr)
    sys.stdout.reconfigure(encoding="utf-8")
    json.dump({"paragraphs": {str(k): v for k, v in P.items()}},
              sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
