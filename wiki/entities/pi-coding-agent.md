---
title: Pi Coding Agent
type: entity
summary: Harness minimo de Mario Zechner; 4 ferramentas, sem MCP nem subagentes
tags: [pi, harness, bracos, minimalismo]
created: 2026-09-10
updated: 2026-09-10
sources: [wiki/sources/pi-earendil-2026.md, wiki/sources/scaffolding-matters-alier-forment-2026.md, wiki/sources/frontierharness-runta-2026.md]
---

# Pi Coding Agent

*Harness* minimo de Mario Zechner, publicado pela Earendil Inc. Repositorio canonico: `github.com/earendil-works/pi` (pacote `packages/coding-agent`); npm `@earendil-works/pi-coding-agent`. Auto-descricao (source: [[pi-earendil-2026]]): "Pi is a minimal agent harness."

## Configuracao

Padrao: `read`, `write`, `edit`, `bash` (+ `grep`, `find`, `ls` disponiveis); system prompt + ferramentas **<1.000 tokens**. Sem MCP, sem subagentes, sem plan mode, sem permissoes, sem checkpoint — por decisao. Com compactacao (`reserveTokens`, `keepRecentTokens`, `/compact`), skills, extensoes TS, `AGENTS.md`/`CLAUDE.md`/`SYSTEM.md`. Aponta a base URL OpenAI-compativel via `~/.pi/agent/models.json`.

## Evidencia externa

- Databricks (*apud* Earendil): >2x custo com qualidade igual entre *harnesses*; Pi ~3x menos contexto por turno (source: [[pi-earendil-2026]]).
- Alier: pi 14.660 tokens/4-4, mais barato da matriz CLI (source: [[scaffolding-matters-alier-forment-2026]]).
- FrontierHarness: Pi 60,0%/$2,43; na tarefa-exemplo passa a $2,50 em 90 turnos vs $64,36/381 do Claude Code (source: [[frontierharness-runta-2026]]).

## No PCC

Polo original do par de H2; um dos bracos da Camada 1 (5.676 bytes / 1.228 tokens na primeira requisicao). Sem adaptador no executor — escrito neste projeto. Ver [[oh-my-pi]] e [[atribuicao-harness-vs-modelo]].

## Contradictions

Nenhuma registrada.
