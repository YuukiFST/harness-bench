---
title: Binding Constraint Thesis
type: concept
summary: Com modelos comparaveis, variancia do harness domina a do modelo (HV/MV 7,8x)
tags: [tese, variancia, hv-mv, falsificabilidade]
created: 2026-09-10
updated: 2026-09-14
sources: [wiki/sources/stop-comparing-harness-zhang-2026.md, wiki/sources/deepswe-huang-2026.md, wiki/sources/holistic-agent-leaderboard-kapoor-2025.md, wiki/sources/agentic-harness-engineering-lin-2026.md]
---

# Binding Constraint Thesis

Enunciado (source: [[stop-comparing-harness-zhang-2026]]): em tarefas de longo horizonte com modelos de fronteira comparaveis, a variancia entre *harnesses* (HV) e comparavel ou maior que a variancia entre modelos (MV), podendo domina-la. Formal: HV(M) = Var_H[B(M,H)], MV(H) = Var_M[B(M,H)].

## Evidencia

- Fatorial 3x3x100x2: HV media 18,48 pp2 vs MV 2,37 pp2, razao **7,80x**; 6/9 reversoes de ranking (source: [[stop-comparing-harness-zhang-2026]]).
- Evolucao de *harness*: 69,7%->77,0% em 10 iteracoes AHE com GPT-5.4 fixo, Terminal-Bench 2 (source: [[agentic-harness-engineering-lin-2026]]); gaps de 30-48 pp entre SWE-Agent e HAL Generalist no SWE-bench Verified Mini, 50 tarefas, execucao unica (source: [[holistic-agent-leaderboard-kapoor-2025]]).
- Custo: 24,7 pp e ~47% de tokens com modelo congelado (source: [[agentic-harness-engineering-lin-2026]]); 20x/139x com tarefa fixa (source: [[scaffolding-matters-alier-forment-2026]]); 17x por pass (source: [[frontierharness-runta-2026]]).

## Escopo e falsificabilidade

Vale no regime longo-horizonte + modelos comparaveis; exclui curto-horizonte e pares desequilibrados. HV depende da amostragem de *harnesses* (sem distancia principiologica ainda). Desenho minimo: grid 2x2 com ordem, ambiente, script, API e paradas constantes (source: [[stop-comparing-harness-zhang-2026]]).

## Uso no projeto

H1 e HV>0 em [[succ-mtok]]; H2 e o contraste *harness* vs *fork* com distancia ETCSOVG minima. Reportar rankings por *harness* + contagens de reversao, nunca ranking unico. Ver [[desenho-experimental-harness-fixo]] e [[especificidade-modelo-inversao]].

## Contradictions

Ver [[atribuicao-harness-vs-modelo]].
