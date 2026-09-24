"""Rebuild dist/roteiro-apresentacao.html for the 33-slide explainer deck
(dist/apresentacao-explainer/index.html) after the 2026-09-18 docx rewrite.
Keeps the stylesheet of the previous script; every section is regenerated.

Run: python tools/roteiro_2026-09-18.py
"""
import html as H
import re
from pathlib import Path

OUT = Path("dist/roteiro-apresentacao.html")
STYLE = re.search(r"<style>.*?</style>", OUT.read_text(encoding="utf-8"), re.S).group(0)

TITLE = "Como o <em>harness</em> altera o custo e o desempenho do modelo"

# (title, time, fale[], numeros[(valor, denominador)], fontes[], perguntas[(q, a)], no_slide)
SLIDES = [
 ("Capa", "20 s", [
   "Bom dia. Meu nome é Fausto Yuuki, curso Sistemas para Internet, orientadora professora Inara Silva. O projeto se chama <em>Como o harness altera o custo e o desempenho de um modelo de linguagem</em>: tokens e taxa de sucesso de agentes de codificação com o modelo fixo.",
   "A ideia em uma frase: na era dos agentes, o modelo não avança sozinho. O <em>harness</em> em volta dele avança junto, e é ele que eu meço."],
  [], [], [], "<kbd>→</kbd> avança. <kbd>F</kbd> tela cheia antes de começar. <kbd>N</kbd> (notas) desligado."),
 ("Seção 1 · Introdução", "10 s", [
   "Seção 1. O <em>harness</em> muda o que o mesmo modelo custa e entrega. Vou mostrar por que isso importa, a pergunta que abre e o que o projeto promete medir."],
  [], [], [], "só passar"),
 ("O problema em números", "60 s", [
   "FrontierHarness, setembro de 2026: doze configurações de nove <em>harnesses</em>, todas sobre o mesmo modelo, o Kimi K3, 30 tarefas, uma tentativa por célula.",
   "A taxa de aprovação fica entre 50,0 % e 66,7 %. O custo por tarefa aprovada vai de US$ 1,05 a US$ 18,34. Claude Code e DSH Creator aprovam as mesmas 19 tarefas e um custa 5,6 vezes o outro, razão que o próprio post declara. O modelo não mudou; o que mudou foi o <em>harness</em>.",
   "Os dois cartões de baixo são os meus braços: pi, 60,0 % a US$ 2,43; OpenCode, 50,0 % a US$ 3,24. Quem paga essa conta é o desenvolvedor, na assinatura, e a empresa, em escala."],
  [("US$ 1,05–18,34", "custo por tarefa aprovada, 12 configurações, Kimi K3, 30 tarefas, 1 tentativa"), ("5,6×", "Claude Code vs DSH Creator, mesma aprovação de 63,3 %; razão declarada no post"), ("50,0–66,7 %", "aprovação, 12 configurações, Kimi K3, 30 tarefas, 1 tentativa"), ("pi US$ 2,43", "60,0 % de aprovação, mesmo post"), ("OpenCode US$ 3,24", "50,0 % de aprovação, mesmo post")],
  ["Runta (2026), <i>Introducing the FrontierHarness eval</i>, blogue institucional de 1 set. 2026, não revisado por pares. Diga isso antes que perguntem."],
  [("Isso é fonte confiável?", "É a única medição pública que fixa o modelo e varia o <em>harness</em> em escala. Uso como motivação. A evidência revisada por pares está no slide 12: SWE-agent, NeurIPS 2024."),
   ("Uma tentativa por célula não é pouco?", "É. Por isso o meu desenho pede n ≥ 3 por célula e reporta mediana com dispersão.")],
  "<kbd>→</kbd> revela os cartões"),
 ("FrontierHarness: custo × aprovação", "45 s", [
   "A mesma tabela em duas dimensões. Para a direita, mais caro; para cima, mais tarefas aprovadas. Passar e passar barato são habilidades separadas.",
   "O ponto isolado à direita é o Claude Code: aprova as mesmas 19 tarefas que o DSH Creator, 63,3 %, e custa US$ 18,34 contra US$ 3,28 por aprovação. Os meus dois braços, pi em teal e OpenCode em ferrugem, ficam perto um do outro. Se a diferença entre eles construindo um produto inteiro for pequena, isso também é resposta."],
  [("US$ 3,28 vs US$ 18,34", "DSH Creator vs Claude Code, mesma aprovação de 63,3 %; 5,6× no post"), ("pi v0.84.2 · OpenCode v1.18.19", "versões no repositório do eval")],
  ["Runta (2026), tabela do post; Kimi K3 via Fireworks."],
  [("Por que escala logarítmica?", "Sem ela o Claude Code esmaga os outros onze pontos num canto. A razão entre vizinhos é o que importa, e o log preserva razão.")],
  "pular se faltar tempo"),
 ("Justificativa e tema", "60 s", [
   "Justificativa. Os agentes de codificação avançam em duas frentes: o modelo e o <em>harness</em> em volta dele. As ferramentas também se movem: Next.js, TanStack e Effect estão se adaptando ao trabalho de agentes. Escolher o modelo deixou de bastar. O desenvolvedor, na assinatura, e a empresa, em escala, precisam conhecer o que avança junto, e o <em>harness</em> é a parte dessa escolha que ninguém mediu na construção de um produto inteiro. As comparações publicadas usam tarefas isoladas.",
   "Tema, e vou ler: o efeito do <em>harness</em> sobre o custo e o desempenho de um modelo de linguagem fixo. Quantos tokens e que taxa de sucesso o mesmo modelo entrega ao construir o mesmo produto sob dois <em>harnesses</em>.",
   "Como eu meço: construindo o Finn duas vezes, com o OpenCode e com o pi, sobre o mesmo modelo e a mesma especificação, com os tokens contados fora do <em>harness</em>."],
  [],
  ["Projeto, §1, parágrafos [43]–[44] (justificativa) e [46] (tema). Next.js, TanStack e Effect entram como observação do autor, sem citação: a lista de referências fica no tema do <em>harness</em>."],
  [("Por que não deixar o OpenCode construir e gerar a especificação para o pi?", "Entrada desigual. O pi receberia um documento destilado de um sistema pronto e a diferença deixaria de ser atribuível ao <em>harness</em>. A especificação é minha, vem das <em>issues</em> e é a mesma para os dois."),
   ("Onde está a fonte para Next.js, TanStack e Effect?", "Não cito: é constatação de mercado, e a lista de referências só tem fontes sobre o <em>harness</em>. Se a banca pedir, retiro a frase; o argumento se sustenta sem ela.")],
  "<kbd>→</kbd> revela os três cartões"),
 ("Problema de pesquisa", "30 s", [
   "O problema, na íntegra: com o modelo já escolhido, quanto mudam o custo em tokens e a taxa de sucesso ao construir o mesmo software com um <em>harness</em> em vez de outro, e quanto dessa diferença vem da carga fixa que cada <em>harness</em> envia em toda requisição?",
   "A primeira metade vira H1; a segunda, H2."],
  [], ["Projeto, §1 [48]."],
  [("Por que tokens e não dólares?", "Dólar depende do preço do modelo, do nível de assinatura e do dia. Token é a unidade que o <em>harness</em> controla. Dinheiro entra como contrafactual rotulado.")],
  "ler na íntegra"),
 ("Objetivos", "50 s", [
   "Objetivo geral: medir, com o modelo fixo, a diferença de tokens e de taxa de sucesso atribuível ao <em>harness</em> na construção do mesmo produto, com OpenCode e pi como braços, separar a parcela que vem da carga fixa e entregar um critério de escolha reproduzível.",
   "Sete específicos, uma linha cada. Um: instrumento externo que conta requisições, tokens e latência por braço. Dois: especificação do Finn em nove unidades, com testes de aceitação meus. Três: espaço de trabalho inicial idêntico, congelado por hash. Quatro: Finn nos dois <em>harnesses</em>, mesmo modelo e <em>prompts</em>, com repetição. Cinco: segundo modelo, a ordenação se mantém ou inverte. Seis: divergência entre tokens relatados e medidos. Sete: publicar tudo, a custo zero."],
  [], ["Projeto, §1 [50] e [52]–[58]."],
  [("Por que o objetivo 6?", "O <em>harness</em> relata o próprio consumo, e esse relato pode divergir do que passou pelo fio. Kapoor et al. (2025) cobram relatar custo; eu meço a divergência.")],
  "<kbd>→</kbd> revela a tabela"),
 ("Hipóteses H1 e H2", "60 s", [
   "H1: entre OpenCode e pi sobre o mesmo modelo, a diferença de tokens para construir o Finn é relevante para quem paga, comparável à de trocar de modelo. Refutada se os intervalos de tokens por construção se sobrepuserem e o teste pareado por unidade não apontar diferença.",
   "H2: a carga fixa por requisição, <em>prompt</em> de sistema e esquemas de ferramenta, explica a maior parte dessa diferença; o número de passos, a menor. Refutada se os passos explicarem a maior parte. Isso é possível: um <em>harness</em> com mais ferramentas pode concluir a unidade em menos passos.",
   "O painel da direita usa só fontes externas. Para H1, os dois braços no FrontierHarness: o OpenCode paga 1,33 vez por tarefa aprovada e aprova 10 pontos a menos. Para H2, o pi tem 4 ferramentas e <em>prompt</em> abaixo de 1.000 tokens, e a Databricks, citada pelo Earendil, mediu três vezes menos contexto por turno."],
  [("1,33×", "US$ 3,24 ÷ US$ 2,43; cálculo do autor"), ("10 pp", "60,0 % − 50,0 %; cálculo do autor"), ("< 1.000 tokens", "prompt e 4 ferramentas do pi (Earendil, 2026)"), ("3× menos contexto", "Databricks apud Earendil (2026); custo por tarefa > 2×")],
  ["Runta (2026); Earendil (2026), blogue de 4 ago. 2026; a medição da Databricks é citação de segunda mão (<em>apud</em>)."],
  [("Três vezes menos contexto não já responde H2?", "Não. Mais bytes por requisição não significam resultado pior. Se o OpenCode conclui a unidade em menos passos, a conta pode virar. É o que H2 testa."),
   ("O que é 'comparável a trocar de modelo'?", "A ordem de grandeza que separa dois níveis de modelo no mesmo gateway. O segundo nível do desenho dá essa régua.")],
  "<kbd>→</kbd> revela H1, H2 e o painel"),
 ("Seção 2 · Referencial teórico", "10 s", [
   "Seção 2. O que é um <em>harness</em>, dez trabalhos em quatro anos e as duas pendências que o projeto responde: atribuição e instrumentação."],
  [], [], [], "só passar"),
 ("O que é um harness", "60 s", [
   "No centro, o modelo: sem estado, recebe texto, devolve texto. É o mesmo nos dois braços; é a variável que eu controlo.",
   "Tudo em volta é o <em>harness</em>. Lin e colegas, 2026, chamam de conjunto de componentes externos ao modelo e editáveis: <em>prompt</em> de sistema, ferramentas, <em>middleware</em> de contexto e laço de execução. Ning e colegas, 2026: ele converte um modelo sem estado em agente funcional.",
   "Fora do anel, o <em>proxy</em>: não é parte do <em>harness</em>, é o meu instrumento. Conta requisições, tokens e latência igual para os dois braços."],
  [], ["Lin et al. (2026, §1); Ning et al. (2026, §2); Wang et al. (2026); Lee et al. (2026, §3). Todos <em>preprints</em>."],
  [("O proxy não altera o que está sendo medido?", "Ele só repassa bytes e conta. O gateway injeta conteúdo, mas é um deslocamento igual para os dois braços que não se cancela em razão; por isso conto no proxy e deixo o relatório do gateway para verificação cruzada."),
   ("Por que não escrever o próprio harness?", "A pergunta é sobre escolher entre os que existem. O projeto escreve instrumento, prompts e testes de aceitação; harness, nenhum.")],
  "<kbd>→</kbd> revela o diagrama e os pontos"),
 ("Componentes do harness", "45 s", [
   "Os quatro componentes, lado a lado nos dois braços, com número medido. <em>Prompt</em> de sistema: 2.499 bytes no pi, 9.738 no OpenCode. Ferramentas: 4 esquemas contra 9; viajam em toda requisição. <em>Middleware</em>: o pi não tem, por decisão; o OpenCode tem compactação, memória e permissões. Laço: ReAct mínimo contra planejamento e subagentes. O <em>proxy</em> é o mesmo para os dois."],
  [("2.499 vs 9.738 bytes", "prompt de sistema; Camada 1, 28 ago. 2026, pi 0.80.10 e OpenCode 1.17.9"), ("4 vs 9", "esquemas de ferramenta por requisição")],
  ["layer1/data/first_request.csv (YuukiFST, 2026c); Earendil (2026) para as decisões de projeto do pi."],
  [], "pular se faltar tempo"),
 ("Referencial 2022–2025", "45 s", [
   "Quatro trabalhos que definem o laço, a interface e a lacuna de custo. Yao et al., 2022, ReAct: o laço observar/agir mínimo; o pi fica perto dele. Yang et al., 2024, SWE-agent: a interface entre modelo e ambiente vira objeto de projeto; NeurIPS, revisado por pares. Kapoor et al., 2024: a avaliação de agentes ignora o custo. Kapoor et al., 2025, HAL: comparações entre <em>harnesses</em> são raras, e o efeito é específico do modelo. Daí o meu objetivo 5."],
  [], ["ReAct (ICLR 2023) e SWE-agent (NeurIPS 2024) têm revisão por pares; Kapoor et al. (2024, 2025) são <em>preprints</em>."],
  [], "<kbd>→</kbd> revela os cartões"),
 ("Referencial 2026", "60 s", [
   "Seis trabalhos do ano. Lin et al.: definição operacional e a métrica Succ/Mtok; Tabela 1, 47,2 % com OpenCode a 71,9 % com Codex, mesmo GPT-5.4. Zhang et al., Binding Constraint Thesis: a parcela do <em>harness</em> pode ser comparável ou maior que a do modelo. Lee et al., Meta-Harness: editar só o código do <em>harness</em>, modelo fixo, 76,4 % contra 74,7 %. Ning et al.: a definição que uso e a lacuna, §5.2.7 pede métricas por componente. Wang et al.: o que o <em>harness</em> faz. Runta: o gráfico do começo.",
   "Sobre revisão por pares: são <em>preprints</em> de 2026, e o FrontierHarness é blogue. O tema é novo; o referencial acompanha."],
  [("47,2 % → 71,9 %", "Lin et al. 2026, Tabela 1; GPT-5.4; Terminal-Bench 2; 89 tarefas; 24,7 pp, cálculo do autor"), ("76,4 % vs 74,7 %", "Lee et al. 2026, Tabela 7; Claude Opus 4.6; 89 tarefas")],
  ["Todos na tela."],
  [("Quase tudo é preprint. Isso sustenta um projeto?", "Sustenta a motivação e a definição. A lacuna que ataco, atribuição por componente, é nomeada por Ning et al. e confirmada por Kapoor et al. (2025). O método de medição não depende de nenhum resultado desses artigos."),
   ("Qual é a sua contribuição em relação a Lin et al.?", "Lin compara harnesses em tarefas isoladas. Eu comparo na construção de um produto completo, unidade a unidade, e decomponho o custo em carga fixa e conversa.")],
  "<kbd>→</kbd> revela os cartões"),
 ("Evidência 1 · Lin et al. (2026)", "45 s", [
   "Modelo congelado, <em>harness</em> humano trocado: 24,7 pontos entre OpenCode e Codex. À direita, o outro achado: quatro <em>harnesses</em> com a mesma acurácia no SWE-bench-verified, de 74,6 % a 75,6 %, gastando de 461 mil a 679 mil tokens por tarefa. Acurácia e custo são eixos separados; o <em>harness</em> evoluído gasta menos pelo mesmo resultado."],
  [("461 mil a 679 mil tokens", "por tarefa, mesma acurácia, 500 tarefas; ~47 % de variação de custo")],
  ["Lin et al. (2026), arXiv:2604.25850 v4; sem desvio-padrão; k = 2. O projeto faz n ≥ 3 e reporta dispersão."],
  [], "pular se faltar tempo"),
 ("Evidência 2 · HAL (Kapoor et al., 2025)", "40 s", [
   "Mesmo modelo, outro <em>scaffold</em>: de 30 a 48 pontos de queda no SWE-bench Verified Mini, quatro modelos, execução única. É a evidência real de que o <em>scaffold</em> move dezenas de pontos com o modelo fixo, e de que o efeito depende do modelo: Claude vai melhor com BrowserUse, OpenAI com SeeAct."],
  [("−30 a −48 pp", "Tabela A19; 50 tarefas; single run")],
  ["Kapoor et al. (2025), arXiv:2510.11977; 21.730 rollouts, ~US$ 40.000."],
  [], "pular se faltar tempo"),
 ("Evidência 3 · Alier Forment et al. (2026)", "40 s", [
   "Custo por tarefa concluída: o <em>scaffold</em> pesa mais que a interface. Uma tarefa, sete <em>scaffoldings</em>: pi a 14.660 tokens de entrada, Claude Code a 410.797, 28 vezes no braço CLI. O artigo também dá o limite de resolução: diferença menor que cerca de duas vezes não se distingue de variação entre execuções. As cinco regras dele viram protocolo meu: condicionar à conclusão, separar, verificar, checar aderência, repetir."],
  [("28×", "pi 14.660 vs Claude Code 410.797 tokens de entrada, braço CLI, mediana por run concluída")],
  ["Alier Forment et al. (2026), arXiv:2608.08654; preços OpenRouter de 3 ago. 2026."],
  [], "pular se faltar tempo"),
 ("Evidência 4 · regras de medição", "40 s", [
   "Como a prática mede. HarnessRank: mesmo benchmark, mesmo modelo, ordena por aprovação e publica custo ao lado; um timeout é resultado, não repetição. Runta: o cache muda a conta, 25,0 % ponderado contra 67,8 % na célula mediana do Claude Code. Lee et al.: decisões de <em>harness</em> são isoláveis. Regra que adoto: contar tokens no <em>proxy</em>, um tokenizador para os dois braços."],
  [("25,0 % vs 67,8 %", "cache do Claude Code, ponderado vs célula mediana; Runta (2026)")],
  ["HarnessRank (2026); Runta (2026); Lee et al. (2026); Miller (2024) para o teste pareado."],
  [], "pular se faltar tempo"),
 ("Seção 3 · Material e método", "10 s", [
   "Seção 3: classificação, uso de IA declarado, duas camadas de medição, o produto, a matriz, a estatística e as limitações."],
  [], [], [], "só passar"),
 ("Classificação da pesquisa", "40 s", [
   "Finalidade aplicada: o produto é um critério de escolha. Abordagem quali-quantitativa: meço tokens e sucesso, e atribuo a diferença à carga fixa ou aos passos. Objetivos: exploratória, porque dois <em>harnesses</em> construindo o mesmo produto completo a partir da mesma especificação não têm precedente publicado. Procedimentos: experimental; variável independente, o <em>harness</em>; controladas, modelo, especificação, espaço inicial e limites. Método dedutivo: hipóteses antes da coleta."],
  [], ["Projeto, §3 [74]. Sem manual de metodologia citado: a lista de referências fica no tema."],
  [("Por que não cita Gil ou Prodanov?", "A lista fica no tema; a classificação é a da disciplina e se sustenta sem citação.")],
  "<kbd>→</kbd> revela os eixos"),
 ("Uso de IA declarado", "60 s", [
   "A Portaria CNPq 2.664 de 2026 pede ferramenta e finalidade. Ferramenta: Claude Code. Finalidade: entender o tema, buscar artigos e registrar as decisões do Finn antes do experimento. Em dois métodos, o papel é o mesmo: eu decido e confiro, o agente escreve.",
   "Fontes: um LLM Wiki, padrão de Karpathy. Fontes brutas guardadas sem alteração, síntese por fonte, registro cronológico, fila de revisão. 29 fontes, 46 páginas; cada afirmação citada eu conferi no original; nenhuma frase do projeto foi escrita pelo agente.",
   "Especificação: o Helmsman, rotina minha. O que o sistema faz, só eu respondo, 9 tickets. Como construir, o agente decide e registra com alternativas e critério, 12 tickets; 3 deles passaram por subagentes de pesquisa. O mapa fechou e é a base da especificação congelada."],
  [("29 fontes · 46 páginas", "wiki do repositório (YuukiFST, 2026c)"), ("21 tickets", "#2–#22 sob o mapa #1; 9 de produto, 12 técnicos, 3 com pesquisa")],
  ["Brasil (2026); Karpathy (2026); YuukiFST (2026a, 2026b, 2026c)."],
  [("O que a IA escreveu?", "Nada do texto final. Leu fontes e montou resumos na wiki, e tomou decisões técnicas do Finn que eu revisei."),
   ("Isso não contamina o experimento?", "A especificação é a mesma para os dois braços e foi fechada antes de qualquer execução. O custo de escrevê-la fica fora da medida.")],
  "<kbd>→</kbd> revela os dois cartões"),
 ("Como o projeto funciona", "45 s", [
   "Quatro passos, nesta ordem. Uma especificação: o Finn em nove unidades, testes de aceitação meus, congelada por SHA-256. Dois <em>harnesses</em>: OpenCode e pi recebem os mesmos bytes, o mesmo espaço vazio e o mesmo modelo, e constroem do zero, unidade a unidade. Um contador externo: o <em>proxy</em>, n ≥ 3 construções por célula. Um critério: tokens por construção ao lado da fração de testes aprovados, Succ/Mtok, teste pareado por unidade."],
  [], ["Projeto, §3 [76]–[83]. «O projeto escreve apenas o instrumento, os prompts e os testes de aceitação» [77]."],
  [], "<kbd>→</kbd> revela os passos"),
 ("Duas camadas de medição", "45 s", [
   "Camada 1: o <em>harness</em> fala com um endpoint simulado que devolve resposta fixa. Vejo esquemas, bytes de <em>prompt</em>, tokens por passo. Determinística, sem cota; dá a carga fixa de H2. Camada 2: a construção contra o modelo real, via <em>proxy</em> reverso. Estocástica, consome cota, n ≥ 3 por célula.",
   "O <em>proxy</em> conta sobre os bytes transmitidos com um tokenizador só; o relatório do gateway fica para verificação cruzada. Limite único: relógio de parede por unidade, três vezes a maior mediana das unidades-piloto. Sem teto de passos, porque teto de passos é decisão de <em>harness</em>."],
  [], ["Projeto, §3 [76], [80], [81]."],
  [("Por que 3× a mediana?", "Larga o suficiente para não punir lentidão normal; estreita o suficiente para cortar laços presos. Calibrada nas unidades-piloto.")],
  "<kbd>→</kbd> revela as camadas"),
 ("Camada 1: carga fixa medida", "40 s", [
   "Medição própria, de 28 de agosto: primeira requisição de cada braço contra o endpoint simulado. pi, 5.676 bytes e 1.228 tokens; OpenCode, 29.997 bytes e 6.659 tokens. 5,3 vezes mais bytes. O que isso não diz: que o OpenCode é pior. A Camada 2 mede se ele compensa a carga concluindo em menos passos."],
  [("5.676 vs 29.997 bytes", "requisição inteira, 5,3×; first_request.csv"), ("1.228 vs 6.659 tokens", "tokens de prompt, 5,4×, um tokenizador")],
  ["layer1/data/first_request.csv (YuukiFST, 2026c). Precedente: Databricks apud Earendil (2026), 3× menos contexto por turno."],
  [], "pular se faltar tempo; o número está no repositório"),
 ("Finn: o produto", "45 s", [
   "Antes de usar o Finn como suíte, o que ele é: financeiro por voz para pequenas empresas. O dono fala pelo WhatsApp ou pelo app e recebe lançamento, relatório e aviso. Multiempresa num banco só. Pipeline de seis passos na tela: áudio, texto por Whisper local, intenção, gate de papel, executar ou negar, resposta.",
   "Tudo decidido antes do experimento: 21 <em>issues</em> fechadas, pilha fixa. Os agentes não escolhem nada disso. É um produto de verdade, com pilha fixa; as comparações publicadas usam tarefas soltas."],
  [("21 issues", "#2–#10 produto; #11–#22 técnicas; mapa #1")],
  ["Finn (YuukiFST, 2026b), github.com/YuukiFST/Finn."],
  [("Por que o seu próprio produto?", "As decisões já estão tomadas e registradas, então a especificação sai das issues. E conheço a pilha o bastante para escrever os testes de aceitação.")],
  "<kbd>→</kbd> revela o pipeline e os cartões"),
 ("A especificação em 9 unidades", "40 s", [
   "As nove <em>issues</em> técnicas viram as nove unidades, em ordem de dependência: tenant, governança, flags, pipeline de voz, confirmação, log, relatório, agendador, cobrança. Entrada idêntica, espaço inicial só com especificação e pilha, congelado por hash. Escore: fração dos meus testes de aceitação, que o agente não vê, rodados sobre uma cópia do espaço ao fim de cada unidade. O que o agente construiu numa unidade é o ponto de partida da seguinte."],
  [("9 unidades", "U1 #15 · U2 #16 · U3 #17 · U4 #14 · U5 #20 · U6 #21 · U7 #19 · U8 #18 · U9 #22")],
  ["Projeto, §3 [78]."],
  [("Como garante que o agente não viu os testes?", "Ficam fora do espaço de trabalho. O agente recebe a especificação e o prompt da unidade; os testes rodam depois, sobre uma cópia.")],
  "<kbd>→</kbd> revela as unidades"),
 ("Braços e matriz experimental", "50 s", [
   "Braços: OpenCode e pi, código aberto, sem interface, URL base compatível com OpenAI. Matriz: braço vezes nível de modelo, nove unidades dentro de cada construção, n ≥ 3 construções válidas por célula. Dois níveis gratuitos no mesmo gateway; o segundo existe porque o efeito é específico do modelo.",
   "Duas classes por unidade. Não concluída: é resultado, entra com a fração aprovada e a construção segue, estouro de relógio incluído. Descartada: medição inconfiável, registrada, sem reparo nem repetição. A classe vem do registro do <em>proxy</em>."],
  [("2 × 2", "braços × níveis = 4 células; 9 unidades por construção"), ("n ≥ 3", "construções válidas por célula, após descartes")],
  ["Opencode (2026a, 2026b); Earendil (2026); projeto, §3 [77], [79], [82], [84]."],
  [("A especificação é sua. Isso não enviesa?", "Enviesa igual para os dois braços: mesma entrada, mesmo início vazio, comparação pareada por unidade. O viés que sobra é sobre o valor absoluto, que já declaro não ter placar."),
   ("E se os dois braços falharem numa unidade?", "Entra como não concluída nos dois, com a fração aprovada, e as construções seguem. O par continua válido para o Wilcoxon.")],
  "<kbd>→</kbd> preenche a matriz"),
 ("Succ/Mtok e teste pareado", "45 s", [
   "Duas medidas. Tokens por construção, sempre ao lado da fração de testes aprovados: um braço que falha barato não pode parecer o mais barato. E Succ/Mtok, de Lin e colegas: sucessos por milhão de tokens.",
   "Estatística: Wilcoxon dos postos sinalizados, bilateral, α de 0,05, pareado por unidade. Não paramétrico porque nove pares não sustentam suposição de distribuição; pareado porque a dificuldade da unidade é o maior fator de perturbação. Com n = 3 e nove unidades, a diferença mínima detectável é cerca de 0,76 desvio-padrão."],
  [("Succ/Mtok", "pass@1 × 10⁶ ÷ tokens por execução (Lin et al. 2026, Eq. 2)"), ("MDE ≈ 0,76σ", "n = 3, 9 unidades, bilateral, α = 0,05"), ("W crítico = 5", "k = 9 pares")],
  ["Lin et al. (2026, Eq. 2); Miller (2024)."],
  [("Nove pares é pouco.", "Nove pares são as nove unidades. O MDE está declarado; se a diferença real for menor que 0,76σ, o resultado é 'não detectado', e isso também responde H1."),
   ("Por que não teste t?", "Nove observações, distribuição desconhecida, outliers de laço preso. Wilcoxon usa postos e resiste a isso.")],
  "<kbd>→</kbd> revela métrica, teste e poder"),
 ("Limitações", "45 s", [
   "Quatro, declaradas de partida. Efeito específico do modelo: pode inverter de sinal; conclusões por nível, objetivo 5. Um produto, uma pilha: vale para essa família; outras pilhas são trabalho futuro. Especificação minha e trajetória própria: cada braço carrega os próprios erros; mitigação pela mesma entrada e comparação pareada. Sem placar público: válido só braço contra braço.",
   "A ameaça principal é a variância no nível gratuito. Resposta: n ≥ 3, mediana com dispersão, reduzir cobertura antes de reduzir repetições."],
  [], ["Projeto, §3 [86]; Kapoor et al. (2025) para a inversão BrowserUse × SeeAct."],
  [("O que acontece se a cota acabar?", "Lotes de um por dia. Repetições primeiro: n = 3 no nível primário. Se não couber, trunco o nível de robustez após a unidade 6; se ainda não couber, tiro esse nível e reporto como não executado. Nunca abaixo de n = 3.")],
  "<kbd>→</kbd> revela cada limitação"),
 ("Seções 4, 5 e 6", "10 s", [
   "Orçamento, cronograma e referências, na ordem do documento."],
  [], [], [], "só passar"),
 ("Orçamento", "30 s", [
   "R$ 0,00 em dinheiro. Inferência nos dois níveis gratuitos do OpenCode Zen. <em>Harnesses</em> e ferramentas de código aberto. Máquinas que já tenho. O limite real não é dinheiro, é cota: um lote da matriz por dia, ao longo de dias."],
  [("R$ 0,00", "Tabela 1 do projeto; inferência, harnesses, máquinas")],
  ["Projeto, §4 [88]–[100]; Opencode (2026b)."],
  [("E se o gateway mudar o nível gratuito?", "O proxy fala com qualquer URL base compatível com OpenAI. A troca seria registrada e as execuções anteriores não se misturariam com as novas.")],
  "<kbd>→</kbd> revela os cartões"),
 ("Cronograma", "30 s", [
   "Agosto e setembro: leitura, tema, toda a escrita, concluída. Outubro e novembro: instrumento, especificação e testes de aceitação. Dezembro e janeiro: a matriz. Janeiro: análise. A folga está onde a cota manda, na matriz e na escrita da especificação e dos testes."],
  [], ["Projeto, §5, Tabela 2 [102]–[180]."],
  [], "<kbd>→</kbd> revela as fases"),
 ("Referências", "15 s", [
   "As 21 entradas da seção 6: 18 sobre o <em>harness</em>, 3 sobre o método de trabalho declarado, que a exceção do documento autoriza. Os <em>preprints</em> estão marcados."],
  [], ["Projeto, §6 [183]–[203]."],
  [("Cadê as normas ABNT e os manuais de metodologia?", "Saíram da lista em 14 de setembro: a lista só tem fontes sobre o harness. A formatação segue a ABNT mesmo assim.")],
  "pular se faltar tempo"),
 ("Fecho", "20 s", [
   "A tela pergunta: quanto pesa, para o desenvolvedor que já escolheu o modelo, conhecer o <em>harness</em> antes de pagar por ele? O projeto responde em tokens e em taxa de sucesso, com o modelo fixo. O produto é um critério de escolha que um desenvolvedor ou uma empresa pode aplicar. Tudo público nos dois repositórios. Obrigado. Perguntas?"],
  [], ["github.com/YuukiFST/harness-bench (2026c) · github.com/YuukiFST/Finn (2026b)."], [], ""),
]

