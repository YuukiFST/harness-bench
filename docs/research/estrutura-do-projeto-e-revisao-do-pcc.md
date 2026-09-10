# Estrutura do projeto de pesquisa e revisão do `projeto-pcc.docx`

Documento vivo.
Confere o `dist/projeto-pcc.docx` contra o material da disciplina em `files/` e contra o que se mede na própria prosa.

**Última atualização:** 10 set. 2026.
Complementa [Pangram — como o detector funciona](pangram-deteccao-de-texto-gerado.md).

Os três arquivos da disciplina citados aqui passaram a ser rastreados em `files/`, então os caminhos deste documento resolvem para um leitor que só tem o repositório.

## 0. Método desta revisão

Três fontes, nesta ordem de autoridade:

1. `files/Template projeto novo3.pdf` — o gabarito do IFMT, com as marcações de formatação.
2. `files/O que é projeto de pesquisa.pdf` (Aula 2) e `files/Estrutura do projeto de pesquisa-aula3.pdf` (Aula 3) — a estrutura exigida.
3. `files/Aula 5- Citacoes e referencias.odt` — citações e referências, já com as emendas de 2023 e 2025.

Onde a revisão afirma um número sobre a prosa, o número foi medido no XML do `.docx`, não estimado.

**Ressalva que vale para tudo abaixo.** Nada aqui derruba o escore do Pangram de forma relevante, e a seção 9 daquele documento explica por quê: o classificador é invariante a transformação de superfície.
O que estas correções fazem é outra coisa — deixam o documento conforme ao que a disciplina pediu e melhor de ler.
Isso vale por si.

## 1. A estrutura que o material exige

O gabarito e a Aula 3 concordam. O sumário é fixo:

| | Seção |
|---|---|
| 1 | Introdução |
| 2 | Referencial Teórico |
| 3 | Material e Método |
| 4 | Orçamento |
| 5 | Cronograma |
| 6 | Referências |

E a Introdução tem ordem interna obrigatória, com o conteúdo de cada bloco fixado pela Aula 3:

| Bloco | O que o material pede | Tamanho |
|---|---|---|
| Justificativa | atualidade do tema, interesse, **contribuição social e acadêmica** | 2 a 3 parágrafos, máx. 12 linhas |
| Tema | só informar qual é | 1 parágrafo |
| Problema | a controvérsia | 1 parágrafo |
| Objetivo geral | o que pretende fazer | 1 parágrafo |
| Objetivos específicos | os caminhos até o objetivo geral | tópicos, **1 linha cada** |
| Metodologia | como coleta, o que espera obter, que método usa | 1 parágrafo breve |
| Hipótese | possível resposta ao problema | encerra a introdução |
| Organização | prévia de como o trabalho está organizado | último parágrafo |

Note que a NBR 15287 reproduzida na Aula 2 lista **Recursos Necessários** como obrigatório, separado de Orçamento.
O gabarito da disciplina colapsa os dois em "4 Orçamento". Onde as duas fontes divergem, o gabarito manda.

## 2. Conformidade — o que já está certo

| Item | Situação |
|---|---|
| Sumário, seções 1 a 6 | confere com o gabarito |
| Ordem interna da Introdução | confere com a Aula 3, bloco a bloco |
| Justificativa em 2 parágrafos | dentro do teto de 12 linhas |
| Hipótese encerrando a introdução | correto |
| Último parágrafo = organização do trabalho | correto |
| Folha de rosto | tem autor, título, natureza, instituição, orientadora, cidade, ano |
| Citação autor-data em minúsculas | correto — a Aula 5 registra que a NBR 10520:2023 aboliu a caixa alta dentro de parênteses |
| Ausência de `< >` nos links | correto — exigência da NBR 6023:2025 registrada na Aula 5 |
| Referências em ordem alfabética | correto |
| Contribuição social e acadêmica na justificativa | correto desde 10 set. 2026 (§3.1) |
| Os quatro tipos de citação da Aula 5 | correto desde 10 set. 2026 (§3.3) |

O documento está, no esqueleto, conforme. Os problemas são de conteúdo e de prosa.

## 3. Não conformidades com o material da disciplina

### 3.1 A justificativa não cumpre o que o gabarito pede dela

O gabarito lista, explicitamente, três coisas que a justificativa deve conter:

> Atualidade do tema
> Interesse (Porque o tema é interessante)
> **Contribuiçao social e acadêmica do assunto**

A justificativa entregava a primeira e a segunda por meio de números (17x, 139x, 11,4x) e não entregava a terceira.

**Resolvido em 10 set. 2026.** O segundo parágrafo fecha nomeando os dois destinatários:

> Medir quanto dessa carga chega ao resultado dá ao desenvolvedor, que hoje decide sem dado próprio, um critério de escolha, e à literatura a primeira comparação com a linhagem do *harness* mantida fixa.

