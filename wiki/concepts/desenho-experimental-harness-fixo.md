---
title: Desenho Experimental com Harness Fixo
type: concept
summary: Grid pareado, n>=3, Wilcoxon sobre Succ-Mtok, H2 com fork direto
tags: [metodo, pareado, wilcoxon, celula, fork, run]
created: 2026-09-10
updated: 2026-09-10
sources: [wiki/sources/adding-error-bars-miller-2024.md, wiki/sources/stop-comparing-harness-zhang-2026.md, wiki/sources/deepswe-huang-2026.md, wiki/sources/scaffolding-matters-alier-forment-2026.md, wiki/sources/harnessrank-2026.md]
---

# Desenho Experimental com Harness Fixo

Vocabulario (autoridade: `CONTEXT.md`): braco, *harness* zero, nivel, run, celula (braco, tarefa, nivel) com n runs, passo (round-trip no proxy), run falhada / descartada / adulterada, tarefa, oraculo, teste visivel / held-out.

## Grid

- Minimo valido 2x2 com ordem, ambiente, script, API e paradas constantes (source: [[stop-comparing-harness-zhang-2026]]).
- Cada celula n>=3 apos descartes (reamostragem; source: [[adding-error-bars-miller-2024]]); cobertura antes de repeticoes se a cota apertar.
- Comparacao pareada por tarefa: Wilcoxon bilateral α=0,05 sobre [[succ-mtok]] (nao-parametrico p/ 8 pares; dificuldade da tarefa e o maior confundidor). MDE ~0,81σ com n=3 e 8 tarefas. Predicoes pre-registradas por nivel; nulo de H2 e reportavel.
- Limite unico: relogio de parede 3x a mediana do *harness* zero; sem teto de passos (teto e decisao de *harness*); max-output igualado no proxy; amostragem registrada, nao normalizada.

## Classes de run

Falhada = resultado (escore zero; estouro do relogio conta como resultado). Descartada = medicao inconfiavel (sem reparo/repeticao, registrada). Classificacao pelo registro do proxy, nao pelo exit code (OpenCode e PI retornam 0 em falha total).

## Controles herdados

*Harness* travado + prompt compartilhado + shallow clone + regra de exclusao + SE run-to-run (source: [[deepswe-huang-2026]]); custo-condicionado + verificacao de comportamento + repeticoes com limite ~2x (source: [[scaffolding-matters-alier-forment-2026]]); timeout-como-resultado + descarte documentado (source: [[harnessrank-2026]]).

## Contradictions

Nenhuma interna; ver [[atribuicao-harness-vs-modelo]] sobre o que o grid pode e nao pode atribuir.
