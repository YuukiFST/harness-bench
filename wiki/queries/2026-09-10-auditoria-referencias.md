---
title: Auditoria das referencias do projeto citacao lista e tema
type: query
summary: 26 refs conferem citacao a citacao; numeros batem; tema alinhado com 2 lacunas
tags: [auditoria, referencias, tema, nbr]
created: 2026-09-10
updated: 2026-09-14
sources: [wiki/sources/scaffolding-matters-alier-forment-2026.md, wiki/sources/frontierharness-runta-2026.md, wiki/sources/agentic-harness-engineering-lin-2026.md, wiki/sources/deepswe-huang-2026.md, wiki/sources/pi-earendil-2026.md]
---

> Histórico: descreve o desenho anterior a 2026-09-14 (harness zero, oh-my-pi, DeepSWE). O desenho vigente está em `docs/spec/11-experimental-protocol.md`.

# Auditoria das referencias do projeto — as of 2026-09-10

Metodo: paragrafos do corpo extraidos de `word/document.xml` de `dist/projeto-de-pesquisa.docx`; cada citacao com ano cruzada com as 26 entradas; cada fato checado contra a wiki.

## Citacao x lista: 26 de 26, zero orfaos

Toda citacao do corpo tem entrada, e toda entrada e citada (regra da Aula 3). `Databricks (2026)` aparece so via `apud Earendil` e corretamente **fora** da lista (só a obra consultada entra). O `.docx` da atividade (17 refs) tambem fecha com o proprio corpo.

## Fatos: batem com as fontes

FrontierHarness 50,0-66,7% e 17x ($1,05-$18,34); Alier 139x e 5,0-28x; Lin 24,7 pp; Databricks >2x mesma qualidade (*apud* Earendil, verbatim do post); DeepSWE 113/91, 5,5x, §8 binario; HAL BrowserUse/SeeAct; Runta 25,0% vs 67,8%; Miller (termostato, reamostragem, pareado); Camada 1 (11,4x, 64.945/5.676, 54 bytes, 2.526 bytes). Niveis: preprint rotulado onde sem venue; ICLR/NeurIPS/TACL onde ha. `et al.` com 4+ autores, conforme Aula 5.

## Ressalvas (nenhuma derruba)

- "Harness determina o desempenho mais que o modelo" ([52]) e sintese sem o escopo de Zhang (longo horizonte, modelos comparaveis) — mas [55] traz a ressalva de inversao; recomendo qualificar em [52].
- "Primeira comparacao com linhagem fixa" ([27]): vale para *fork* direto; Alier pi-vs-Tau e reimplementacao independente, nao *fork* — uma frase resolve.
- MDE ~0,81σ ([65]): calculo do autor, nao verificavel nas fontes; manter como pre-registro, nao como achado.
- Marcadores `[A MEDIR/A VERIFICAR/A DEFINIR]` e cronograma relativo: pendentes do orientador (ja em `_review.md`).

## Tema vs intencao do autor: alinhado, 2 lacunas

Custo por tarefa + taxa de sucesso com modelo fixo, desenvolvedor como destinatario, Claude Code e Codex cobertos pelo FrontierHarness. Lacunas: **Cursor** sem evidencia em nenhuma fonte (so adaptador do Pier); "vagas pedem" sem fonte, retirada do texto e da wiki em 2026-09-14.
