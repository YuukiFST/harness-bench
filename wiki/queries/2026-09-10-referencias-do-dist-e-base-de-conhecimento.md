---
title: 2026-09-10 referencias do dist e base de conhecimento
type: query
summary: Mapa das 26 referencias do PCC, PDFs baixados e paginas da wiki
tags: [referencias, dist, mapa]
created: 2026-09-10
updated: 2026-09-14
sources: [wiki/sources/agentic-harness-engineering-lin-2026.md, wiki/sources/deepswe-huang-2026.md, wiki/sources/frontierharness-runta-2026.md, wiki/sources/scaffolding-matters-alier-forment-2026.md]
---

> Histórico: descreve o desenho anterior a 2026-09-14 (harness zero, oh-my-pi, DeepSWE). O desenho vigente está em `docs/spec/11-experimental-protocol.md`.

# Referencias do `dist/` e base de conhecimento — as of 2026-09-10

## O que foi feito

`dist/projeto-pcc.docx` (26 refs) e `dist/atividade-introducao-e-citacoes.docx` (17 refs) extraidos do XML; fonte da verdade e o `.docx` (gerador parado em cc15d7b). 14 arXiv + e-book Feevale baixados para `raw/sources/` (PDFs validos, ~50 MB); conversao fiel via `bin/pdf-to-md.py` (PyMuPDF, duas colunas, tabelas). Wiki Omoikane instalada na raiz: `AGENTS.md` (com Dominio PCC), `prompts/`, `bin/wiki-*.py`, `.opencode/command`, `.claude/skills`, `index.md`, `log.md`, `_review.md`.

## Artigos-ancora

[[agentic-harness-engineering-lin-2026]] (24,7 pp, [[succ-mtok]]) e [[code-as-agent-harness-ning-2026]] (3 camadas, lacunas 5.2.1/5.2.7) — ver [[agent-harness]].

## Custo com modelo fixo

[[scaffolding-matters-alier-forment-2026]] (20x, 139x) > [[frontierharness-runta-2026]] (17x por pass) > [[stop-comparing-harness-zhang-2026]] (HV/MV 7,8x) > [[holistic-agent-leaderboard-kapoor-2025]] (34-48 pp) > [[ai-agents-that-matter-kapoor-2024]] (~100x HumanEval). Sintese: [[binding-constraint-thesis]], [[atribuicao-harness-vs-modelo]].

## Metodo

[[adding-error-bars-miller-2024]] (pareado, SE, n) + [[stop-comparing-harness-zhang-2026]] (grid 2x2) + [[deepswe-huang-2026]] (travado) + [[scaffolding-matters-alier-forment-2026]] (resolucao 2x) = [[desenho-experimental-harness-fixo]]. Medicao: [[medicao-custo-proxy-vs-relato]]. Oraculo: [[adequacao-oraculo]]. Inversao: [[especificidade-modelo-inversao]].

## Fundacoes e bracos

[[swe-bench-jimenez-2023]], [[swe-agent-yang-2024]], [[react-yao-2022]], [[lost-in-the-middle-liu-2023]]; [[pi-coding-agent]], oh-my-pi (pagina retirada em 2026-09-14), [[opencode]], cline (pagina retirada em 2026-09-14), harness-zero (pagina retirada em 2026-09-14); datacurve (pagina retirada em 2026-09-14), [[runta]], [[pier-datacurve-2026]], [[zen-opencode-2026]], [[harnessrank-2026]].

## Normas e aula

[[aula-5-citacoes-referencias]], [[estrutura-projeto-template-ifmt-2022]], [[metodologia-prodanov-freitas-2013]].

## Pendencias (ver `_review.md`)

Todas fechadas em 2026-09-14: denominadores de Zhang/HAL conferidos nos PDFs ([[stop-comparing-harness-zhang-2026]], [[holistic-agent-leaderboard-kapoor-2025]]); Lakatos/Marconi nao esta na lista; data de entrega resolvida em 2026-09-10; `tools/build_pcc.py` aposentado em `tools/legacy/`.