GLOSS = [
 ("<em>harness</em>", "Componentes externos ao modelo e editáveis: <em>prompt</em> de sistema, ferramentas, <em>middleware</em> de contexto, laço de execução (Lin et al., 2026, §1). Converte um modelo sem estado em agente funcional (Ning et al., 2026, §2). Sinônimo aproximado: <em>scaffold</em>."),
 ("modelo de linguagem", "O núcleo sem estado. Fixo em todos os braços; é a variável controlada."),
 ("braço", "Um <em>harness</em> sob teste. Dois: OpenCode e pi."),
 ("carga fixa", "Bytes que o <em>harness</em> envia em toda requisição, independentemente da tarefa: <em>prompt</em> de sistema e esquemas de ferramentas. Medida na Camada 1."),
 ("unidade", "Uma parte da especificação do Finn, com testes de aceitação próprios. Nove, em ordem de dependência; cada uma veio de uma <em>issue</em> técnica."),
 ("especificação", "Documento único, escrito por mim a partir das <em>issues</em> do Finn antes de qualquer execução e congelado por SHA-256."),
 ("espaço de trabalho inicial", "O diretório de onde uma construção parte: só a especificação e a pilha. Daí em diante é do braço; eu não escrevo código."),
 ("construção", "Uma execução de um braço, num nível, que constrói o produto inteiro, uma invocação do <em>harness</em> por unidade."),
 ("teste de aceitação", "Teste meu, que o agente não vê. Escore = fração aprovada; unidade concluída quando todos passam."),
 ("célula", "Um par (braço, nível de modelo). Cada célula recebe n ≥ 3 construções válidas."),
 ("unidade não concluída", "O agente não a concluiu. É resultado: entra com a fração aprovada e a construção segue. Estouro do relógio incluído."),
 ("construção descartada", "Medição inconfiável em alguma unidade. Registrada, sem reparo nem repetição. Classe lida do registro do <em>proxy</em>."),
 ("<em>proxy</em> reverso", "O instrumento. Entre <em>harness</em> e gateway; conta requisições, tokens e latência sobre os bytes transmitidos, um só tokenizador."),
 ("gateway", "OpenCode Zen, o serviço que entrega o modelo. Dois níveis gratuitos. O relatório dele serve para verificação cruzada."),
 ("Succ/Mtok", "pass@1 × 10⁶ ÷ média de tokens por execução (Lin et al., 2026, Eq. 2). Sucessos por milhão de tokens."),
 ("Wilcoxon dos postos sinalizados", "Teste não paramétrico para pares. Pareado por unidade. Bilateral, α = 0,05."),
 ("MDE", "Diferença mínima detectável. Com n = 3 por célula e 9 unidades, ≈ 0,76σ."),
 ("<em>preprint</em>", "Artigo sem revisão por pares. A maior parte do referencial de 2026 está nessa condição; dizer antes que perguntem."),
]

