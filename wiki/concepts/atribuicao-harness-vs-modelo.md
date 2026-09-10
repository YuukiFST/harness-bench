---
title: Atribuicao Harness vs Modelo
type: concept
summary: Lacuna central: dispersoes agregam tudo sem separar; fork fixo isola
tags: [atribuicao, lacuna, fork, variancia]
created: 2026-09-10
updated: 2026-09-10
sources: [wiki/sources/code-as-agent-harness-ning-2026.md, wiki/sources/scaffolding-matters-alier-forment-2026.md, wiki/sources/stop-comparing-harness-zhang-2026.md, wiki/sources/deepswe-huang-2026.md, wiki/sources/holistic-agent-leaderboard-kapoor-2025.md, wiki/sources/meta-harness-lee-2026.md]
---

# Atribuicao Harness vs Modelo

A primeira pendencia do PCC: toda comparacao publicada contrasta *harnesses* de equipes diferentes sobre fundacoes diferentes; a dispersao agrega prompt, ferramentas, contexto e laco sem separa-los (source: [[code-as-agent-harness-ning-2026]], Secao 5.2.1; pedido de metricas por componente em 5.2.7).

## O que cada fonte diz

- [[scaffolding-matters-alier-forment-2026]]: com linhagem solta, "What we cannot do is attribute the difference to MCP support specifically." Resposta parcial: controles sem MCP + verificacao de comportamento real.
- [[stop-comparing-harness-zhang-2026]]: decomposicao HV/MV + cartao ETCSOVG; distancia de *fork* direto e minima por construcao.
- [[deepswe-huang-2026]]: *harness* travado isola capacidade do modelo "at the cost of realism"; piloto n=10 direcional, sem significancia; futuro declarado: decompor modelo vs *scaffolding*.
- [[holistic-agent-leaderboard-kapoor-2025]]: fatorial modelo x *scaffold* x benchmark revela interacoes escondidas.
- [[meta-harness-lee-2026]]: +80 linhas sobre Terminus-KIRA ganham 7/89 tarefas — deltas de escala de *fork* sao reais e pequenos.

## Resposta do PCC

O par pi / [[oh-my-pi]] (fork direto, linhagem fixa) faz variar so as modificacoes — teste mais estrito que pi-vs-Tau (source: [[scaffolding-matters-alier-forment-2026]]). H2 e refutada se nao diferirem em [[succ-mtok]] apesar dos 11,4x bytes na primeira requisicao; nulo e achado reportavel.

## Contradictions

- C1 modelo-dirige vs *harness*-domina: [[deepswe-huang-2026]] Secao 2 (citando Merrill 2026: modelo dirige mais que *scaffold*) vs [[stop-comparing-harness-zhang-2026]] (HV/MV 7,80x, 6/9 reversoes) vs [[holistic-agent-leaderboard-kapoor-2025]] (34-48 pp). Leitura: o piloto DeepSWE n=10 e impotente (Wilson [17-69]%); nao importar o "modelo dirige" como geral — testar no proprio par com reversoes.
- C2 tokens x acuracia: [[deepswe-huang-2026]] ("mais tokens/tempo/custo nao resolve consistentemente mais") vs [[holistic-agent-leaderboard-kapoor-2025]] (correlacao positiva em 6/9). Leitura: condicionado a benchmark/metrica; estimar dentro do proprio conjunto fixo e reportar medianas + Pareto + custo-por-concluida.
- Minimal vs aditivo: [[scaffolding-matters-alier-forment-2026]] (reduzir vale ordens de magnitude) vs [[meta-harness-lee-2026]] (+80 linhas ganham). Leitura: objetivos diferem (custo vs acuracia); reportar Pareto conjunto.
- Resolucao: deltas de 1-2 pp sem variancia ([[meta-harness-lee-2026]], [[harness-handbook-wang-2026]]) nao passam no criterio ~2x de [[scaffolding-matters-alier-forment-2026]] — exigir repeticoes.
