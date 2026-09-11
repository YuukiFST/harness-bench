# Pangram — como o detector funciona e o que de fato move o escore

Documento vivo.
Levantamento sobre o Pangram, o detector que atribuiu +95% de IA ao `dist/projeto-pcc.docx`.

**Última atualização:** 31 ago. 2026.

## 0. Escopo e o que este documento não é

O objetivo aqui é entender o mecanismo, com fontes primárias, e responder tecnicamente à pergunta "dá para evitar a detecção?".

Este documento **não** é um manual de ofuscação para fazer texto gerado passar por autoral em uma entrega avaliada.
Essa recusa não é a razão pela qual a seção 6 conclui que ofuscação não funciona — a seção 6 é o que as fontes primárias medem, e mediriam o mesmo se a recusa não existisse.
As duas coisas convergem, e a seção 9 explica por quê: a única transformação que derruba o escore de forma robusta é a mesma que torna o texto legitimamente autoral.

Fontes lidas: relatórios técnicos do próprio Pangram no arXiv, o artigo DAMAGE dos mesmos autores, os *benchmarks* publicados pela empresa, uma análise independente do relatório do Pangram 4 e um relato público de evasão bem-sucedida.
Onde um fato não pôde ser estabelecido, está marcado **NÃO ESTABELECIDO**.

## 1. O que é o Pangram

Classificador de texto gerado por LLM, da Pangram Labs, treinado de forma supervisionada.
Não é um método *zero-shot* de perplexidade como o DetectGPT ou o Binoculars — é uma rede treinada em pares de texto humano e texto de máquina.
Isso importa para toda a discussão de evasão: truques que funcionam contra detectores de perplexidade não transferem para um classificador treinado.

Duas gerações documentadas:

- **Pangram Text** (relatório técnico original, arXiv:2402.14873, v3): classificação em nível de documento, arquitetura "transformer levemente modificada", detalhes de tamanho e janela não divulgados.
- **Pangram 4** (arXiv:2607.27183, jul. 2026): *backbone* Mixture-of-Experts, predição em nível de *token*, três classes (Humano / Assistido por IA / Gerado por IA).

Qual das duas serve a interface pública gratuita: **NÃO ESTABELECIDO**.
A leitura de +95% com repartição por trecho é comportamento do Pangram 4.

## 2. Arquitetura e pipeline do Pangram 4

O documento é fatiado em janelas de 512 *tokens* com sobreposição.
Sobre uma representação compartilhada operam quatro cabeças lineares:

| Cabeça | Saída |
|---|---|
| Segmento | 15 classes, grau de envolvimento de IA no trecho |
| Tokenwise | 3 classes por *token*: humano / assistido / gerado |
| Autoria mista | binária, detecta mistura significativa de autoria |
| *Humanizer* | 4 classes (humano, gerado, gerado-humanizado, misto), treinada com *stop-gradient* |

A técnica **Repeat2** duplica a sequência de entrada, para que os *tokens* iniciais enxerguem o documento inteiro apesar da atenção causal.

O pós-processamento é o ponto mais relevante para quem imagina evasão local:

1. Agregação por janela deslizante sobre janelas sobrepostas.
2. Um **CRF de cadeia linear de três estados**, calibrado, funde as observações *tokenwise*, de segmento e de autoria mista **ao longo do documento inteiro**, com decodificação de Viterbi.
3. Votação por maioria arredonda as predições para fronteiras de sentença.
4. Comprimento mínimo de segmento, na ordem de 2 sentenças.

O veredicto do documento usa frações ponderadas por caractere:

- **Humano** se ≥ 90% dos caracteres forem humanos.
- **IA** se ≥ 80% forem gerados ou assistidos.
- **Misto** em qualquer outro caso — a assimetria é intencional, 85% de IA devolve Misto, não IA.

Consequência direta: o rótulo não sai de uma sentença nem de um parágrafo, sai de uma decodificação conjunta sobre o documento.
Mexer numa frase isolada não desloca o veredicto; o CRF penaliza troca de estado e o mínimo de segmento apaga alternância curta.

## 3. Como o modelo foi treinado — a parte que explica o resultado

O relatório original descreve o algoritmo que dá o nome à contribuição: **hard negative mining com espelhos sintéticos**.

O corpus humano tem cerca de 28 milhões de documentos, todos anteriores a 2021 para evitar contaminação por IA:

