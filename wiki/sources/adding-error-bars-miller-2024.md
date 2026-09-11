---
title: Adding Error Bars to Evals (Miller, 2024)
type: source
summary: Estatistica de evals; diferencas pareadas, SE clusterizado e n>=1000
tags: [estatistica, pareado, wilcoxon, variancia, poder, mde]
created: 2026-09-10
updated: 2026-09-11
dated: 2024-11-01
sources: []
---

# Adding Error Bars to Evals (Miller, 2024)

## Identificacao

- Titulo: *Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations*.
- Autor: Evan Miller (Anthropic).
- arXiv:2411.00640v1 [stat.AP], 1 nov 2024 (capa: 4 nov 2024). 14 paginas.
- *Preprint*, nao revisado por pares.
- PDF: `raw/sources/2411.00640-miller-adding-error-bars.pdf`.

## Referencia ABNT (como citada no PCC)

MILLER, Evan. **Adding error bars to evals**: a statistical approach to language model evaluations. arXiv:2411.00640, 2024. *Preprint*, nao revisado por pares. Disponivel em: https://arxiv.org/abs/2411.00640. Acesso em: 28 ago. 2026.

## Receitas (5 recomendacoes, Secao 1)

1. SE da media pelo TLC; 2. SE clusterizado em grupos relacionados; 3. reducao de variancia por reamostragem K e next-token probs; 4. inferencia nas **diferencas pareadas** por questao, nao nas medias agregadas; 5. power analysis (n e MDE).

## Numeros-guia

- Cluster real: DROP SE x3,05 (1,34 vs 0,44); MGSM x1,88 — ignorar cluster estreita o IC indevidamente; Bernoulli em escore fracionario alarga indevidamente.
- Reamostragem (dificuldade uniforme): K=1->2 corta 1/3 da variancia; K=4 corta 1/2; limite 2/3. Regra: subir K ate E[σ2]/K << Var(x). SE sobre KxN respostas agregadas e inconsistente.
- Pareado (correlacao 0,5): corta 1/3 da variancia do estimador; exemplo ficticio mostra vencedor aparente revertendo apos pareado+cluster.
- Poder: exemplo ω2=1/9, δ=0,03 => **n≈969 (~1.000 questoes)**; com n=198 fixo, K=1->10 corta MDE de 13,2% para 7,5%.
- **Nao** mexer na temperatura para reduzir variancia (pode triplicar/quintuplicar a variancia e deslocar a media).

## Uso no PCC

- Licenca estatistica do teste de Wilcoxon pareado por tarefa sobre Succ/Mtok (α=0,05, bilateral): analisar diferencas por tarefa, reportar SE pareado + correlacao + IC95% no formato Tabela 5.
- Reportar media (SE) + n (+ clusters), MDE pre-registrada (~0,81σ com n=3 e 8 tarefas).
- Protocolo de reamostragem sem vies: K por tarefa com media no nivel da tarefa; parametros de amostragem registrados, nao normalizados (gateway nao os honra).

### Auditoria de conteudo 2026-09-11

- Citada em: §3 [63], [64], [65].
- Afirmacao sustentada: nao mexer na temperatura (§3.3); reamostragem (§3.1); diferenca pareada por questao (§1, §4.2).
- Veredito: CONCRETA. Detalhe em [[2026-09-11-auditoria-conteudo-referencias-pcc]].