QA = [
 ("Por que OpenCode e pi, e não Claude Code ou Cursor?", "Os dois são código aberto, rodam sem interface e aceitam URL base compatível com OpenAI, então passam pelo mesmo proxy e pelo mesmo modelo. Ferramentas fechadas não deixam fixar o modelo nem interceptar a requisição. E os dois estão em pontos distantes da camada."),
 ("O resultado vale para outros modelos?", "Não necessariamente. Kapoor et al. (2025) mostram inversão de sinal entre modelos. Por isso o objetivo 5 roda um segundo nível e as conclusões são por nível."),
 ("Qual é a variável independente?", "O <em>harness</em>. Controladas: modelo, especificação, espaço de trabalho inicial, limites. Dependentes: tokens por construção, fração de testes aprovada, Succ/Mtok."),
 ("Isso é pesquisa ou benchmark?", "Pesquisa experimental com hipóteses refutáveis declaradas antes da coleta. O benchmark é o instrumento; a contribuição é a decomposição do custo em carga fixa e conversa, que Ning et al. (2026, §5.2.7) pedem."),
 ("Por que o proxy e não o relatório do próprio harness?", "O objetivo 6 mede a divergência entre os dois. O relatório do harness é auto-relato; o proxy é medição sobre os bytes que passaram."),
 ("Qual o tamanho do efeito esperado?", "Não declaro um número. H1 diz 'comparável a trocar de modelo' e o segundo nível dá a régua. O MDE de 0,76σ diz o que o desenho consegue ver."),
 ("Se H2 for refutada, o projeto falhou?", "Não. Se os passos explicarem mais que a carga fixa, o resultado diz que a diferença está no laço de execução, e H2 sai refutada como previsto."),
 ("O que mudou no tema em relação à versão anterior?", "O foco. Antes o título falava na decisão do desenvolvedor; agora fala no efeito do harness sobre o custo e o desempenho do modelo, que é o que se mede. A justificativa nomeia o movimento das ferramentas para agentes; o método não mudou."),
]

