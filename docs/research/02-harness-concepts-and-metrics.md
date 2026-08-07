# Ticket #2 — Conceitos e métricas de *agent harness* nos dois artigos-âncora

Pesquisa de fontes primárias para o *projeto de pesquisa* sobre custo e desempenho de harnesses de agentes de código com modelo fixo.

Fontes lidas em texto integral (não apenas resumos):

- **AHE** — LIN et al. *Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses*. arXiv:2604.25850. Texto integral lido em <https://arxiv.org/html/2604.25850v4> (v4, versão mais recente) e <https://arxiv.org/html/2604.25850v1>. PDF: <https://arxiv.org/pdf/2604.25850v4>.
- **CaAH** — NING et al. *Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems*. arXiv:2605.18747. Texto integral lido em <https://arxiv.org/html/2605.18747v1>. PDF: <https://arxiv.org/pdf/2605.18747v1>.

Ao longo do documento, citações marcadas como *verbatim* são transcrições literais do texto em inglês.
Trechos não marcados como verbatim são paráfrases.
Onde um fato não pôde ser estabelecido, isso está dito explicitamente com o rótulo **NÃO ESTABELECIDO**.

Aviso de versionamento: o AHE tem quatro versões no arXiv e elas diferem materialmente (lista de autores, seção de limitações, apêndice de métricas).
Tudo abaixo refere-se à **v4**, salvo indicação em contrário.

---

## 1. Definição operacional de *agent harness*

### 1.1 A definição a citar (recomendada)

