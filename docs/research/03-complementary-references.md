# Ticket #3 — Referências complementares para o referencial teórico

Levantamento de fontes primárias para o *referencial teórico* do projeto de pesquisa sobre *agent harnesses* para agentes de codificação.
Problema de pesquisa: com o modelo fixo, quanto o *harness* altera custo e desempenho?

Os dois artigos-âncora (arXiv 2604.25850, *Agentic Harness Engineering*; arXiv 2605.18747, *Code as Agent Harness*) pertencem ao ticket #2 e não são cobertos aqui.

Data de acesso adotada em todas as entradas: **7 ago. 2026**.

Convenção de formatação: ABNT NBR 6023, convenção em português.
Toda afirmação bibliográfica abaixo tem a URL da fonte primária consultada.
Onde um dado não pôde ser confirmado na fonte que o detém, ele está marcado como **[NÃO VERIFICADO]** em vez de ser preenchido por suposição.

---

## Três achados que afetam o projeto antes da escrita

### 1. Existe um artigo que enuncia exatamente a tese do projeto

O preprint arXiv:2605.23950, *Stop Comparing LLM Agents Without Disclosing the Harness*, sustenta a chamada "Binding Constraint Thesis": em tarefas de horizonte longo, com modelos de fronteira comparáveis, o *harness* de execução é determinante mais forte do desempenho do que o modelo que ele encapsula.
Ele traz ainda um protocolo de decomposição de variância entre efeito do *harness* e efeito do modelo.
Isso é o núcleo do referencial e provavelmente também um insumo de metodologia; ver seção 1.3.

Fonte: <https://arxiv.org/abs/2605.23950>.

### 2. Quatro das normas ABNT que o projeto usa foram atualizadas

Em agosto de 2026, estão desatualizadas as versões NBR 15287:2011, NBR 14724:2011, NBR 6023:2018 e NBR 10520:2002.
As vigentes são NBR 15287:2025 (3ª edição, 18 mar. 2025), NBR 14724:2024 (4ª edição, com errata em abr. 2025), NBR 6023:2025 (3ª edição, 21 maio 2025) e NBR 10520:2023.
A maioria dos modelos de TCC em circulação ainda segue as versões antigas, de modo que copiar um modelo pronto introduz divergência em relação à norma vigente.
Se o regulamento do curso ainda exigir as versões antigas, siga o regulamento e registre a divergência no texto.

Fontes: <https://bibliotecas.ufu.br/acontece/2025/06/atualizacao-da-norma-de-apresentacao-de-projeto-de-pesquisa-abnt-nbr-15287> e <https://biblioteca.ufes.br/normalizacao>; detalhamento na seção 2.2.

### 3. A NBR 10520:2023 mudou a forma das citações no corpo do texto

O sobrenome nas citações passou a levar apenas a inicial maiúscula.
Escreva `(Prodanov; Freitas, 2013, p. 51)` e não `(PRODANOV; FREITAS, 2013, p. 51)`.
A caixa-alta permanece apenas nas entradas da lista de referências, que seguem a NBR 6023 — é por isso que as referências deste documento estão em caixa-alta e os exemplos de citação, não.
Na mesma revisão, o recuo de 4 cm em citações longas passou de obrigatório a recomendado e o `et al.` para quatro ou mais autores tornou-se opcional.

Fonte: seção 2.2 abaixo, com a verificação completa.

---

## Frente 1 — Técnica

### 1.1 Benchmarks

#### SWE-bench (artigo original)

- **Referência ABNT:** JIMENEZ, Carlos E.; YANG, John; WETTIG, Alexander; YAO, Shunyu; PEI, Kexin; PRESS, Ofir; NARASIMHAN, Karthik. **SWE-bench**: can language models resolve real-world GitHub issues? arXiv:2310.06770, 2023. Trabalho apresentado na International Conference on Learning Representations (ICLR), 2024. Disponível em: https://arxiv.org/abs/2310.06770. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2310.06770> (site oficial: <https://www.swebench.com/>)
- **Usado para:** definir o benchmark canônico de agentes de código sobre *issues* reais (2.294 tarefas, 12 repositórios Python) e estabelecer a unidade de medida de desempenho na comparação entre *harnesses* com modelo fixo.
- **Verificação:** página de resumo do arXiv consultada; título, os sete autores na ordem, identificador, ano de submissão (2023) e campo de comentários indicando ICLR 2024 conferidos. A contagem de 2.294 tarefas e o resultado de 1,96% para o Claude 2 constam do resumo.

#### SWE-bench Verified

- **Referência ABNT:** SWE-BENCH. **SWE-bench Verified**: a human-filtered subset of 500 instances from SWE-bench. 2024. Disponível em: https://www.swebench.com/verified.html. Acesso em: 7 ago. 2026.
- **Referência ABNT (anúncio do fabricante):** OPENAI. **Introducing SWE-bench Verified**. 2024. Disponível em: https://openai.com/index/introducing-swe-bench-verified/. Acesso em: 7 ago. 2026.
- **URL:** <https://www.swebench.com/verified.html>
- **Usado para:** justificar o uso do subconjunto validado por humanos (500 instâncias) em vez do SWE-bench integral, de modo que ruído de enunciado ou testes injustos não sejam confundidos com efeito do *harness*.
- **Verificação:** a página oficial swebench.com/verified.html foi consultada diretamente e confirma "a human-filtered subset of 500 instances from SWE-bench, created in collaboration with OpenAI", além de apontar o anúncio da OpenAI. O domínio openai.com retorna HTTP 403 a acesso automatizado, de modo que a URL foi confirmada por link a partir da fonte oficial, mas o **texto do anúncio não foi lido diretamente**. Consequentemente, os números de uso corrente (data de 13 ago. 2024; 93 desenvolvedores anotadores; 38,3% de enunciados subespecificados) **[NÃO VERIFICADO]** — confirme-os no navegador antes de citar.

