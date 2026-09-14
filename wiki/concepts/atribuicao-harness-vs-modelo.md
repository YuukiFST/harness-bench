---
title: Atribuicao Harness vs Modelo
type: concept
summary: Lacuna central: dispersoes agregam tudo sem separar; fork fixo isola
tags: [atribuicao, lacuna, fork, variancia]
created: 2026-09-10
updated: 2026-09-14
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

Desde 2026-09-14 o PCC compara dois *harnesses* de codigo aberto, [[opencode]] e [[pi-coding-agent]], construindo o mesmo produto ([[finn]]) do zero, a partir da mesma especificacao, unidade a unidade. A atribuicao e feita pelo lado da medicao: em cada requisicao o *proxy* separa a carga fixa do *harness* (prompt de sistema + schemas, medida na Camada 1: OpenCode 29.997 bytes / 9 schemas vs pi 5.676 / 4) do conteudo da conversa. H2 afirma que a carga fixa explica a maior parte da diferenca de tokens por *ticket*; e refutada se o numero de passos explicar a maior parte (o *harness* com mais ferramentas pode compensar em menos passos). Nulo e achado reportavel. Ver [[desenho-experimental-harness-fixo]].

## Contradictions

- C1 modelo-dirige vs *harness*-domina: [[deepswe-huang-2026]] Secao 2 (citando Merrill 2026: modelo dirige mais que *scaffold*) vs [[stop-comparing-harness-zhang-2026]] (HV/MV 7,80x, 6/9 reversoes) vs [[holistic-agent-leaderboard-kapoor-2025]] (30-48 pp, execucao unica). Leitura: o piloto DeepSWE n=10 e impotente (Wilson [17-69]%); nao importar o "modelo dirige" como geral — testar no proprio par com reversoes. Posicao do PCC (2026-09-14): nenhuma antes de H1. O projeto nao afirma que o *harness* domina nem que o modelo dirige; H1 testa a diferenca entre OpenCode e pi no proprio par e por nivel de modelo, e a tensao fica registrada aqui sem vencedor.
- C2 tokens x acuracia: [[deepswe-huang-2026]] ("mais tokens/tempo/custo nao resolve consistentemente mais") vs [[holistic-agent-leaderboard-kapoor-2025]] (correlacao positiva em 6/9). Leitura: condicionado a benchmark/metrica; estimar dentro do proprio conjunto fixo e reportar medianas + Pareto + custo-por-concluida.
- Minimal vs aditivo: [[scaffolding-matters-alier-forment-2026]] (reduzir vale ordens de magnitude) vs [[meta-harness-lee-2026]] (+80 linhas ganham). Leitura: objetivos diferem (custo vs acuracia); reportar Pareto conjunto.
- Resolucao: deltas de 1-2 pp sem variancia ([[meta-harness-lee-2026]], [[harness-handbook-wang-2026]]) nao passam no criterio ~2x de [[scaffolding-matters-alier-forment-2026]] — exigir repeticoes.
