"""Rebuild dist/roteiro-apresentacao.html for the 27-slide explainer deck
(dist/apresentacao-explainer/index.html) after the 2026-09-23 docx rewrite (issue #80).
Derived from tools/roteiro_2026-09-18.py; keeps its stylesheet and layout, and regenerates
every section so that no word, number or reference diverges from dist/projeto-de-pesquisa.docx.
Every number cites its paragraph [n] in `python tools/docx_prose.py dump dist/projeto-de-pesquisa.docx`.

Run: python tools/roteiro_2026-09-23.py
"""
import html as H
import re
from pathlib import Path

OUT = Path("dist/roteiro-apresentacao.html")
STYLE = re.search(r"<style>.*?</style>", OUT.read_text(encoding="utf-8"), re.S).group(0)

TITLE = "O <em>harness</em> no custo e no desempenho de agentes de codificação: tokens e taxa de sucesso com o modelo fixo"

# (title, time, fale[], numeros[(valor, denominador)], fontes[], perguntas[(q, a)], no_slide)
SLIDES = [
 ("Capa", "20 s", [
   "Bom dia. Meu nome é Fausto Yuuki, curso Sistemas para Internet, orientadora professora Inara Silva. O projeto se chama <em>O harness no custo e no desempenho de agentes de codificação</em>: tokens e taxa de sucesso com o modelo fixo.",
   "Em uma frase: com o mesmo modelo, eu meço quanto o <em>harness</em> muda o custo e quanto muda o sucesso."],
  [], ["Projeto, capa e folha de rosto [21]–[24]."], [], "<kbd>→</kbd> avança. <kbd>F</kbd> tela cheia antes de começar. <kbd>N</kbd> (notas) desligado."),
 ("Seção 1 · Introdução", "10 s", [
   "Seção 1. O mesmo modelo custa diferente conforme o <em>harness</em>. Vou mostrar a justificativa, o problema, os objetivos e as hipóteses."],
  [], [], [], "só passar"),
 ("Justificativa: o imposto do harness", "60 s", [
   "Um agente de codificação tem duas partes: o modelo de linguagem e o <em>harness</em>, o software em volta dele que monta o contexto, expõe as ferramentas e conduz a execução. Claude Code, Codex, OpenCode e pi são <em>harnesses</em>.",
   "Pan e colegas, da Universidade da Califórnia em Berkeley, avaliaram sete modelos em três <em>harnesses</em>. A escolha do <em>harness</em> quase não mudou a taxa de sucesso, mas mudou o custo. No SWE-bench Lite, o Claude Fable 5 resolve 97,8 % das tentativas no Claude Code e 96,7 % no pi. O Claude Code custa cerca do dobro por tentativa: US$ 1,33 contra US$ 0,67.",
   "Quem paga por tokens paga também essa diferença. Os autores chamam isso de imposto do <em>harness</em>."],
  [("97,8 % vs 96,7 %", "sucesso do Claude Fable 5 no Claude Code e no pi, SWE-bench Lite [43]"), ("US$ 1,33 vs US$ 0,67", "custo por tentativa, mesma comparação [43]"), ("7 modelos · 3 harnesses", "desenho do HarnessTax [43]")],
  ["Pan et al. (2026), HarnessTax, publicação de blogue de pesquisa, não revisada por pares. Diga isso antes que perguntem."],
  [("Isso é fonte confiável?", "É blogue de pesquisa, sem revisão por pares, e eu digo isso na tela. Uso como motivação. O meu desenho mede com instrumento próprio, fora do <em>harness</em>."),
   ("Por que o Claude Code, se ele não é braço do projeto?", "É o par que o próprio HarnessTax destaca. Os meus braços são o OpenCode e o pi, que rodam sem interface e aceitam o <em>proxy</em> [76].")],
  "<kbd>→</kbd> revela o gráfico e os cartões"),
 ("Justificativa e tema", "45 s", [
   "Essas medições usam tarefas isoladas de <em>benchmarks</em> que os modelos podem ter visto no treino. Os próprios autores dizem que o próximo passo é medir o <em>harness</em> em fluxos reais de desenvolvimento, com tarefas de várias sessões.",
   "Tema, e vou ler: o efeito do <em>harness</em> sobre o custo e o desempenho de um modelo de linguagem fixo na construção de um produto de software completo.",
   "O que eu faço: construo o mesmo produto, o Finn, com o OpenCode e com o pi, sobre o mesmo modelo e a mesma especificação, e conto os tokens fora do <em>harness</em>."],
  [], ["Projeto, §1, justificativa [44] e tema [46]."],
  [("Por que não deixar o OpenCode construir e gerar a especificação para o pi?", "Entrada desigual. A especificação é única, escrita antes, e a mesma para os dois braços [77].")],
  "<kbd>→</kbd> revela os três cartões"),
 ("Problema de pesquisa", "30 s", [
   "O problema, na íntegra: com o modelo fixo, quanto mudam o custo em tokens e a taxa de sucesso ao construir o mesmo software com um <em>harness</em> em vez de outro, e quanto da diferença de custo vem da carga fixa que cada <em>harness</em> envia em toda requisição?",
   "A primeira metade vira H1; a segunda, H2."],
  [], ["Projeto, §1 [48]."],
  [("Por que tokens e não dólares?", "O token é a unidade que o <em>harness</em> controla e que o <em>proxy</em> conta igual para os dois braços [80]. O orçamento é R$ 0,00 no nível gratuito [91]–[92].")],
  "ler na íntegra"),
 ("Objetivos", "45 s", [
   "Objetivo geral: medir, com o modelo fixo, a diferença de tokens e de taxa de sucesso atribuível ao <em>harness</em> na construção do mesmo produto a partir da mesma especificação, com o OpenCode e o pi como braços, e separar a parcela que vem da carga fixa por requisição.",
   "Seis específicos. Um: construir o <em>proxy</em> que conta requisições, tokens e latência por braço. Dois: escrever a especificação do Finn em nove unidades, com testes de aceitação. Três: construir o Finn nos dois <em>harnesses</em>, com o mesmo modelo, <em>prompt</em> e espaço inicial. Quatro: repetir em um segundo modelo e ver se a ordenação dos braços se mantém. Cinco: comparar os tokens relatados por cada <em>harness</em> com os medidos no <em>proxy</em>. Seis: publicar executor, <em>prompts</em>, testes, dados e scripts de análise."],
  [], ["Projeto, §1 [50] e [52]–[57]."],
  [("Por que o objetivo 5?", "Cada <em>harness</em> conta turnos e tokens do seu jeito, e Pan et al. registram que a definição de turno varia entre eles [70]. O <em>proxy</em> mede igual para os dois; o objetivo 5 compara as duas contagens.")],
  "<kbd>→</kbd> revela a tabela"),
 ("Hipóteses H1 e H2", "50 s", [
   "H1: com o modelo fixo, o <em>harness</em> muda mais o custo do que o sucesso. Os tokens por unidade diferem entre o OpenCode e o pi, e a fração de testes aprovados fica igual. H1 é refutada se o teste pareado não apontar diferença de tokens ou se apontar diferença de sucesso.",
   "H2: a carga fixa por requisição, <em>prompt</em> de sistema e esquemas de ferramenta, explica a maior parte da diferença de tokens; o número de passos, a menor. H2 é refutada se os passos ou o conteúdo da conversa explicarem a maior parte."],
  [], ["Projeto, §1 [61]–[62]; predições registradas antes da coleta [83]."],
  [("H1 não é só repetir o HarnessTax?", "O HarnessTax usa tarefas isoladas. Eu testo a mesma pergunta na construção de um produto inteiro, com outros dois braços, e pareio por unidade."),
   ("Se H2 for refutada, o projeto falhou?", "Não. Se os passos ou a conversa explicarem mais, o resultado diz onde está a diferença, e H2 sai refutada pelo critério declarado.")],
  "<kbd>→</kbd> revela H1 e H2"),
 ("Seção 2 · Referencial teórico", "10 s", [
   "Seção 2. O que é um <em>harness</em>, o que as fontes dizem sobre sucesso e custo, e as duas pendências: de onde vem o custo e como medi-lo."],
  [], [], [], "só passar"),
 ("O que é um harness", "50 s", [
   "Ning e colegas: um <em>harness</em> converte um modelo de linguagem sem estado em um agente funcional, ao ancorar as saídas em execução externa, estado persistente e realimentação verificável.",
   "Lin e colegas dizem o que ele contém: o <em>prompt</em> de sistema que molda o estilo de trabalho, as ferramentas que expõem o sistema de arquivos e o shell, e o <em>middleware</em> que controla contexto, execução e recuperação. Componentes externos ao modelo e editáveis.",
   "Só esse conjunto varia entre os meus braços. O pi envia quatro ferramentas e um <em>prompt</em> de sistema curto. O OpenCode envia mais ferramentas, um <em>prompt</em> maior, subagentes e permissões."],
  [], ["Ning et al. (2026, §2); Lin et al. (2026, §1). <em>Preprints</em>. Projeto, §2 [65]–[67]."],
  [("O proxy não altera o que está sendo medido?", "Ele fica fora do <em>harness</em> e conta igual para os dois braços [59]. As contagens do <em>harness</em> e do <em>gateway</em> servem só para verificação cruzada [80]."),
   ("Por que não escrever o próprio harness?", "A pergunta é sobre os <em>harnesses</em> que existem. O projeto escreve o <em>proxy</em>, os <em>prompts</em> e os testes.")],
  "<kbd>→</kbd> revela o diagrama e os pontos"),
 ("Sucesso: as fontes divergem", "50 s", [
   "Sobre o sucesso, as fontes não concordam. Na Tabela 1 de Lin e colegas, <em>harnesses</em> escritos por humanos sobre o GPT-5.4 vão de 47,2 % no OpenCode a 71,9 % no Codex, no Terminal-Bench 2. Zhang e colegas dizem que, entre modelos de fronteira comparáveis, a parcela do <em>harness</em> é comparável ou maior que a do modelo.",
   "Pan e colegas mediram outra coisa no SWE-bench Lite: o efeito médio do <em>harness</em> sobre o sucesso ficou dentro de ±2 %, e o Claude Code custou cerca de 2,0 vezes o pi. Por isso eu meço sucesso e custo juntos."],
  [("47,2 % → 71,9 %", "OpenCode → Codex, GPT-5.4, Terminal-Bench 2; Lin et al. (2026), Tabela 1 [68]"), ("±2 %", "efeito médio do harness no sucesso, SWE-bench Lite; Pan et al. (2026) [68]"), ("≈ 2,0×", "custo do Claude Code sobre o pi [68]")],
  ["Lin et al. (2026); Zhang et al. (2026); Pan et al. (2026). Projeto, §2 [68]."],
  [("Quem está certo?", "Não escolho. Os <em>benchmarks</em> e os braços são diferentes. Por isso H1 mede as duas coisas no mesmo desenho.")],
  "<kbd>→</kbd> revela o gráfico e os cartões"),
 ("Primeira pendência: o custo", "50 s", [
   "A primeira pendência é saber de onde vem a diferença de custo. Pan e colegas apontam a primeira requisição: o contexto inicial do Claude Code passa de dez vezes o do pi, com número de turnos parecido, 15,3 contra 15,4 no Claude Fable 5.",
   "Liu e colegas, no SoL-Pi, apontam o resto da conversa. Mudando só a execução das ações, a compactação de contexto e o tratamento das observações, cortaram de 44,7 % a 49,0 % dos tokens em relação ao pi, e mantiveram de 93,7 % a 94,3 % da pontuação dele.",
   "Ning e colegas pedem métricas que isolem componentes do <em>harness</em>. H2 testa se pesa mais a carga fixa ou a conversa."],
  [("> 10×", "contexto inicial do Claude Code sobre o do pi; Pan et al. (2026) [69]"), ("15,3 vs 15,4", "turnos, Claude Code vs pi, Claude Fable 5 [69]"), ("44,7–49,0 %", "tokens a menos que o pi; Liu et al. (2026) [69]"), ("93,7–94,3 %", "da pontuação do pi mantida [69]")],
  ["Pan et al. (2026); Liu et al. (2026), <em>preprint</em>; Ning et al. (2026, §5.2.7). Projeto, §2 [69]."],
  [("Essas duas fontes não se contradizem?", "Não. Uma olha para a primeira requisição, a outra para a conversa. H2 mede as duas partes no mesmo experimento.")],
  "<kbd>→</kbd> revela os cartões"),
 ("Segunda pendência: a medida", "40 s", [
   "A segunda pendência é a instrumentação. Cada <em>harness</em> conta turnos e tokens do seu jeito, e Pan e colegas registram que a definição de turno varia entre eles. Aqui a medição ocorre num <em>proxy</em> externo, igual para os dois braços, e o objetivo 5 compara essa medida com o relato de cada <em>harness</em>.",
   "Métricas: tokens por construção, ao lado da fração de testes aprovados, e o Succ/Mtok de Lin e colegas, sucessos por milhão de tokens. O efeito também depende do modelo: em nove de doze comparações de Pan e colegas, o maior sucesso veio de um <em>harness</em> de outro fornecedor. Por isso o desenho tem dois níveis de modelo."],
  [("9 de 12", "comparações em que o maior sucesso veio de harness de outro fornecedor; Pan et al. (2026) [71]")],
  ["Projeto, §2 [70]–[71]."],
  [], "<kbd>→</kbd> revela os três cartões"),
 ("Seção 3 · Material e método", "10 s", [
   "Seção 3: classificação, uso de IA declarado, duas camadas de medição, o produto, a matriz, a estatística e as limitações."],
  [], [], [], "só passar"),
 ("Classificação da pesquisa", "30 s", [
   "Aplicada quanto à finalidade, quali-quantitativa quanto à abordagem, exploratória quanto aos objetivos, experimental quanto aos procedimentos e dedutiva quanto ao método. É exploratória porque não há comparação publicada de <em>harnesses</em> construindo o mesmo produto completo. O <em>harness</em> é a variável manipulada; modelo, especificação, espaço de trabalho inicial e limites ficam controlados."],
  [], ["Projeto, §1 [59] e §3 [73]."],
  [("Por que não cita um manual de metodologia?", "A lista de referências fica no tema do <em>harness</em>; a classificação segue a da disciplina.")],
  "<kbd>→</kbd> revela os eixos"),
 ("Uso de IA declarado", "40 s", [
   "Conforme a Portaria CNPq 2.664 de 2026, declaro o uso do Claude Code em duas frentes. No levantamento das fontes, organizado pelo método <em>LLM Wiki</em> de Karpathy no repositório do projeto. E na especificação do Finn, feita com o Helmsman.",
   "Eu conferi cada afirmação citada na obra original e respondo pelo texto e pelas decisões de produto."],
  [], ["Brasil (2026); Karpathy (2026); YuukiFST (2026a, 2026c). Projeto, §3 [74]."],
  [("Isso não contamina o experimento?", "A especificação é a mesma para os dois braços e foi fechada antes de qualquer execução [77].")],
  "<kbd>→</kbd> revela os dois cartões"),
 ("Como o projeto funciona", "35 s", [
   "Quatro passos, nesta ordem. Uma especificação: o Finn em nove unidades, congelada por SHA-256. Dois <em>harnesses</em>: OpenCode e pi, com o mesmo modelo, o mesmo <em>prompt</em> e o mesmo espaço inicial, cada um construindo do zero. Um contador externo: o <em>proxy</em>. Um critério: tokens ao lado da fração de testes aprovados e Succ/Mtok, com Wilcoxon pareado por unidade. Cada braço constrói o Finn ao menos três vezes."],
  [], ["Projeto, §1 [59] e §3 [75]–[83]."],
  [], "pular se faltar tempo"),
 ("Duas camadas de medição", "40 s", [
   "Camada 1: contra um <em>endpoint</em> simulado, mede os esquemas de ferramenta, o <em>prompt</em> de sistema e os tokens de cada requisição. Dá a carga fixa que H2 usa. Camada 2: a construção do produto contra o modelo real.",
   "O <em>proxy</em> conta os tokens sobre os bytes transmitidos, com o mesmo tokenizador para os dois braços; as contagens do <em>harness</em> e do <em>gateway</em> servem só para verificação cruzada. Limite único: tempo de relógio por unidade, três vezes a maior mediana dos braços nas unidades-piloto. O número de passos fica livre, porque um teto de passos é decisão de projeto de <em>harness</em>."],
  [("3×", "a maior mediana dos braços nas unidades-piloto, por unidade [81]")],
  ["Projeto, §3 [75], [80], [81]."],
  [("Por que três vezes a mediana?", "É o limite declarado no projeto, calibrado nas unidades-piloto e igual para os dois braços [81].")],
  "<kbd>→</kbd> revela as camadas"),
 ("Finn: o produto", "35 s", [
   "O Finn é um SaaS multiempresa em que a empresa cliente fala com o próprio financeiro por voz e recebe lançamento, relatório e aviso no celular. Produto e pilha foram decididos antes do experimento, em 21 <em>tickets</em>: TypeScript, TanStack Start, tRPC, Drizzle ORM, PostgreSQL e Vitest. Os agentes não escolhem nada disso."],
  [("21 tickets", "produto e pilha decididos antes do experimento [77]")],
  ["Finn (YuukiFST, 2026b), github.com/YuukiFST/Finn. Projeto, §3 [77]."],
  [("Por que o seu próprio produto?", "As decisões já estão tomadas e registradas, então a especificação sai delas e é a mesma para os dois braços.")],
  "pular se faltar tempo"),
 ("A especificação em 9 unidades", "40 s", [
   "Uma especificação única, congelada por SHA-256, com a pilha e nove unidades em ordem de dependência. O executor chama o <em>harness</em> uma vez por unidade, com o mesmo <em>prompt</em> nos dois braços, e cada unidade parte do que o agente construiu na anterior. Eu não escrevo código no espaço de trabalho.",
   "A pontuação é a fração dos testes de aceitação aprovados. Escrevo os testes antes da execução, deixo fora do espaço de trabalho e rodo sobre uma cópia dele ao fim de cada unidade. Os testes do agente não contam. Uma unidade conta como concluída quando todos os seus testes passam."],
  [("9 unidades", "U1 #15 · U2 #16 · U3 #17 · U4 #14 · U5 #20 · U6 #21 · U7 #19 · U8 #18 · U9 #22")],
  ["Projeto, §3 [77]–[78]; ordem das unidades nas <em>issues</em> do Finn."],
  [("Como garante que o agente não viu os testes?", "Ficam fora do espaço de trabalho e rodam depois, sobre uma cópia [78].")],
  "<kbd>→</kbd> revela as unidades"),
 ("Braços e matriz experimental", "45 s", [
   "Braços: OpenCode e pi. Os dois são de código aberto, rodam sem interface e aceitam URL base compatível com a API da OpenAI, o que permite passá-los pelo <em>proxy</em>. As versões ficam fixadas no repositório.",
   "Dois níveis de modelo, primário e de robustez, gratuitos no mesmo <em>gateway</em>, com resultados por nível. Se a ordenação dos braços inverter de um nível para o outro, a inversão é resultado. Cada combinação de braço e nível tem ao menos três construções completas válidas, relatadas em mediana e dispersão.",
   "Unidade não concluída conta como resultado, com a fração aprovada, e a construção segue. Medição não confiável, como a troca do modelo servido no meio da coleta, descarta a construção inteira."],
  [("2 × 2", "braços × níveis de modelo [76][79]"), ("≥ 3", "construções completas válidas por combinação [82]")],
  ["Opencode (2026a, 2026b); Earendil (2026); projeto, §3 [76], [79], [82], [84]."],
  [("E se os dois braços falharem numa unidade?", "A unidade entra como não concluída nos dois, com a fração aprovada, e as construções seguem [84].")],
  "<kbd>→</kbd> preenche a matriz"),
 ("Métrica e teste pareado", "40 s", [
   "Três medidas: tokens, fração de testes aprovados e Succ/Mtok, sucessos por milhão de tokens. Teste de Wilcoxon dos postos sinalizados, bilateral, α de 0,05, pareado por unidade, porque a dificuldade da unidade é a maior fonte de variação.",
   "Para H2, os tokens de cada unidade se dividem em carga fixa, que é a Camada 1 vezes o número de passos, e conversa. As predições ficam registradas antes da coleta."],
  [("α = 0,05", "Wilcoxon bilateral, pareado por unidade [83]")],
  ["Lin et al. (2026); Miller (2024). Projeto, §2 [71] e §3 [83]."],
  [("Por que não teste t?", "Com poucas unidades e distribuição desconhecida, o Wilcoxon usa postos e não supõe normalidade."),
   ("As unidades não são independentes?", "Não são, e isso está nas limitações: o valor-p vale como indicativo, ao lado da diferença e da dispersão [86].")],
  "<kbd>→</kbd> revela métrica, teste e H2"),
 ("Limitações", "40 s", [
   "Quatro. O efeito do <em>harness</em> depende do modelo, então as conclusões valem por nível. O produto é um único SaaS numa única pilha. Cada braço carrega os próprios erros de uma unidade à seguinte, então as unidades não são independentes, embora o Wilcoxon suponha que sejam; leio o valor-p como indicativo, ao lado da diferença e da dispersão. E o nível gratuito do <em>gateway</em> pode trocar o modelo ou cortar a cota durante a coleta."],
  [], ["Projeto, §3 [86]."],
  [("O que acontece se o gateway trocar o modelo?", "A medição deixa de ser confiável e a construção inteira é descartada [84].")],
  "<kbd>→</kbd> revela cada limitação"),
 ("Seções 4, 5 e 6", "10 s", [
   "Orçamento, cronograma e referências, na ordem do documento."],
  [], [], [], "só passar"),
 ("Orçamento", "25 s", [
   "R$ 0,00. Inferência nos dois níveis, no nível gratuito do <em>gateway</em>. <em>Harnesses</em> e ferramentas de código aberto. Máquinas que já tenho, uma estação NixOS e uma Windows. O risco do custo zero está nas limitações: o nível gratuito pode trocar o modelo ou cortar a cota."],
  [("R$ 0,00", "Tabela 1 do projeto; inferência, harnesses, máquinas [88]–[98]")],
  ["Projeto, §4 [88]–[99]; Opencode (2026b)."],
  [], "<kbd>→</kbd> revela os cartões"),
 ("Cronograma", "25 s", [
   "Agosto e setembro: leitura, tema e hipóteses, e toda a escrita. Outubro e novembro: construção do <em>proxy</em> e dos testes. Outubro: execução da matriz e análise. A revisão final e a apresentação ficam em setembro."],
  [], ["Projeto, §5, Tabela 2 [101]–[157]."],
  [], "<kbd>→</kbd> revela as fases"),
 ("Referências", "15 s", [
   "As entradas da seção 6. Todas tratam do <em>harness</em>, exceto as do método declarado: a Portaria do CNPq, o <em>LLM Wiki</em> e o Helmsman. <em>Preprints</em> e blogues estão marcados como não revisados por pares."],
  [], ["Projeto, §6 [159]–[172]."],
  [("Cadê as normas ABNT e os manuais de metodologia?", "A lista só tem fontes sobre o <em>harness</em>. A formatação segue a ABNT mesmo assim.")],
  "pular se faltar tempo"),
 ("Fecho", "20 s", [
   "A tela repete a pergunta de H1: com o modelo fixo, o <em>harness</em> muda mais o custo do que o sucesso? O projeto responde em tokens e em taxa de sucesso, e separa a parte da carga fixa. Tudo fica público nos dois repositórios. Obrigado. Perguntas?"],
  [], ["github.com/YuukiFST/harness-bench (2026c) · github.com/YuukiFST/Finn (2026b) [170][171]."], [], ""),
]

