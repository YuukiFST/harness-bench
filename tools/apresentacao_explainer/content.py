"""Dados do deck explicativo: números com denominador e fonte.

Fonte única: dist/projeto-de-pesquisa.docx (dump via `python tools/docx_prose.py dump`).
Cada bloco cita o parágrafo [n] de onde o número saiu. Nenhum número novo: o que não está
no projeto não entra aqui (regra de 2026-09-23, issue #80).
"""

# HarnessTax (Pan et al., 2026), SWE-bench Lite, Claude Fable 5; projeto [43].
# (harness, sucesso %, US$ por tentativa, braço)
HARNESSTAX: list[tuple[str, float, float, str]] = [
    ("Claude Code", 97.8, 1.33, "other"),
    ("pi", 96.7, 0.67, "pi"),
]

# Lin et al. (2026), Tabela 1: harnesses escritos por humanos sobre o GPT-5.4, Terminal-Bench 2; projeto [68].
LIN_T1: list[tuple[str, float, str]] = [
    ("OpenCode", 47.2, "oc"),
    ("Codex", 71.9, "other"),
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

# Objetivos específicos [52]–[57].
OBJECTIVES: list[tuple[str, str]] = [
    ("<em>Proxy</em>", "conta requisições, tokens e latência por braço"),
    ("Especificação do Finn", "nove unidades, com testes de aceitação"),
    ("Finn nos dois <em>harnesses</em>", "mesmo modelo, <em>prompt</em> e espaço inicial"),
    ("Segundo modelo", "a ordenação dos braços se mantém?"),
    ("Tokens relatados × medidos", "o relato de cada <em>harness</em> contra o <em>proxy</em>"),
    ("Publicar", "executor, <em>prompts</em>, testes, dados e scripts de análise"),
]

# Classificação [73].
CLASS_AXES: list[tuple[str, str, str]] = [
    ("Finalidade", "aplicada", ""),
    ("Abordagem", "quali-quantitativa", "tokens e testes aprovados; atribuição à carga fixa ou à conversa"),
    ("Objetivos", "exploratória", "não há comparação publicada de <em>harnesses</em> construindo o mesmo produto completo"),
    ("Procedimentos", "experimental", "manipulada: o <em>harness</em> · controladas: modelo, especificação, espaço de trabalho inicial e limites"),
    ("Método", "dedutivo", "predições registradas antes da coleta [83]"),
]

# Tabela 2 [101]–[179]: X por mês, ago a jan.
GANTT_MONTHS = ["Ago", "Set", "Out", "Nov", "Dez", "Jan"]
GANTT: list[tuple[str, list[int]]] = [
    ("Leitura e levantamento bibliográfico", [1, 1, 0, 0, 0, 0]),
    ("Definição do tema e das hipóteses", [1, 1, 0, 0, 0, 0]),
    ("Construção do <em>proxy</em> e dos testes", [0, 0, 1, 1, 0, 0]),
    ("Escrevendo introdução", [1, 1, 0, 0, 0, 0]),
    ("Escrevendo referencial teórico", [1, 1, 0, 0, 0, 0]),
    ("Escrevendo material e método", [1, 1, 0, 0, 0, 0]),
    ("Execução da matriz de experimentos", [0, 0, 0, 0, 1, 1]),
    ("Análise dos resultados", [0, 0, 0, 0, 0, 1]),
    ("Elaborando as referências", [1, 1, 0, 0, 0, 0]),
    ("Revisão final e apresentação", [0, 1, 0, 0, 0, 0]),
]

# As 15 entradas da seção 6 [181]–[194], formato abreviado.
REFS: list[str] = [
    "BRASIL. CNPq. <b>Portaria CNPq nº 2.664, de 6 de março de 2026</b>. Política de Integridade na Atividade Científica do CNPq. DOU, 11 mar. 2026.",
    "EARENDIL. <b>Pi, minimal and performant</b>. 2026. Blogue institucional.",
    "KARPATHY, A. <b>LLM Wiki</b>: a pattern for building personal knowledge bases using LLMs. 2026. Gist (GitHub).",
    "LIN, J. <em>et al.</em> <b>Agentic harness engineering</b>. arXiv:2604.25850, 2026. <em>Preprint</em>.",
    "LIU, H. <em>et al.</em> <b>SoL-Pi</b>: recursively scaling auto-research loops for efficient agent harness. arXiv:2609.20519, 2026. <em>Preprint</em>.",
    "MILLER, E. <b>Adding error bars to evals</b>. arXiv:2411.00640, 2024. <em>Preprint</em>.",
    "NING, X. <em>et al.</em> <b>Code as agent harness</b>. arXiv:2605.18747, 2026. <em>Preprint</em>.",
    "OPENCODE. <b>OpenCode</b>: the open source coding agent. 2026a. Repositório de código.",
    "OPENCODE. <b>Zen</b>. 2026b. Documentação do produto.",
    "PAN, M. Z. <em>et al.</em> <b>HarnessTax</b>: how much does the harness matter for coding agents? 2026. Blogue de pesquisa, não revisado por pares.",
    "YUUKIFST. <b>agent-dotfiles</b>: skill Helmsman, mapa de decisões para agentes de codificação. 2026a. Repositório de código.",
    "YUUKIFST. <b>Finn</b>: SaaS universal de financeiro por voz. 2026b. Repositório de código.",
    "YUUKIFST. <b>harness-bench</b>: executor, prompts, testes de aceitação, dados brutos e scripts de análise deste projeto. 2026c. Repositório de código.",
    "ZHANG, Y. <em>et al.</em> <b>Stop comparing LLM agents without disclosing the harness</b>. arXiv:2605.23950, 2026. <em>Preprint</em>.",
]