NUMS = [
 ("5,6×", "Claude Code vs DSH Creator, mesma aprovação de 63,3 %", "12 configurações, 9 harnesses, Kimi K3, 30 tarefas, 1 tentativa, set. 2026", "Runta (2026); razão declarada no post"),
 ("50,0–66,7 %", "faixa de aprovação", "idem", "Runta (2026)"),
 ("US$ 1,05–18,34", "custo por tarefa concluída", "idem", "Runta (2026)"),
 ("US$ 2,43 / 60,0 %", "pi", "idem", "Runta (2026)"),
 ("US$ 3,24 / 50,0 %", "OpenCode", "idem", "Runta (2026)"),
 ("1,33× / 10 pp", "OpenCode paga mais e aprova menos que o pi", "idem; cálculo do autor", "Runta (2026)"),
 ("2.499 / 9.738 bytes", "prompt de sistema, pi / OpenCode (3,9×)", "Camada 1, endpoint simulado, 28 ago. 2026, pi 0.80.10, OpenCode 1.17.9", "layer1/data"),
 ("4 / 9", "esquemas de ferramentas por requisição", "idem", "layer1/data"),
 ("5.676 / 29.997 bytes", "primeira requisição completa (5,3×)", "idem", "first_request.csv"),
 ("1.228 / 6.659 tokens", "primeira requisição (5,4×)", "idem, tokenizador cl100k_base", "first_request.csv"),
 ("47,2 % → 71,9 %", "aprovação OpenCode → Codex (24,7 pp)", "GPT-5.4, Terminal-Bench 2, 89 tarefas", "Lin et al. (2026), Tabela 1"),
 ("461–679 mil tokens", "mesma acurácia, custo diferente", "SWE-bench-verified, 500 tarefas", "Lin et al. (2026)"),
 ("−30 a −48 pp", "SWE-Agent vs HAL Generalist", "SWE-bench Verified Mini, 50 tarefas, single run", "Kapoor et al. (2025), Tabela A19"),
 ("28×", "pi vs Claude Code, tokens de entrada", "braço CLI, mediana por run concluída", "Alier Forment et al. (2026)"),
 ("76,4 % vs 74,7 %", "Meta-Harness vs Terminus-KIRA", "TerminalBench-2, 89 tarefas, Claude Opus 4.6", "Lee et al. (2026), Tabela 7"),
 ("25,0 % vs 67,8 %", "cache do Claude Code, ponderado vs célula mediana", "FrontierHarness", "Runta (2026)"),
 ("< 1.000 tokens", "prompt e 4 ferramentas do pi", "blogue, 4 ago. 2026", "Earendil (2026)"),
 ("3× / > 2×", "menos contexto por turno / custo por tarefa", "medição da Databricks, segunda mão", "Databricks apud Earendil (2026)"),
 ("9", "unidades da especificação", "issues #14–#22 de 21 tickets", "YuukiFST (2026b)"),
 ("n ≥ 3", "construções válidas por célula", "2 braços × 2 níveis = 4 células", "projeto, §3"),
 ("3×", "limite de relógio por unidade", "maior mediana nas unidades-piloto", "projeto, §3"),
 ("≈ 0,76σ", "diferença mínima detectável", "n = 3, 9 unidades, Wilcoxon bilateral, α = 0,05", "projeto, §3"),
 ("R$ 0,00", "orçamento total", "inferência, harnesses, máquinas", "projeto, Tabela 1"),
]


