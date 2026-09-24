---
title: Pi Coding Agent
type: entity
summary: Braco do projeto; harness minimo de Mario Zechner, 4 ferramentas, sem MCP nem subagentes
tags: [pi, harness, bracos, minimalismo]
created: 2026-09-10
updated: 2026-09-23
sources: [wiki/sources/pi-earendil-2026.md, wiki/sources/scaffolding-matters-alier-forment-2026.md, wiki/sources/frontierharness-runta-2026.md, wiki/sources/harnesstax-pan-2026.md, wiki/sources/sol-pi-liu-2026.md]
---

# Pi Coding Agent

*Harness* minimo de Mario Zechner, publicado pela Earendil Inc. Repositorio canonico: `github.com/earendil-works/pi` (pacote `packages/coding-agent`); npm `@earendil-works/pi-coding-agent`. Auto-descricao (source: [[pi-earendil-2026]]): "Pi is a minimal agent harness."

## Configuracao

Padrao: `read`, `write`, `edit`, `bash` (+ `grep`, `find`, `ls` disponiveis); system prompt + ferramentas **<1.000 tokens**. Sem MCP, sem subagentes, sem plan mode, sem permissoes, sem checkpoint — por decisao. Com compactacao (`reserveTokens`, `keepRecentTokens`, `/compact`), skills, extensoes TS, `AGENTS.md`/`CLAUDE.md`/`SYSTEM.md`. Aponta a base URL OpenAI-compativel via `~/.pi/agent/models.json`.

## Evidencia externa

- Databricks (*apud* Earendil): >2x custo com qualidade igual entre *harnesses*; Pi ~3x menos contexto por turno (source: [[pi-earendil-2026]]).
- Alier: Pi 14.660 tokens/4-4, mais barato da matriz CLI (source: [[scaffolding-matters-alier-forment-2026]]).
- FrontierHarness: Pi 60,0%/$2,43; na tarefa-exemplo passa a $2,50 em 90 turnos vs $64,36/381 do Claude Code (source: [[frontierharness-runta-2026]]).
- HarnessTax (7 modelos, SWE-bench Lite e Terminal-Bench 2.0, 30 tarefas x 3 execucoes, precos de 1 set. 2026): Pi na fronteira de Pareto nos dois benchmarks com quatro ferramentas; Claude Code custa ~2,0x o Pi no SWE-bench Lite e 1,5x no Terminal-Bench 2.0 (media geometrica); Claude Fable 5 faz 96,7% no Pi a $0,67 vs 97,8% no Claude Code a $1,33, com 15,4 vs 15,3 turnos; contexto inicial do Claude Code passa de 10x o do Pi nos 7 modelos; GPT-5.6 Sol faz 83,3% no Pi vs 78,9% no Codex no Terminal-Bench 2.0 ($0,42 vs $0,76) (source: [[harnesstax-pan-2026]]).
- SoL-Pi: no EdgeBench com GPT-5.6 Sol, Pi tem o maior *score* e o melhor $/*score* entre seis *harnesses* publicos (44,833; $1.339; 0,5855 $/ponto). Quatro extensoes do Pi achadas por auto-pesquisa (*Action Fusion*, *Online Context Compact*, *ObservationPack*, *Evidence-Preserving Reducer*) cortam 49,0% (GPT-5.6 Sol) e 44,7% (Opus 5) dos tokens e cerca de 1/3 do custo, com 93,7% e 94,3% do *score* do Pi (source: [[sol-pi-liu-2026]]).

## No projeto

Um dos dois bracos (com [[opencode]]) desde 2026-09-14: constroi o [[finn]] do zero, da mesma especificacao, unidade a unidade, via `pi --mode json` apontando `models.json` para o *proxy*. Camada 1: 5.676 bytes / 1.228 tokens / 4 schemas na primeira requisicao (Pi 0.80.10, 28 ago. 2026), +555 bytes por passo. Referencia no projeto: Earendil (2026). Ver [[atribuicao-harness-vs-modelo]] e [[desenho-experimental-harness-fixo]].

## Contradictions

Nenhuma registrada. Nota de medida, sem conflito: [[pi-earendil-2026]] fala em ~3x menos contexto por turno (*apud* Databricks) e [[harnesstax-pan-2026]] em mais de 10x menos contexto na primeira chamada frente ao Claude Code; sao metricas diferentes.