Contribuição social é o desenvolvedor; contribuição acadêmica é a comparação com linhagem fixa, que nenhuma fonte levantada publica.
O teto de 12 linhas foi respeitado cortando redundância dos dois parágrafos: a justificativa continua com dois parágrafos e cerca de 11 linhas.
A Aula 3 põe a finalidade da justificativa em uma linha: "Convencer o leitor a ler o meu trabalho".

### 3.2 Objetivos específicos ocupam 2 a 3 linhas cada

O gabarito é literal: "Escreve objetivo específico em tópicos", "1 linha para cada".

Os sete objetivos atuais têm de 20 a 35 palavras. O (2) é o pior caso:

> definir uma suíte de tarefas de programação com objetivos numerados e crédito parcial, acompanhada de um oráculo automatizado independente dos testes produzidos pelo próprio agente

Cada um comporta ser cortado a uma linha sem perder o que decide. O detalhe já está na seção 3, que é onde ele pertence.

### 3.3 Zero citações diretas

A Aula 5 inteira é sobre citação: direta curta (até 3 linhas, entre aspas, autor-ano-página), direta longa (recuo de 4 cm, fonte menor, espaçamento simples, sem aspas), indireta, e citação de citação com `apud`.

O documento tinha **28 citações e nenhuma direta**. Todas eram indiretas, e o corpo do texto, excluídas as referências, não continha uma única aspa.
Um Referencial Teórico numa disciplina que acabou de ensinar os quatro tipos de citação e não exibe nenhum deles deixa de demonstrar o que foi ensinado.

**Resolvido em 10 set. 2026**, com um exemplar de cada tipo na seção 2, todos com fonte verbatim registrada em `docs/research/02-harness-concepts-and-metrics.md`:

| Tipo | Onde | Fonte |
|---|---|---|
| Direta curta | definição de *harness*, § 2 ¶ 1 | Ning et al. (2026, §2, tradução nossa) |
| Direta longa | o que a camada contém, § 2, bloco recuado | Lin et al. (2026, §1, tradução nossa) |
| Direta curta | "métricas que isolem componentes do harness", § 2 ¶ 4 | Ning et al. (2026, §5.2.7, tradução nossa) |
| Citação de citação | custo por tarefa variando mais de 2x | Databricks, 2026 *apud* Earendil, 2026 |

As três diretas transcrevem texto em inglês, então levam `tradução nossa`, que a Aula 5 não cobre e a NBR 10520 prevê.
Nenhuma obra nova entrou nas referências: Ning, Lin e Earendil já estavam lá, e o `apud` mantém na lista só a obra consultada, como a Aula 5 exige.
A citação longa segue a formatação pedida: recuo de 4 cm, 10 pt, espaçamento simples, sem aspas, com a fonte depois do ponto final.

Continua **não transcrita** a *Binding Constraint Thesis* de Zhang et al. (2026): a pesquisa em `docs/research/03-complementary-references.md` só registra paráfrase em português, e não há trecho verbatim para transcrever sem inventá-lo.

### 3.4 Marcadores editoriais no texto entregue

~~Quatro no corpo: `[A VERIFICAR]` (crédito parcial, §3), dois `[A MEDIR]` (relógio §3, cota §4) e `[A DEFINIR]` (data, §5).~~ Resolvidos: a data virou prosa com a entrega em setembro de 2026, e os três das pilotos viraram prosa futura ("será confirmado", "gastar nas tarefas-piloto", "consome nas tarefas-piloto") — proposta descreve trabalho a fazer, então o futuro no texto está certo e o colchete, errado.

### 3.5 Cronograma em meses relativos

O gabarito usa meses nomeados (MARÇO a JULHO). O documento usa SETEMBRO a JANEIRO, 5 colunas de trabalho futuro a partir da entrega em setembro de 2026 — proposta planeja para frente, e o futuro no cronograma está certo. Plano do autor: hoje só o documento do projeto; o prático da pesquisa, para janeiro (matriz em DEZ–JAN).

### 3.6 Recursos Necessários

A NBR 15287 reproduzida na Aula 2 pede a seção; o gabarito não a tem.
A Aula 3 explica o que ela responderia: "Onde você espera achar as informações?".
O documento responde isso disperso pela seção 3 (DeepSWE, gateway, proxy, duas estações).
Baixa prioridade — o gabarito manda —, mas vale confirmar com a orientadora, porque é gratuito acrescentar e caro descobrir depois.

### 3.7 `tools/build_pcc.py` não reproduz mais o `.docx`

Não é não conformidade com a disciplina; é com o repositório, e é a de maior risco.