#### Terminal-Bench

- **Referência ABNT:** MERRILL, Mike A. et al. **Terminal-Bench**: benchmarking agents on hard, realistic tasks in command line interfaces. arXiv:2601.11868, 2026. Disponível em: https://arxiv.org/abs/2601.11868. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2601.11868> · site oficial: <https://www.tbench.ai/> · repositório: <https://github.com/harbor-framework/terminal-bench>
- **Usado para:** benchmark de agentes em ambiente de terminal (89 tarefas, 16 categorias); é o mais sensível ao *harness* porque mede o agente operando o ambiente de execução, e não apenas gerando código.
- **Verificação:** página do arXiv consultada; título exato, primeiro autor Mike A. Merrill, **85 autores no total**, ano 2026, categorias cs.SE/cs.AI, 89 tarefas e a observação de que modelos de fronteira pontuam menos de 65% conferidos. A lista de autores extensa justifica `et al.` conforme NBR 6023. O BibTeX recomendado no README indica `booktitle={The Fourteenth International Conference on Learning Representations}, year={2026}` (ICLR 2026), mas a **página do OpenReview exige verificação de navegador e não pôde ser lida, e o campo de comentários do arXiv não menciona a conferência [NÃO VERIFICADO]** — se citar como ICLR 2026, a base é o BibTeX do próprio projeto. Nota: o repositório `laude-institute/terminal-bench` redireciona para `harbor-framework/terminal-bench`; o site oficial declara-se "a stanford x laude collaboration" e lista as versões 1.0 (80 tarefas), 2.0 (89), 2.1, 3 e Terminal-Bench Science. Fixe no texto a versão efetivamente usada no experimento.

#### Aider polyglot benchmark

- **Referência ABNT:** AIDER. **Aider LLM leaderboards**. 2024. Disponível em: https://aider.chat/docs/leaderboards/. Acesso em: 7 ago. 2026.
- **Referência ABNT (post de lançamento):** AIDER. **o1 tops aider's new polyglot leaderboard**. 21 dez. 2024. Disponível em: https://aider.chat/2024/12/21/polyglot.html. Acesso em: 7 ago. 2026.
- **URL:** <https://aider.chat/docs/leaderboards/>
- **Usado para:** benchmark multilinguagem de edição de código e, sobretudo, artefato que **já reporta custo em dólares ao lado da acurácia** — precedente direto para o par custo-desempenho que o projeto quer medir.
- **Verificação:** ambas as páginas oficiais consultadas. Confirmados: "225 challenging Exercism coding exercises across C++, Go, Java, JavaScript, Python, and Rust"; seleção a partir de 697 problemas, mantendo os 225 resolvidos por três ou menos de sete modelos de topo; distribuição por linguagem (C++ 26, Go 39, Java 47, JavaScript 49, Python 34, Rust 30); e o *leaderboard* exibindo percentual correto, custo e métricas de formato de edição.

#### SWE-Lancer

- **Referência ABNT:** MISERENDINO, Samuel; WANG, Michele; PATWARDHAN, Tejal; HEIDECKE, Johannes. **SWE-Lancer**: can frontier LLMs earn $1 million from real-world freelance software engineering? arXiv:2502.12115, 2025. Disponível em: https://arxiv.org/abs/2502.12115. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2502.12115>
- **Usado para:** benchmark que monetiza a tarefa (mais de 1.400 tarefas do Upwork, US$ 1 milhão em pagamentos reais, de US$ 50 a US$ 32.000), ancorando a discussão de custo-benefício em valor econômico e não apenas em tokens.
- **Verificação:** página do arXiv consultada; título, quatro autores, identificador, ano e as cifras do resumo conferidos. Inclui o subconjunto aberto SWE-Lancer Diamond.

### 1.2 Scaffolding / harness (trabalhos anteriores)

#### SWE-agent — Agent-Computer Interface

- **Referência ABNT:** YANG, John; JIMENEZ, Carlos E.; WETTIG, Alexander; LIERET, Kilian; YAO, Shunyu; NARASIMHAN, Karthik; PRESS, Ofir. **SWE-agent**: agent-computer interfaces enable automated software engineering. In: ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS, 37., 2024. *Anais* [...]. 2024. arXiv:2405.15793. Disponível em: https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2405.15793> · anais: <https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html>
- **Usado para:** fonte central do referencial. Formaliza a *Agent-Computer Interface*: agentes baseados em modelos de linguagem são uma nova classe de usuário que se beneficia de interfaces feitas sob medida. Mostra que o desenho da interface — e não o modelo — altera capacidade e comportamento (12,5% pass@1 no SWE-bench contra o estado da arte não interativo anterior).
- **Verificação:** página do arXiv consultada (título, sete autores, identificador, ano). A publicação na NeurIPS 2024 (vol. 37) foi confirmada pela existência da página nos anais oficiais em proceedings.neurips.cc; o campo de comentários do arXiv não menciona a conferência, de modo que a atribuição de *venue* vem dos anais.

#### OpenHands (ex-OpenDevin)

- **Referência ABNT:** WANG, Xingyao et al. **OpenHands**: an open platform for AI software developers as generalist agents. arXiv:2407.16741, 2024. Trabalho apresentado na International Conference on Learning Representations (ICLR), 2025. Disponível em: https://arxiv.org/abs/2407.16741. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2407.16741>
- **Usado para:** exemplo de *harness* aberto e completo (sandbox, navegador, execução de código, coordenação multiagente) que pode ser instanciado com modelos distintos, o que o torna candidato natural a tratamento experimental no desenho "modelo fixo, *harness* variável".
- **Verificação:** página do arXiv consultada; título exato, **24 autores**, submissão em julho de 2024, campo de comentários "Accepted by ICLR 2025", renomeação a partir de OpenDevin e licença MIT conferidos.

