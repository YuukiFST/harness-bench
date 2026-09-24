"""Rebuild dist/roteiro-apresentacao.html for the 27-slide explainer deck
(dist/apresentacao-explainer/index.html) after tools/docx_edits_2026-09-24.py.
On 2026-09-24 the author replaced the nine units taken from Finn issues #14-#22 with a
reference Finn the author builds first: the specification is extracted from it, one unit
per stage tagged in git, at least six, and the acceptance tests must pass on the reference.
Realigned the same day with the author's own docx revision (placed over the working tree,
then tools/docx_edits_2026-09-24.py and tools/docx_edits_2026-09-24b.py): new justificativa
and problema, Pi (capital P, rest lowercase) as the author names it, no Portaria CNPq, Young (2025) in the list,
hardware row in Tabela 1, Tabela 2 from August to October (after 24d/24e), and every [n] renumbered.
Derived from tools/roteiro_2026-09-23.py; keeps its stylesheet and layout, and regenerates
every section so that no word, number or reference diverges from dist/projeto-de-pesquisa.docx.
Every number cites its paragraph [n] in `python tools/docx_prose.py dump dist/projeto-de-pesquisa.docx`.

Run: python tools/roteiro_2026-09-24.py
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
   "Um <em>coding agent</em> tem duas partes: o modelo de linguagem e o <em>harness</em>, o software em volta dele que monta o contexto, expõe as ferramentas e conduz a execução.",
   "Pan e colegas, da Universidade da Califórnia em Berkeley, avaliaram sete modelos em três <em>harnesses</em> e concluíram que a escolha do <em>harness</em> influencia notavelmente o custo. No SWE-bench Lite, o Claude Fable 5 resolve 97,8 % das tentativas no Claude Code e 96,7 % no Pi. O Claude Code custa cerca do dobro por tentativa: US$ 1,33 contra US$ 0,67.",
   "Quem paga por tokens paga também essa diferença. Os autores chamam isso de imposto do <em>harness</em>."],
  [("97,8 % vs 96,7 %", "sucesso do Claude Fable 5 no Claude Code e no Pi, SWE-bench Lite [43]"), ("US$ 1,33 vs US$ 0,67", "custo por tentativa, mesma comparação [43]"), ("7 modelos · 3 harnesses", "desenho do HarnessTax [43]")],
  ["Pan et al. (2026), HarnessTax, publicação de blogue de pesquisa, não revisada por pares. Diga isso antes que perguntem."],
  [("Isso é fonte confiável?", "É blogue de pesquisa, sem revisão por pares, e eu digo isso na tela. Uso como motivação. O meu desenho mede com instrumento próprio, fora do <em>harness</em>."),
   ("Por que o Claude Code, se ele não é braço do projeto?", "É a comparação que o projeto cita no SWE-bench Lite [43]. Os meus braços são o OpenCode e o Pi, que rodam sem interface e aceitam o <em>proxy</em> [76].")],
  "<kbd>→</kbd> revela o gráfico e os cartões"),
 ("Justificativa e tema", "45 s", [
   "Essas medições usam tarefas isoladas de <em>benchmarks</em> que os modelos podem ter visto no treino. Os próprios autores dizem que o próximo passo é medir o <em>harness</em> em fluxos reais de desenvolvimento, com tarefas de várias sessões.",
   "Tema, e vou ler: o efeito do <em>harness</em> sobre o custo e o desempenho de um modelo de linguagem fixo na construção de um produto de software completo.",
   "O que eu faço: construo o mesmo produto, o Finn, com o OpenCode e com o Pi, sobre o mesmo modelo e a mesma especificação, e conto os tokens fora do <em>harness</em>."],
  [], ["Projeto, §1, justificativa [44] e tema [46]."],
  [("Por que não deixar o OpenCode construir e gerar a especificação para o Pi?", "Entrada desigual. A especificação sai do Finn de referência, que eu construo, e é a mesma para os dois braços [77].")],
  "<kbd>→</kbd> revela os três cartões"),
 ("Problema de pesquisa", "30 s", [
   "O problema, na íntegra: com o modelo fixo, quanto a escolha do <em>harness</em> influencia o custo e a taxa de sucesso na construção do mesmo software?",
   "H1 responde a ele. H2 e o objetivo geral acrescentam a parcela da carga fixa."],
  [], ["Projeto, §1 [48]."],
  [("Por que tokens e não dólares?", "O token é a unidade que o <em>harness</em> controla e que o <em>proxy</em> conta igual para os dois braços [80]. O orçamento é R$ 0,00 no nível gratuito [91]–[92].")],
  "ler na íntegra"),
 ("Objetivos", "45 s", [
   "Objetivo geral: medir, com o modelo fixo, a diferença de tokens e de taxa de sucesso atribuível ao <em>harness</em> na construção do mesmo produto a partir da mesma especificação, com o OpenCode e o Pi como braços, e separar a parcela que vem da carga fixa por requisição.",
   "Seis específicos. Um: construir o <em>proxy</em> que conta requisições, tokens e latência por braço. Dois: construir o Finn de referência e extrair dele a especificação e os testes. Três: construir o Finn nos dois <em>harnesses</em>, com o mesmo modelo, <em>prompt</em> e espaço inicial. Quatro: repetir em um segundo modelo e ver se a ordenação dos braços se mantém. Cinco: comparar os tokens relatados por cada <em>harness</em> com os medidos no <em>proxy</em>. Seis: publicar executor, <em>prompts</em>, testes, dados e scripts de análise."],
  [], ["Projeto, §1 [50] e [52]–[57]."],
  [("Por que o objetivo 5?", "Cada <em>harness</em> conta turnos e tokens do seu jeito, e Pan et al. registram que a definição de turno varia entre eles [70]. O <em>proxy</em> mede igual para os dois; o objetivo 5 compara as duas contagens.")],
  "<kbd>→</kbd> revela a tabela"),
 ("Hipóteses H1 e H2", "50 s", [
   "H1: com o modelo fixo, o <em>harness</em> muda mais o custo do que o sucesso. Os tokens por unidade diferem entre o OpenCode e o Pi, e a fração de testes aprovados fica igual. H1 é refutada se o teste pareado não apontar diferença de tokens ou se as medianas da fração final de testes aprovados diferirem entre os braços.",
   "H2: a carga fixa por requisição, <em>system prompt</em> e esquemas de ferramenta, explica a maior parte da diferença de tokens; o número de passos, a menor. H2 é refutada se os passos ou o conteúdo da conversa explicarem a maior parte."],
  [], ["Projeto, §1 [61]–[62]; predições registradas antes da coleta [83]."],
  [("H1 não é só repetir o HarnessTax?", "O HarnessTax usa tarefas isoladas. Eu testo a mesma pergunta na construção de um produto inteiro, com o OpenCode no lugar do Claude Code, e pareio por unidade."),
   ("Se H2 for refutada, o projeto falhou?", "Não. Se os passos ou a conversa explicarem mais, o resultado diz onde está a diferença, e H2 sai refutada pelo critério declarado.")],
  "<kbd>→</kbd> revela H1 e H2"),
 ("Seção 2 · Referencial teórico", "10 s", [
   "Seção 2. O que é um <em>harness</em>, o que as fontes dizem sobre sucesso e custo, e as duas pendências: de onde vem o custo e como medi-lo."],
  [], [], [], "só passar"),
 ("O que é um harness", "50 s", [
   "Ning e colegas: um <em>harness</em> converte um modelo de linguagem sem estado em um agente funcional, ao ancorar as saídas em execução externa, estado persistente e realimentação verificável.",
   "Lin e colegas dizem o que ele contém: o <em>system prompt</em> que molda o estilo de trabalho, as ferramentas que expõem o sistema de arquivos e o shell, e o <em>middleware</em> que controla contexto, execução e recuperação. Componentes externos ao modelo e editáveis.",
   "Só esse conjunto varia entre os meus braços. O Pi envia quatro ferramentas e um <em>system prompt</em> curto. O OpenCode envia mais ferramentas, subagentes e permissões."],
  [], ["Ning et al. (2026, p. 7); Lin et al. (2026, p. 1). <em>Preprints</em>. Projeto, §2 [65]–[67]."],
  [("O proxy não altera o que está sendo medido?", "Ele fica fora do <em>harness</em> e guarda os tokens que o <em>gateway</em> informa, igual para os dois braços [59][80]. A contagem do próprio <em>harness</em> serve só para verificação cruzada [80]."),
   ("Por que não escrever o próprio harness?", "A pergunta é sobre os <em>harnesses</em> que existem. O projeto escreve o <em>proxy</em>, os <em>prompts</em> e os testes.")],
  "<kbd>→</kbd> revela o diagrama e os pontos"),
 ("Sucesso: as fontes divergem", "50 s", [
   "Sobre o sucesso, as fontes não concordam. Na Tabela 1 de Lin e colegas, <em>harnesses</em> escritos por humanos sobre o GPT-5.4 vão de 47,2 % no OpenCode a 71,9 % no Codex, no Terminal-Bench 2. Zhang e colegas dizem que, em tarefas longas e entre modelos de fronteira comparáveis, a variação de desempenho devida ao <em>harness</em> é comparável ou maior que a devida ao modelo.",
   "Pan e colegas mediram outra coisa no SWE-bench Lite: o efeito médio do <em>harness</em> sobre o sucesso ficou dentro de ±2 %, e o Claude Code custou, em média, cerca de 2,0 vezes o Pi. Por isso eu meço sucesso e custo juntos."],
  [("47,2 % → 71,9 %", "OpenCode → Codex, GPT-5.4, Terminal-Bench 2; Lin et al. (2026), Tabela 1 [68]"), ("±2 %", "efeito médio do harness no sucesso, SWE-bench Lite; Pan et al. (2026) [68]"), ("≈ 2,0×", "custo do Claude Code sobre o Pi [68]")],
  ["Lin et al. (2026); Zhang et al. (2026); Pan et al. (2026). Projeto, §2 [68]."],
  [("Quem está certo?", "Não escolho. Os <em>benchmarks</em> e os braços são diferentes. Por isso H1 mede as duas coisas no mesmo desenho.")],
  "<kbd>→</kbd> revela o gráfico e os cartões"),
 ("Primeira pendência: o custo", "50 s", [
   "A primeira pendência é saber de onde vem a diferença de custo. Para Pan e colegas, o imposto pode começar na primeira requisição: nos sete modelos, o contexto inicial médio do Claude Code passa de dez vezes o do Pi, e no Claude Fable 5 os turnos quase se igualam, 15,3 contra 15,4.",
   "Liu e colegas, no SoL-Pi, apontam o resto da conversa. Mudando só a execução das ações, a compactação de contexto, o tratamento das observações e a leitura delegada, cortaram de 44,7 % a 49,0 % dos tokens em relação ao Pi, e mantiveram de 93,7 % a 94,3 % da pontuação dele.",
   "Ning e colegas pedem métricas que isolem componentes do <em>harness</em>. H2 testa se pesa mais a carga fixa ou a conversa."],
  [("> 10×", "contexto inicial do Claude Code sobre o do Pi; Pan et al. (2026) [69]"), ("15,3 vs 15,4", "turnos, Claude Code vs Pi, Claude Fable 5 [69]"), ("44,7–49,0 %", "tokens a menos que o Pi; Liu et al. (2026) [69]"), ("93,7–94,3 %", "da pontuação do Pi mantida [69]")],
  ["Pan et al. (2026); Liu et al. (2026), <em>preprint</em>; Ning et al. (2026, p. 66). Projeto, §2 [69]."],
  [("Essas duas fontes não se contradizem?", "Não. Uma olha para a primeira requisição, a outra para a conversa. H2 mede as duas partes no mesmo experimento.")],
  "<kbd>→</kbd> revela os cartões"),
 ("Segunda pendência: a medida", "40 s", [
   "A segunda pendência é a instrumentação. Cada <em>harness</em> conta turnos e tokens do seu jeito, e Pan e colegas registram que a definição de turno varia entre eles. Aqui a medição ocorre num <em>proxy</em> externo, igual para os dois braços, e o objetivo 5 compara essa medida com o relato de cada <em>harness</em>.",
   "Métricas: tokens por construção, ao lado da fração de testes aprovados, e o Succ/Mtok de Lin e colegas, sucessos por milhão de tokens. O efeito também depende do modelo: em nove de doze comparações de Pan e colegas, o maior sucesso veio de um <em>harness</em> que não é o do fornecedor do modelo. Por isso o desenho tem dois níveis de modelo."],
  [("9 de 12", "comparações em que o maior sucesso veio de harness que não é o do fornecedor do modelo; Pan et al. (2026) [71]")],
  ["Projeto, §2 [70]–[71]."],
  [], "<kbd>→</kbd> revela os três cartões"),
 ("Seção 3 · Material e método", "10 s", [
   "Seção 3: classificação, uso de IA declarado, duas camadas de medição, o produto, a matriz, a estatística e as limitações."],
  [], [], [], "só passar"),
 ("Classificação da pesquisa", "30 s", [
   "Aplicada quanto à finalidade, quali-quantitativa quanto à abordagem, exploratória quanto aos objetivos, experimental quanto aos procedimentos e dedutiva quanto ao método. É exploratória porque não se encontrou comparação publicada de <em>harnesses</em> construindo o mesmo produto completo. O <em>harness</em> é a variável manipulada; modelo, especificação, espaço de trabalho inicial e limites ficam controlados."],
  [], ["Projeto, §1 [59] e §3 [73]."],
  [("Por que não cita um manual de metodologia?", "A lista de referências fica no tema do <em>harness</em>; a classificação segue a da disciplina.")],
  "<kbd>→</kbd> revela os eixos"),
 ("Uso de IA declarado", "40 s", [
   "Declaro o uso do Claude Code em três frentes. No levantamento das fontes, organizado pelo método <em>LLM Wiki</em> de Karpathy no repositório do projeto. Nas decisões do Finn, mapeadas com o Helmsman. E na versão de referência do Finn.",
   "Eu conferi cada afirmação citada na obra original e respondo pelo texto e pelas decisões de produto."],
  [], ["Karpathy (2026); YuukiFST (2026a, 2026c). Projeto, §3 [74]."],
  [("Isso não contamina o experimento?", "A especificação é a mesma para os dois braços, congelada por SHA-256 antes de qualquer execução, e nenhum código do autor entra no espaço de trabalho [77].")],
  "<kbd>→</kbd> revela os dois cartões"),
 ("Como o projeto funciona", "35 s", [
   "Quatro passos, nesta ordem. Uma especificação: sai do Finn de referência, congelada por SHA-256, uma unidade por etapa. Dois <em>harnesses</em>: OpenCode e Pi, com o mesmo modelo, o mesmo <em>prompt</em> e o mesmo espaço inicial, cada um construindo do zero. Um contador externo: o <em>proxy</em>. Um critério: tokens e Succ/Mtok, com Wilcoxon pareado por unidade, sempre ao lado da fração de testes aprovados. Cada braço constrói o Finn ao menos três vezes."],
  [], ["Projeto, §1 [59] e §3 [75]–[83]."],
  [], "pular se faltar tempo"),
 ("Duas camadas de medição", "40 s", [
   "Camada 1: contra um <em>endpoint</em> simulado, mede os esquemas de ferramenta, o <em>system prompt</em> e os tokens de cada requisição. Mostra a carga fixa de cada braço sem tarefa. Camada 2: a construção do produto contra o modelo real.",
   "O <em>proxy</em> guarda os tokens que o <em>gateway</em> informa em cada resposta, com o cache à parte, e separa em cada requisição a carga fixa do resto da conversa. A contagem do <em>harness</em> serve só para verificação cruzada. Limite único: tempo de relógio por unidade, três vezes a maior mediana dos braços nas unidades-piloto. O número de passos fica livre, porque um teto de passos é decisão de projeto de <em>harness</em>."],
  [("3×", "a maior mediana dos braços nas unidades-piloto, por unidade [81]")],
  ["Projeto, §3 [75], [80], [81]."],
  [("Por que três vezes a mediana?", "É o limite declarado no projeto, calibrado nas unidades-piloto e igual para os dois braços [81].")],
  "<kbd>→</kbd> revela as camadas"),
 ("Finn: o produto", "35 s", [
   "O Finn é um SaaS multiempresa em que a empresa cliente fala com o próprio financeiro por voz e recebe lançamento, relatório e aviso no celular. Ele foi decidido em 21 <em>tickets</em>. A pilha entra na especificação, que sai da versão de referência."],
  [("21 tickets", "decisões do Finn [77]")],
  ["Finn (YuukiFST, 2026b), github.com/YuukiFST/Finn. Projeto, §3 [77]."],
  [("Por que o seu próprio produto?", "As decisões já estão registradas em 21 <em>tickets</em>, e a especificação sai da versão de referência, a mesma para os dois braços [77].")],
  "pular se faltar tempo"),
 ("A especificação e as unidades", "45 s", [
   "Primeiro eu construo uma versão de referência do Finn e marco no git o fim de cada etapa. Dela sai a especificação, congelada por SHA-256: o produto, a pilha, a interface que os testes usam e as funcionalidades em JSON. Cada etapa vira uma unidade, e são ao menos seis.",
   "O executor chama o <em>harness</em> uma vez por unidade, com o mesmo <em>prompt</em> nos dois braços, e cada unidade parte do que o agente construiu na anterior. Nenhum código meu entra no espaço de trabalho.",
   "A pontuação é a fração dos testes de aceitação aprovados. Escrevo os testes antes da execução, deixo fora do espaço de trabalho e rodo sobre uma cópia dele ao fim de cada unidade. Todos precisam passar antes na referência, no marco da etapa. Os testes do agente não contam, e uma unidade conta como concluída quando todos os seus testes passam."],
  [("≥ 6 unidades", "uma por etapa do Finn de referência [77]")],
  ["Projeto, §3 [77]–[78]."],
  [("Como garante que o agente não viu os testes?", "Ficam fora do espaço de trabalho e rodam depois, sobre uma cópia [78]."),
   ("Como a especificação sai do Finn de referência?", "Eu construo o Finn até ele fazer o que o produto pede, com o fim de cada etapa marcado no git. Do resultado escrevo o produto, a pilha, a interface dos testes e a lista de funcionalidades em JSON, e congelo tudo por SHA-256. O código não vai junto. Os testes de cada unidade passam na referência, no marco da etapa, antes do congelamento [77]–[78]."),
   ("Por que ao menos seis unidades?", "É o mínimo para o Wilcoxon pareado bilateral chegar a p abaixo de 0,05. Com seis pares, o menor p possível é 2/2⁶, cerca de 0,031 (conta própria, não está no projeto).")],
  "<kbd>→</kbd> revela a especificação e os cartões"),
 ("Braços e matriz experimental", "45 s", [
   "Braços: OpenCode e Pi. Os dois são de código aberto, rodam sem interface e aceitam URL base compatível com a API da OpenAI, o que permite passá-los pelo <em>proxy</em>. As versões ficam fixadas e registradas no repositório do projeto.",
   "Dois níveis de modelo, primário e de robustez, gratuitos no mesmo <em>gateway</em>, com resultados por nível. Se a ordenação dos braços inverter de um nível para o outro, a inversão é resultado. Cada combinação de braço e nível tem ao menos três construções completas válidas, relatadas em mediana e dispersão.",
   "Unidade não concluída conta como resultado, com a fração aprovada, e a construção segue. Medição não confiável, como a troca do modelo servido no meio da coleta, descarta a construção inteira."],
  [("2 × 2", "braços × níveis de modelo [76][79]"), ("≥ 3", "construções completas válidas por combinação [82]")],
  ["Opencode (2026a, 2026b); Earendil (2026); YuukiFST (2026c); projeto, §3 [76], [79], [82], [84]."],
  [("E se os dois braços falharem numa unidade?", "A unidade entra como não concluída nos dois, com a fração aprovada, e as construções seguem [84].")],
  "<kbd>→</kbd> preenche a matriz"),
 ("Como os tokens são contados e comparados", "50 s", [
   "São quatro passos. Primeiro, medir. Toda requisição passa pelo <em>proxy</em>. Ele guarda o número de tokens que o próprio <em>gateway</em> informa na resposta: entrada, cache e saída. Eu somo por unidade e por construção. O número que o <em>harness</em> mostra serve só para conferir.",
   "Segundo, resumir. Cada braço constrói o Finn ao menos três vezes, e eu uso a mediana dos tokens por construção. Ao lado, o Succ/Mtok, que é o número de sucessos dividido pelos milhões de tokens gastos.",
   "Terceiro, comparar. O teste de Wilcoxon põe a unidade 1 do OpenCode contra a unidade 1 do Pi, a 2 contra a 2, e assim por diante. Ele diz se a diferença de tokens é consistente ou pode ser acaso. O número principal é a razão entre as medianas dos dois braços. A fração de testes aprovados vai sem teste: se os dois passarem em tudo, não sobra diferença.",
   "Quarto, explicar. Em cada requisição, o <em>proxy</em> separa o <em>system prompt</em> e as ferramentas do resto da conversa. É isso que responde H2. As predições ficam registradas antes da coleta."],
  [("α = 0,05", "Wilcoxon bilateral, pareado por unidade, sobre tokens e Succ/Mtok [83]")],
  ["Lin et al. (2026); Miller (2024). Projeto, §2 [71] e §3 [80], [83]."],
  [("Por que não teste t?", "Com poucas unidades e distribuição desconhecida, o Wilcoxon usa postos e não supõe normalidade."),
   ("As unidades não são independentes?", "Não são, e isso está nas limitações: o valor-p vale como indicativo, ao lado da diferença e da dispersão [86].")],
  "<kbd>→</kbd> revela métrica, teste e H2"),
 ("Limitações", "40 s", [
   "Quatro. O efeito do <em>harness</em> depende do modelo, então as conclusões valem por nível. O produto é um único SaaS, especificado a partir da solução que eu mesmo construí. Cada braço carrega os próprios erros de uma unidade à seguinte, então as unidades não são independentes, embora o Wilcoxon suponha que sejam; leio o valor-p como indicativo, ao lado da diferença e da dispersão. E o nível gratuito do <em>gateway</em> pode trocar o modelo ou cortar a cota durante a coleta."],
  [], ["Projeto, §3 [86]."],
  [("O que acontece se o gateway trocar o modelo?", "A medição deixa de ser confiável e a construção inteira é descartada [84].")],
  "<kbd>→</kbd> revela cada limitação"),
 ("Seções 4, 5 e 6", "10 s", [
   "Orçamento, cronograma e referências, na ordem do documento."],
  [], [], [], "só passar"),
 ("Orçamento", "25 s", [
   "R$ 0,00. Inferência nos dois níveis, no nível gratuito do <em>gateway</em>. <em>Harnesses</em> e ferramentas de código aberto. Hardware: o meu PC pessoal, com NixOS. O risco do custo zero está nas limitações: o nível gratuito pode trocar o modelo ou cortar a cota."],
  [("R$ 0,00", "Tabela 1 do projeto; inferência, harnesses, hardware [88]–[99]")],
  ["Projeto, §4 [88]–[99]; Opencode (2026b)."],
  [], "<kbd>→</kbd> revela os cartões"),
 ("Cronograma", "25 s", [
   "O calendário vai de agosto a outubro. Agosto e setembro: leitura, tema e hipóteses, e toda a escrita. Outubro: o Finn de referência, o <em>proxy</em> e os testes, a execução da matriz e a análise. A revisão final e a apresentação ficam em setembro."],
  [], ["Projeto, §5, Tabela 2 [101]–[146]."],
  [], "<kbd>→</kbd> revela as fases"),
 ("Referências", "15 s", [
   "As 14 entradas da seção 6. Tratam do <em>harness</em>, exceto as do método declarado, o <em>LLM Wiki</em> e o Helmsman, e os repositórios do Finn e do projeto. <em>Preprints</em> e blogues estão marcados como não revisados por pares."],
  [], ["Projeto, §6 [147]–[161]."],
  [("Cadê as normas ABNT e os manuais de metodologia?", "A lista fica no tema do <em>harness</em>; as normas orientam a formatação e não são citadas.")],
  "pular se faltar tempo"),
 ("Fecho", "20 s", [
    "A tela fecha com o recado prático: conhecer o modelo não basta, o <em>harness</em> tem grande influência no custo. No mercado atual, quem desenvolve com agentes precisa entender os dois: o modelo que gera e o <em>harness</em> que o envolve. O projeto testa isso em H1, com o modelo fixo, medindo tokens e taxa de sucesso e separando a parte da carga fixa. Tudo fica público nos dois repositórios."],
  [], ["github.com/YuukiFST/harness-bench (2026c) · github.com/YuukiFST/Finn (2026b) [160][159]."], [], ""),
]

GLOSS = [
 ("<em>harness</em>", "O software ao redor do modelo que monta o contexto, expõe as ferramentas e conduz a execução [43]: <em>system prompt</em>, ferramentas e <em>middleware</em> (Lin et al., 2026, p. 1). Converte um modelo sem estado em agente funcional (Ning et al., 2026, p. 7)."),
 ("imposto do <em>harness</em>", "O que quem paga por tokens paga a mais só pela escolha do <em>harness</em> (Pan et al., 2026) [44]."),
 ("modelo de linguagem", "O núcleo sem estado. Fixo em cada nível; é a variável controlada."),
 ("braço", "Um <em>harness</em> sob teste. Dois: OpenCode e Pi."),
 ("carga fixa", "O que o <em>harness</em> envia em toda requisição: <em>system prompt</em> e esquemas de ferramenta [62]. Medida sem tarefa na Camada 1 [75] e separada em cada requisição pelo <em>proxy</em> [80]."),
 ("unidade", "Uma parte da especificação do Finn, com testes de aceitação próprios. Uma por etapa do Finn de referência, ao menos seis [77]."),
 ("Finn de referência", "A versão do Finn que o autor constrói antes do experimento, com o fim de cada etapa marcado no git. Dela sai a especificação; o código não entra no espaço de trabalho [77]."),
 ("especificação", "Extraída do Finn de referência e congelada por SHA-256 antes de qualquer execução: produto, pilha, interface dos testes e funcionalidades em JSON [77]."),
 ("espaço de trabalho inicial", "O diretório de onde uma construção parte. Nenhum código do autor entra nele [77]."),
 ("construção", "Uma execução de um braço, num nível, que constrói o produto inteiro, uma chamada do <em>harness</em> por unidade."),
 ("teste de aceitação", "Teste do autor, escrito antes, mantido fora do espaço de trabalho e aprovado antes na referência. Pontuação = fração aprovada; unidade concluída quando todos passam [78]."),
 ("célula", "Um par (braço, nível de modelo), com ao menos três construções completas válidas [82]."),
 ("unidade não concluída", "Conta como resultado, com a fração aprovada, e a construção segue [84]."),
 ("construção descartada", "Medição não confiável, como a troca do modelo servido no meio da coleta, descarta a construção inteira [84]."),
 ("<em>proxy</em> reverso", "O instrumento. Entre o <em>harness</em> e o modelo; guarda requisições, latência e os tokens que o <em>gateway</em> informa, e separa a carga fixa do resto da conversa [59][80]."),
 ("<em>gateway</em>", "O serviço que entrega os dois níveis gratuitos de modelo (Opencode, 2026b). Sua contagem de tokens, lida no <em>proxy</em>, é a medida do projeto [80]."),
 ("Succ/Mtok", "Sucessos por milhão de tokens (Lin et al., 2026) [71]."),
 ("Wilcoxon dos postos sinalizados", "Teste não paramétrico para pares. Pareado por unidade, bilateral, α = 0,05 [83]."),
 ("<em>preprint</em>", "Artigo sem revisão por pares. Quase todo o referencial está nessa condição; o HarnessTax é blogue de pesquisa. Dizer antes que perguntem."),
]

QA = [
 ("Por que OpenCode e Pi, e não Claude Code?", "Os dois são de código aberto, rodam sem interface e aceitam URL base compatível com a API da OpenAI, o que permite passá-los pelo <em>proxy</em> [76]. E ficam em pontos distantes da camada: o Pi com quatro ferramentas e <em>system prompt</em> curto, o OpenCode com mais ferramentas, subagentes e permissões [67]."),
 ("O resultado vale para outros modelos?", "Não necessariamente. O efeito depende do modelo [71]. Por isso há dois níveis e as conclusões valem por nível [79][86]."),
 ("Qual é a variável manipulada?", "O <em>harness</em>. Controladas: modelo, especificação, espaço de trabalho inicial e limites [73]. Medidas: tokens e Succ/Mtok, com a fração de testes aprovados ao lado [83]."),
 ("Isso é pesquisa ou benchmark?", "Pesquisa experimental com hipóteses refutáveis e predições registradas antes da coleta [83]. A contribuição é separar a carga fixa da conversa, o que Ning et al. (2026, p. 66) pedem [69]."),
 ("Por que o proxy e não o relatório do próprio harness?", "Cada <em>harness</em> conta do seu jeito [70]. O objetivo 5 compara o relato com o que o <em>proxy</em> mede."),
 ("O que mudou desde a versão anterior do projeto?", "O título, a justificativa com o HarnessTax, o problema, a H1, que agora compara custo e sucesso, o referencial com o SoL-Pi, seis objetivos específicos, quatro limitações, o cronograma, com matriz e análise em outubro, e a especificação, que agora sai do Finn de referência."),
]

NUMS = [
 ("97,8 % / 96,7 %", "sucesso do Claude Fable 5, Claude Code / Pi", "SWE-bench Lite", "Pan et al. (2026) [43]"),
 ("US$ 1,33 / US$ 0,67", "custo por tentativa, Claude Code / Pi", "idem", "Pan et al. (2026) [43]"),
 ("7 / 3", "modelos / harnesses avaliados", "HarnessTax", "Pan et al. (2026) [43]"),
 ("±2 %", "efeito médio do harness sobre o sucesso", "SWE-bench Lite", "Pan et al. (2026) [68]"),
 ("≈ 2,0×", "custo do Claude Code sobre o Pi", "SWE-bench Lite", "Pan et al. (2026) [68]"),
 ("47,2 % → 71,9 %", "aprovação OpenCode → Codex", "GPT-5.4, Terminal-Bench 2, harnesses escritos por humanos", "Lin et al. (2026), Tabela 1 [68]"),
 ("> 10×", "contexto inicial do Claude Code sobre o do Pi", "Claude Fable 5", "Pan et al. (2026) [69]"),
 ("15,3 / 15,4", "turnos, Claude Code / Pi", "Claude Fable 5", "Pan et al. (2026) [69]"),
 ("44,7–49,0 %", "tokens a menos que o Pi", "mudando execução, compactação, observações e leitura delegada", "Liu et al. (2026) [69]"),
 ("93,7–94,3 %", "da pontuação do Pi mantida", "idem", "Liu et al. (2026) [69]"),
 ("9 de 12", "comparações em que o maior sucesso veio de harness que não é o do fornecedor do modelo", "HarnessTax", "Pan et al. (2026) [71]"),
 ("≥ 6", "unidades da especificação", "uma por etapa do Finn de referência", "projeto, §3 [77]"),
 ("≥ 3", "construções completas válidas por braço e nível", "2 braços × 2 níveis", "projeto, §3 [82]"),
 ("3×", "limite de relógio por unidade", "maior mediana dos braços nas unidades-piloto", "projeto, §3 [81]"),
 ("α = 0,05", "Wilcoxon bilateral, pareado por unidade", "tokens e Succ/Mtok", "projeto, §3 [83]"),
 ("R$ 0,00", "orçamento total", "inferência, harnesses, hardware", "projeto, Tabela 1 [97]–[98]"),
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
  <li><b>Ordem do documento.</b> O deck segue o projeto: capa, seção 1 (justificativa, tema, problema, objetivos, hipóteses), seção 2, seção 3, seções 4 a 6. Os índices <code>[n]</code> nas notas do deck (tecla <kbd>N</kbd>) e neste roteiro são os parágrafos do <code>.docx</code> no dump de 24 set. 2026 (versão do autor, com as correções de citação).</li>
  <li><b>Decore quatro pares autor-ano:</b> Pan et al. (2026), Liu et al. (2026), Lin et al. (2026), Ning et al. (2026).</li>
</ul>
</div>

<h2 id="pitch">Versões curtas do projeto</h2>
<div class="card hi">
<h3>Uma frase</h3>
<p class="say">Com o modelo fixo, eu meço quanto o <em>harness</em> muda o custo em tokens e a taxa de sucesso na construção do mesmo SaaS, e quanto da diferença de custo é carga fixa por requisição.</p>
<h3>Trinta segundos</h3>
<div class="say">
<p>No HarnessTax, o Claude Fable 5 resolve 97,8 % no Claude Code e 96,7 % no Pi, mas custa US$ 1,33 contra US$ 0,67 por tentativa. Os autores chamam isso de imposto do <em>harness</em>. Essas medições usam tarefas isoladas. Meu projeto constrói o mesmo produto, o Finn, com o OpenCode e com o Pi, a partir da mesma especificação e sobre o mesmo modelo, e conta os tokens fora do <em>harness</em>, num <em>proxy</em>.</p>
</div>
<h3>Dois minutos</h3>
<div class="say">
<p><b>Problema.</b> Com o modelo fixo, quanto a escolha do <em>harness</em> influencia o custo e a taxa de sucesso na construção do mesmo software?</p>
<p><b>Por que importa.</b> Pan et al. (2026) concluem que a escolha do <em>harness</em> influencia notavelmente o custo: o Claude Code custa cerca do dobro do Pi por tentativa, e o efeito médio sobre o sucesso fica dentro de ±2 %. Lin et al. (2026) acham diferenças grandes de sucesso. As fontes divergem, então eu meço os dois.</p>
<p><b>Método.</b> Duas camadas. Camada 1: a forma da requisição contra um <em>endpoint</em> simulado; mostra a carga fixa sem tarefa. Camada 2: a construção do Finn contra o modelo real, pelo <em>proxy</em>, ao menos três construções por braço e nível. Especificação extraída do Finn de referência, congelada por SHA-256, uma unidade por etapa, testes de aceitação do autor aprovados antes na referência. Medição: os tokens que o <em>gateway</em> informa, lidos no <em>proxy</em>. Métricas: tokens por construção, Succ/Mtok e fração de testes aprovados. Estatística: Wilcoxon pareado por unidade sobre tokens e Succ/Mtok; resultado principal, a razão entre as medianas.</p>
<p><b>Hipóteses.</b> H1: com o modelo fixo, o <em>harness</em> muda mais o custo do que o sucesso. H2: a carga fixa explica a maior parte da diferença de tokens. As duas têm critério de refutação declarado.</p>
<p><b>Limites.</b> O efeito depende do modelo, um produto especificado a partir da solução do autor, unidades dependentes e o nível gratuito do <em>gateway</em>. Orçamento R$ 0,00.</p>
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