Os dois últimos commits que tocaram o documento — `cd30dbe` e `3791e1a` — alteram apenas `dist/projeto-pcc.docx`, sem tocar em `tools/build_pcc.py`.
O gerador ficou parado em `cc15d7b`: ele ainda tem o título antigo ("HARNESSES DE AGENTES DE CODIFICAÇÃO…"), a justificativa antiga, a seção 2 antiga e a lista de referências sem as quatro fontes que `cd30dbe` acrescentou.

Consequência dura: **rodar `python tools/build_pcc.py` hoje desfaz os dois commits.** O script escreve em `dist/projeto-pcc.docx` e sobrescreve tudo.

Por isso as correções de 10 set. 2026 foram aplicadas em `word/document.xml` dentro do `.docx`, e não no gerador.
Reconciliar os dois é trabalho próprio, e enquanto não acontecer o `.docx` é a fonte da verdade e o gerador é uma armadilha.

A paginação também deixou de ser calculável fora do Word: as páginas do sumário vêm da paginação real e precisam ser reconferidas ao abrir o documento.

## 4. Projetos de pesquisa anteriores a 2020 — o que foi possível estabelecer

**NÃO ESTABELECIDO por fonte primária.** Duas monografias pré-2020 de institutos federais em computação foram localizadas (IF Farroupilha, 2018; IFPE) e **nenhuma das duas pôde ser lida**: os PDFs são digitalizações sem camada de texto.
Não há, portanto, corpus verbatim pré-2020 citável nesta revisão. Fica como pendência.

O que existe é uma amostra pré-LLM legítima e à mão: o próprio material da professora.
Ele foi escrito para a disciplina, é humano, e serve de linha de base medida:

| | `projeto-pcc.docx` (prosa) | Aula 5 (professora) |
|---|---|---|
| Sentenças medidas | 171 | 63 |
| Palavras por sentença, média | 17,5 | 10,5 |
| Mediana | 15 | 9 |
| Sentenças curtas | 35% com ≤ 10 palavras | 49% com ≤ 8 palavras |
| Sentenças longas | 7% com ≥ 35 palavras | 2% |

A prosa acadêmica brasileira de graduação é mais curta, mais chã e mais repetitiva do que a do documento.
Ela também **retoma**: "Ou seja", "Quer dizer", "Isto é" — o material da professora faz isso o tempo todo, e o `projeto-pcc.docx` não faz nenhuma vez.
Um autor humano que acabou de escrever uma frase densa a explica de novo mais simples. O documento nunca se explica duas vezes.

## 5. O que se mede na prosa do documento

Contagens sobre os 25 parágrafos de prosa corrida, excluídas tabelas, títulos e listas.

**Medidas em 31 ago. 2026, antes das correções de 10 set.** Estas reescreveram dois parágrafos da justificativa e três da seção 2, e acrescentaram dois. As contagens abaixo, portanto, erram por poucas unidades para baixo no número de parágrafos e para cima nos conectores causais — uma das ocorrências de `porque` saiu com a reescrita da justificativa. A leitura qualitativa não muda; os itens 5 a 7 da seção 6 continuam abertos.

### 5.1 Todo parágrafo fecha justificando

Doze dos vinte e cinco parágrafos terminam em oração subordinada de justificativa, e outros cinco em veredicto sentencioso — dezessete de vinte e cinco.
Os conectores: **`porque` 13 vezes, `já que` 5, `por isso` 6** — 24 marcadores causais explícitos em 25 parágrafos.

Amostra dos fechos:

> ... **porque** é isso que determina quanto do modelo pago cada harness aproveita.
> ... **pois** o oh-my-pi pode recuperar o custo concluindo a tarefa em menos passos.
> **Por isso** a medição ocorre em proxy externo, e o objetivo (6) quantifica essa divergência.
> ... **já que** a variância é a principal ameaça ao desenho.
> ... **porque** a data de entrega ainda não está confirmada.

É o traço mais forte do texto e o mais mecânico. Um LLM treinado a justificar fecha cada unidade com a razão dela.
Um autor humano justifica onde a objeção é previsível e segue adiante onde não é.

Correção: escolha os cinco lugares onde a objeção é real e mantenha a justificativa. Nos outros doze, a afirmação fica de pé sozinha.

### 5.2 Sessenta e um dois-pontos

Média de 2,4 por parágrafo. É a construção "montagem: desfecho", repetida até virar cadência:

> A Camada 1 mede a forma da requisição contra um endpoint simulado que não encaminha nada ao modelo: não consome cota, é determinística e nomeia o mecanismo.
> Quanto à finalidade, esta é uma pesquisa aplicada: seu produto é uma decisão de engenharia que um desenvolvedor pode tomar hoje.

Isoladas, boas frases. Sessenta e uma vezes, um metrônomo.

### 5.3 Dez construções "X, e não Y"

O contraste corretivo, dez ocorrências:

> A contagem vem do proxy, **e não** do relatório do harness nem do gateway...
> A classificação vem do registro do proxy, **e não** do código de saída, que não discrimina desfecho.
> ... **em vez de** ao conjunto indistinto de diferenças entre implementações independentes.