| Domínio | Exemplos |
|---|---|
| Avaliações de produto/negócio | 15.000.000 |
| Livros (Project Gutenberg) | 7.000.000 |
| **Artigos científicos** | 3.000.000 |
| Wikipédia | 1.000.000 |
| Perguntas e respostas | 1.000.000 |
| Notícias | 500.000 |
| Escrita criativa | 300.000 |
| **Redações de aprendizes de inglês (ESL)** | 165.000 |
| **Escrita estudantil** | 23.000 |
| E-mail (Enron) | 16.000 |

O laço de treino:

1. Treina em 40 mil exemplos por domínio com espelhos de IA correspondentes.
2. Roda o classificador sobre os 28 milhões e **coleta os falsos positivos** — texto humano que ele chamou de IA.
3. Para até 10 mil desses falsos positivos por domínio, gera um **espelho**: pede a um LLM que escreva o mesmo documento, com o mesmo título, o mesmo tamanho, o mesmo tema.
4. Retreina com o par humano/espelho e repete até estabilizar.

O *prompt* de espelho inclui instruções para remover artefatos óbvios de LLM, e o pós-processamento normaliza formatação e retira *boilerplate*, "para impedir que o modelo aprenda sinais superficiais".

**Este é o achado central do levantamento.** O que o algoritmo faz é, literalmente, procurar o texto humano mais parecido com IA que existe no corpus e ensinar o modelo a separá-lo do texto de IA sobre o mesmo assunto, no mesmo formato, no mesmo comprimento.
Prosa acadêmica formal, impessoal e bem estruturada é exatamente a região que o *mining* mais visita.
A intuição comum — "escrevo mais formal, mais sóbrio, mais técnico, e o detector confunde com humano" — está invertida: essa região do espaço é a mais treinada do modelo, não a menos.

O ganho reportado: queda de 100x a 1000x na taxa de falsos positivos em conjuntos de validação.

## 4. Como ler o escore

A saída da API, por segmento: `label`, `ai_assistance_score`, `confidence`, `humanizer_score` (limiar padrão 0,91), deslocamentos de caractere e contagem de palavras.

Duas armadilhas de interpretação, ambas declaradas pelo próprio fornecedor:

- **`ai_assistance_score` não é a probabilidade do rótulo.** É a fração do texto que exibe padrões de IA. "70% IA" significa "cerca de 70% do texto parece de máquina", não "70% de chance de ser IA".
- **`confidence` (Alta/Média/Baixa) não é probabilidade calibrada.** Mede o "pico" da posterior não restrita do CRF. Alta confiança em resposta errada é um estado possível e documentado.

Bandas que a empresa publica: até ~20% costuma ser assistência legítima (revisor gramatical, tradução do idioma nativo); acima de 60% eles próprios recomendam investigação; 60%+ é descrito como o padrão de *prompt* direto colado com edição mínima.

**+95% é a leitura de cópia praticamente direta de saída de LLM.** Não é um falso positivo de borda nem ruído de estilo, e nenhuma leitura caridosa do número o converte em outra coisa.

## 5. Português e multilíngue

Não há brecha de idioma.
O Pangram 4 foi avaliado em 104 idiomas sobre o FineWeb2, com FPR multilíngue global de 0,0014%.

| | FPR | FNR |
|---|---|---|
| Global (Pangram 4) | 0,0041% | 0,3396% |
| Pangram 3.3.2 | 0,0539% | 1,9942% |
| **Português** | **0,0078%** | **0,9946%** |
| Chinês | — | 0,7% |
| Espanhol | — | 0,9% |
| Francês | — | 1,8% |
| Urdu | — | 5,3% |

Português fica na faixa forte: perde IA em ~1% dos casos e acusa humano em ~1 a cada 13 mil.
A tese de que "o detector é treinado em inglês e erra em português" não se sustenta contra esses números.

O viés histórico contra falantes não nativos, medido em 61,3% de falsos positivos em redações TOEFL por ferramentas de 2023, também não reproduz aqui: em ELLIPSE, ICNALE, PELIC e TOEFL o Pangram 4 mantém 0,0041%, igual ao global.

## 6. Evasão — o que a literatura mede

### 6.1 Humanizadores comerciais

