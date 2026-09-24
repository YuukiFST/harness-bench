---
title: Especificidade de Modelo e Inversao
type: concept
summary: Efeito do harness e por modelo; ordenacao pode inverter entre niveis
tags: [modelo, inversao, robustez, niveis]
created: 2026-09-10
updated: 2026-09-23
sources: [wiki/sources/agentic-harness-engineering-lin-2026.md, wiki/sources/holistic-agent-leaderboard-kapoor-2025.md, wiki/sources/frontierharness-runta-2026.md, wiki/sources/stop-comparing-harness-zhang-2026.md, wiki/sources/harnesstax-pan-2026.md, wiki/sources/sol-pi-liu-2026.md]
---

# Especificidade de Modelo e Inversao

Ressalva permanente do projeto: o efeito e especifico do modelo e pode inverter de sinal (source: [[agentic-harness-engineering-lin-2026]]: "a harness tuned for one base model often underperforms on another").

## Evidencias

- HAL: Anthropic vai melhor com BrowserUse, OpenAI com SeeAct, mesmo benchmark (source: [[holistic-agent-leaderboard-kapoor-2025]]).
- FrontierHarness: Claude Code eficiente em Anthropic parece caro sob K3 com cache implicito (25,0% ponderado vs 67,8% mediano; 68% dos tokens numa celula) — propriedade do par, nao defeito isolado (source: [[frontierharness-runta-2026]]).
- Zhang: H3 (verificacao/recuperacao) expoe diferencas ocultas — variancia cross-model maior em H3 que H2 (source: [[stop-comparing-harness-zhang-2026]]).
- AHE: evolucao ajustada ao GPT-5.4 confunde portabilidade com ponto de operacao.
- HarnessTax: nos seis modelos Anthropic e OpenAI, em SWE-bench Lite e Terminal-Bench 2.0, um *harness* de outro fornecedor ou o Pi tem a maior taxa de sucesso observada em 9 de 12 comparacoes; GPT-5.6 Sol faz 83,3% no Pi vs 78,9% no Codex no Terminal-Bench 2.0 ($0,42 vs $0,76); Sonnet 4.6 faz 68,9% no Codex vs 66,7% no Claude Code no SWE-bench Lite. O par nativo nao garante o melhor resultado (source: [[harnesstax-pan-2026]]).
- SoL-Pi: mecanismos achados so com trajetorias do GPT-5.6 Sol disparam menos e com menor intensidade no Opus 5, mas a pilha completa mantem 94,3% do *score* do Pi e corta 44,7% dos tokens no Opus 5 sem nova busca (EdgeBench) (source: [[sol-pi-liu-2026]]).

## Resposta do projeto

Dois niveis (primario + robustez), mesmo gateway (source: [[zen-opencode-2026]]), relatados em separado, nunca medios. Se a ordenacao inverter, a inversao e o resultado. Conclusoes enunciadas por nivel. Objetivo (5): a ordenacao OpenCode vs Pi se mantem ou inverte no segundo nivel.

## Contradictions

Ver [[binding-constraint-thesis]] para escopo (tese vale com modelos comparaveis).

- Custo do Claude Code como propriedade do par vs custo do *harness* em qualquer modelo. [[frontierharness-runta-2026]] le o custo alto do Claude Code sob Kimi K3 ($18,34 por pass) como possivel interacao *harness*-modelo-*gateway* (cache implicito do K3 contra a estrategia do Claude Code para Anthropic), nao do *harness* sozinho. [[harnesstax-pan-2026]] mede o Claude Code caro tambem com modelos da propria Anthropic: Claude Fable 5 no SWE-bench Lite custa $1,33 no Claude Code vs $0,67 no Pi, e o contexto inicial do Claude Code passa de 10x o do Pi nos 7 modelos. [[sol-pi-liu-2026]] vai na mesma direcao com Opus 5 no EdgeBench (Claude Code $2.535 vs Pi $1.741). Registrado em `_review.md`.
- Portabilidade entre modelos. [[agentic-harness-engineering-lin-2026]]: "a harness tuned for one base model often underperforms on another". [[sol-pi-liu-2026]] fala em "strong cross-model generalization within the evaluated setting" para um *harness* buscado so com GPT-5.6 Sol e aplicado ao Opus 5 (1 modelo de transferencia, sem IC). Registrado em `_review.md`.
