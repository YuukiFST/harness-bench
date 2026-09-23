---
title: Binding Constraint Thesis
type: concept
summary: Com modelos comparaveis, variancia do harness domina a do modelo (HV/MV 7,8x)
tags: [tese, variancia, hv-mv, falsificabilidade]
created: 2026-09-10
updated: 2026-09-23
sources: [wiki/sources/stop-comparing-harness-zhang-2026.md, wiki/sources/deepswe-huang-2026.md, wiki/sources/holistic-agent-leaderboard-kapoor-2025.md, wiki/sources/agentic-harness-engineering-lin-2026.md, wiki/sources/harnesstax-pan-2026.md, wiki/sources/sol-pi-liu-2026.md]
---

# Binding Constraint Thesis

Enunciado (source: [[stop-comparing-harness-zhang-2026]]): em tarefas de longo horizonte com modelos de fronteira comparaveis, a variancia entre *harnesses* (HV) e comparavel ou maior que a variancia entre modelos (MV), podendo domina-la. Formal: HV(M) = Var_H[B(M,H)], MV(H) = Var_M[B(M,H)].

## Evidencia

- Fatorial 3x3x100x2: HV media 18,48 pp2 vs MV 2,37 pp2, razao **7,80x**; 6/9 reversoes de ranking (source: [[stop-comparing-harness-zhang-2026]]).
- Evolucao de *harness*: 69,7%->77,0% em 10 iteracoes AHE com GPT-5.4 fixo, Terminal-Bench 2 (source: [[agentic-harness-engineering-lin-2026]]); gaps de 30-48 pp entre SWE-Agent e HAL Generalist no SWE-bench Verified Mini, 50 tarefas, execucao unica (source: [[holistic-agent-leaderboard-kapoor-2025]]).
- Custo: 24,7 pp e ~47% de tokens com modelo congelado (source: [[agentic-harness-engineering-lin-2026]]); 20x/139x com tarefa fixa (source: [[scaffolding-matters-alier-forment-2026]]); 17x por pass (source: [[frontierharness-runta-2026]]).
- EdgeBench, GPT-5.6 Sol fixo, 51 tarefas publicas: o *score* medio vai de 24,5 (OpenSquilla) e 29,6 (OpenCode) a 44,8 (Pi), e Codex fica em 34,7; custo de $1.243 a $3.422. Execucoes por configuracao e IC nao informados (source: [[sol-pi-liu-2026]]).
- Contra-evidencia no acerto, a favor no custo: 7 modelos x Claude Code/Codex/Pi, 30 tarefas x 3 execucoes, efeito medio do *harness* no sucesso dentro de +-2% (SWE-bench Lite) e cerca de +-5% (Terminal-Bench 2.0), com custo ate 5x para o mesmo modelo (source: [[harnesstax-pan-2026]]). Ver Contradictions.

## Escopo e falsificabilidade

Vale no regime longo-horizonte + modelos comparaveis; exclui curto-horizonte e pares desequilibrados. HV depende da amostragem de *harnesses* (sem distancia principiologica ainda). Desenho minimo: grid 2x2 com ordem, ambiente, script, API e paradas constantes (source: [[stop-comparing-harness-zhang-2026]]).

## Uso no projeto

H1 e HV>0 em [[succ-mtok]]; H2 e o contraste *harness* vs *fork* com distancia ETCSOVG minima. Reportar rankings por *harness* + contagens de reversao, nunca ranking unico. Ver [[desenho-experimental-harness-fixo]] e [[especificidade-modelo-inversao]].

## Contradictions

Ver tambem [[atribuicao-harness-vs-modelo]] (C1 modelo-dirige vs *harness*-domina).

- *Harness* pouco muda o acerto vs *harness* domina ou se compara ao modelo. [[harnesstax-pan-2026]]: "Harness choice has little effect on task success rate"; efeito medio dentro de +-2% no SWE-bench Lite e cerca de +-5% no Terminal-Bench 2.0 (7 modelos, Claude Code/Codex/Pi, 30 tarefas por benchmark, 3 execucoes, IC por *bootstrap*, precos de 1 set. 2026). Do outro lado: [[stop-comparing-harness-zhang-2026]] (HV/MV 7,80x, 6/9 reversoes); [[agentic-harness-engineering-lin-2026]] Tabela 1, OpenCode 47,2% vs Codex 71,9% no mesmo Terminal-Bench 2, GPT-5.4 fixo, 89 tarefas (24,7 pp); [[holistic-agent-leaderboard-kapoor-2025]] (30-48 pp, execucao unica); [[sol-pi-liu-2026]] (EdgeBench, GPT-5.6 Sol: Codex 34,7 vs Pi 44,8 de *score*). Diferencas de recorte que nao resolvem a disputa: HarnessTax compara so tres *harnesses* (dois de fornecedor e o Pi), com 30 tarefas por benchmark, e o SWE-bench Lite fica fora do regime de longo horizonte da tese; Lin inclui OpenCode, ausente em HarnessTax. Nas duas fontes o custo varia muito com o modelo fixo. Sem vencedor; registrado em `_review.md`.