A definição mais completa e mais citável está no **CaAH, §1 Introduction**, logo após a Figura 1.
Verbatim (<https://arxiv.org/html/2605.18747v1>, §1):

> "An agent harness refers to the software layer that surrounds an LLM with tools, APIs, sandboxes, memory, validators, permission boundaries, execution loops, and feedback channels, thereby turning a stateless model into a functional agent capable of long-running task execution."

Tradução de trabalho sugerida para o texto em português (tradução minha, não do artigo):

> Um *agent harness* é a camada de software que envolve um LLM com ferramentas, APIs, *sandboxes*, memória, validadores, fronteiras de permissão, laços de execução e canais de realimentação, convertendo assim um modelo sem estado em um agente funcional capaz de executar tarefas de longo horizonte.

A frase imediatamente seguinte é a justificativa direta do problema de pesquisa deste projeto.
Verbatim (<https://arxiv.org/html/2605.18747v1>, §1):

> "In this view, the bottleneck of autonomy is not only the reasoning ability of the base model, but also the reliability of the system that connects model outputs to long-horizon actions and persistent states."

O CaAH repete a definição em forma mais curta na abertura do §2, útil como versão condensada.
Verbatim (<https://arxiv.org/html/2605.18747v1>, §2, primeira frase):

> "A harness turns a stateless language model into a functional agent by grounding its outputs in external execution, persistent state, and verifiable feedback."

E uma terceira formulação, na abertura do §3, que enfatiza o harness como sistema de políticas.
Verbatim (<https://arxiv.org/html/2605.18747v1>, §3):

> "Code therefore serves as an executable medium inside the harness, while the harness remains the larger policy-governed system that decides what code may be executed, trusted, persisted, reused, or promoted into future workflows."

### 1.2 A definição complementar do AHE

O AHE dá uma definição mais enxuta e mais operacional, centrada em *editabilidade*.
Verbatim (<https://arxiv.org/html/2604.25850v4>, §1 Introduction, primeiro parágrafo):

> "In practice, such progress relies not only on the underlying language model, but equally on the surrounding engineering components: the system prompt that shapes work style, the tools that expose the file system and shell, and the middleware that controls context, execution, and recovery. This collection of model-external, editable components is collectively referred to as the agent's *harness*."

Ou seja: **harness = o conjunto de componentes externos ao modelo e editáveis**.
Essa é a definição mais útil para este projeto, porque delimita exatamente o que varia entre os braços experimentais quando o modelo é mantido fixo.

O AHE também define a *prática* de engenharia de harness, no §2.1 "Harness Engineering and Evaluation for Coding Agents".
Verbatim (<https://arxiv.org/html/2604.25850v4>, §2.1):

> "Harness engineering refers to the practice of designing the system surrounding the model, including its tools, interfaces, memory, execution constraints, and feedback loops, which together shape what an agent can do on long-horizon tasks."

E uma definição funcional, na sequência do mesmo parágrafo.
Verbatim (<https://arxiv.org/html/2604.25850v4>, §2.1):

> "Concretely, the harness mediates how the model perceives and acts on its environment: it exposes the action and observation interfaces over which tool-augmented reasoning unfolds, custom agent-computer interfaces for repository navigation, file editing, and command execution, as well as sandboxed execution and orchestration support that keep long-horizon runs reproducible."

A primeira frase do resumo do AHE serve como epígrafe curta.
Verbatim (<https://arxiv.org/abs/2604.25850>, Abstract):

> "Harnesses are now central to agent performance, mediating how models interact with tools and execution environments."

### 1.3 A frase que justifica a hipótese central do projeto

Esta é a citação mais importante do conjunto para a seção de justificativa.
Verbatim (<https://arxiv.org/html/2604.25850v4>, §1, segundo parágrafo):

> "Harness design materially shifts task completion on long-horizon coding benchmarks, even with the base model held fixed, making harness engineering a first-class lever for improving coding agents."

O parágrafo continua com uma afirmação que sustenta a escolha de um modelo local pequeno como sujeito de teste.
Verbatim (mesma seção):

> "Moreover, the optimal harness is model-specific: a harness tuned for one base model often underperforms on another and must be re-adapted as the base model changes."

### 1.4 A distinção de três elementos do CaAH (vocabulário a adotar)

O CaAH separa explicitamente três coisas que a literatura costuma confundir, e essa separação é o vocabulário mais diretamente aproveitável por este projeto.
Verbatim (<https://arxiv.org/html/2605.18747v1>, §1):

> "To clarify the role of code in this broader harness view, we distinguish three coupled elements of long-running agentic systems: *model-internal capabilities*, *system-provided harness infrastructure*, and *agent-initiated code artifacts*."

As definições de cada um, verbatim (mesma seção):

> "*Model-internal capabilities* refer to the model's reasoning, perception, planning, simulation, and evaluation abilities."

> "*System-provided harness infrastructure* refers to the predefined tools, APIs, sandboxes, memory systems, validators, permission boundaries, telemetry, and workflows that connect model outputs to external actions and feedback, and forms the main focus of harness engineering."

> "In contrast, *agent-initiated code artifacts*, which remain relatively underexplored, are interactive code objects that agents create, execute, observe, revise, persist, and share within the task execution loop."

Consequência metodológica para este projeto: o desenho experimental mantém *model-internal capabilities* constante (LFM2.5-2.6B Q4_K_M via Ollama) e varia *system-provided harness infrastructure* (OpenCode, PI, Cline, laço ReAct mínimo).
Os *agent-initiated code artifacts* são um efeito observável, não uma variável independente.
Esse é exatamente o recorte que o CaAH nomeia como pouco explorado.

### 1.5 Os componentes concretos de um harness

O AHE dá a enumeração mais operacional da literatura: **sete tipos ortogonais de componente**.
Verbatim (<https://arxiv.org/html/2604.25850v4>, §3.1 "NexAU: an editable, decoupled harness substrate"):

> "We instantiate the harness on the NexAU framework, which exposes seven orthogonal component types as explicit files at fixed mount points in a single workspace: system prompt, tool description, tool implementation, middleware, skill, sub-agent configuration, and long-term memory."

Verbatim, na sequência:

> "The component types are loosely coupled, so adding a middleware does not require editing the system prompt, and adding a skill does not require touching any tool."

Esses sete tipos formam uma boa grade de comparação estrutural entre os quatro braços deste projeto, independentemente do desempenho medido.

O AHE também descreve o *seed* mínimo, que é o análogo direto do controle científico deste projeto.
Verbatim (<https://arxiv.org/html/2604.25850v4>, §3.1):

> "Our seed harness is deliberately minimal: a single shell-execution tool, no middleware, no skills, no sub-agents. A seed already fitted to the target benchmark would contaminate every subsequent edit's attribution, since we could not tell whether a gain came from the loop or from the seed. The minimal seed forces every component AHE adds to earn its place against measured rollouts."

Esse trecho é a justificativa metodológica pronta para o laço ReAct mínimo deste projeto: um controle não-contaminado que obriga cada componente dos harnesses maduros a justificar seu custo.

---

## 2. O enquadramento em três camadas do *Code as Agent Harness*

### 2.1 A frase-tese

Verbatim (<https://arxiv.org/html/2605.18747v1>, Abstract):

> "In emerging agentic systems, code is no longer only a target output. It increasingly serves as an operational substrate for agent reasoning, acting, environment modeling, and execution-based verification. We frame this shift through the lens of agent harnesses and introduce *code as agent harness*: a unified view that centers code as the basis for agent infrastructure."

### 2.2 O parágrafo que introduz as três camadas

Verbatim (<https://arxiv.org/html/2605.18747v1>, Abstract):

> "To systematically study this perspective, we organize the survey around three connected layers. First, we study the *harness interface*, where code connects agents to reasoning, action, and environment modeling. Second, we examine *harness mechanisms*: planning, memory, and tool use for long-horizon execution, together with feedback-driven control and optimization that make harness reliable and adaptive. Third, we discuss *scaling the harness* from single-agent systems to multi-agent settings, where shared code artifacts support multi-agent coordination, review, and verification."

### 2.3 Estrutura completa das três camadas

Os títulos de seção abaixo são transcritos literalmente do sumário do artigo (<https://arxiv.org/html/2605.18747v1>).

**Camada 1 — §2 "Harness Interface: Code for Reasoning, Acting, and Environment Modeling"**

- §2.1 Code for Reasoning — §2.1.1 Program-Delegated Reasoning; §2.1.2 Formal Verification and Symbolic Reasoning Interfaces; §2.1.3 Iterative Code-Grounded Reasoning.
- §2.2 Code for Acting — §2.2.1 Grounded Skill Selection; §2.2.2 Programmatic Policy Generation; §2.2.3 Lifelong Code-Based Agents.
- §2.3 Code for Environment — §2.3.1 Structured World Representations; §2.3.2 Execution-Trace World Modeling; §2.3.3 Code-Grounded Evaluation Environments; §2.3.4 Verifiable Environment Construction.

**Camada 2 — §3 "Harness Mechanisms: Planning, Memory, Tool Use, Control, and Optimization"**

- §3.1 Planning for Agent Harness — §3.1.1 Linear Decomposition Planning; §3.1.2 Structure-grounded Planning; §3.1.3 Search-based Planning; §3.1.4 Orchestration-based Planning.
- §3.2 Memory and Context Engineering for Agent Harness — §3.2.1 Working Memory; §3.2.2 Semantic Memory; §3.2.3 Experiential Memory; §3.2.4 Long-Term Memory; §3.2.5 Multi-Agent Memory; §3.2.6 Context Compaction and State Offloading.
- §3.3 Tool Use for Agent Harness — §3.3.1 Function-Oriented Tool Use; §3.3.2 Environment-Interaction Tool Use; §3.3.3 Verification-Driven Tool Use; §3.3.4 Workflow-Orchestration Tool Use.
- §3.4 Harness Control through the Plan, Execute, and Verify Loop — §3.4.1 From Debugging to Harness-Level Control; §3.4.2 Planning as Contract Formation; §3.4.3 Sandboxed Execution and Permissioned State Transition; §3.4.4 Verification through Deterministic Sensors.
- §3.5 Agentic Harness Engineering for Adaptive Harness Optimization — §3.5.1 Deep Telemetry as the Optimization Substrate; §3.5.2 The Evolution Agent; §3.5.3 Governed Harness Mutation.

**Camada 3 — §4 "Scaling the Harness: Multi-Agent Orchestration over Code"**

- §4.1 Improved Coding Support through Multi-agent Collaboration — §4.1.1 Functional Role Specialization and Human-Guided Planning; §4.1.2 Diverse Interaction Modes Grounded in Shared Program State; §4.1.3 Optimized Workflow Topology for Agentic Coordination.
- §4.2 Execution Feedback and Shared-Harness Synchronization — §4.2.1 Execution Feedback Integration; §4.2.2 Shared-Harness Synchronization.
- §4.3 Position: The Shared Code-Centric Harness Substrate — §4.3.1 Shared Harness Representation; §4.3.2 Harness-State Convergence.
- §4.4 Patterns and Trends.

Observação: o §3.5 do CaAH é uma síntese do próprio artigo AHE, que o CaAH cita como `lin2026agentic` (<https://arxiv.org/html/2605.18747v1>, §3.5).
Os dois artigos-âncora deste ticket, portanto, não são independentes: o survey incorpora o artigo empírico como uma de suas subseções.
Isso deve ser dito no texto do projeto para não superestimar a convergência entre eles.

### 2.4 Definições internas úteis de cada camada

Sobre uso de ferramentas (Camada 2), verbatim (<https://arxiv.org/html/2605.18747v1>, §3.3):

> "Tool usage is the action and observation layer of the code-agent harness. […] From the perspective of code as agent harness, tool use is not merely an auxiliary capability for code generation. It is a governed interface between model intent and external systems. A reliable harness must decide which tools are available, how their schemas are exposed, what permissions each tool receives, where execution happens, how results are sanitized or compacted, and when risky actions require human approval."

Sobre o laço de controle PEV (Camada 2), verbatim (<https://arxiv.org/html/2605.18747v1>, §3.4):

> "Code-as-harness systems require a control loop that turns model intentions into bounded, observable, and revisable state transitions. This subsection frames that loop as Plan–Execute–Verify (PEV): the harness first externalizes an intended change and its validation criteria, then executes the change inside a sandboxed and permissioned environment, and finally verifies the resulting state through deterministic sensors and human-review gates."

O artigo também usa uma metáfora de controle que vale citar, verbatim (<https://arxiv.org/html/2605.18747v1>, §3.5):

> "In this view, the harness acts as a *cybernetic governor*: a control layer that observes the effects of agent actions and regulates subsequent state transitions."

Sobre ReAct especificamente, verbatim (<https://arxiv.org/html/2605.18747v1>, §3.1.1 "Linear Decomposition Planning"):

> "A lightweight precursor of this pattern is ReAct, where the agent interleaves thoughts, actions, and observations in a serial trajectory. In this framework, each reasoning step externalizes the current subgoal and constrains the next action, turning the trajectory itself into a stepwise harness for control."

Essa frase é a autorização textual para tratar o laço ReAct mínimo deste projeto como um harness legítimo (o mais raso possível), e não como "ausência de harness".

Sobre o paradigma CodeAct (Camada 1, interface de ação), verbatim (<https://arxiv.org/html/2605.18747v1>, §5.1.2):

> "rather than emitting JSON tool calls, agents emit Python or JavaScript snippets that compose primitives"

Essa é a distinção central da Camada 1 que serve para classificar os braços: **chamadas de ferramenta estruturadas (JSON/function calling)** versus **código executável como ação (CodeAct)** versus **comandos de shell**.

Ressalva: **NÃO ESTABELECIDO — o CaAH não tem uma seção dedicada a comparar "function calling" com "code-as-action"**, e a expressão "function calling" não aparece no texto. A distinção é feita apenas pela frase do §5.1.2 acima e pelo contraste entre raciocínio puramente textual e raciocínio em código no §2.1.

Por fim, o CaAH define a própria *engenharia de harness* como problema de projeto, no §3.5.
Verbatim (<https://arxiv.org/html/2605.18747v1>, §3.5):

> "Agentic Harness Engineering (AHE) names a harness-level design problem: how to measure and revise the software substrate that turns a language model into a coding agent. Whereas prompt engineering changes instructions and context engineering changes what evidence is presented to the model, AHE treats the operating environment itself as the object of analysis, including tool schemas, planning artifacts, memory policies, retrieval strategies, sandbox configuration, verification sensors, permission tiers, routing rules, multi-agent workflows, and human-review gates."

Essa lista de onze itens é a enumeração mais granular disponível do que constitui um harness e complementa os sete tipos de componente do AHE citados na seção 1.5.

---

## 3. Onde os quatro braços deste projeto se encaixam

### 3.1 Cobertura dos braços na literatura examinada

| Braço | Situação nos dois artigos |
|---|---|
| **OpenCode** | Avaliado como *baseline* no AHE, Tabela 1, rótulo "Human-designed harness"; 47,2 % de pass@1 no Terminal-Bench 2 (<https://arxiv.org/html/2604.25850v4>, §4.2). Referência [2] do AHE: "Anomaly (2025). Opencode: the open source coding agent." **Não é mencionado no CaAH** — a chave de citação `opencodexloop2026` do CaAH §3.5 refere-se a um guia sobre o *laço do Codex aberto* ("open codex loop"), não à ferramenta OpenCode |
| **PI** | **Não mencionado em nenhum dos dois artigos.** Busca em texto integral de ambos: zero ocorrências como nome de harness |
| **Cline** | **Não mencionado em nenhum dos dois artigos.** Busca em texto integral de ambos: zero ocorrências |
| **Laço ReAct mínimo** | O AHE **não usa o termo "ReAct" em nenhum ponto**; seu controle equivalente é o *seed* NexAU₀ (<https://arxiv.org/html/2604.25850v4>, §3.1). O CaAH posiciona ReAct em §3.1.1 como "a lightweight precursor" do planejamento por decomposição linear (<https://arxiv.org/html/2605.18747v1>, §3.1.1) |

Consequência para o desenho experimental: **dois dos quatro braços deste projeto (PI e Cline) não têm cobertura em nenhum dos dois artigos-âncora.**
Isso não é uma falha do projeto — é a lacuna que o projeto ocupa, e deve ser apresentado assim na justificativa.
O único braço com número publicado é o OpenCode, e esse número é de um modelo de fronteira (GPT-5.4), não de um modelo local de 2,6 B.

### 3.2 Classificação nas três camadas do CaAH

Fontes primárias da documentação de cada ferramenta, consultadas para esta classificação, estão citadas célula a célula abaixo.

**Camada 1 — Harness Interface (interface de ação).**

| Braço | Formato de ação | Ferramentas embutidas (nomes documentados) | Fonte |
|---|---|---|---|
| **OpenCode** | Chamadas de ferramenta estruturadas, via Vercel AI SDK | `bash`, `edit`, `write`, `read`, `grep`, `glob`, `lsp` (experimental), `apply_patch`, `skill`, `todowrite`, `webfetch`, `websearch`, `question` | <https://opencode.ai/docs/tools/> |
| **Cline** | **Híbrido, e este é um confundidor crítico deste projeto.** Chamada de ferramenta nativa apenas para uma lista fechada de modelos; os demais caem no formato textual XML legado | `bash`, `editor`, `read_files`, `apply_patch`, `search` (ripgrep), `fetch_web`, `ask_question` | <https://docs.cline.bot/tools-reference/all-cline-tools.md>; <https://cline.bot/blog/cline-v3-35> |
| **PI** | Chamadas de ferramenta estruturadas; conjunto padrão deliberadamente mínimo | Padrão: `read`, `write`, `edit`, `bash`. Disponíveis: mais `grep`, `find`, `ls` | <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md> |
| **ReAct mínimo** | Ações em texto simples analisadas da geração; sem esquema de ferramenta. No artigo original, o espaço de ação é `search[entity]`, `lookup[string]`, `finish[answer]` | A definir por este projeto; o artigo original não tem ferramenta de arquivo, shell ou edição de código | <https://arxiv.org/abs/2210.03629>, §2 e §3.1 |

O ponto sobre o Cline é metodologicamente sério e precisa constar da seção de limitações do projeto.
Verbatim (<https://cline.bot/blog/cline-v3-35>):

> "Native tool calling is currently supported for next-generation models: Claude 4+, Gemini 2.5, Grok 4, Grok Code, and GPT-5 (excluding gpt-5-chat)" … "Models without native support continue using the text-based approach."

O LFM2.5-2.6B não está nessa lista.
Portanto, sob o modelo deste projeto, **o Cline usará o caminho XML textual enquanto OpenCode e PI usarão chamada de ferramenta estruturada**.
Isso é uma diferença de interface (Camada 1) que se confunde com uma diferença de harness, e deve ser declarada explicitamente, não escondida.
Também infla o custo em tokens do Cline por construção, já que o esquema XML vive no *system prompt* a cada chamada.

**Camada 2 — Harness Mechanisms (mecanismos).**

Grade construída sobre as subseções §3.1 a §3.5 do CaAH.

| Mecanismo (CaAH) | OpenCode | Cline | PI | ReAct mínimo |
|---|---|---|---|---|
| §3.1 Planejamento explícito | Sim — agente primário `plan`, com edições em "ask" | Sim — modo "Plan & Act", com modelo configurável por modo | **Não, por decisão de projeto** | Não como módulo; só como *pensamento* em linha |
| §3.2 Memória / regras persistentes | `AGENTS.md` (projeto e global), fallback para `CLAUDE.md` | `.clinerules/`, regras globais, `AGENTS.md`; "Memory Bank" é padrão de usuário, não recurso embutido | `AGENTS.md` / `CLAUDE.md` / `SYSTEM.md` | Nenhuma; só a trajetória na janela de contexto |
| §3.2.6 Compactação de contexto | Sim — chave `compaction` (`auto`, `prune`, `reserved`), comando `/compact` | Sim — "Auto Compact", comandos `/smol` e `/compact` | Sim — `reserveTokens`, `keepRecentTokens`, `/compact` | Não; o artigo trata o limite de contexto como restrição dura |
| §3.3 Uso de ferramenta governado (permissões) | Matriz de permissão mais rica dos três: `allow`/`ask`/`deny` por ferramenta, com padrões glob para bash | Aprovação por uso de ferramenta; CLI `--auto-approve` | **Nenhum por padrão** — a documentação de segurança diz isso explicitamente | Não |
| §3.3 MCP | Sim | Sim | **Não, por decisão de projeto** | Não |
| §3.4 Verificação / rollback (PEV) | `snapshot`, `/undo`, `/redo` | Checkpoints em repositório Git sombra, com três modos de restauração | **Não embutido**; delegado a extensões | Não |
| Skills | Sim (`SKILL.md`) | Sim (`SKILL.md`) | Sim (padrão Agent Skills) | Não |
| Hooks / extensões | Plugins JS/TS com eventos de ciclo de vida | Hooks via `--hooks-dir` e plugins do SDK | Extensões TypeScript com hooks, incluindo `tool_call` bloqueante | Não |

Fontes: <https://opencode.ai/docs/agents/>, <https://opencode.ai/docs/permissions/>, <https://opencode.ai/docs/config/>, <https://opencode.ai/docs/skills/>, <https://opencode.ai/docs/plugins/>; <https://docs.cline.bot/core-workflows/plan-and-act.md>, <https://docs.cline.bot/customization/cline-rules.md>, <https://docs.cline.bot/best-practices/memory-bank.md>, <https://docs.cline.bot/features/auto-compact>, <https://docs.cline.bot/core-workflows/checkpoints.md>, <https://docs.cline.bot/customization/skills.md>; <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/compaction.md>, <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md>, <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md>, <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md>.

A recusa deliberada do PI a três mecanismos inteiros é declarada na seção de filosofia do seu README.
Verbatim (<https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md>):

> "**No MCP.** Build CLI tools with READMEs (see Skills), or build an extension that adds MCP support."
> "**No sub-agents.** There's many ways to do this. Spawn pi instances via tmux, or build your own with extensions, or install a package that does it your way."
> "**No plan mode.** Write plans to files, or build it with extensions, or install a package."

O próprio PI se descreve como harness, o que é conveniente para este projeto.
Verbatim (<https://pi.dev/>):

> "Pi is a minimal agent harness. Adapt Pi to your workflows, not the other way around."

**Camada 3 — Scaling the Harness (escala).**

| Braço | Subagentes / paralelismo | Fonte |
|---|---|---|
| **OpenCode** | Subagentes embutidos `general`, `explore`, `scout`; invocação automática ou por `@mention`; `subagent_depth` para aninhamento. **NÃO ESTABELECIDO: primitiva documentada de execução de N agentes em paralelo** | <https://opencode.ai/docs/agents/> |
| **Cline** | Subagentes com janela de contexto e orçamento de tokens próprios, lançados simultaneamente, somente-leitura e sem aninhamento; "Agent Teams"; sessão de fundo via `--zen` / `cline hub` | <https://docs.cline.bot/features/subagents.md>, <https://docs.cline.bot/cli/agent-teams.md> |
| **PI** | Nenhum. A alternativa documentada é externa ao harness ("Spawn pi instances via tmux"). Sessões em árvore com `/tree`, `/fork`, `/clone` | <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/sessions.md> |
| **ReAct mínimo** | Ausente por construção | <https://arxiv.org/abs/2210.03629> |

### 3.3 O eixo ordinal que emerge da classificação

A grade acima produz uma ordenação natural de profundidade de harness, que é o eixo independente deste estudo:

**ReAct mínimo < PI < OpenCode ≈ Cline**

O PI ocupa uma posição intermediária genuína: quatro ferramentas padrão, sem MCP, sem subagentes, sem modo de planejamento, sem porta de permissão e sem checkpoint, tendo como acréscimos sobre um laço nu apenas a compactação de contexto e as *skills*.
Isso torna o conjunto de braços deste projeto uma escada razoavelmente espaçada, e não quatro pontos aglomerados — o que é uma virtude do desenho e vale ser argumentado no texto.

### 3.4 Viabilidade de execução sobre Ollama (verificada)

Todos os três harnesses de terceiros aceitam um endpoint local compatível com OpenAI.
Isso é pré-requisito do projeto e está confirmado em documentação primária.

| Braço | Chave de configuração | Fonte |
|---|---|---|
| **OpenCode** | `provider.<id>.npm = "@ai-sdk/openai-compatible"` e `provider.<id>.options.baseURL`. A documentação traz um exemplo explícito de Ollama com `http://localhost:11434/v1` | <https://opencode.ai/docs/providers/> |
| **Cline** | Provedor "Ollama" com Base URL `http://localhost:11434`, ou provedor "OpenAI Compatible" com Base URL, modelo, janela de contexto e preços por token | <https://docs.cline.bot/running-models-locally/overview.md>, <https://docs.cline.bot/provider-config/openai-compatible.md> |
| **PI** | `~/.pi/agent/models.json` com `providers.<id>.baseUrl`, `.api = "openai-completions"`, `.apiKey`, `.models[].id`. A documentação nomeia Ollama, LM Studio e vLLM | <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md>, <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md> |

Correção de nomenclatura para o restante do projeto: o PI é o **Pi Coding Agent**, de Mario Zechner, publicado por Earendil Inc.
O repositório canônico atual é <https://github.com/earendil-works/pi> (o pacote fica em `packages/coding-agent`); URLs antigas em `badlogic/pi-mono` redirecionam para lá.
O pacote npm é `@earendil-works/pi-coding-agent`.
Os caminhos de configuração são `~/.pi/agent/settings.json` (global) e `.pi/settings.json` (projeto), com ponto inicial.

Nota semelhante para o OpenCode: `github.com/sst/opencode` **redireciona para `github.com/anomalyco/opencode`**; cite o segundo.

### 3.5 Instrumentação de custo por braço (o risco de execução do projeto)

O projeto mede custo em tokens, então a capacidade de cada harness de reportar tokens é um risco de viabilidade, não um detalhe.

| Braço | O que expõe | Avaliação |
|---|---|---|
| **OpenCode** | `opencode stats` — "token usage and cost statistics", com `--days`, `--models`, `--tools`; `opencode run --format json` | Melhor dos três (<https://opencode.ai/docs/cli/>) |
| **PI** | Rodapé interativo com tokens, cache, custo e uso de contexto; `/session` com mensagens, tokens e custo; sessões em JSONL em `~/.pi/agent/sessions/`. **NÃO ESTABELECIDO: se os eventos de `--mode json` carregam campos de token/custo** | Bom por sessão, incerto por mensagem (<https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/usage.md>) |
| **Cline** | Custo exibido no cabeçalho da tarefa na interface; custos de subagente agregados. **NÃO ESTABELECIDO: se o fluxo `--json` da CLI inclui campos de token/custo** — a referência da CLI não lista nenhuma flag de custo | Pior dos três em modo headless (<https://docs.cline.bot/core-workflows/task-management>) |
| **ReAct mínimo** | Instrumentado por este projeto | Controle total |

**Recomendação metodológica que decorre disso:** não confie na contabilidade de tokens de cada harness.
Meça no **servidor Ollama**, que é o ponto comum a todos os quatro braços e o único instrumento idêntico entre eles.
Isso elimina de uma vez as três incertezas da tabela acima e satisfaz a dimensão *replayability* do CaAH §5.2.1.

**O achado mais valioso para a hipótese do projeto** está na Tabela 1 do AHE (<https://arxiv.org/html/2604.25850v4>, §4.2).
Os três harnesses feitos por humanos, todos rodando **o mesmo modelo base (GPT-5.4)** no **mesmo benchmark (Terminal-Bench 2, 89 tarefas)**, obtiveram:

| Harness projetado por humanos | pass@1 (todas as 89 tarefas) |
|---|---|
| OpenCode | 47,2 % |
| Terminus-2 | 62,9 % |
| Codex | 71,9 % |

Isso é uma dispersão de **24,7 pontos percentuais atribuível exclusivamente ao harness**, com o modelo congelado.
Para comparação, no mesmo artigo a troca do modelo base sob um harness fixo (Figura 3, <https://arxiv.org/html/2604.25850v4>, §4.3) produz linhas de base de 36,5 % (gemini-3.1-flash-lite-preview), 51,7 % (deepseek-v4-flash) e 56,2 % (qwen-3.6-plus).
Essa é evidência publicada, de fonte primária, de que a dispersão entre harnesses sobre o mesmo modelo é da mesma ordem de grandeza que a dispersão entre modelos — exatamente a hipótese deste projeto.
É a citação de abertura mais forte disponível.

---

## 4. Métricas: inventário completo e viabilidade nesta escala

### 4.1 Métricas do AHE (artigo empírico)

O AHE usa **três** métricas quantitativas de comparação de harness, mais dois pares de métricas de qualidade de predição.
Não há nas tabelas nenhuma métrica de tempo de parede, contagem de passos/turnos, contagem de chamadas de ferramenta ou custo em dólares.

| Métrica | O que mede | Unidade | Cálculo | Onde aparece |
|---|---|---|---|---|
| **pass@1** | Taxa média de sucesso binário sobre *k* execuções por tarefa | % | Eq. (1), Apêndice A: média das recompensas binárias sobre todas as tarefas e execuções | Fig. 1, Fig. 3, Tabelas 1, 2 (como "Success rate"), Tabela 3 |
| **Tokens k** | Média por execução de tokens de *prompt* + *completion* em todas as chamadas ao LLM | milhares de tokens (menor é melhor) | Média sobre execuções concluídas | Tabela 2 (metade direita), §4.1, Apêndice A |
| **Succ/Mtok** | Eficiência de custo: sucessos esperados por milhão de tokens | sucessos / 10⁶ tokens (maior é melhor) | Eq. (2), Apêndice A: `pass@1 × 10⁶ / média de tokens por execução` | **Tabela 5, apenas no Apêndice A** |
| **fix-precision / fix-recall** | Se o agente de evolução acerta quais tarefas o próximo round vai corrigir | % | Precisão e revocação padrão sobre as 89 tarefas | Fig. 4 (esquerda), §4.4.2 |
| **regression-precision / regression-recall** | Idem, para regressões previstas | % | Idem | Fig. 4 (direita), §4.4.2 |

Convenções de contagem que valem copiar, verbatim (<https://arxiv.org/html/2604.25850v4>, Apêndice A):

> "Trials that terminate on an infrastructure exception, such as a sandbox crash or API timeout, contribute 0 rather than being dropped, a strictly harsher convention than discarding failures that keeps our numbers comparable to the official terminal-bench leaderboard."

> "For token cost we count every LLM call as prompt plus completion across the rollout and report the mean over completed trials in thousands, denoted Tokens k; infrastructure-aborted trials are excluded to avoid truncated figures. To compare configurations that trade accuracy for cost we combine the two via [Eq. 2] the expected number of successes per million tokens."

Note a assimetria deliberada: falhas de infraestrutura contam como **0** no pass@1, mas são **excluídas** da média de tokens.
Este projeto deve adotar a mesma convenção e declará-la, porque ela evita inflar artificialmente a eficiência de um harness que aborta cedo.

Dado empírico relevante para a hipótese de custo: no SWE-bench-verified (Tabela 2, <https://arxiv.org/html/2604.25850v4>, §4.3), os quatro harnesses sobre **o mesmo modelo** gastaram, em agregado sobre 500 tarefas, 679 / 582 / 526 / 461 mil tokens por tarefa (ACE / TF-GRPO / NexAU₀ / AHE).
Isso é uma variação de **~47 % no custo em tokens atribuível ao harness**, com acurácia praticamente empatada (74,6 % a 75,6 %).
É a demonstração publicada de que harness move custo muito mais do que move acurácia — outra citação central para este projeto.

### 4.2 Dimensões de avaliação propostas pelo CaAH

O CaAH não roda experimentos; ele **propõe** um conjunto de dimensões, e essa proposta é a melhor fonte de vocabulário métrico para este projeto.
Verbatim (<https://arxiv.org/html/2605.18747v1>, §5.2.1 "Harness-Level Evaluation and Oracle Adequacy"):

> "A key open problem is therefore to define harness-level metrics that evaluate the operational substrate itself. These metrics should complement final task accuracy with measurements of execution reliability, feedback quality, context sustainability, safety, coordination, and reproducibility. Useful dimensions include: (i) *trajectory efficiency*, such as number of tool calls, tokens, edits, executions, and wall-clock time; (ii) *verification strength*, such as test coverage, oracle diversity, and rate of false acceptance; (iii) *recovery ability*, such as whether the agent can diagnose and repair failures after invalid actions; (iv) *state consistency*, such as whether memory, repository state, execution traces, and agent beliefs remain synchronized; (v) *safety compliance*, such as whether permissions, sandboxes, and human-approval gates are respected; and (vi) *replayability*, such as whether the full trajectory can be reconstructed and audited from logs and artifacts."

Essas seis dimensões, com os nomes do artigo, formam a grade de métricas mais defensável que este projeto pode adotar, porque vêm nomeadas e justificadas por um survey de 2026 e cobrem custo (i) e reprodutibilidade (vi), que são os eixos do projeto.

### 4.3 Avaliação de reprodutibilidade nesta escala

Contexto de escala: modelo LFM2.5-2.6B (Q4_K_M) servido por Ollama, RTX 3060 12 GB, uma máquina, ~15 tarefas sintéticas, custo monetário zero.

| Métrica / dimensão | Origem | Reprodutível aqui? | Justificativa |
|---|---|---|---|
| **pass@1** | AHE, Eq. (1) | **Sim, com ressalva** | Trivial de calcular. Com ~15 tarefas, a resolução é de ~6,7 pp por tarefa e o intervalo de confiança binomial é largo. Compensar com *k* alto (o AHE usou apenas k=2; sem custo de API, aqui é viável k=10 ou mais) e reportar intervalo de confiança, que o AHE não faz |
| **Tokens k** | AHE, Apêndice A | **Sim** | O melhor eixo deste projeto. Ollama expõe contagens de tokens por requisição, e o custo zero permite repetição. Instrumentar no nível do servidor Ollama, não do harness, pelas razões da seção 3.5 |
| **Succ/Mtok** | AHE, Eq. (2) | **Sim — métrica principal recomendada** | É exatamente a métrica custo-desempenho de que este projeto precisa, já publicada e definida por fonte primária. Combina os dois eixos em um número comparável entre braços |
| **(i) trajectory efficiency** (chamadas de ferramenta, tokens, edições, execuções, tempo de parede) | CaAH, §5.2.1 | **Sim** | Todos são observáveis localmente. Tempo de parede é *mais* informativo aqui do que nos artigos, porque uma única GPU serializa a inferência e o custo real é tempo, não dinheiro. Este é um ponto onde o projeto pode ir além dos dois artigos, que não reportam tempo por execução |
| **(vi) replayability** | CaAH, §5.2.1 | **Sim** | Uma máquina, modelo local congelado, temperatura fixável, *seed* fixável. Reprodutibilidade é a vantagem comparativa deste projeto sobre os dois artigos, que dependem de APIs hospedadas cujos modelos podem mudar sob os pés |
| **(iii) recovery ability** | CaAH, §5.2.1 | **Parcialmente** | Mensurável injetando falhas determinísticas (comando inválido, teste quebrado) e contando se o agente se recupera. Exige tarefas sintéticas desenhadas para isso, o que é compatível com as ~15 tarefas planejadas |
| **(ii) verification strength** | CaAH, §5.2.1 | **Parcialmente** | Cobertura de testes e taxa de falsa aceitação são calculáveis em tarefas sintéticas com oráculo conhecido. "Oracle diversity" exige um conjunto de tarefas maior do que 15 |
| **(iv) state consistency** | CaAH, §5.2.1 | **Não recomendado** | Exige instrumentação profunda e comparável dos quatro harnesses, cujas representações internas de estado diferem. Custo de engenharia desproporcional ao escopo de um projeto de graduação |
| **(v) safety compliance** | CaAH, §5.2.1 | **Não recomendado** | Depende de modelos de permissão que diferem por harness; comparar seria comparar políticas, não desempenho. Fora do problema de pesquisa |
| **fix/regression precision e recall** | AHE, §4.4.2 | **Não aplicável** | Medem a qualidade da auto-predição de um agente de *evolução* de harness. Este projeto compara harnesses fixos, não os evolui |
| **Ablação por componente** (Tabela 3 do AHE) | AHE, §4.4.1 | **Não recomendado como método primário** | Requer harnesses decompostos em arquivos ao estilo NexAU. Os harnesses de terceiros deste projeto não são desmontáveis dessa forma sem modificá-los, o que descaracterizaria o braço |

**Ressalva metodológica herdada do AHE.**
O AHE roda **uma única campanha**, sem desvio-padrão, sem barras de erro e sem intervalo de confiança em nenhuma tabela, com apenas k=2 execuções por tarefa (<https://arxiv.org/html/2604.25850v4>, §4.2 e Apêndice A, Tabela 4).
O próprio artigo abre a seção de limitações reconhecendo, verbatim: *"This work studies a promising but high-variance setting."*
Este projeto, por ter custo marginal zero, **pode e deve** fazer melhor: mais repetições por tarefa e reporte explícito de variância.
Superar os artigos-âncora nesse ponto específico é uma contribuição defensável e barata.

---

## 5. Lacunas e problemas em aberto nomeados pelos próprios artigos

Esta seção é a matéria-prima direta da justificativa do problema de pesquisa.

### 5.1 CaAH §5.2.1 — Avaliação em nível de harness (a lacuna central)

Verbatim (<https://arxiv.org/html/2605.18747v1>, §5.2.1):

> "Evaluation becomes difficult once an LLM is embedded in a code-agent harness. In this setting, performance is no longer determined by the base model alone, but also by the surrounding runtime: which repository files are retrieved, which tools are exposed, how many retries are allowed, whether the agent can execute tests, how failures are summarized, and what verifier decides success. However, most existing evaluations measure end-task success: whether a generated solution passes tests, solves an issue, or completes an interactive task. Such metrics conflate the capabilities of the base model, the quality of the harness, the reliability of tools, the informativeness of feedback, and the difficulty of the environment."

E o fecho da subseção, verbatim:

> "A central bottleneck in this agenda is *oracle adequacy*: whether the evaluator captures the intended task rather than only a narrow executable proxy. The open problem is not merely to build harder benchmarks, but to evaluate the code-agent harness as an executable runtime system."

Essa é a formulação canônica do problema de confundimento harness-versus-modelo, escrita pelo survey, e é exatamente o problema que o desenho deste projeto (modelo congelado, harness variável) resolve por construção.

### 5.2 CaAH §5.2.7 — "Toward a Science of Harness Engineering"

Verbatim (<https://arxiv.org/html/2605.18747v1>, §5.2.7):

> "Taken together, these open problems suggest that code-as-harness research is moving toward a broader science of harness engineering. The central object of study is no longer only the model or the generated program, but the complete closed-loop system: context, memory, tools, execution, feedback, safety, coordination, and evaluation. Progress will require benchmarks that expose long-horizon failures, telemetry that makes trajectories auditable, metrics that isolate harness components, and design principles that allow agents to operate safely in persistent program worlds."

A expressão **"metrics that isolate harness components"** é a frase mais curta e mais citável para justificar a existência deste projeto.

Verbatim, o fecho do survey (mesma seção):

> "The most important future systems will likely be those that combine four properties. First, they will be *executable*, grounding decisions in code, tools, tests, and environments. Second, they will be *inspectable*, exposing plans, state, provenance, and failure causes. Third, they will be *stateful*, preserving task-relevant information across long trajectories and multiple agents. Fourth, they will be *governed*, ensuring that autonomy is constrained by permissions, verification, and accountability."

### 5.3 Demais problemas em aberto do CaAH

Os títulos abaixo são literais do sumário (<https://arxiv.org/html/2605.18747v1>, §5.2):

- §5.2.2 Semantic Verification Beyond Executable Feedback — o artigo alerta que a realimentação por execução "can create a false sense of correctness", e resume: "the agent sees a green test, but the green test is not the full specification".
- §5.2.3 Self-Evolving Harnesses without Regression — encerra com uma agenda de pesquisa cujo último item é literalmente o problema deste projeto. Verbatim: *"A practical research agenda includes: defining mutation operators for harness components; building telemetry standards; evaluating evolved harnesses across diverse tasks; enforcing safety invariants during evolution; and separating improvements in the harness from improvements in the base model."* A mesma subseção nomeia o compromisso custo-desempenho de forma explícita: *"a new tool schema may reduce token cost while weakening permission boundaries"*.
- §5.2.4 Transactional Shared Program State and Semantic Conflict Resolution.
- §5.2.5 Human-in-the-Loop Safety and Accountability as Harness State.
- §5.2.6 Multimodal Code-Harness Systems.

O CaAH tem ainda uma lista de seis desafios específicos de harnesses de assistente de código, em §5.1.1 "Open Challenges for Code-Assistant Harnesses".
Dois deles são diretamente úteis a este projeto.

Sobre adequação do oráculo, verbatim (<https://arxiv.org/html/2605.18747v1>, §5.1.1):

> "verification beyond unit tests remains largely unsolved: the *oracle-adequacy crisis* exposed by PatchDiff and SWE-Bench++, the security-correctness gap addressed by Aardvark and Codex Security, and the organicity gap between functional and accepted patches all point to a verifier surface that current harnesses underspecify."

Sobre atribuição de falhas, verbatim (mesma seção):

> "*failure attribution* in long-horizon agent loops is still immature: empirical studies such as 'Why do multi-agent systems fail?', the Who&When attribution dataset, AgenTracer, and AgentDebug report best step-level attribution accuracies in the 14–53% range, suggesting that production harnesses lack the structured traces needed for principled debugging."

Essa faixa de 14 % a 53 % é um número concreto e citável para argumentar que atribuir desempenho a componentes de harness é, hoje, um problema não resolvido.

O resumo do artigo lista as mesmas lacunas de forma condensada, verbatim (<https://arxiv.org/html/2605.18747v1>, Abstract):

> "We further outline open challenges for harness engineering, including evaluation beyond final task success, verification under incomplete feedback, regression-free harness improvement, consistent shared state across multiple agents, human oversight for safety-critical actions, and extensions to multimodal environments."

### 5.4 Limitações declaradas pelo AHE

A seção "Limitations" do AHE (não numerada, entre a Conclusão e as Referências) abre com, verbatim (<https://arxiv.org/html/2604.25850v4>):

> "This work studies a promising but high-variance setting, and the scope of our claims should be interpreted accordingly."

**Benchmark scope**, verbatim:

> "Our evaluation drives evolution on Terminal-Bench 2 and probes transfer on SWE-bench-verified. Even though the frozen harness transfers to a second task surface and to three alternate base-model families, broader programming languages, repository-scale deployments, and human-in-the-loop workflows remain untested."

**Evolution operating point**, verbatim — é a admissão de confundimento do artigo:

> "AHE's step budget and per-task timeout were fitted to GPT-5.4 high during evolution, so cross-model transfer numbers conflate harness portability with operating-point coupling—within one family the gain is non-monotone across reasoning tiers. Untangling these factors will require re-running the loop under multiple operating points."

Isso importa diretamente para este projeto: **orçamento de passos e timeout por tarefa são variáveis de confundimento** e precisam ser fixados de forma idêntica entre os quatro braços, e essa decisão precisa ser declarada.

**Self-modification governance**, verbatim:

> "AHE bounds edits to a workspace, attributes every change in a versioned manifest, and rolls back ineffective edits at file granularity, but it does not provide a complete guardrail stack. Long-horizon harness cleanup and stronger misuse prevention remain incomplete, and AHE should be viewed as a controlled research prototype rather than a fully mature autonomous self-improvement system."

Duas outras limitações são declaradas no §1 e detalhadas no §4.4, verbatim:

> "Our analysis reveals two limits of agent-driven evolution: harness components interact non-additively, so stacking effective edits caps the aggregate gain; and the loop's self-attribution is reliable for fixes but blind to regressions, pinpointing regression foresight as the clearest direction for future self-evolution loops."

A não-aditividade é relevante para este projeto: significa que não se pode inferir o desempenho de um harness somando os efeitos de seus componentes, o que reforça a necessidade de comparar harnesses **inteiros**, como este projeto faz.

### 5.5 O que os artigos *não* dizem (lacunas negativas, verificadas)

Estas ausências são tão importantes quanto as lacunas declaradas, porque delimitam o espaço que este projeto ocupa.

- **Nenhum dos dois artigos avalia modelos pequenos, abertos ou executados localmente.** O AHE usa exclusivamente APIs hospedadas (GPT-5.4, qwen-3.6-plus, gemini-3.1-flash-lite-preview, deepseek-v4-flash) e não nomeia nenhum endpoint local, vLLM ou GPU (<https://arxiv.org/html/2604.25850v4>, §4.1 e Apêndice A). No CaAH, as expressões "small model", "open-source model" e "local model" não ocorrem no texto, e nenhum dos sete problemas em aberto do §5.2 trata de modelos pequenos ou locais. **NÃO ESTABELECIDO: qualquer experimento ou discussão de modelo local em qualquer um dos dois artigos.**
- **O CaAH não usa "pass@k" em nenhum ponto** (a expressão usada é "pass rate"), e não nomeia HumanEval, BigCodeBench, CodeContests, APPS, GAIA nem RepoBench. Os benchmarks de código que ele nomeia incluem SWE-bench e variantes, Terminal-Bench, InterCode, CRUXEval, LiveCodeBench, AgentBench e AppWorld (<https://arxiv.org/html/2605.18747v1>, §2.3.3 e §5.1.1).
- **O AHE também não é neutro em relação ao CaAH:** o §3.5 do survey resume o próprio AHE, citado como `lin2026agentic`. Os dois artigos-âncora não constituem duas confirmações independentes da mesma tese.
- **O AHE não reporta custo em dólares, tempo de parede por execução, contagem de turnos nem contagem de chamadas de ferramenta em nenhuma tabela.** O único número temporal é uma menção em prosa de que a campanha de dez iterações levou "roughly 32 hours" (<https://arxiv.org/html/2604.25850v4>, §4.2).
- **O AHE não reconhece o desenho de campanha única, sem barras de erro, como limitação.** A ausência de variância reportada não é discutida na seção de limitações.
- **A falta de padronização na comparação entre harnesses não é declarada como limitação pelo AHE.** É o CaAH, em §5.2.1, que a formula. Atribuir essa crítica ao AHE seria incorreto.
- **Cline e PI não aparecem em nenhum dos dois artigos.** Busca em texto integral de ambos: zero ocorrências de "Cline"; zero ocorrências de "PI" como nome de harness.
- **O AHE nunca usa o termo "ReAct".** Seu controle mínimo é o NexAU₀, um agente somente-bash.

---

## 6. Referências em formato ABNT NBR 6023:2018

Convenções aplicadas, com fonte:

- Para quatro ou mais autores, a norma permite indicar apenas o primeiro seguido de *et al.* — "Quando houver quatro ou mais autores, convém indicar todos. Permite-se que se indique apenas o primeiro, seguido da expressão *et al*." (<https://bibliotecabenedictomonteiro.wordpress.com/2018/11/22/nbr-6023-2018-de-referencias-bibliograficas-principais-alteracoes/>). Dado que o AHE tem 11 autores e o CaAH tem 42, a forma com *et al.* é a recomendada.
- Local de publicação desconhecido: `[S. l.]`, com S maiúsculo por ser o primeiro elemento dos dados de publicação (mesma fonte).
- A NBR 6023:2018 eliminou os sinais `<` e `>` ao redor do URL (mesma fonte).
- Documento em meio eletrônico exige "Disponível em:" seguido do endereço e "Acesso em:" seguido da data (<https://www.ufrgs.br/bibliotecas/ferramentas/campos-basicos-abnt-mendeley/>).
- Título em caixa-baixa após a primeira palavra, subtítulo após dois-pontos sem destaque (mesma fonte).

**NÃO ESTABELECIDO: a NBR 6023:2018 não define uma categoria explícita para *preprint*.** As entradas abaixo seguem o padrão de "documento em meio eletrônico" / monografia no todo, que é a prática corrente das bibliotecas universitárias brasileiras para material de repositório. Verifique com a norma da sua instituição antes da entrega.

### 6.1 Forma abreviada (recomendada)

```
LIN, Jiahang et al. Agentic harness engineering: observability-driven automatic
evolution of coding-agent harnesses. [S. l.]: arXiv, 2026. arXiv:2604.25850v4.
DOI: 10.48550/arXiv.2604.25850. Disponível em: https://arxiv.org/abs/2604.25850.
Acesso em: 7 ago. 2026.

NING, Xuying et al. Code as agent harness: toward executable, verifiable, and
stateful agent systems. [S. l.]: arXiv, 2026. arXiv:2605.18747v1.
DOI: 10.48550/arXiv.2605.18747. Disponível em: https://arxiv.org/abs/2605.18747.
Acesso em: 7 ago. 2026.
```

### 6.2 Forma com todos os autores (também aceita pela norma)

```
LIN, Jiahang; LIU, Shichun; PAN, Chengjun; LIN, Lizhi; DOU, Shihan; XI, Zhiheng;
HUANG, Xuanjing; YAN, Hang; HAN, Zhenhua; GUI, Tao; JIANG, Yu-Gang.
Agentic harness engineering: observability-driven automatic evolution of
coding-agent harnesses. [S. l.]: arXiv, 2026. arXiv:2604.25850v4.
DOI: 10.48550/arXiv.2604.25850. Disponível em: https://arxiv.org/abs/2604.25850.
Acesso em: 7 ago. 2026.
```

Para o CaAH, a listagem completa dos 42 autores é desaconselhável em um trabalho de 5 a 7 páginas; use a forma com *et al.*
A ordem completa, caso necessária, está registrada em <https://arxiv.org/abs/2605.18747>.

### 6.2.1 Referência auxiliar do ReAct

O artigo original do ReAct é necessário para fundamentar o braço de controle deste projeto.
Metadados verificados em <https://arxiv.org/abs/2210.03629>: autores Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan e Yuan Cao; v1 de 6 out. 2022; v3 de 10 mar. 2023, versão final do ICLR 2023.

```
YAO, Shunyu et al. ReAct: synergizing reasoning and acting in language models.
[S. l.]: arXiv, 2023. arXiv:2210.03629v3. DOI: 10.48550/arXiv.2210.03629.
Disponível em: https://arxiv.org/abs/2210.03629. Acesso em: 7 ago. 2026.
```

Definição do laço, verbatim (<https://arxiv.org/abs/2210.03629>, §2):

> "We augment the agent's action space to Â = A ∪ L, where L is the space of language. An action â_t ∈ L in the language space, which we will refer to as a *thought* or a *reasoning trace*, does not affect the external environment, thus leading to no observation feedback."

O que um laço ReAct nu **não** inclui, verificado contra o artigo: memória persistente entre episódios, módulo de planejamento separado, compactação de contexto, subagentes, porta de permissão, checkpoint e esquemas de ferramenta.
O único estado é a trajetória `c_t` dentro da janela de contexto.
**NÃO ESTABELECIDO: qualquer ferramenta de sistema de arquivos, shell ou edição de código no artigo original** — os ambientes são apenas a API da Wikipédia, ALFWorld e WebShop.
Portanto, o braço de controle deste projeto é um *laço ReAct aplicado a ferramentas de código*, uma extensão do artigo, e o texto deve dizer isso em vez de sugerir que o artigo já define esse agente.

### 6.3 Metadados de apoio (para conferência)

**arXiv:2604.25850 — AHE**

- Título exato: *Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses*.
- Autores (v4, 11): Jiahang Lin, Shichun Liu, Chengjun Pan, Lizhi Lin, Shihan Dou, Zhiheng Xi, Xuanjing Huang, Hang Yan, Zhenhua Han, Tao Gui, Yu-Gang Jiang. Afiliações: Universidade Fudan, Universidade de Pequim, Shanghai Qiji Zhifeng Co., Ltd.
- Atenção: a **v1 tem apenas 9 autores** e omite Zhiheng Xi e Yu-Gang Jiang. Use a lista da v4.
- Categorias: cs.CL (primária), cs.SE.
- Histórico de submissão (<https://arxiv.org/abs/2604.25850>): v1 — 28 abr. 2026; v2 — 29 abr. 2026; v3 — 30 abr. 2026; v4 (mais recente) — 18 maio 2026.
- Ano a usar na referência: **2026**.
- DOI: 10.48550/arXiv.2604.25850.
- Extensão: 35 páginas (PDF da v4).
- Código: <https://github.com/china-qijizhifeng/agentic-harness-engineering>.
- **NÃO ESTABELECIDO: veículo de publicação.** A página do arXiv não traz campo `Comments:` nem `Journal ref:`, portanto não há revista ou conferência declarada. Trate como preprint.

**arXiv:2605.18747 — CaAH**

- Título exato, com subtítulo: *Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems*. (No HTML do arXiv o subtítulo aparece separado por um losango ornamental; o título canônico do registro é "Code as Agent Harness".)
- Autores (42, primeira autora Xuying Ning; lista completa em <https://arxiv.org/abs/2605.18747>). Autores correspondentes: Hanghang Tong e Jingrui He. Afiliações: Universidade de Illinois em Urbana-Champaign, Meta, Universidade Stanford.
- Categorias: cs.CL (primária), cs.AI. Licença CC BY 4.0.
- Histórico de submissão: v1 — 18 maio 2026, 17:59:03 UTC (única versão).
- Ano a usar na referência: **2026**.
- DOI: 10.48550/arXiv.2605.18747.
- Extensão: 102 páginas (PDF da v1).
- Repositório complementar: <https://github.com/YennNing/Awesome-Code-as-Agent-Harness-Papers>.
- **NÃO ESTABELECIDO: veículo de publicação.** Sem campo `Comments:` ou `Journal ref:`. Trate como preprint.

---

## 7. Resumo executivo — o que este ticket entrega ao texto do projeto

1. **Definição a citar:** a do CaAH §1 ("the software layer that surrounds an LLM with tools, APIs, sandboxes, memory, validators, permission boundaries, execution loops, and feedback channels"), complementada pela do AHE §1 ("this collection of model-external, editable components").
2. **Vocabulário a adotar:** a tripartição do CaAH §1 entre *model-internal capabilities* / *system-provided harness infrastructure* / *agent-initiated code artifacts*, que descreve com precisão o desenho experimental deste projeto.
3. **Taxonomia a adotar:** as três camadas do CaAH (interface, mecanismos, escala) para descrição qualitativa, e os sete tipos de componente do AHE §3.1 para comparação estrutural braço a braço.
4. **Métrica principal:** **Succ/Mtok** (AHE, Eq. 2, Apêndice A) — sucessos esperados por milhão de tokens. É a métrica custo-desempenho de fonte primária que o problema de pesquisa exige.
5. **Métricas secundárias:** pass@1 com *k* alto e intervalo de confiança (superando a campanha única do AHE), Tokens k, e a dimensão *trajectory efficiency* do CaAH §5.2.1, incluindo tempo de parede — que nenhum dos dois artigos reporta por execução e que é o custo real em uma única GPU.
6. **Justificativa mais forte:** a Tabela 1 do AHE, onde três harnesses humanos sobre **o mesmo modelo** variam de 47,2 % a 71,9 % de pass@1 (24,7 pp de dispersão), enquanto a troca de modelo sob harness fixo produz linhas de base de 36,5 % a 56,2 %. Evidência publicada de que a dispersão entre harnesses rivaliza com a dispersão entre modelos.
7. **Lacuna que o projeto ocupa:** CaAH §5.2.1 ("Such metrics conflate the capabilities of the base model, the quality of the harness…") e §5.2.7 ("metrics that isolate harness components"), somadas à ausência verificada de qualquer experimento com modelo local pequeno em ambos os artigos e à ausência de Cline e PI na literatura examinada.
8. **Eixo independente do estudo:** a classificação da seção 3 produz a ordenação de profundidade **ReAct mínimo < PI < OpenCode ≈ Cline**, com o PI ocupando uma posição intermediária genuína (quatro ferramentas padrão, sem MCP, sem subagentes, sem modo de planejamento, sem porta de permissão). A escada é bem espaçada, o que fortalece o desenho.
9. **Confundidor a declarar obrigatoriamente:** o Cline só usa chamada de ferramenta nativa para uma lista fechada de modelos de fronteira (<https://cline.bot/blog/cline-v3-35>); sob o LFM2.5-2.6B ele cairá no formato XML textual legado, enquanto OpenCode e PI usarão chamada estruturada. Isso mistura uma diferença de interface com a diferença de harness e infla o custo em tokens do Cline por construção.
10. **Decisão de instrumentação:** medir tokens no servidor Ollama, e não na contabilidade de cada harness. É o único instrumento idêntico entre os quatro braços, e resolve as lacunas de reporte headless do Cline e do PI documentadas na seção 3.5.
11. **Confundidores herdados do AHE a controlar:** orçamento de passos e *timeout* por tarefa devem ser idênticos entre os braços e declarados, conforme a limitação "Evolution operating point" do AHE (seção 5.4).
