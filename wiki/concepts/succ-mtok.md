---
title: Succ Mtok
type: concept
summary: Sucesso por milhao de tokens; metrica primaria de custo-eficiencia do projeto
tags: [metrica, succ-mtok, custo, pass-at-1]
created: 2026-09-10
updated: 2026-09-10
sources: [wiki/sources/agentic-harness-engineering-lin-2026.md, wiki/sources/deepswe-huang-2026.md, wiki/sources/ai-agents-that-matter-kapoor-2024.md, wiki/sources/holistic-agent-leaderboard-kapoor-2025.md]
---

# Succ Mtok

Definicao (source: [[agentic-harness-engineering-lin-2026]], Eq. 2, Apendice A): `pass@1 x 10^6 / media de tokens por execucao`. Sucessos esperados por milhao de tokens; maior e melhor. No AHE aparece so na Tabela 5 do apendice; no projeto e a **metrica primaria** (razao que interessa a quem paga a conta).

## Por que conjunta

Acuracia sozinha nao identifica progresso: pode subir por retry e outros metodos cientificamente vazios (source: [[ai-agents-that-matter-kapoor-2024]]). Custo e acuracia devem ser otimizados juntos, na fronteira de Pareto (sources: [[ai-agents-that-matter-kapoor-2024]], [[holistic-agent-leaderboard-kapoor-2025]]).

## Contagem (convencao AHE)

Falhas de infra contam 0 no pass@1 mas saem da media de tokens (source: [[agentic-harness-engineering-lin-2026]]). O projeto distingue run falhada (resultado, escore zero) de run descartada (medicao inconfiavel, sem reparo) — ver [[desenho-experimental-harness-fixo]].

## Nuances

- Tokens de input somados crescem ~quadraticamente nos passos (toda chamada recarrega o historico): reportar prefill total + contexto final + output (ver [[medicao-custo-proxy-vs-relato]]).
- HarnessRank usa tokens sem cache; FrontierHarness, custo por pass; DeepSWE, medianas por trial sem condicionar a conclusao. O projeto condiciona a conclusao (custo por tarefa **concluida**), como [[scaffolding-matters-alier-forment-2026]].

## Contradictions

Ver [[atribuicao-harness-vs-modelo]] (correlacao tokens x acuracia difere entre DeepSWE e HAL).