def slide_card(i: int, s: tuple) -> str:
    title, t, fale, nums, fontes, qa, no_slide = s
    parts = [f'<div class="card slide"><span class="n">{i}</span><h3>{title}</h3><p class="meta"><b>{t}</b>'
             + (f" · {no_slide}" if no_slide else "") + "</p>"]
    parts.append('<div class="blk"><b>Fale</b><div class="say">' + "".join(f"<p>{p}</p>" for p in fale) + "</div></div>")
    if nums:
        parts.append('<div class="blk"><b>Números</b><div class="num">' + "".join(f"<div><b>{v}</b><small>{d}</small></div>" for v, d in nums) + "</div></div>")
    if fontes:
        parts.append('<div class="blk"><b>Fontes</b><ul class="src">' + "".join(f"<li>{f}</li>" for f in fontes) + "</ul></div>")
    if qa:
        parts.append('<div class="blk"><b>Se perguntarem</b><ul class="q">' + "".join(f"<li><b>{q}</b>{a}</li>" for q, a in qa) + "</ul></div>")
    parts.append("</div>")
    return "".join(parts)


def main() -> None:
    # Superseded: rerunning would overwrite dist/roteiro-apresentacao.html with a stale schedule
    # and stale [n] indices (review of PR #82).
    raise SystemExit("superseded by tools/roteiro_2026-09-24.py; run that instead")
    total = sum(int(s[1].split()[0]) for s in SLIDES)
    # The cut list is derived from the "pular se faltar tempo" markers so the
    # two never disagree; the marked slides alone do not reach a 12-minute slot.
    skip = [i for i, s in enumerate(SLIDES, 1) if len(s) > 6 and "pular" in s[6]]
    t_skip = total - sum(int(SLIDES[i - 1][1].split()[0]) for i in skip)
    body = f"""
<h1>Roteiro de estudo da apresentação</h1>
<p class="sub">Projeto de pesquisa "{TITLE}" · Metodologia Científica · IFMT · setembro de 2026.<br>
Companheiro de <code>dist/apresentacao-explainer/index.html</code> (33 slides, ordem do documento). Leia em voz alta, cronometre, corte o que passar do tempo.</p>

<nav class="nav">
  <a href="#uso">Como usar</a><a href="#pitch">Versões curtas</a><a href="#gloss">Glossário</a><a href="#slides">Slide a slide</a><a href="#perguntas">Banco de perguntas</a><a href="#numeros">Tabela de números</a><a href="#check">Checklist</a>
</nav>

<h2 id="uso">Como usar este roteiro</h2>
<div class="card">
<ul>
  <li><b>Tempo.</b> Falando tudo, cerca de {total // 60} min {total % 60:02d} s. Pulando os {len(skip)} slides marcados "pular se faltar tempo" ({", ".join(map(str, skip))}), {t_skip // 60} min {t_skip % 60:02d} s.</li>
  <li><b>Blocos por slide:</b> <i>Fale</i> é o texto para dizer, em primeira pessoa, na ordem em que o slide revela. <i>Números</i> traz cada valor com o seu denominador. <i>Fontes</i> diz de onde veio cada afirmação. <i>Se perguntarem</i> antecipa a pergunta mais provável.</li>
  <li><b>Regra dos números:</b> nunca diga um número sem o denominador. "5,6×" sozinho é fraco; "5,6× entre dois harnesses com a mesma aprovação, sobre o mesmo modelo, Kimi K3, 30 tarefas" fecha a pergunta óbvia.</li>
  <li><b>Ordem do documento.</b> O deck segue o projeto: capa, seção 1 (justificativa, tema, problema, objetivos, hipóteses), seção 2, seção 3, seções 4 a 6. Os índices <code>[n]</code> nas notas do deck (tecla <kbd>N</kbd>) e neste roteiro são os parágrafos do <code>.docx</code> no dump de 18 set. 2026.</li>
  <li><b>Decore quatro pares autor-ano:</b> Runta (2026), Lin et al. (2026), Ning et al. (2026), Kapoor et al. (2025).</li>
</ul>
</div>

<h2 id="pitch">Versões curtas do projeto</h2>
<div class="card hi">
<h3>Uma frase</h3>
<p class="say">Eu meço como o <em>harness</em> altera o custo em tokens e a taxa de sucesso de um modelo de linguagem fixo, construindo o mesmo SaaS duas vezes, e quanto dessa diferença é carga fixa por requisição.</p>
<h3>Trinta segundos</h3>
<div class="say">
<p>Na era dos agentes o modelo não avança sozinho: o <em>harness</em> em volta dele, e as ferramentas feitas para agentes, avançam junto. Com o mesmo modelo, o custo por tarefa vai de US$ 1,05 a US$ 18,34 só pelo <em>harness</em>, mas as comparações usam tarefas isoladas. Meu projeto constrói o mesmo produto, o Finn, duas vezes, com OpenCode e com pi, a partir da mesma especificação, unidade a unidade, sobre o mesmo modelo, e conta os tokens fora do <em>harness</em>, num <em>proxy</em>. Saída: um critério de escolha para o desenvolvedor e a empresa.</p>
</div>
<h3>Dois minutos</h3>
<div class="say">
<p><b>Problema.</b> Com o modelo já escolhido, quanto mudam o custo em tokens e a taxa de sucesso ao construir o mesmo software com um <em>harness</em> em vez de outro, e quanto dessa diferença vem da carga fixa que cada <em>harness</em> envia em toda requisição?</p>
<p><b>Por que importa.</b> Os modelos avançam, e com eles os <em>harnesses</em> e as ferramentas para agentes; escolher o modelo deixou de bastar. No FrontierHarness (Runta, 2026), doze configurações sobre o mesmo modelo ficam entre 50,0 % e 66,7 % de aprovação e o custo por tarefa vai de US$ 1,05 a US$ 18,34. Os meus braços estão nesse levantamento: pi a US$ 2,43 e OpenCode a US$ 3,24.</p>
<p><b>Método.</b> Duas camadas. Camada 1: a forma da requisição contra um endpoint simulado; dá a carga fixa. Camada 2: a construção do Finn contra o modelo real, via <em>proxy</em> reverso, n ≥ 3 construções por célula. Especificação em nove unidades, congelada por SHA-256, testes de aceitação meus. Métrica: tokens por construção ao lado da fração de testes aprovados, e Succ/Mtok. Estatística: Wilcoxon pareado por unidade.</p>
<p><b>Hipóteses.</b> H1: a diferença de tokens é relevante para quem paga, comparável a trocar de modelo. H2: a carga fixa explica a maior parte. As duas têm condição de refutação declarada.</p>
<p><b>Limites.</b> Efeito específico do modelo, um produto numa pilha só, especificação minha, sem placar público. Orçamento R$ 0,00; a cota gratuita é o limite.</p>
</div>
</div>

<h2 id="gloss">Glossário para não travar</h2>
<div class="card"><dl>{"".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in GLOSS)}</dl></div>

<h2 id="slides">Slide a slide</h2>
{"".join(slide_card(i + 1, s) for i, s in enumerate(SLIDES))}

<h2 id="perguntas">Banco de perguntas gerais</h2>
<div class="card"><ul class="q">{"".join(f"<li><b>{q}</b>{a}</li>" for q, a in QA)}</ul></div>

<h2 id="numeros">Tabela de números com denominador</h2>
<div class="card"><table><thead><tr><th>Valor</th><th>O que é</th><th>Denominador</th><th>Fonte</th></tr></thead><tbody>
{"".join(f"<tr><td class='r'><b>{v}</b></td><td>{w}</td><td>{d}</td><td>{f}</td></tr>" for v, w, d, f in NUMS)}
</tbody></table></div>

<h2 id="check">Checklist do dia</h2>
<div class="card"><ul class="check">
<li>Abrir <code>dist/apresentacao-explainer/index.html</code> no Chrome; testar <kbd>→</kbd>, <kbd>F</kbd>, <kbd>O</kbd> (sumário) e <kbd>?</kbd> (ajuda).</li>
<li>Confirmar que <kbd>N</kbd> (notas) está desligado; <kbd>T</kbd> alterna o tema, deixar no escuro.</li>
<li>Ensaiar os slides 5, 8 e 13 com o cronômetro: são os que mais têm nomes e números.</li>
<li>Ter na ponta da língua: US$ 1,05 a 18,34; 5,6×; 2.499 vs 9.738; 4 vs 9; n ≥ 3; 0,76σ; R$ 0,00.</li>
<li>Decidir o corte antes de começar: 12 min ou 10 min, conforme a lista acima.</li>
</ul></div>
"""
    doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Roteiro de estudo — apresentação do projeto "{H.unescape(re.sub('<[^>]+>', '', TITLE))}"</title>
{STYLE}
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"roteiro written: {len(SLIDES)} slides, {total} s")


if __name__ == "__main__":
    main()