Corrigir um erro que o leitor não cometeu é hábito de modelo de linguagem, e é a assinatura retórica mais reconhecível do documento.
Onde a alternativa errada é óbvia, afirme a certa e pare.

### 5.4 Frases-sentença de fecho

> Um harness que envia 11,4x os bytes não é, por isso, 11,4x pior.
> Se a ordenação entre braços se inverter entre os níveis, a inversão é o resultado.

Aforismo fechando parágrafo é registro de ensaio, não de projeto de pesquisa ABNT.
Ambas dizem coisas verdadeiras e importantes; ditas de outro jeito continuam verdadeiras.

### 5.5 Nenhuma primeira pessoa, nenhuma hesitação

Zero ocorrências de primeira pessoa e zero marcadores de incerteza (`talvez`, `provavelmente`, `parece`, `acredita-se`).
Só um `Espera-se obter`, em toda a Metodologia.

Projeto de pesquisa é documento sobre o que **ainda não** aconteceu, e prosa acadêmica brasileira marca isso: `pretende-se`, `espera-se`, `optou-se por`, `adotou-se`.
O documento fala do experimento futuro com a segurança de quem já o rodou. É o descompasso mais visível entre o que o texto é e como ele soa.

Aqui há um ganho real de honestidade junto com o de estilo: a seção 3 descreve uma matriz que a Camada 2 ainda não executou.

### 5.6 O que já está bom e não deve ser mexido

- A tabela 1 e os números dela. São seus, medidos, datados.
- A seção de limitações. Declarar cinco limitações de partida é raro e é força.
- O parágrafo de organização do trabalho, que faz exatamente o que o gabarito pede.
- As referências, conformes à NBR 6023:2025.

## 6. Ordem de execução sugerida

Por retorno, do maior para o menor:

1. ~~Escrever a **contribuição social e acadêmica** na justificativa (§3.1).~~ Feito em 10 set. 2026.
2. ~~Inserir **citações diretas** no Referencial Teórico (§3.3).~~ Feito em 10 set. 2026: duas diretas curtas, uma direta longa e uma citação de citação.
3. Cortar os **objetivos específicos a uma linha** cada (§3.2).
3b. Reconciliar `tools/build_pcc.py` com o `.docx`, ou aposentá-lo (§3.7). Enquanto os dois divergirem, rodar o gerador destrói o documento.
4. ~~Perguntar à orientadora a data de entrega; resolver os três **marcadores editoriais** e o cronograma (§3.4, §3.5).~~ Data: setembro de 2026; cronograma em SETEMBRO-JANEIRO e marcadores virados em prosa.
5. Reescrever os fechos de parágrafo: manter cinco justificativas, soltar as outras (§5.1).
6. Marcar o tempo futuro na Metodologia e na seção 3 (§5.5).
7. Reduzir dois-pontos e construções "e não" (§5.2, §5.3).

De 1 a 4 o documento fica conforme à disciplina. De 5 a 7 ele passa a soar como alguém escrevendo, e são os itens que só funcionam se for você escrevendo — trocar as palavras por sinônimos reproduz o mesmo padrão com outro vocabulário.

## 7. Pendências

- **NÃO ESTABELECIDO:** nenhum projeto de pesquisa pré-2020 de instituto federal em computação pôde ser lido em texto integral; os dois localizados são digitalizações sem camada de texto. Um corpus verbatim pré-2020 continua desejável como linha de base.
- **NÃO ESTABELECIDO:** se a disciplina exige a seção Recursos Necessários da NBR 15287, que o gabarito omite (§3.6).
- ~~**NÃO ESTABELECIDO:** a data de entrega, que trava o cronograma (§3.5).~~ Estabelecida: setembro de 2026 (mês; o documento não fixa dia).
- A contagem de linhas da justificativa foi verificada por contagem de palavras, não por renderização paginada do `.docx`.

## 8. Fontes

- IFMT. *Template projeto novo3* — `files/Template projeto novo3.pdf`. **No repositório.**
- IFMT. *Aula 2 — Projeto de Conclusão de Curso* — `files/O que é projeto de pesquisa.pdf`. **Cópia local; não foi publicada.**
- IFMT. *Aula 3 — Estrutura do Projeto de Pesquisa* — `files/Estrutura do projeto de pesquisa-aula3.pdf`. **No repositório.**
- IFMT. *Aula 5 — Citações e referências* — `files/Aula 5- Citacoes e referencias.odt`. **No repositório.**
- ABNT NBR 15287, NBR 6023, NBR 10520, NBR 14724, conforme reproduzidas no material acima.
- Medições de prosa: extraídas de `dist/projeto-pcc.docx`, `word/document.xml`, em 31 ago. 2026.