GLOSS = [
 ("<em>harness</em>", "O software ao redor do modelo que monta o contexto, expõe as ferramentas e conduz a execução [43]: <em>prompt</em> de sistema, ferramentas e <em>middleware</em> (Lin et al., 2026, §1). Converte um modelo sem estado em agente funcional (Ning et al., 2026, §2)."),
 ("imposto do <em>harness</em>", "O que quem paga por tokens paga a mais só pela escolha do <em>harness</em> (Pan et al., 2026) [44]."),
 ("modelo de linguagem", "O núcleo sem estado. Fixo em cada nível; é a variável controlada."),
 ("braço", "Um <em>harness</em> sob teste. Dois: OpenCode e pi."),
 ("carga fixa", "O que o <em>harness</em> envia em toda requisição: <em>prompt</em> de sistema e esquemas de ferramenta [62]. Medida na Camada 1."),
 ("unidade", "Uma parte da especificação do Finn, com testes de aceitação próprios. Nove, em ordem de dependência [77]."),
 ("especificação", "Documento único, escrito pelo autor antes de qualquer execução e congelado por SHA-256 [77]."),
 ("espaço de trabalho inicial", "O diretório de onde uma construção parte. O autor não escreve código nele [77]."),
 ("construção", "Uma execução de um braço, num nível, que constrói o produto inteiro, uma chamada do <em>harness</em> por unidade."),
 ("teste de aceitação", "Teste do autor, escrito antes e mantido fora do espaço de trabalho. Pontuação = fração aprovada; unidade concluída quando todos passam [78]."),
 ("célula", "Um par (braço, nível de modelo), com ao menos três construções completas válidas [82]."),
 ("unidade não concluída", "Conta como resultado, com a fração aprovada, e a construção segue [84]."),
 ("construção descartada", "Medição não confiável, como a troca do modelo servido no meio da coleta, descarta a construção inteira [84]."),
 ("<em>proxy</em> reverso", "O instrumento. Entre o <em>harness</em> e o modelo; conta requisições, tokens e latência sobre os bytes transmitidos, com o mesmo tokenizador [59][80]."),
 ("<em>gateway</em>", "O serviço que entrega os dois níveis gratuitos de modelo (Opencode, 2026b). Suas contagens servem só para verificação cruzada [80]."),
 ("Succ/Mtok", "Sucessos por milhão de tokens (Lin et al., 2026) [71]."),
 ("Wilcoxon dos postos sinalizados", "Teste não paramétrico para pares. Pareado por unidade, bilateral, α = 0,05 [83]."),
 ("<em>preprint</em>", "Artigo sem revisão por pares. Quase todo o referencial está nessa condição; o HarnessTax é blogue de pesquisa. Dizer antes que perguntem."),
]

