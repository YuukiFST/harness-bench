---
title: OpenCode
type: entity
summary: Harness open-source; 47,2% no AHE e vazamento de chamada de titulo
tags: [opencode, harness, bracos, vazamento]
created: 2026-09-10
updated: 2026-09-14
sources: [wiki/sources/agentic-harness-engineering-lin-2026.md, wiki/sources/frontierharness-runta-2026.md, wiki/sources/zen-opencode-2026.md]
---

# OpenCode

*Harness* open-source (repo atual `github.com/anomalyco/opencode`; v1.17.9 na pesquisa). Ferramentas via Vercel AI SDK (`bash`, `edit`, `write`, `read`, `grep`, `glob`, `lsp`, `apply_patch`, `skill`, `todowrite`, `webfetch`, `websearch`, `question`); subagentes `general`/`explore`/`scout`; permissoes allow/ask/deny; compactacao; MCP; snapshots `/undo`.

## Evidencia

- AHE Tabela 1: **47,2%** pass@1 (GPT-5.4, Terminal-Bench 2) — unico braco do PCC com numero publicado, em modelo de fronteira (source: [[agentic-harness-engineering-lin-2026]]).
- Camada 1: 29.997 bytes / 6.659 tokens (9 schemas) na primeira requisicao; + chamada auxiliar de 2.526 bytes/sessao nao auto-reportada.
- Vazamentos (`docs/research/04`): titulo toda sessao (1 LLM call invisivel; mitigar `--title`); retries sem teto aparentemente perdidos; compactacao contada.
- FrontierHarness: 50,0%/$3,24 (source: [[frontierharness-runta-2026]]).
- Gateway dos dois niveis do PCC (source: [[zen-opencode-2026]]).

## No PCC

Um dos dois bracos (com [[pi-coding-agent]]) desde 2026-09-14: constroi o [[finn]] do zero, da mesma especificacao, unidade a unidade, via `opencode run --pure --format json` com provedor apontado ao *proxy*. Camada 1: 29.997 bytes / 6.659 tokens / 9 schemas (OpenCode 1.17.9, 28 ago. 2026), +698 bytes por passo; 5,3x os bytes do pi. `step_finish` = 1 round-trip (calibracao do proxy); hangs headless + exit 0 em falha exigem timeout externo e classificacao pelo proxy. Referencias no PCC: Opencode (2026a, repositorio) e Opencode (2026b, Zen). Ver [[medicao-custo-proxy-vs-relato]].

## Contradictions

Nenhuma registrada.