#### ReAct

- **Referência ABNT:** YAO, Shunyu; ZHAO, Jeffrey; YU, Dian; DU, Nan; SHAFRAN, Izhak; NARASIMHAN, Karthik; CAO, Yuan. **ReAct**: synergizing reasoning and acting in language models. arXiv:2210.03629, 2022. Trabalho apresentado na International Conference on Learning Representations (ICLR), 2023. Disponível em: https://arxiv.org/abs/2210.03629. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2210.03629>
- **Usado para:** fundamento do laço raciocínio-ação que todo *harness* implementa; base conceitual para tratar o *prompt loop* como variável independente.
- **Verificação:** página do arXiv consultada; título, sete autores, submissão em outubro de 2022 e revisão final em março de 2023 conferidos. O campo de comentários identifica a v3 como *camera-ready* da ICLR, o que sustenta a atribuição ICLR 2023.

#### Reflexion

- **Referência ABNT:** SHINN, Noah; CASSANO, Federico; BERMAN, Edward; GOPINATH, Ashwin; NARASIMHAN, Karthik; YAO, Shunyu. **Reflexion**: language agents with verbal reinforcement learning. arXiv:2303.11366, 2023. Disponível em: https://arxiv.org/abs/2303.11366. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2303.11366>
- **Usado para:** demonstra que memória e autocrítica verbal — componentes de gerenciamento de contexto do *harness* — elevam o desempenho sem alterar pesos do modelo (91% pass@1 no HumanEval contra 80% do GPT-4 anterior). Evidência direta de que o ganho veio do *scaffold*, não do modelo.
- **Verificação:** página do arXiv consultada; título, seis autores, identificador, ano e números do resumo conferidos. A página **não declara publicação em NeurIPS 2023 nem em outra conferência [NÃO VERIFICADO]** — cite como preprint ou confirme nos anais antes de atribuir *venue*.

#### Claude Code (harness comercial, artefato primário)

- **Referência ABNT:** ANTHROPIC. **Claude Code overview**. 2026. Disponível em: https://code.claude.com/docs/en/overview. Acesso em: 7 ago. 2026.
- **URL:** <https://code.claude.com/docs/en/overview>
- **Usado para:** descrição oficial de um *harness* de linha de comando e de seus componentes de contexto e ferramentas, operacionalizando concretamente o que o projeto define como *harness*.
- **Verificação:** página consultada após redirecionamento 301 a partir de docs.claude.com; descrição oficial conferida no texto da página. É documentação de fabricante, não obra revisada por pares — declare isso ao citar.

#### "A harness for every task" (fonte de fabricante que emprega o termo)

- **Referência ABNT:** SHIHIPAR, Thariq; BIDASARIA, Sid. **A harness for every task**: dynamic workflows in Claude Code. Anthropic, 2 jun. 2026. Disponível em: https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code. Acesso em: 7 ago. 2026.
- **URL:** <https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code>
- **Usado para:** fonte primária de fabricante que emprega explicitamente o termo *harness* e sustenta que ele é ajustável por tarefa; útil na delimitação terminológica do objeto de estudo, já que o termo ainda não está consolidado na literatura revisada por pares.
- **Verificação:** página consultada; título, os dois autores, data e as citações conferidos. Post institucional de fabricante — use apenas como fonte de definição prática, sempre marcado como tal.

### 1.3 Modelo versus scaffold: custo e desempenho

Esta é a subseção mais próxima do problema de pesquisa e deve receber o maior peso no referencial.

#### Stop Comparing LLM Agents Without Disclosing the Harness — a fonte mais alinhada ao problema

- **Referência ABNT:** ZHANG, Yunbei; WANG, Janet; GE, Yingqiang; XU, Weijie; HAMM, Jihun; REDDY, Chandan K. **Stop comparing LLM agents without disclosing the harness**. arXiv:2605.23950, 2026. Disponível em: https://arxiv.org/abs/2605.23950. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2605.23950>
- **Usado para:** sustenta a hipótese exata do projeto por meio da "Binding Constraint Thesis" — em tarefas de horizonte longo com modelos de fronteira comparáveis, o *harness* de execução é determinante mais forte do desempenho do que o modelo encapsulado. Fornece ainda o protocolo de decomposição de variância entre efeito do *harness* e efeito do modelo, aproveitável diretamente na metodologia.
- **Verificação:** página do arXiv consultada; título, seis autores, submissão em 7 de maio de 2026, categorias cs.AI/cs.SE e teor do resumo conferidos. Os **valores numéricos por *harness* que circulam em buscas (por exemplo, 9,5 pontos entre dois *harnesses*, ou 69,7% para 77,0% no Terminal-Bench 2) não constam do resumo [NÃO VERIFICADO]** — leia o PDF antes de reproduzir qualquer número.

#### AI Agents That Matter

- **Referência ABNT:** KAPOOR, Sayash; STROEBL, Benedikt; SIEGEL, Zachary S.; NADGIR, Nitya; NARAYANAN, Arvind. **AI agents that matter**. arXiv:2407.01502, 2024. Disponível em: https://arxiv.org/abs/2407.01502. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2407.01502>
- **Usado para:** fundamenta a métrica do projeto. Argumenta que a avaliação de agentes tem foco estreito em acurácia e ignora custo, defende a otimização conjunta das duas métricas e mostra que isso reduz muito o custo mantendo a acurácia. Também critica a ausência de *holdout* e de padronização, o que serve de base ao desenho experimental.
- **Verificação:** página do arXiv consultada; título, os cinco autores, identificador, data de submissão (1 jul. 2024), categoria cs.LG e as teses do resumo conferidos.

