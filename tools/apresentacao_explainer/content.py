"""Dados do deck explicativo: números com denominador e fonte.

Fontes: dist/projeto-de-pesquisa.docx (dump via tools/docx_prose.py), deck/src/content.ts
(auditado em 2026-09-14) e as páginas wiki/sources/*.md citadas em cada bloco.
Nenhum número novo: o que não está no projeto ou numa página de fonte da wiki não entra aqui.
"""

# FrontierHarness (Runta, 2026): tabela "Pass Rate / Median Cost Per Pass" do post, 12 configurações.
# Fonte: wiki/sources/frontierharness-runta-2026.md, seção "Origem de cada número".
# (nome, aprovação %, US$ por aprovação, braço)
FRONTIER: list[tuple[str, float, float, str]] = [
    ("Codex", 66.7, 3.47, "other"),
    ("DSH Creator", 63.3, 3.28, "other"),
    ("Claude Code", 63.3, 18.34, "other"),
    ("Pi", 60.0, 2.43, "pi"),
    ("DSH Standard", 60.0, 3.46, "other"),
    ("DSH PTC", 60.0, 4.58, "other"),
    ("Kimi Code", 56.7, 3.65, "other"),
    ("DSH Minimal", 56.7, 4.72, "other"),
    ("Oh My Pi", 56.7, 4.75, "other"),
    ("Exo Harness", 53.3, 1.05, "other"),
    ("Hermes", 50.0, 2.90, "other"),
    ("OpenCode", 50.0, 3.24, "oc"),
]

# Camada 1, medição própria: layer1/data/first_request.csv (28 ago. 2026), pi 0.80.10 e OpenCode 1.17.9.
LAYER1 = {
    "system_bytes": (2499, 9738),
    "tools_bytes": (2900, 20007),
    "total_bytes": (5676, 29997),
    "prompt_tokens": (1228, 6659),
    "schemas": (4, 9),
}

# Lin et al. (2026), Tabela 1: GPT-5.4 fixo, Terminal-Bench 2, 89 tarefas, k = 2.
# Fonte: wiki/sources/agentic-harness-engineering-lin-2026.md.
LIN_T1: list[tuple[str, float, str]] = [
    ("OpenCode", 47.2, "oc"),
    ("Terminus-2", 62.9, "other"),
    ("Codex", 71.9, "other"),
]
# Lin et al. (2026): SWE-bench-verified, 500 tarefas, mesmo modelo; acurácia 74,6–75,6 % (empate),
# tokens por tarefa em milhares. Ordem da página da wiki: ACE / TF-GRPO / NexAU0 / AHE.
LIN_SWE: list[tuple[str, float, str]] = [
    ("ACE", 679, "other"),
    ("TF-GRPO", 582, "other"),
    ("NexAU0", 526, "other"),
    ("AHE", 461, "other"),
]

# Kapoor et al. (2025), HAL, Tabela A19: SWE-bench Verified Mini, 50 tarefas, execução única.
# (modelo, SWE-Agent %, HAL Generalist %). Fonte: wiki/sources/holistic-agent-leaderboard-kapoor-2025.md.
HAL: list[tuple[str, float, float]] = [
    ("GPT-5 Medium", 46.0, 12.0),
    ("o4-mini Low", 54.0, 6.0),
    ("o4-mini High", 50.0, 2.0),
    ("Claude 3.7 Sonnet High", 54.0, 24.0),
]

# Alier Forment et al. (2026): mediana de tokens de entrada por run concluída, mesma tarefa de
# 6 operações GitHub, braço CLI. Fonte: wiki/sources/scaffolding-matters-alier-forment-2026.md.
ALIER: list[tuple[str, float, str]] = [
    ("pi (4/4)", 14660, "pi"),
    ("qwen-code (7/8)", 288808, "other"),
    ("Claude Code", 410797, "other"),
]

# Lee et al. (2026), Meta-Harness: TerminalBench-2, 89 tarefas, modelo fixo por linha, sem variância.
LEE: list[tuple[str, float, float, str]] = [
    ("Claude Opus 4.6", 76.4, 74.7, "Terminus-KIRA"),
    ("Claude Haiku 4.5", 37.6, 35.5, "Goose"),
]

