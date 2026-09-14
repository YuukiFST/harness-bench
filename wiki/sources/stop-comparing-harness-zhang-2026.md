---
title: Stop Comparing LLM Agents Without Disclosing the Harness (Zhang et al., 2026)
type: source
summary: Binding Constraint Thesis e protocolo fatorial HV/MV com 7,8x de razao
tags: [harness, binding-constraint-thesis, variancia, metodologia, disclusao]
created: 2026-09-10
updated: 2026-09-14
dated: 2026-05-07
sources: []
---

# Stop Comparing LLM Agents Without Disclosing the Harness (Zhang et al., 2026)

## Identificacao

- Titulo: *Stop Comparing LLM Agents Without Disclosing the Harness*.
- Autores: Yunbei Zhang, Janet Wang, Yingqiang Ge, Weijie Xu, Jihun Hamm, Chandan K. Reddy (Tulane, Rutgers, Virginia Tech).
- arXiv:2605.23950v1 [cs.AI], 7 maio 2026. 17 paginas. Posicao teórica + fatorial controlado.
- *Preprint*, nao revisado por pares.
- PDF: `raw/sources/2605.23950-zhang-stop-comparing.pdf`.

## Referencia ABNT (como citada no PCC)

ZHANG, Yunbei; WANG, Janet; GE, Yingqiang; XU, Weijie; HAMM, Jihun; REDDY, Chandan K. **Stop comparing LLM agents without disclosing the harness**. arXiv:2605.23950, 2026. *Preprint*, nao revisado por pares. Disponivel em: https://arxiv.org/abs/2605.23950. Acesso em: 28 ago. 2026.

## Tese (Binding Constraint Thesis, verbatim)

> "For LLM agents operating on long-horizon tasks with comparable frontier models... HV is often comparable to or larger than MV, and may dominate it in many current long-horizon agent evaluations."

Onde HV(M) = Var_H[B(M,H)] (variancia entre *harnesses*, modelo fixo) e MV(H) = Var_M[B(M,H)] (variancia entre modelos, *harness* fixo). Corolario pratico (verbatim): "Until harness specifications are disclosed, leaderboard comparisons for long-horizon agents should be treated as incomplete and potentially misleading."

## Fatorial controlado (denominador completo)

3 modelos (GPT-5.4, Kimi K2.6, GLM-5.1, cluster 44,6-45,4 no leaderboard Abr 2026) x 3 *harnesses* (H1 Minimal, H2 Improved, H3 Full), 100 tarefas SWE-bench Verified estratificadas (seed 42), 2 runs por celula, ordem compartilhada, Docker, 50 passos, 120 s/passo. Resultado: HV media 18,48 pp2 vs MV media 2,37 pp2, razao **7,80x** (runs 8,72x e 6,76x). Mudanca de *harness* move +8,5 a +13,0 pp com modelo fixo; troca de modelo move 2,5 a 5,0 pp. **6 de 9** pares modelo/*harness* invertem ordenacao. Custo do grid: $215,79, 261,1M tokens, 84,4 h sequenciais.

## Verificacao no PDF (2026-09-14)

Numeros conferidos em `raw/sources/2605.23950-zhang-stop-comparing.pdf` (pdftotext), Secao 4 "Findings" e Tabela 2; VERIFICADO.

- "Average HV is 18.48 pp2 versus average MV of 2.37 pp2, a ratio of 7.80x. Changing the harness moves GLM-5.1 by 13.0 percentage points and GPT-5.4 and Kimi K2.6 by 8.5 points each. Changing the model within a fixed harness moves scores by only 3.0, 2.5, and 5.0 points for H1, H2, H3. The interaction term is visible as six ranking reversals across the nine possible model-pair / harness-pair comparisons." (Secao 4)
- "We do not claim that the 7.80x ratio is universal." (Secao 4)
- Tabela 2: "Cells report mean pass@1 percentages over two runs"; Apendice B, Tabela 7: "First run: mean HV = 20.67, mean MV = 2.37, HV/MV = 8.72x. Second run: mean HV = 16.52, mean MV = 2.44, HV/MV = 6.76x."
- Denominador: "subset100 with seed 42 and stratification by the SWE-bench difficulty label"; "50-step budget, and 120-second per-step timeout"; "Each model-harness cell submits all 100 tasks in each of two final runs." (Apendice B)
- Custo do grid: $215,79, 261,1M tokens, 84,4 h (tabela de custo, Apendice B).
- Os valores "69,7% -> 77,0%" e "9,5 pp" herdados de `docs/research/03` como NAO VERIFICADO **nao estao neste artigo**: 69,7% -> 77,0% e a campanha AHE de [[agentic-harness-engineering-lin-2026]] (Terminal-Bench 2, GPT-5.4); "9,5 pp" nao aparece em fonte alguma da wiki e fica descartado.

## Framework proposto

- Cartao de divulgacao ETCSOVG em 7 camadas (Execution, Tool, Context, Scheduling, Observability, Verification, Governance).
- Desenho minimo valido (verbatim): "a 2x2 model-by-harness grid with task order, execution environment, evaluation script, API parameters, and stopping rules held constant."
- Metricas de trajetoria: Recovery Rate RR(k), Context Retention, Control Lag τ.

## Limitacoes declaradas

Escopo restrito a longo horizonte + modelos de fronteira comparaveis; HV depende da amostragem de *harnesses*; eta2 com vies positivo em grids pequenos; metricas de trajetoria especificadas mas nao estimadas no grid.

## Uso no PCC

- Hipoteses/desenho: backbone estatistico de H1 (HV>0 em custo por tarefa concluida) e H2 (contraste *harness* vs *fork* com distancia ETCSOVG minima).
- Instrumentacao: cartao ETCSOVG como apendice de especificacao dos bracos.
- Ameacas: 6/9 reversoes obrigam relatar rankings por *harness*, nunca ranking unico.

### Auditoria de conteudo 2026-09-11

- Citada em: §2 [52].
- Afirmacao sustentada: tese formal condicionada a "comparable frontier models", "often comparable to or larger than", "may dominate" (§3); HV/MV 7,80x (§4).
- Veredito: DIVERGENTE: projeto omite os qualificadores. Detalhe em [[2026-09-11-auditoria-conteudo-referencias-pcc]].

## Contradictions

- Tensao com DeepSWE (que minimiza *scaffold* como segunda ordem sob *harness* travado): ver [[atribuicao-harness-vs-modelo]].