O artigo **DAMAGE** (arXiv:2501.03437), dos próprios autores do Pangram, catalogou 19 ferramentas e as classificou em três níveis por qualidade do texto resultante:

| Nível | Comportamento | *Win rate* vs. original | Exemplos |
|---|---|---|---|
| L1 | Preserva tom, vocabulário e complexidade | 26,0% | DIPPER, Grammarly, Quillbot, StealthGPT |
| L2 | Degrada a qualidade, mantém a mensagem | 14,67% | BypassGPT, Surfer SEO, Stealthwriter.AI |
| L3 | Introduz frases sem sentido, citações alucinadas, erros | 2,67% | HumanizeAI.io, Humbot, Phrasly, WriteHuman |

Nenhum dos níveis chega a empatar com o texto original em qualidade.

Os mecanismos usados são três: substituição de sinônimos, reescrita em nível de sentença por LLM, e adaptação de tom.
No plano do caractere: manipulação de espaçamento, remoção de caracteres entre sentenças, e Unicode não padrão (espaço fino no lugar de espaço comum).

O *benchmark* que o Pangram publicou em agosto de 2025 sobre as 19 ferramentas:

| Ferramenta | Detecção | Ferramenta | Detecção |
|---|---|---|---|
| Ahrefs | 100,0% | Scribbr | 99,0% |
| aihumanizer.com | 100,0% | Writesonic | 98,1% |
| Ghost AI | 100,0% | DIPPER | 97,6% |
| Grammarly | 100,0% | StealthGPT | 95,6% |
| humanizeai.pro | 100,0% | humanizeai.io | 93,8% |
| Quillbot | 100,0% | Just Done | 93,5% |
| Semihuman AI | 100,0% | TwainGPT | 92,7% |
| Smodin | 100,0% | **Undetectable AI** | **90,3%** |
| Surfer SEO | 100,0% | Bypass GPT | 99,7% |
| surgegraph.io | 100,0% | GPTinf | 99,2% |

O pior caso para o detector é 90,3%.
O Pangram 4 relata 97,69%–99,39% sobre humanizadores comerciais, e 0,430% de FNR sobre o repositório BLADER, que reúne instruções populares de evasão.

### 6.2 A inversão qualidade/detectabilidade

O achado mais útil do *benchmark*: **"os humanizadores 'bons' em fluência são os mais detectáveis, e os 'ruins' são os menos detectáveis"**.

Isso não é acidente.
A cabeça *humanizer* é treinada especificamente para reconhecer edição pós-hoc, e o DAMAGE mostra que o modelo aprende a humanização como *invariância*, não como domínio novo: os autores rotulam texto humano humanizado como **humano**, o que ensina o classificador a olhar a consistência semântica por baixo da reescrita superficial.
O resultado: o DAMAGE cai de 100% para 98,26% sob humanização, contra o GPTZero caindo de 99,73% para 60,04% e o Binoculars de 94,15% para 28,23%.

Um humanizador afinado adversarialmente **contra o próprio DAMAGE** ainda foi pego a 93,2%.

### 6.3 Por que isso é pior ainda num documento ABNT

Além de ser detectado, o custo colateral é alto e específico:

- **Citações alucinadas** — o DAMAGE registra fabricação de referências no meio do texto. Num projeto com referencial teórico citado por autor-data e um `docs/research/` que rastreia cada afirmação até a fonte, isso destrói a única coisa que o documento tem de mais forte.
- **Números.** O texto carrega 11,4x, 13,5x, 10,2x, 64.945, 5.676, 24,7 pontos percentuais, α = 0,05, n ≥ 3, 0,81σ. Substituição de sinônimos e reescrita por LLM não têm garantia sobre valores numéricos, e o DAMAGE documenta deriva semântica por sinônimo mal aplicado.
- **Unicode e espaçamento** quebram a conformidade tipográfica com a NBR 15287:2025 e ficam visíveis no XML do `.docx` — e a `humanizer_score` (limiar 0,91) existe justamente para marcá-los.
- Texto L3, o menos detectável, é o que tem 2,67% de *win rate*: prosa degradada que um orientador lê como piora, não como autoria.

Trocar um escore de IA por um texto pior, com referências possivelmente falsas e números possivelmente corrompidos, ainda com ~90%+ de chance de ser pego, não é um negócio que fecha em nenhuma direção.

