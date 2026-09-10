---
title: AI Agents That Matter (Kapoor et al., 2024)
type: source
summary: Avaliacao deve ser controlada por custo; Pareto acuracia-custo e holdouts
tags: [custo, pareto, holdout, reprodutibilidade, atribuicao]
created: 2026-09-10
updated: 2026-09-10
dated: 2024-07-01
sources: []
---

# AI Agents That Matter (Kapoor et al., 2024)

## Identificacao

- Titulo: *AI Agents That Matter*.
- Autores: Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, Arvind Narayanan (Princeton).
- arXiv:2407.01502v1 [cs.LG], 1 jul 2024. 33 paginas.
- *Preprint*, nao revisado por pares.
- PDF: `raw/sources/2407.01502-kapoor-ai-agents-that-matter.pdf`.

## Referencia ABNT (como citada no PCC)

KAPOOR, Sayash; STROEBL, Benedikt; SIEGEL, Zachary S.; NADGIR, Nitya; NARAYANAN, Arvind. **AI agents that matter**. arXiv:2407.01502, 2024. *Preprint*, nao revisado por pares. Disponivel em: https://arxiv.org/abs/2407.01502. Acesso em: 28 ago. 2026.

## Teses (verbatim)

- "agent evaluations must be cost-controlled; otherwise it will encourage researchers to develop extremely costly agents just to claim they topped the leaderboard."
- "Accuracy alone cannot identify progress because it can be improved by scientifically meaningless methods such as retrying."
- "Since papers proposing new agents haven't adequately tested simple baselines, it has led to widespread beliefs in the community that complex ideas like planning, reflection, and debugging are responsible for accuracy gains."

## Numeros (HumanEval 164, precos abr 2024, media de 5 runs)

- Warming-GPT-4 93,2% a $2,45 vs LATS-GPT-4 88,0% a $134,50: mesma acuracia, **~55x custo**; LATS custa 50x+ o warming.
- Escalation 85,0% a $0,27 domina LDB-GPT-3.5 (80,2%, $0,63).
- HotPotQA: otimizacao conjunta corta **53% (GPT-3.5) e 41% (Llama-3-70B)** do custo variavel com acuracia similar; break-even apos ~1.350 tarefas.
- Holdouts: 7/17 benchmarks sem holdout; so 5/10 no nivel certo de generalidade.
- Reprodutibilidade: SWE-bench 2.000+ tarefas x $4 = **>$8.000 por run** (sem repeticao/CI); escores acima do maximo de 5 runs; tarefas descartadas silenciosamente.

## Uso no PCC

- Precedente central de H1: mesmo modelo, so *harness* muda -> ~100x custo com acuracia empatada; fronteira de Pareto como figura de resultados; Succ/Mtok como metrica conjunta.
- Medicao: custo em dolar + tokens in/out recalculaveis, nunca proxies (n. parametros).
- H2/metodos: holdouts no nivel certo + scripts congelados + repeticoes (licao STeP/WebArena); separar custo fixo de tuning do custo variavel por run.