QA = [
 ("Por que OpenCode e pi, e não Claude Code?", "Os dois são de código aberto, rodam sem interface e aceitam URL base compatível com a API da OpenAI, o que permite passá-los pelo <em>proxy</em> [76]. E ficam em pontos distantes da camada: o pi com quatro ferramentas e <em>prompt</em> curto, o OpenCode com mais ferramentas, subagentes e permissões [67]."),
 ("O resultado vale para outros modelos?", "Não necessariamente. O efeito depende do modelo [71]. Por isso há dois níveis e as conclusões valem por nível [79][86]."),
 ("Qual é a variável manipulada?", "O <em>harness</em>. Controladas: modelo, especificação, espaço de trabalho inicial e limites [73]. Medidas: tokens, fração de testes aprovados e Succ/Mtok [83]."),
 ("Isso é pesquisa ou benchmark?", "Pesquisa experimental com hipóteses refutáveis e predições registradas antes da coleta [83]. A contribuição é separar a carga fixa da conversa, o que Ning et al. (2026, §5.2.7) pedem [69]."),
 ("Por que o proxy e não o relatório do próprio harness?", "Cada <em>harness</em> conta do seu jeito [70]. O objetivo 5 compara o relato com o que o <em>proxy</em> mede."),
 ("O que mudou desde a versão anterior do projeto?", "O título, a justificativa com o HarnessTax, a H1, que agora compara custo e sucesso, o referencial com o SoL-Pi, seis objetivos específicos e quatro limitações."),
]

