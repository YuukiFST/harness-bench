---
title: FrontierHarness Eval (Runta, 2026)
type: source
summary: 9 harnesses x Kimi K3 fixo; pass 50-66,7% e custo 17x por pass
tags: [harness, leaderboard, custo-por-pass, kimi-k3, pi, oh-my-pi]
created: 2026-09-10
updated: 2026-09-14
dated: 2026-09-01
sources: []
---

# FrontierHarness Eval (Runta, 2026)

## Identificacao

- Titulo: *Introducing FrontierHarness Eval*. Autores: Shilin Zhu, Shiqi Mei (Runta).
- Blogue institucional, 1 set 2026, ~14 min. https://runta.com/blog/introducing-frontierharness-eval/
- Leaderboard: frontierharness.org. Dados + tarefas: github.com/frontier-harness-eval/eval.
- Publicacao de blogue institucional (nao revisada por pares).

## Referencia ABNT (como citada no projeto)

RUNTA. Introducing the FrontierHarness eval. 2026. Publicacao de blogue institucional. Disponivel em: https://runta.com/blog/introducing-frontierharness-eval/. Acesso em: 9 set. 2026.

## Desenho (modelo/tarefas/runtime constantes)

30 tarefas (21 Terminal-Bench + 9 DeepSWE) x 9 *harnesses* em 12 configuracoes = 360 trials, 1 tentativa por celula, checkpoint dourado restaurado por trial (vCPU, memoria, disco, **estado de memoria**), pass/fail por verificador deterministico, cache de primeiro turno reprecificado igual para todos. Modelo neutro Kimi K3 via Fireworks, gateway unico (Responses + Anthropic Messages). Debug nunca nas tarefas oficiais (cache de prefixo contamina por horas).

## Numeros

- Pass rates 50,0%-66,7% (17 pp); **custo mediano por pass $1,05-$18,34 (17x)**.
- Codex 66,7%/$3,47; DSH Creator 63,3%/$3,28; Claude Code 63,3%/**$18,34 (5,6x o DSH Creator no mesmo pass)**; Pi 60,0%/$2,43; Exo $1,05/53,3%; OpenCode 50,0%/$3,24; oh-my-pi 56,7%/$4,75.
- Tarefa-exemplo (python-statemachine, pass oficial 38%): Pi passa a **$2,50 em 90 turnos**; Claude Code passa a **$64,36 em 381 turnos (26x)**; 68% dos tokens do Claude Code numa so celula (cache 15,7% vs 98%+ dos demais).
- Cache hit mediano != custo: falha de 300 turnos cacheada queima mais que acerto curto sem cache.

## Origem de cada numero (2026-09-14)

Tres superficies publicam o FrontierHarness; o projeto cita o blogue (entrada RUNTA, 2026) e o repositorio, e nao cita o site.

- **Blogue** (https://runta.com/blog/introducing-frontierharness-eval/, relido em 14 set 2026): tabela "Pass Rate / Median Cost Per Pass" com as 12 configuracoes (Codex 66,7%/$3,47; DSH Creator 63,3%/$3,28; Claude Code 63,3%/$18,34; Pi 60,0%/$2,43; DSH Standard 60,0%/$3,46; DSH PTC 60,0%/$4,58; Kimi Code 56,7%/$3,65; DSH Minimal 56,7%/$4,72; Oh My Pi 56,7%/$4,75; Exo Harness 53,3%/$1,05; Hermes 50,0%/$2,90; OpenCode 50,0%/$3,24). Em prosa: "Claude Code and DSH Creator both pass 19 tasks. One costs $3.28 per pass, the other $18.34."; "Claude Code paid 5.6x more per pass"; "Claude Code's cache hit rate is 25.0% token-weighted and 67.8% by median cell."; "Pi and Claude Code both passed, with a 26x difference in price." Todos os numeros usados no projeto ([26], [52], [55]) vem daqui; 17,5x e 5,3x sao razoes calculadas pelo autor sobre a tabela.
- **Repositorio** (github.com/frontier-harness-eval/eval): tarefas, `results/eval-data.json` e a metrica `effective_cost_per_pass`; fonte das versoes dos *harnesses* (Pi v0.84.2, oh-my-pi v17.4.0, OpenCode v1.18.19, Claude Code v2.1.237, Codex v0.148.0) e do protocolo de restauracao.
- **Site** (frontierharness.org): tabela "median cost per successful task" ($0,06-$0,29) com base e unidade nao documentadas, incompativel com a tabela do blogue. Nao reconciliada contra `eval-data.json`; nao entra no projeto nem em pagina alguma da wiki como numero.

## Caveat (verbatim na essencia)

Resultado do Claude Code pode refletir interacao *harness*-modelo-gateway (cache implicito do K3 vs estrategia do Claude Code para Anthropic), nao o *harness* sozinho. Separar os efeitos e o item 1 da v1.1.

## Uso no projeto

- Justificativa: passar e passar barato sao habilidades separadas (Claude Code = DSH Creator em passes, 5,6x em custo).
- H2: Pi e oh-my-pi medidos no mesmo protocolo (60,0%/$2,43 vs 56,7%/$4,75) — ponto externo de comparacao para o experimento do projeto.
- Metodo: checkpoint dourado, 1 tentativa/celula, reprecificacao de cache, debug fora das oficiais.
- Limitacoes: cada *harness* como entregue, sem adaptar caching; matriz *harness* x modelo futura (v1.1).

### Auditoria de conteudo 2026-09-11

- Citada em: §1 [26]; §2 [52], [55].
- Afirmacao sustentada: 50,0-66,7% (12 configuracoes); $1,05-$18,34; Codex 66,7%/$3,47; Claude Code 63,3%/$18,34; cache 25,0% ponderado / 67,8% mediana por celula do Claude Code.
- Veredito: DIVERGENTE em [55] (67,8% nao e mediana entre *harnesses*); 17x e 5,3x sao calculos do autor (post diz 5,6x vs DSH Creator). Detalhe em [[2026-09-11-auditoria-conteudo-referencias]].