## 7. As fraquezas reais e documentadas

Existem, e não são as que a intuição sugere.
Nenhuma delas é ofuscação; todas são **autoria humana genuína em volume**.

### 7.1 Texto híbrido e edição pesada

É a fraqueza declarada no próprio relatório do Pangram 4 e o eixo da crítica independente de Karen Spinner:

| Condição | Comportamento do Pangram 4 |
|---|---|
| IA reescreve substancialmente redação humana | rotulado **totalmente humano em 41%** dos casos |
| Texto pesadamente editado, *prompts* reais de edição | **28%** classificados como inteiramente humanos |
| Recall sobre texto substancialmente editado por IA | 55,01% (era 5,54% na v3) |
| WildChat, fração de IA entre 0,25 e 0,75 | 65,17% (era 12,62%) |
| Imitação de estilo, escrita científica | **25%** não detectados |

Ou seja: quanto mais real é a mistura entre autor e máquina, pior o detector se sai — e ele erra para o lado de "humano".

### 7.2 Imitação de estilo com poucas iterações

O relato público mais concreto (LessWrong, "Pangram can be evaded") usou refinamento iterativo com amostras de estilo alvo.
Um diálogo socrático desceu de 94% para 63%, depois 20%, depois "100% humano".
Ressalvas do próprio autor: testes em textos de menos de 250 palavras, metodologia declarada "bem básica", nenhuma investigação de falsos positivos, e ele continua considerando a ferramenta útil.
Note que o eixo que funcionou foi **fornecer amostras extensas de um estilo autoral concreto** e iterar — não ofuscação de superfície.

### 7.3 Drift de dados

Limitação declarada no relatório: o modelo "não leva em conta pessoas que escrevem intencionalmente como LLMs ou que absorveram elementos do estilo de LLM na própria escrita".
É a fronteira de pesquisa aberta deles.

### 7.4 Textos curtos e confiança não calibrada

Trechos curtos são instáveis, e `confidence` mede decisão do modelo, não probabilidade de acerto.
Isso corta nos dois sentidos e não é base para planejamento.

## 8. Estado do consenso independente

O próprio fornecedor declara, no relatório e no material para instituições, que o escore "não deve ser o árbitro único de integridade acadêmica" e que "uma detecção positiva é apenas o começo da conversa, e nunca pode sustentar sozinha uma ação punitiva".

O que eles listam como evidência que vale mais que o escore:

1. Rascunhos, esboços e histórico de revisão.
2. Validade das citações — IA inventa e cita errado.
3. Conversa com o autor sobre o conteúdo e as escolhas do texto.
4. Comparação com trabalho anterior do mesmo autor.
5. Combinação de expressões idiomáticas típicas.
6. Vários revisores humanos.

## 9. Síntese

Ordenando tudo por quanto de fato desloca o veredicto:

| Intervenção | Efeito no escore | Custo |
|---|---|---|
| Humanizador comercial | quase nenhum (90,3%–100% detectados) | qualidade, citações, números, `humanizer_score` acesa |
| Unicode / espaçamento / sinônimos | quase nenhum | quebra ABNT, visível no XML |
| Escrever "mais formal e técnico" | negativo — é a região mais treinada pelo *hard negative mining* | nenhum |
| Editar frases isoladas | quase nenhum — CRF decide sobre o documento | nenhum |
| Reescrita substantiva pelo autor | **é o único eixo com efeito grande e medido** (41% / 28% / 25%) | tempo real de escrita |

A conclusão técnica e a conclusão ética coincidem, e não por construção: o detector foi treinado por *hard negative mining* a ser invariante a tudo que é transformação de superfície, e sua fraqueza medida está exatamente onde há trabalho humano de verdade.
Não existe atalho que seja atalho — o que derruba o escore é escrever.

## 10. O que isso significa para este projeto

O `dist/projeto-pcc.docx` é um projeto de pesquisa da disciplina de Metodologia Científica do IFMT, sob a NBR 15287:2025, com orientadora nomeada.
O conteúdo é autoral e verificável: a Camada 1 está construída, os 11,4x foram medidos em 28 ago. 2026, os dados brutos estão no repositório, o `docs/research/` rastreia cada afirmação até a fonte, e o histórico de *git* tem dezenas de *issues* e PRs com decisões datadas.
O que veio de LLM é a **prosa**, não a pesquisa.