FINN_PIPELINE: list[tuple[str, str]] = [
    ("áudio", "WhatsApp ou app"),
    ("texto", "Whisper local"),
    ("intenção", "palavras-chave"),
    ("gate", "papel × ação"),
    ("executar", "ou negar"),
    ("resposta", "push"),
]

UNITS: list[tuple[str, str, str]] = [
    ("U1", "tenant", "#15"),
    ("U2", "governança", "#16"),
    ("U3", "flags", "#17"),
    ("U4", "pipeline de voz", "#14"),
    ("U5", "confirmação", "#20"),
    ("U6", "log", "#21"),
    ("U7", "relatório", "#19"),
    ("U8", "agendador", "#18"),
    ("U9", "cobrança", "#22"),
]

OBJECTIVES: list[tuple[str, str]] = [
    ("Instrumento externo", "requisições, tokens e latência por braço"),
    ("Especificação do Finn", "9 unidades, com testes de aceitação do autor"),
    ("Espaço de trabalho inicial idêntico", "para os dois braços, congelado por hash"),
    ("Finn nos dois <em>harnesses</em>", "mesmo modelo e <em>prompts</em>, com repetição (n ≥ 3)"),
    ("Segundo modelo", "a ordenação se mantém ou inverte?"),
    ("Tokens relatados × medidos", "divergência entre o relato do <em>harness</em> e o instrumento"),
    ("Publicar tudo", "executor, <em>prompts</em>, testes, dados e scripts, custo zero"),
]

CLASS_AXES: list[tuple[str, str, str]] = [
    ("Natureza", "aplicada", "produto: critério de escolha"),
    ("Abordagem", "quanti + quali", "medir tokens e sucesso; atribuir à carga fixa ou aos passos"),
    ("Objetivos", "exploratória", "mesmo produto completo, dois <em>harnesses</em>, sem precedente"),
    ("Procedimentos", "experimental", "VI: <em>harness</em> · controladas: modelo, especificação, espaço de trabalho inicial, limites"),
    ("Método", "dedutivo", "hipóteses antes da coleta"),
]

TIMELINE_A: list[tuple[str, str, str]] = [
    ("2022", "Yao <em>et al.</em> · ReAct", "O laço observar/agir mínimo. É um <em>harness</em> legítimo, o mais raso; o pi, com quatro ferramentas, fica perto dele."),
    ("2024", "Yang <em>et al.</em> · SWE-agent", "A interface entre modelo e ambiente é objeto de projeto desde aqui: melhora sem tocar nos pesos."),
    ("2024", "Kapoor <em>et al.</em> · AI agents that matter", "A avaliação de agentes ignora o custo e por isso erra sobre a origem dos ganhos."),
    ("2025", "Kapoor <em>et al.</em> · HAL", "Avaliações raramente relatam custo; comparações entre <em>harnesses</em> são raras. Anthropic vai melhor com BrowserUse, OpenAI com SeeAct: efeito específico do modelo."),
]
TIMELINE_B: list[tuple[str, str, str]] = [
    ("2026", "Lin <em>et al.</em> · Agentic Harness Engineering", "Definição operacional e Succ/Mtok. Tabela 1: 47,2 % (OpenCode) a 71,9 % (Codex), GPT-5.4, Terminal-Bench 2, 89 tarefas; 24,7 pp (cálculo do autor)."),
    ("2026", "Zhang <em>et al.</em> · Binding Constraint Thesis", "Com modelos de fronteira comparáveis, a parcela do <em>harness</em> é frequentemente comparável ou maior que a do modelo, e pode dominá-la."),
    ("2026", "Lee <em>et al.</em> · Meta-Harness", "Editar só o código do <em>harness</em>, modelo fixo: 76,4 % contra 74,7 % do Terminus-KIRA (TerminalBench-2, 89 tarefas, Claude Opus 4.6). Decisões são isoláveis."),
    ("2026", "Ning <em>et al.</em> · Code as agent harness", "Definição: converte um modelo sem estado em agente funcional. §5.2.1 nomeia a lacuna de atribuição; §5.2.7 pede métricas por componente."),
    ("2026", "Wang <em>et al.</em> · Harness Handbook", "O <em>harness</em> monta os prompts, gerencia o estado, invoca as ferramentas e coordena o laço."),
    ("2026", "Runta · FrontierHarness", "12 configurações, Kimi K3: 50,0–66,7 % e US$ 1,05–18,34 por tarefa concluída. Cache do Claude Code 25,0 % ponderado vs 67,8 % na célula mediana."),
]