#### Large Language Monkeys

- **Referência ABNT:** BROWN, Bradley; JURAVSKY, Jordan; EHRLICH, Ryan; CLARK, Ronald; LE, Quoc V.; RÉ, Christopher; MIRHOSEINI, Azalia. **Large language monkeys**: scaling inference compute with repeated sampling. arXiv:2407.21787, 2024. Disponível em: https://arxiv.org/abs/2407.21787. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2407.21787>
- **Usado para:** demonstra ganho por computação em tempo de inferência **com o modelo fixo**: no SWE-bench Lite, o desempenho sobe de 15,9% para 56% ao passar de uma para 250 amostras. Evidência quantitativa de que a estratégia do *harness* domina o resultado e de que o custo é a variável de troca.
- **Verificação:** página do arXiv consultada; título, os sete autores, identificador, data de submissão e os números do resumo (15,9% para 56%, 250 amostras, escala log-linear ao longo de quatro ordens de grandeza) conferidos.

#### Os limites do escalonamento por reamostragem

- **Referência ABNT:** STROEBL, Benedikt; KAPOOR, Sayash; NARAYANAN, Arvind. **The limits of inference scaling through resampling**. arXiv:2411.17501, 2024. Disponível em: https://arxiv.org/abs/2411.17501. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2411.17501>
- **Usado para:** contraponto necessário ao anterior. Com verificadores imperfeitos, reamostrar deixa de compensar: o número ótimo de tentativas costuma ficar abaixo de dez e modelos fracos não alcançam modelos fortes apenas por inferência. Delimita até onde o *harness* pode compensar o modelo, que é exatamente a pergunta do projeto.
- **Verificação:** página do arXiv consultada; título atual, três autores, identificador, submissão em 26 de novembro de 2024 e conclusões conferidos. **Atenção:** o artigo circulou antes sob o título "Inference Scaling fLaws" — cite o título atual da página do arXiv.

#### The Shift from Models to Compound AI Systems

- **Referência ABNT:** ZAHARIA, Matei; KHATTAB, Omar; CHEN, Lingjiao; DAVIS, Jared Quincy; MILLER, Heather; POTTS, Chris; ZOU, James; CARBIN, Michael; FRANKLE, Jonathan; RAO, Naveen; GHODSI, Ali. **The shift from models to compound AI systems**. Berkeley Artificial Intelligence Research (BAIR) Blog, 18 fev. 2024. Disponível em: https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/. Acesso em: 7 ago. 2026.
- **URL:** <https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/>
- **Usado para:** enquadramento conceitual da separação entre modelo e sistema. Sustenta que resultados de ponta vêm de sistemas compostos, não de modelos monolíticos, e que o desenho de sistema costuma ter melhor relação custo-benefício do que escalar o treinamento — o que justifica teoricamente tratar o *harness* como variável independente.
- **Verificação:** post oficial do BAIR consultado; título, os 11 autores, data de publicação e a tese central conferidos. É blog acadêmico institucional (Berkeley), não obra revisada por pares — declare isso no texto.

#### The SWE-Bench Illusion (validade do benchmark)

- **Referência ABNT:** LIANG, Shanchao; GARG, Spandan; ZILOUCHIAN MOGHADDAM, Roshanak. **The SWE-Bench illusion**: when state-of-the-art LLMs remember instead of reason. arXiv:2506.12286, 2025. Disponível em: https://arxiv.org/abs/2506.12286. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2506.12286>
- **Usado para:** ameaça à validade a discutir na metodologia. Parte do desempenho no SWE-bench Verified pode vir de memorização e contaminação, com até 76% de acerto na identificação do arquivo com defeito apenas pelo enunciado, contra 53% fora do benchmark. Reforça a decisão de manter o modelo fixo, já que a contaminação afeta igualmente todos os *harnesses* testados.
- **Verificação:** página do arXiv consultada; título, três autores, identificador, submissão em 14 de junho de 2025 e os números do resumo conferidos.

#### Towards a Science of Scaling Agent Systems

- **Referência ABNT:** KIM, Yubin et al. **Towards a science of scaling agent systems**. arXiv:2512.08296, 2025. Disponível em: https://arxiv.org/abs/2512.08296. Acesso em: 7 ago. 2026.
- **URL:** <https://arxiv.org/abs/2512.08296>
- **Usado para:** estudo de ablação em larga escala do *scaffold* (260 configurações, 6 benchmarks, 5 arquiteturas mono e multiagente, múltiplas famílias de modelo), com variação de +80,8% a −70,0% conforme o alinhamento entre tarefa e arquitetura. Serve de modelo de referência para o desenho experimental do projeto.
- **Verificação:** página do arXiv consultada; título, **20 autores** (primeiro: Yubin Kim), identificador, submissão em 9 de dezembro de 2025, categoria cs.AI e os números do resumo conferidos.

### 1.4 Fonte técnica em português