NUMS = [
 ("97,8 % / 96,7 %", "sucesso do Claude Fable 5, Claude Code / pi", "SWE-bench Lite", "Pan et al. (2026) [43]"),
 ("US$ 1,33 / US$ 0,67", "custo por tentativa, Claude Code / pi", "idem", "Pan et al. (2026) [43]"),
 ("7 / 3", "modelos / harnesses avaliados", "HarnessTax", "Pan et al. (2026) [43]"),
 ("±2 %", "efeito médio do harness sobre o sucesso", "SWE-bench Lite", "Pan et al. (2026) [68]"),
 ("≈ 2,0×", "custo do Claude Code sobre o pi", "SWE-bench Lite", "Pan et al. (2026) [68]"),
 ("47,2 % → 71,9 %", "aprovação OpenCode → Codex", "GPT-5.4, Terminal-Bench 2, harnesses escritos por humanos", "Lin et al. (2026), Tabela 1 [68]"),
 ("> 10×", "contexto inicial do Claude Code sobre o do pi", "Claude Fable 5", "Pan et al. (2026) [69]"),
 ("15,3 / 15,4", "turnos, Claude Code / pi", "Claude Fable 5", "Pan et al. (2026) [69]"),
 ("44,7–49,0 %", "tokens a menos que o pi", "mudando execução, compactação e observações", "Liu et al. (2026) [69]"),
 ("93,7–94,3 %", "da pontuação do pi mantida", "idem", "Liu et al. (2026) [69]"),
 ("9 de 12", "comparações em que o maior sucesso veio de harness de outro fornecedor", "HarnessTax", "Pan et al. (2026) [71]"),
 ("9", "unidades da especificação", "21 tickets de produto e pilha", "projeto, §3 [77]"),
 ("≥ 3", "construções completas válidas por braço e nível", "2 braços × 2 níveis", "projeto, §3 [82]"),
 ("3×", "limite de relógio por unidade", "maior mediana dos braços nas unidades-piloto", "projeto, §3 [81]"),
 ("α = 0,05", "Wilcoxon bilateral, pareado por unidade", "tokens, testes aprovados, Succ/Mtok", "projeto, §3 [83]"),
 ("R$ 0,00", "orçamento total", "inferência, harnesses, máquinas", "projeto, Tabela 1 [97]–[98]"),
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
    total = sum(int(s[1].split()[0]) for s in SLIDES)
    # The cut list is derived from the "pular se faltar tempo" markers so the
    # two never disagree.
    skip = [i for i, s in enumerate(SLIDES, 1) if len(s) > 6 and "pular" in s[6]]
    t_skip = total - sum(int(SLIDES[i - 1][1].split()[0]) for i in skip)
    body = f"""
<h1>Roteiro de estudo da apresentação</h1>
<p class="sub">Projeto de pesquisa "{TITLE}" · Metodologia Científica · IFMT · setembro de 2026.<br>
Companheiro de <code>dist/apresentacao-explainer/index.html</code> ({len(SLIDES)} slides, ordem do documento). Leia em voz alta, cronometre, corte o que passar do tempo.</p>

<nav class="nav">
  <a href="#uso">Como usar</a><a href="#pitch">Versões curtas</a><a href="#gloss">Glossário</a><a href="#slides">Slide a slide</a><a href="#perguntas">Banco de perguntas</a><a href="#numeros">Tabela de números</a><a href="#check">Checklist</a>
</nav>

<h2 id="uso">Como usar este roteiro</h2>
<div class="card">
<ul>
  <li><b>Tempo.</b> Falando tudo, cerca de {total // 60} min {total % 60:02d} s. Pulando os {len(skip)} slides marcados "pular se faltar tempo" ({", ".join(map(str, skip))}), {t_skip // 60} min {t_skip % 60:02d} s.</li>
  <li><b>Blocos por slide:</b> <i>Fale</i> é o texto para dizer, em primeira pessoa, na ordem em que o slide revela. <i>Números</i> traz cada valor com o seu denominador. <i>Fontes</i> diz de onde veio cada afirmação. <i>Se perguntarem</i> antecipa a pergunta mais provável.</li>
  <li><b>Regra dos números:</b> nunca diga um número sem o denominador. "Cerca do dobro" sozinho é fraco; "US$ 1,33 contra US$ 0,67 por tentativa, mesmo Claude Fable 5, SWE-bench Lite" fecha a pergunta óbvia. Todo número deste roteiro está no <code>.docx</code>, no parágrafo indicado.</li>
  <li><b>Ordem do documento.</b> O deck segue o projeto: capa, seção 1 (justificativa, tema, problema, objetivos, hipóteses), seção 2, seção 3, seções 4 a 6. Os índices <code>[n]</code> nas notas do deck (tecla <kbd>N</kbd>) e neste roteiro são os parágrafos do <code>.docx</code> no dump de 23 set. 2026.</li>
  <li><b>Decore quatro pares autor-ano:</b> Pan et al. (2026), Liu et al. (2026), Lin et al. (2026), Ning et al. (2026).</li>
</ul>
</div>

<h2 id="pitch">Versões curtas do projeto</h2>
<div class="card hi">
<h3>Uma frase</h3>
<p class="say">Com o modelo fixo, eu meço quanto o <em>harness</em> muda o custo em tokens e a taxa de sucesso na construção do mesmo SaaS, e quanto da diferença de custo é carga fixa por requisição.</p>
<h3>Trinta segundos</h3>
<div class="say">
<p>No HarnessTax, o Claude Fable 5 resolve 97,8 % no Claude Code e 96,7 % no pi, mas custa US$ 1,33 contra US$ 0,67 por tentativa. Os autores chamam isso de imposto do <em>harness</em>. Essas medições usam tarefas isoladas. Meu projeto constrói o mesmo produto, o Finn, com o OpenCode e com o pi, a partir da mesma especificação e sobre o mesmo modelo, e conta os tokens fora do <em>harness</em>, num <em>proxy</em>.</p>
</div>
<h3>Dois minutos</h3>
<div class="say">
<p><b>Problema.</b> Com o modelo fixo, quanto mudam o custo em tokens e a taxa de sucesso ao construir o mesmo software com um <em>harness</em> em vez de outro, e quanto da diferença de custo vem da carga fixa que cada <em>harness</em> envia em toda requisição?</p>
<p><b>Por que importa.</b> Pan et al. (2026) mostram que o <em>harness</em> quase não muda o sucesso e muda o custo: o Claude Code custa cerca do dobro do pi por tentativa. Lin et al. (2026) acham diferenças grandes de sucesso. As fontes divergem, então eu meço os dois.</p>
<p><b>Método.</b> Duas camadas. Camada 1: a forma da requisição contra um <em>endpoint</em> simulado; dá a carga fixa. Camada 2: a construção do Finn contra o modelo real, pelo <em>proxy</em>, ao menos três construções por braço e nível. Especificação em nove unidades, congelada por SHA-256, testes de aceitação do autor. Métricas: tokens, fração de testes aprovados e Succ/Mtok. Estatística: Wilcoxon pareado por unidade.</p>
<p><b>Hipóteses.</b> H1: com o modelo fixo, o <em>harness</em> muda mais o custo do que o sucesso. H2: a carga fixa explica a maior parte da diferença de tokens. As duas têm critério de refutação declarado.</p>
<p><b>Limites.</b> O efeito depende do modelo, um produto numa pilha só, unidades dependentes e o nível gratuito do <em>gateway</em>. Orçamento R$ 0,00.</p>
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
<li>Ensaiar os slides 3, 10 e 11 com o cronômetro: são os que mais têm nomes e números.</li>
<li>Ter na ponta da língua: 97,8 % vs 96,7 %; US$ 1,33 vs US$ 0,67; ±2 %; mais de 10×; 15,3 vs 15,4; 44,7 % a 49,0 %; R$ 0,00.</li>
<li>Decidir o corte antes de começar, conforme a lista acima.</li>
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