GANTT_MONTHS = ["Ago", "Set", "Out", "Nov", "Dez", "Jan"]
GANTT: list[tuple[str, list[int]]] = [
    ("Leitura e levantamento bibliográfico", [1, 1, 0, 0, 0, 0]),
    ("Definição do tema, do problema e das hipóteses", [1, 1, 0, 0, 0, 0]),
    ("Instrumento, especificação e testes de aceitação", [0, 0, 1, 1, 0, 0]),
    ("Escrevendo introdução", [1, 1, 0, 0, 0, 0]),
    ("Escrevendo referencial teórico", [1, 1, 0, 0, 0, 0]),
    ("Escrevendo material e método", [1, 1, 0, 0, 0, 0]),
    ("Execução da matriz de experimentos", [0, 0, 0, 0, 1, 1]),
    ("Análise dos resultados", [0, 0, 0, 0, 0, 1]),
    ("Elaborando as referências", [1, 1, 0, 0, 0, 0]),
    ("Revisão final e preparação da apresentação", [0, 1, 0, 0, 0, 0]),
]

# As 21 entradas da seção 6 do projeto, formato abreviado do deck (deck/src/content.ts, REFS).
REFS: list[str] = [
    "ALIER FORMENT, M. <em>et al.</em> <b>The scaffolding matters more than the interface</b>. arXiv:2608.08654, 2026. <em>Preprint</em>.",
    "BRASIL. CNPq. <b>Portaria CNPq nº 2.664, de 6 de março de 2026</b>. Política de Integridade na Atividade Científica. DOU, 11 mar. 2026.",
    "EARENDIL. <b>Pi, minimal and performant</b>. 2026. Blogue institucional.",
    "HARNESSRANK. <b>HarnessRank</b>: coding-agent harness rankings. 2026. Disponível em: https://harnessrank.net/.",
    "KAPOOR, S. <em>et al.</em> <b>AI agents that matter</b>. arXiv:2407.01502, 2024. <em>Preprint</em>.",
    "KAPOOR, S. <em>et al.</em> <b>Holistic Agent Leaderboard</b>. arXiv:2510.11977, 2025. <em>Preprint</em>.",
    "KARPATHY, A. <b>LLM Wiki</b>: a pattern for building personal knowledge bases using LLMs. 2026. Gist (GitHub).",
    "LEE, Y. <em>et al.</em> <b>Meta-Harness</b>: end-to-end optimization of model harnesses. arXiv:2603.28052, 2026. <em>Preprint</em>.",
    "LIN, J. <em>et al.</em> <b>Agentic harness engineering</b>. arXiv:2604.25850, 2026. <em>Preprint</em>.",
    "MILLER, E. <b>Adding error bars to evals</b>. arXiv:2411.00640, 2024. <em>Preprint</em>.",
    "NING, X. <em>et al.</em> <b>Code as agent harness</b>. arXiv:2605.18747, 2026. <em>Preprint</em>.",
    "OPENCODE. <b>OpenCode</b>: the open source coding agent. 2026a. Repositório de código.",
    "OPENCODE. <b>Zen</b>. 2026b. Documentação do produto.",
    "RUNTA. <b>Introducing the FrontierHarness eval</b>. 2026. Blogue institucional.",
    "WANG, R. <em>et al.</em> <b>Harness Handbook</b>. arXiv:2607.13285, 2026. <em>Preprint</em>.",
    "YANG, J. <em>et al.</em> <b>SWE-agent</b>: agent-computer interfaces enable automated software engineering. NeurIPS, 2024.",
    "YAO, S. <em>et al.</em> <b>ReAct</b>: synergizing reasoning and acting in language models. ICLR, 2023.",
    "YUUKIFST. <b>agent-dotfiles</b>: skill Helmsman, mapa de decisões para agentes de codificação. 2026a. Repositório de código.",
    "YUUKIFST. <b>Finn</b>: SaaS universal de financeiro por voz. 2026b. Repositório de código.",
    "YUUKIFST. <b>harness-bench</b>: executor, prompts, testes de aceitação, dados brutos e scripts de análise deste projeto. 2026c. Repositório de código.",
    "ZHANG, Y. <em>et al.</em> <b>Stop comparing LLM agents without disclosing the harness</b>. arXiv:2605.23950, 2026. <em>Preprint</em>.",
]