- **Referência ABNT:** PINHEIRO, Francisco Victor da S.; COUTINHO, Emanuel F.; SILVA, Marcelo M. da; CARVALHO, Sidartha A. Lobo de; ANDRADE, Rossana M. C. Investigando a integração estrutural de LLMs em ecossistemas de software: um estudo com modelagem SSN. In: SIMPÓSIO BRASILEIRO DE ENGENHARIA DE SOFTWARE, 39., 2025, Recife. *Anais* [...]. Porto Alegre: SBC, 2025. p. 832-838. DOI: 10.5753/sbes.2025.11601. Disponível em: https://sol.sbc.org.br/index.php/sbes/article/view/37066. Acesso em: 7 ago. 2026.
- **URL:** <https://sol.sbc.org.br/index.php/sbes/article/view/37066>
- **Usado para:** ancoragem nacional. Evidencia que a comunidade brasileira de engenharia de software já investiga LLMs atuando como agentes em ecossistemas de código, situando o projeto em relação à produção da SBC.
- **Verificação:** registro oficial na SBC OpenLib consultado; título, os cinco autores, evento (XXXIX SBES, Recife, 2025), páginas 832-838, DOI e editora conferidos.

**Ressalva sobre a lacuna nacional.**
Buscas dirigidas ao repositório SOL/SBC por trabalhos brasileiros especificamente sobre *harness* de agentes, avaliação de agentes de codificação ou comparação custo-desempenho com modelo fixo não retornaram resultado.
Até onde foi verificado, não há fonte primária brasileira sobre o recorte exato do projeto, o que é argumento a favor da relevância da pesquisa.
Ao usar isso na justificativa, qualifique a afirmação como "não localizada nos anais da SBC até ago. 2026" em vez de afirmar inexistência.

---

## Frente 2 — Metodológica

### 2.1 Obras de metodologia científica

#### Prodanov & Freitas — a base da classificação da pesquisa

- **Referência ABNT:** PRODANOV, Cleber Cristiano; FREITAS, Ernani Cesar de. **Metodologia do trabalho científico**: métodos e técnicas da pesquisa e do trabalho acadêmico. 2. ed. Novo Hamburgo: Feevale, 2013. Disponível em: https://www.feevale.br/Comum/midias/0163c988-1f5d-496f-b118-a6e009a7a2f9/E-book%20Metodologia%20do%20Trabalho%20Cientifico.pdf. Acesso em: 7 ago. 2026.
- **URL:** <https://www.feevale.br/Comum/midias/0163c988-1f5d-496f-b118-a6e009a7a2f9/E-book%20Metodologia%20do%20Trabalho%20Cientifico.pdf>
- **Usado para:** obra de referência para a taxonomia completa da pesquisa — natureza (básica ou aplicada), objetivos (exploratória, descritiva, explicativa), abordagem (quantitativa ou qualitativa) e procedimentos técnicos (experimental, bibliográfica e outros). É a fonte que sustenta a classificação declarada do projeto.
- **Verificação:** página institucional da Editora Feevale consultada, confirmando título, subtítulo, ordem dos autores, 2ª edição, ISBN 978-85-7717-158-3, 276 páginas e o link de download do e-book, que resolve para um PDF de 5,2 MB. O PDF baixado veio em fluxo comprimido e não pôde ser lido diretamente, de modo que o **ano de 2013 foi confirmado por fontes cruzadas** — registro no Internet Archive, cujo editor consta como "Associação Pró-Ensino Superior em Novo Hamburgo", mantenedora da Feevale, e repositórios institucionais (UFPE, UFSC). A cidade Novo Hamburgo corresponde à sede da Feevale. A página do editor não exibe o ano explicitamente, daí a confirmação cruzada.

#### Gil — elaboração do projeto de pesquisa

- **Referência ABNT (edição recomendada):** GIL, Antonio Carlos. **Como elaborar projetos de pesquisa**. 7. ed. São Paulo: Atlas, 2022.
- **Referência ABNT (edição mais recente):** GIL, Antonio Carlos. **Como elaborar projetos de pesquisa**. 8. ed. São Paulo: Atlas, 2026.
- **URL:** sem URL de acesso livre; 7. ed. em <https://minhabiblioteca.com.br/catalogo/livro/84609/como-elaborar-projetos-de-pesquisa/> e 8. ed. em <https://www.grupogen.com.br/livro-como-elaborar-projetos-de-pesquisa-antonio-carlos-gil-editora-atlas-9786559777860>
- **Usado para:** origem da tipologia de classificação **quanto aos objetivos** (exploratória, descritiva, explicativa) e definição canônica de **pesquisa experimental** — determinar o objeto de estudo, selecionar as variáveis capazes de influenciá-lo e definir as formas de controle e observação dos efeitos. Também sustenta a estrutura do próprio projeto.
- **Verificação:** 7ª edição de 2022 confirmada em catálogo institucional (Minha Biblioteca / Grupo A-GEN), ISBN digital 9786559771639 e impresso 9786559771653. **A 8ª edição, de 2026, foi confirmada na página oficial do Grupo GEN**, ISBN 9786559777860, 224 páginas; essa edição declara incorporar o uso de IA em todas as etapas da pesquisa, o que é diretamente pertinente ao tema do projeto. Edições anteriores (4. ed./2002 e 6. ed./2017) circulam amplamente em PDFs hospedados por universidades, mas são digitalizações de edições antigas — não as cite como se fossem a versão em catálogo. Se não tiver acesso físico à 8ª, cite a 7. ed./2022, que está plenamente confirmada.

#### Marconi & Lakatos — atenção, são três obras distintas

A confusão entre os três títulos é o erro bibliográfico mais comum na graduação brasileira.
São livros diferentes, com edição, ano e ISBN próprios, e **a ordem de autoria muda entre eles** conforme o registro do editor.

**a) Fundamentos de metodologia científica** — base epistemológica e métodos.