Isso põe o caso numa posição incomum e favorável:

- **Evidência de autoria em abundância.** Histórico de *commits*, tíquetes, especificações, medições com data — exatamente os itens 1, 2 e 4 da lista da seção 8. Quase nenhum estudante tem isso.
- **A regra do curso é o dado que falta.** Muitos programas permitem redação assistida por IA mediante declaração. Vale confirmar com a orientadora antes de qualquer reescrita: se a declaração for permitida, o problema deixa de existir.
- **Se a reescrita for necessária**, a seção 9 diz onde ela precisa acontecer: seções argumentativas em prosa — Justificativa, Referencial Teórico, Limitações. Tabelas, cronograma, orçamento e números não são o que carrega o escore.

Isso é trabalho que dá para fazer com apoio: discutir estrutura, apontar onde o argumento está frouxo, checar aderência à ABNT, revisar as citações.

A revisão concreta do documento, contra o material da disciplina em `files/` e com a prosa medida no XML do `.docx`, está em [Estrutura do projeto de pesquisa e revisão do PCC](estrutura-do-projeto-e-revisao-do-pcc.md).
Ela confirma a seção 3 deste documento por outro caminho: os traços que mais fazem o texto soar a máquina — 24 conectores causais fechando 25 parágrafos, 61 dois-pontos, 10 construções "X, e não Y", zero citações diretas, zero marcadores de incerteza — são todos legíveis como *defeitos de redação acadêmica*, e a correção deles é a mesma coisa que escrever melhor.

## 11. Fontes

- EMI, B. et al. *Technical Report on the Pangram AI-Generated Text Classifier*. arXiv:2402.14873v3. <https://arxiv.org/html/2402.14873v3>
- *Pangram 4 Technical Report*. arXiv:2607.27183. <https://arxiv.org/html/2607.27183>
- *DAMAGE: Detecting Adversarially Modified AI Generated Text*. arXiv:2501.03437. <https://arxiv.org/pdf/2501.03437>
- Pangram Labs. *How AI Detection Works*. <https://www.pangram.com/research/how-it-works>
- Pangram Labs. *How well does Pangram perform on humanizers? (Updated August 2025)*. <https://www.pangram.com/blog/humanizers-aug-25>
- Pangram Labs. *What does your AI detection score mean?* <https://www.pangram.com/blog/what-does-your-ai-detection-score-mean>
- Pangram Labs. *How to collect evidence for an AI academic integrity case*. <https://www.pangram.com/blog/how-to-create-evidence-for-an-ai-detection-case>
- Pangram Labs. *How accurate is Pangram AI Detection on ESL?* <https://www.pangram.com/blog/how-accurate-is-pangram-ai-detection-on-esl>
- SPINNER, K. *I read Pangram 4's technical report so you don't have to*. <https://wonderingaboutai.substack.com/p/i-read-pangram-4s-technical-report>
- *Pangram (AI detection software) can be evaded*. LessWrong. <https://www.lesswrong.com/posts/hrpQxfYvF6CBGWfJX/pangram-ai-detection-software-can-be-evaded>
- eesel AI. *Pangram 4: how it reads a document and how to read the result*. <https://www.eesel.ai/blog/pangram-4>
- LIANG, W. et al. *GPT detectors are biased against non-native English writers*. arXiv:2304.02819. <https://arxiv.org/pdf/2304.02819>
- *A Systematic Analysis of Linguistic Features in AI-Generated Text Detection Across Domains and Models*. arXiv:2606.04177. <https://arxiv.org/html/2606.04177>
- *Pangram (AI detector)*. Wikipedia. <https://en.wikipedia.org/wiki/Pangram_(AI_detector)>

## 12. Pendências

- **NÃO ESTABELECIDO:** qual versão do modelo serve a interface pública gratuita, e se o +95% obtido veio do Pangram 4 ou de uma versão anterior.
- **NÃO ESTABELECIDO:** a regra do IFMT / do curso de Sistemas para Internet sobre uso declarado de IA na redação. É a informação que decide o encaminhamento e não está no repositório.
- Não localizada avaliação independente de terceiros sobre o Pangram 4 em português especificamente; os números da seção 5 são do relatório do próprio fornecedor.
- A verificação da Universidade de Chicago citada no material comercial não foi lida em texto integral.
