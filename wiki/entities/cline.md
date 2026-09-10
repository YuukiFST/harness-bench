---
title: Cline
type: entity
summary: Harness com modo XML legado em modelos sem tool-call nativo; compactacao invisivel
tags: [cline, harness, bracos, xml, compactacao]
created: 2026-09-10
updated: 2026-09-10
sources: []
---

# Cline

*Harness* de terceiros avaliado na pesquisa (`docs/research/02-harness-concepts-and-metrics.md`, `04-measuring-tokens-steps-time.md`). Confundidor critico: chamada nativa so para lista fechada de modelos; demais (incl. o do PCC) caem no **XML textual legado** — diferenca de interface (Camada 1) confundida com diferenca de *harness*, a declarar nas limitacoes; infla tokens por construcao (schema XML no prompt a cada chamada).

## Contabilidade

Compactacao agentica (padrao) descarta o chunk de uso — tokens invisiveis em toda superficie (usar `--compaction basic|off` ou rejeitar runs contaminadas via `notice auto_compaction`). Retries de resposta vazia (middleware com Ollama em mente) contam tokens sem contar passo. `run_result` NDJSON: `usage`/`aggregateUsage` (5 campos), `iterations`, `durationMs` (run do agente, nao wall). Custo local 0; cache sempre 0.

## No PCC

Braco historico da matriz (substituido no desenho atual pelo par pi/oh-my-pi + *harness* zero + terceiros via executor). Nao aparece nos artigos-ancora (busca: zero ocorrencias).

## Contradictions

Nenhuma registrada.