- **Referência ABNT:** MARCONI, Marina de Andrade; LAKATOS, Eva Maria. **Fundamentos de metodologia científica**. 9. ed. São Paulo: Atlas, 2021.
- **URL:** sem URL de acesso livre; página do editor: <https://www.grupogen.com.br/fundamentos-de-metodologia-cientifica>
- **Usado para:** conceituação de ciência, método científico e tipos de método (dedutivo, indutivo, hipotético-dedutivo), além das etapas do trabalho científico. Camada epistemológica, opcional em um projeto de graduação.
- **Verificação:** página oficial do Grupo GEN/Atlas conferida — 9ª edição, 2021, ISBN 9788597026566, 376 páginas, autoria impressa como "Marina de Andrade Marconi e Eva Maria Lakatos" nessa ordem. Catálogos universitários corroboram (UFPel, 9. ed./2021; UFMS registra 9. ed./2022, provável tiragem posterior). Nenhuma edição posterior à 9ª foi localizada; uma 10ª edição seria **[NÃO VERIFICADO]**. A 5ª edição de 2003 circula catalogada na ordem inversa, `LAKATOS; MARCONI` — se citar uma edição antiga, confira a capa dela.

**b) Metodologia científica** — delineamentos de pesquisa e triangulação.

- **Referência ABNT:** LAKATOS, Eva Maria; MARCONI, Marina de Andrade. **Metodologia científica**. 8. ed. São Paulo: Atlas, 2022.
- **URL:** sem URL de acesso livre; página do editor: <https://www.grupogen.com.br/livro-metodologia-cientifica-eva-maria-lakatos-e-marina-marconi-editora-atlas-9786559770656>
- **Usado para:** fundamentar a **abordagem quali-quantitativa**. É a única das três que trata explicitamente de delineamentos qualitativos (estudo de caso, etnografia, análise de conteúdo), quantitativos (ensaio clínico, coorte, *survey*) e da **triangulação de métodos**.
- **Verificação:** página oficial do Grupo GEN/Atlas conferida — 8ª edição, 2022, ISBN 9786559770656, 392 páginas, autoria "Eva Maria Lakatos e Marina Marconi", com Lakatos em primeiro, ordem inversa à de *Fundamentos*.

**c) Metodologia do trabalho científico** — ofício acadêmico e formatação.

- **Referência ABNT:** LAKATOS, Eva Maria; MARCONI, Marina de Andrade. **Metodologia do trabalho científico**. 9. ed. São Paulo: Atlas, 2021.
- **URL:** sem URL de acesso livre; página do editor: <https://www.grupogen.com.br/metodologia-do-trabalho-cientifico>
- **Usado para:** estrutura formal do trabalho acadêmico, leitura e análise de texto, pesquisa bibliográfica e aplicação das normas ABNT de citação e referência.
- **Verificação:** página oficial do Grupo GEN/Atlas conferida — 9ª edição, 2021, ISBN 9788597026535, 264 páginas. **Divergência de ordem de autoria:** a página do editor lista "Eva Maria Lakatos e Marina de Andrade Marconi", enquanto metadados de varejo para o mesmo ISBN invertem a ordem; varejo é fonte fraca. **Confirme na capa física antes de fechar a referência [NÃO VERIFICADO]**; na dúvida, siga a ordem do editor. Note que este título é homônimo do livro de Prodanov & Freitas — são obras diferentes de autores diferentes.

#### Gil — Métodos e técnicas de pesquisa social

- **Referência ABNT:** GIL, Antonio Carlos. **Métodos e técnicas de pesquisa social**. 7. ed. São Paulo: Atlas, 2019.
- **URL:** sem URL de acesso livre; catálogo institucional: <https://minhabiblioteca.com.br/catalogo/livro/80628/m-todos-e-t-cnicas-de-pesquisa-social/>
- **Usado para:** delineamento da pesquisa, operacionalização de variáveis, amostragem e análise de dados; complementa Gil (2022) quando o texto precisar detalhar o controle de variáveis no procedimento experimental e os instrumentos de coleta.
- **Verificação:** catálogo institucional Minha Biblioteca e página de e-book do Grupo GEN conferidos — 7ª edição, 2019, ISBN 9788597020571, 377 páginas; registrada também em catálogos governamentais (ENAP, MDS). A reimpressão de 2024 mantém a 7ª edição. **Não há 8ª edição verificada [NÃO VERIFICADO]**.

#### Severino — Metodologia do trabalho científico

- **Referência ABNT:** SEVERINO, Antônio Joaquim. **Metodologia do trabalho científico**. 24. ed. rev. e atual. São Paulo: Cortez, 2016.
- **URL:** sem URL de acesso livre; página do editor: <https://www.cortezeditora.com.br/educacao/metodologia-do-trabalho-cientifico-1569/p>
- **Usado para:** fundamentação epistemológica do conhecimento científico e diretrizes práticas do trabalho acadêmico. Reforço conceitual, não indispensável à classificação metodológica.
- **Verificação:** página oficial da Cortez Editora conferida — autor, editora, ano 2016, ISBN 9788524924484, 320 páginas; a página não exibe o número da edição, e "24. ed. rev. e atual." foi confirmada por catálogo de livraria e pela loja da Editora UnB, além de acervos universitários. **Não há 25ª edição verificada [NÃO VERIFICADO]**. Muitas ementas citam "Cortez, 2017", que é reimpressão da 24ª edição.

### 2.2 Normas ABNT

