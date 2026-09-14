---
title: Desenho Experimental com Harness Fixo
type: concept
summary: Dois bracos constroem o mesmo SaaS do zero, da mesma especificacao; tokens por construcao, pareado por unidade
tags: [metodo, pareado, wilcoxon, celula, unidade, construcao, finn]
created: 2026-09-10
updated: 2026-09-14
sources: [wiki/sources/adding-error-bars-miller-2024.md, wiki/sources/stop-comparing-harness-zhang-2026.md, wiki/sources/deepswe-huang-2026.md, wiki/sources/scaffolding-matters-alier-forment-2026.md, wiki/sources/harnessrank-2026.md]
---

# Desenho Experimental com Harness Fixo

Vocabulario (autoridade: `CONTEXT.md`): braco, nivel, especificacao, unidade, espaco de trabalho inicial, construcao (a run), celula (braco, nivel) com n construcoes, passo (round-trip no proxy), carga fixa, unidade nao concluida / adulterada, construcao descartada, oraculo, teste de aceitacao (held-out).

Desenho vigente desde 2026-09-14: os dois bracos, [[opencode]] e [[pi-coding-agent]], constroem o mesmo produto, o [[finn]], do zero, a partir da mesma especificacao congelada, sobre o mesmo modelo; compara-se o total de tokens por construcao. Desenhos anteriores retirados no mesmo dia: harness zero como controle, par pi / oh-my-pi e 8 tarefas do DeepSWE (manha); *tickets* isolados partindo de estados de referencia escritos pelo autor (tarde). A proposta do autor de deixar o OpenCode construir e gerar a especificacao para o pi foi descartada por entrada desigual (o pi receberia um documento destilado de um sistema pronto); ver `log.md` 2026-09-14.

## Especificacao e construcao

- Especificacao unica, escrita pelo autor a partir das *issues* fechadas do Finn antes de qualquer execucao e congelada por SHA-256: produto, pilha, restricoes gerais e 9 unidades em ordem de dependencia (#15 tenant, #16 governanca, #17 flags, #14 pipeline de voz, #20 confirmacao, #21 log, #19 relatorio, #18 agendador, #22 cobranca). Os testes de aceitacao nao estao nela.
- Construcao: espaco de trabalho inicial so com a especificacao e a pilha; o executor invoca o *harness* uma vez por unidade, em ordem, com prompt identico para os dois bracos; o que o agente construiu numa unidade e o ponto de partida da seguinte (conversa nao carrega, codigo sim). O autor nao escreve codigo depois do inicio. Entrada identica para os dois bracos e o que torna a diferenca de tokens atribuivel ao *harness*.
- Escore: fracao dos testes de aceitacao do autor, escritos antes da execucao e held-out (nunca a suite do agente; ver [[adequacao-oraculo]]), rodados sobre uma copia do espaco ao fim de cada unidade. Unidade concluida = todos os seus testes passam; construcao concluida = todos de todas as unidades passam ao fim.

## Grid

- Minimo valido 2x2 com ordem, ambiente, script, API e paradas constantes (source: [[stop-comparing-harness-zhang-2026]]).
- Celula = (braco, nivel), n>=3 construcoes apos descartes (reamostragem; source: [[adding-error-bars-miller-2024]]); cobertura antes de repeticoes se a cota apertar (truncar apos a unidade 6 so no nivel de robustez; nunca pular unidades do meio).
- Metrica primaria: tokens por construcao, sempre ao lado da fracao final de testes aprovados (braco que falha barato nao pode parecer o mais barato). Comparacao inferencial pareada por unidade: Wilcoxon bilateral α=0,05 sobre tokens por unidade e sobre [[succ-mtok]] por unidade (nao-parametrico p/ 9 pares; dificuldade da unidade e o maior confundidor). Unidades nao sao independentes (a seguinte parte do que o mesmo braco construiu); a dependencia de trajetoria e custo do *harness*, reportada por unidade. MDE ~0,76σ com n=3 e 9 unidades (2,80·σ·sqrt(2/27)). Predicoes pre-registradas por nivel; nulo de H2 e reportavel.
- H2: tokens de cada unidade decompostos em carga fixa (Camada 1 x passos) e conversa; parcela reportada por unidade e por construcao. Ver [[atribuicao-harness-vs-modelo]].
- Limite unico: relogio de parede por unidade, 3x a maior mediana dos dois bracos nas unidades-piloto; sem teto de passos (teto e decisao de *harness*); max-output igualado no proxy; amostragem registrada, nao normalizada.

## Classes

Por unidade. Nao concluida = resultado (entra com a fracao aprovada e a construcao segue; estouro do relogio conta como resultado). Descartada = medicao inconfiavel numa unidade descarta a construcao (sem reparo/repeticao, registrada). Classificacao pelo registro do proxy, nao pelo exit code (OpenCode e pi retornam 0 em falha total).

## Controles herdados

*Harness* travado + prompt compartilhado + regra de exclusao + SE run-to-run (source: [[deepswe-huang-2026]]); custo-condicionado + verificacao de comportamento + repeticoes com limite ~2x (source: [[scaffolding-matters-alier-forment-2026]]); timeout-como-resultado + descarte documentado (source: [[harnessrank-2026]]).

## Contradictions

Nenhuma interna; ver [[atribuicao-harness-vs-modelo]] sobre o que o grid pode e nao pode atribuir.
