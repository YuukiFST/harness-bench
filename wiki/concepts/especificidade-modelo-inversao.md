---
title: Especificidade de Modelo e Inversao
type: concept
summary: Efeito do harness e por modelo; ordenacao pode inverter entre niveis
tags: [modelo, inversao, robustez, niveis]
created: 2026-09-10
updated: 2026-09-10
sources: [wiki/sources/agentic-harness-engineering-lin-2026.md, wiki/sources/holistic-agent-leaderboard-kapoor-2025.md, wiki/sources/frontierharness-runta-2026.md, wiki/sources/stop-comparing-harness-zhang-2026.md]
---

# Especificidade de Modelo e Inversao

Ressalva permanente do PCC: o efeito e especifico do modelo e pode inverter de sinal (source: [[agentic-harness-engineering-lin-2026]]: "a harness tuned for one base model often underperforms on another").

## Evidencias

- HAL: Anthropic vai melhor com BrowserUse, OpenAI com SeeAct, mesmo benchmark (source: [[holistic-agent-leaderboard-kapoor-2025]]).
- FrontierHarness: Claude Code eficiente em Anthropic parece caro sob K3 com cache implicito (25,0% ponderado vs 67,8% mediano; 68% dos tokens numa celula) — propriedade do par, nao defeito isolado (source: [[frontierharness-runta-2026]]).
- Zhang: H3 (verificacao/recuperacao) expoe diferencas ocultas — variancia cross-model maior em H3 que H2 (source: [[stop-comparing-harness-zhang-2026]]).
- AHE: evolucao ajustada ao GPT-5.4 confunde portabilidade com ponto de operacao.

## Resposta do PCC

Dois niveis (primario + robustez), mesmo gateway (source: [[zen-opencode-2026]]), relatados em separado, nunca medios. Se a ordenacao inverter, a inversao e o resultado. Conclusoes enunciadas por nivel.

## Contradictions

Nenhuma direta; ver [[binding-constraint-thesis]] para escopo (tese vale com modelos comparaveis).