As normas são fontes citáveis e sustentam a forma do documento.
Elas são de acesso pago, sem URL pública para o texto integral; as URLs abaixo apontam para o catálogo ABNT/Target ou para anúncios de bibliotecas universitárias, que foram as fontes de verificação.
A lista de normas vigentes do Sistema Integrado de Bibliotecas da UFES (<https://biblioteca.ufes.br/normalizacao>) corrobora todos os anos.

#### NBR 15287 — projeto de pesquisa

- **Referência ABNT:** ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 15287**: informação e documentação — projeto de pesquisa — apresentação. 3. ed. Rio de Janeiro: ABNT, 2025.
- **URL:** registro em catálogo: <https://www.normas.com.br/visualizar/abnt-nbr-nm/24874/abnt-nbr15287-informacao-e-documentacao-projeto-de-pesquisa-apresentacao>; anúncio institucional: <https://bibliotecas.ufu.br/acontece/2025/06/atualizacao-da-norma-de-apresentacao-de-projeto-de-pesquisa-abnt-nbr-15287>
- **Usado para:** norma que rege a estrutura do próprio documento entregue — elementos pré-textuais, textuais e pós-textuais, formatação e apresentação gráfica.
- **Verificação:** catálogo Target/ABNT conferido — versão vigente de 03/2025, 9 páginas, com histórico "03/2025 publicada nova edição / 12/2019 confirmação / 12/2015 confirmação / 03/2011 nova edição / 12/2005 edição". Confirmado de forma independente pela Biblioteca da UFU (3ª edição, 18 mar. 2025, cancela e substitui a de 2011) e pela lista de normas vigentes da Biblioteca do Campus Ananindeua da UFPA. **Mudança prática relevante: na 3ª edição a capa passou a ser opcional e a folha de rosto é obrigatória** — confira o restante da norma antes de montar os pré-textuais. Observação sobre a fonte: a página da Target exibe um aviso genérico de que a norma "foi cancelada", que aparece igualmente em normas comprovadamente vigentes; o rótulo de status na mesma página é "Vigente".

#### NBR 14724 — trabalhos acadêmicos

- **Referência ABNT:** ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 14724**: informação e documentação — trabalhos acadêmicos — apresentação. 4. ed. Rio de Janeiro: ABNT, 2024.
- **URL:** registro em catálogo: <https://www.normas.com.br/visualizar/abnt-nbr-nm/21434/abnt-nbr14724-informacao-e-documentacao-trabalhos-academicos-apresentacao>; anúncio institucional: <https://bibliotecas.ufu.br/acontece/2025/01/atualizacao-da-norma-de-apresentacao-de-trabalhos-academicos-abnt-nbr-14724>
- **Usado para:** regras gerais de formatação (margens, fonte, espaçamento, paginação) que a NBR 15287 compartilha ou remete.
- **Verificação:** catálogo Target/ABNT conferido — versão vigente de 12/2024, 12 páginas, substitui a de 03/2011, com **errata publicada em 04/2025 e edição com errata incorporada na mesma data**. Confirmado pela Biblioteca da UFU (4ª edição, 16 dez. 2024) e por PUCPR, UFRB e UFPA.

#### NBR 6023 — referências

- **Referência ABNT:** ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6023**: informação e documentação — referências — elaboração. 3. ed. Rio de Janeiro: ABNT, 2025.
- **URL:** registro em catálogo: <https://www.normas.com.br/visualizar/abnt-nbr-nm/5262/abnt-nbr6023-informacao-e-documentacao-referencias-elaboracao>
- **Usado para:** formatação de todas as entradas da lista de referências deste levantamento e do projeto final.
- **Verificação:** catálogo Target/ABNT conferido — versão vigente de 05/2025, 68 páginas, ISBN 978-85-07-07757-2, comitê CB-014; versão anterior de 08/2020, que é a versão corrigida da 2ª edição de nov. 2018. Confirmado pela Biblioteca da UFU (3ª edição, 21 maio 2025). A linha do tempo real é 2ª ed. nov./2018, versão corrigida ago./2020 com errata em 2023, e 3ª ed. maio/2025. Se a instituição ainda exigir a de 2018, cite `Rio de Janeiro: ABNT, 2018` e registre a divergência; a estrutura básica das referências não mudou.

#### NBR 10520 — citações

- **Referência ABNT:** ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 10520**: informação e documentação — citações em documentos — apresentação. Rio de Janeiro: ABNT, 2023.
- **URL:** anúncio institucional da Biblioteca da UFU (jul. 2023); lista de vigentes: <https://biblioteca.ufes.br/normalizacao>
- **Usado para:** forma das citações diretas e indiretas no corpo do texto, incluindo o sistema autor-data usado ao longo do referencial teórico.
- **Verificação:** vigente desde 19 de julho de 2023, cancelando e substituindo a NBR 10520:2002. Confirmado pela Biblioteca da UFU, por UFRGS/ICBS, UFMS, IFCE, UNESP e pela lista da UFPA. **Mudança que afeta o texto do projeto: o sobrenome nas citações passou a levar apenas a inicial maiúscula**, de modo que se escreve `(Prodanov; Freitas, 2013, p. 51)` e não a forma em caixa-alta. O recuo de 4 cm em citações longas passou de obrigatório a recomendado, e o `et al.` para quatro ou mais autores tornou-se opcional. A NBR 14724:2024 reforça explicitamente a aplicação da NBR 10520:2023.

#### Normas complementares

- ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6024**: informação e documentação — numeração progressiva das seções de um documento — apresentação. Rio de Janeiro: ABNT, 2012.
- ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6027**: informação e documentação — sumário — apresentação. Rio de Janeiro: ABNT, 2012.
- ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6028**: informação e documentação — resumo, resenha e recensão — apresentação. Rio de Janeiro: ABNT, 2021.

- **Usado para:** numeração das seções (6024), montagem do sumário (6027) e redação do resumo e das palavras-chave (6028).
- **Verificação:** NBR 6024 conferida no catálogo Target/ABNT — vigente desde 02/2012, 4 páginas, cancela a de 2003. NBR 6027:2012 e NBR 6028:2021 confirmadas pela lista de normas vigentes da Biblioteca do Campus Ananindeua da UFPA e por manuais de normalização institucionais (UFSCar, USP/IAU, UFABC). O título da NBR 6028 mudou na versão de 2021 para incluir "resenha e recensão", e a norma fixa o resumo de dissertações e teses entre 150 e 500 palavras. Registro em catálogo da NBR 6024: <https://www.normas.com.br/visualizar/abnt-nbr-nm/5265/abnt-nbr6024-informacao-e-documentacao-numeracao-progressiva-das-secoes-de-um-documento-apresentacao>.

### 2.3 Notas de uso — a quem atribuir cada afirmação metodológica

Para evitar atribuição incorreta na seção de metodologia:

| Afirmação no projeto | Fonte a citar | Observação |
|---|---|---|
| Natureza: pesquisa aplicada | Prodanov & Freitas (2013) | Fonte padrão da graduação brasileira para o eixo "natureza"; livro aberto e gratuito, o que facilita a conferência pelo avaliador. |
| Objetivo: exploratória | Gil (2022 ou 2026) como origem da tipologia; Prodanov & Freitas (2013) como reprodução didática | A tríade exploratória/descritiva/explicativa é de Gil; citar os dois é o uso mais comum e defensável. |
| Abordagem: quali-quantitativa | Lakatos & Marconi, *Metodologia científica* (2022) para a combinação e a triangulação; Prodanov & Freitas (2013) para as definições isoladas | **Não atribua a triangulação a Prodanov & Freitas nem a *Fundamentos*.** Quem trata delineamentos quali e quanti lado a lado é *Metodologia científica*. Este é o erro de atribuição mais provável. |
| Procedimento: experimental | Gil (2022 ou 2026) | Definição canônica: determinar o objeto de estudo, selecionar as variáveis capazes de influenciá-lo e definir as formas de controle e observação. Complemente com Gil (2019) para detalhar controle de variáveis e instrumentos. |
| Estrutura do projeto (problema, objetivos, justificativa) | Gil (2022 ou 2026) | — |
| Forma de apresentação do projeto | ABNT NBR 15287:2025 | Não cite a versão 2011. Capa opcional, folha de rosto obrigatória. |
| Formatação geral (margens, fonte, paginação) | ABNT NBR 14724:2024 | Com a errata de abr. 2025. |
| Referências | ABNT NBR 6023:2025 | Versão 2018 superada em 21 maio 2025. |
| Citações no texto | ABNT NBR 10520:2023 | Use `(Sobrenome, ano)` com inicial maiúscula apenas, não caixa-alta. |
| Numeração de seções, sumário, resumo | NBR 6024:2012, NBR 6027:2012, NBR 6028:2021 | Resumo entre 150 e 500 palavras. |
| Conceito de ciência e de método científico | Marconi & Lakatos, *Fundamentos* (2021), ou Severino (2016) | Camada epistemológica, opcional em projeto de graduação. |
| Reportar custo junto com acurácia | Kapoor et al. (2024) | Ver seção 1.3. |
| Decompor variância entre harness e modelo | Zhang et al. (2026) | Ver seção 1.3. |

Prodanov & Freitas é a fonte que apresenta as quatro dimensões da classificação de forma unificada, o que a torna a citação mais econômica para o parágrafo de classificação da pesquisa.
Gil entra para a origem da tipologia, a definição de pesquisa experimental e a estrutura do projeto.

**Três riscos de erro que valem checagem final no texto:**

1. Confundir as três obras de Marconi e Lakatos — são livros distintos, com edições e ISBN distintos, e a ordem de autoria muda entre eles conforme o registro do editor.
2. Citar NBR 15287:2011, NBR 14724:2011, NBR 6023:2018 ou NBR 10520:2002, todas desatualizadas em agosto de 2026.
3. Citar Gil "2002" ou "2008" com base nos PDFs que circulam em sites universitários — são digitalizações de edições antigas, não a versão em catálogo.

---

## Resumo do que ficou pendente de verificação

1. Data e números do post da OpenAI sobre SWE-bench Verified — o domínio bloqueia requisição automatizada (HTTP 403); a URL foi confirmada por link a partir de swebench.com.
2. Publicação do Terminal-Bench na ICLR 2026 — atribuição vem do BibTeX do próprio repositório; a página do OpenReview exige verificação de navegador.
3. *Venue* do Reflexion — não consta do campo de comentários do arXiv; cite como preprint até confirmar.
4. Valores numéricos por *harness* em arXiv:2605.23950 — não constam do resumo; leia o PDF antes de reproduzir.
5. Cidade e ano na folha de rosto de Prodanov & Freitas — o PDF não foi legível na requisição automatizada; o ano de 2013 foi confirmado por fontes cruzadas, não pela ficha catalográfica.
6. Ordem impressa dos autores em Lakatos & Marconi, *Metodologia do trabalho científico* (9. ed., 2021) — editor e varejo divergem; confira a capa física.
7. Existência de edição posterior à 9ª de *Fundamentos de metodologia científica*, à 7ª de *Métodos e técnicas de pesquisa social* e à 24ª de Severino — nenhuma foi localizada.

Os itens de normas ABNT que constavam como pendentes na primeira versão deste documento foram resolvidos: números de edição, datas, contagens de páginas e histórico de cancelamento estão conferidos no catálogo Target/ABNT e em anúncios de bibliotecas universitárias (seção 2.2).

## Pistas não perseguidas

Dois preprints aparentemente on-topic apareceram em busca e **não foram verificados**, valendo checagem se a seção 1.3 precisar de mais peso:

- *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*, arXiv:2512.10398 **[NÃO VERIFICADO]**.
- *Agent Psychometrics*, arXiv:2604.00594 **[NÃO VERIFICADO]**.
