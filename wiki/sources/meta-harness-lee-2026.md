---
title: Meta-Harness (Lee et al., 2026)
type: source
summary: Busca outer-loop sobre codigo do harness; +7,7 pp com 4x menos tokens
tags: [harness, otimizacao, outer-loop, terminal-bench, traces]
created: 2026-09-10
updated: 2026-09-11
dated: 2026-03-30
sources: []
---

# Meta-Harness (Lee et al., 2026)

## Identificacao

- Titulo: *Meta-Harness: End-to-End Optimization of Model Harnesses*.
- Autores: Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, Chelsea Finn (Stanford, MIT).
- arXiv:2603.28052v1 [cs.AI], 30 mar 2026. 26 paginas. HTML: <https://arxiv.org/html/2603.28052>.
- *Preprint*, nao revisado por pares.
- PDF: `raw/sources/2603.28052-lee-meta-harness.pdf`.

## Referencia ABNT (como citada no PCC)

LEE, Yoonho; NAIR, Roshen; ZHANG, Qizheng; LEE, Kangwook; KHATTAB, Omar; FINN, Chelsea. Meta-Harness: end-to-end optimization of model harnesses. arXiv:2603.28052, 2026. *Preprint*, nao revisado por pares. Disponivel em: https://arxiv.org/abs/2603.28052. Acesso em: 9 set. 2026.

## Definicao formal (verbatim, Secao 3)

> "A harness is a stateful program that wraps a language model and determines what context the model sees at each step."

Objetivo: H* = argmax sobre codigo do *harness*, com modelo M fixo. Tese (Secao 1, verbatim): "Changing the harness around a fixed large language model (LLM) can produce a 6x performance gap on the same benchmark."

## Numeros (modelo fixo por experimento)

- Classificacao textual online: **+7,7 pp com 4x menos tokens** (GPT-OSS-120B congelado; Meta-Harness 48,6% em 11,4K ctx vs ACE 40,9% em 50,8K). OOD: 73,1% vs 70,2%.
- Raciocinio matematico com recuperacao: **+4,7 pp media em 5 modelos held-out** (200 problemas IMO-level, pass@1 media de 3 amostras; 38,8 vs 34,1 sem retriever).
- Codificacao agentica: 76,4% no TerminalBench-2 (Opus 4.6) vs 74,7% Terminus-KIRA (+1,7); 37,6% (Haiku 4.5) vs 35,5% Goose (+2,1). **Sem repeticoes/variancia reportadas.**
- Ablacao: traces completos 50,0/56,7 (mediana/melhor) vs so-escores 34,6/41,3 — traces importam.
- Escala de feedback: ate 10M tokens de diagnostico por avaliacao (1000x otimizadores previos).

## Limitacoes declaradas

Busca e avaliacao final no mesmo TerminalBench-2 de 89 tarefas (sem split held-out para codigo); propositor unico forte (Claude Code + Opus-4.6); sem custo/token/variancia nos ganhos de codigo.

## Uso no PCC

- Referencial: definicao formal e objetivo com M fixo, adotaveis verbatim.
- Material e metodo: protocolo propose-evaluate-log em filesystem, Pareto acuracia vs custo, validacao leve — modelo para logging de runs/celulas.
- Cautela: PCC **nao** segue busca=avaliacao; mantem descoberta e confirmacao disjuntas.

### Auditoria de conteudo 2026-09-11

- Citada em: §2 [53].
- Afirmacao sustentada: 7,7 pontos com 4x menos tokens de contexto.
- Veredito: DIVERGENTE: resultado e em classificacao de texto *online* contra ACE, nao em codificacao. Detalhe em [[2026-09-11-auditoria-conteudo-referencias-pcc]].

## Contradictions

- Ganhos de codigo (+1,7/+2,1 pp sem variancia) nao passariam no criterio ~2x de [[scaffolding-matters-alier-forment-2026]]. Ver [[atribuicao-harness-vs-modelo]].
