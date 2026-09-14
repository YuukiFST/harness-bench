---
title: Holistic Agent Leaderboard (Kapoor et al., 2025)
type: source
summary: HAL com 21.730 rollouts; scaffolds movem 30-48 pp (execucao unica) e front open-source vence
tags: [leaderboard, hal, pareto, scaffold, generalista, gaming]
created: 2026-09-10
updated: 2026-09-14
dated: 2025-10-13
sources: []
---

# Holistic Agent Leaderboard (Kapoor et al., 2025)

## Identificacao

- Titulo: *Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation*.
- Autores: Sayash Kapoor, Benedikt Stroebl, Peter Kirgis *et al.* (31 total, Princeton *et al.*).
- arXiv:2510.11977v1 [cs.AI], 13 out 2025. 66 paginas.
- *Preprint*, nao revisado por pares.
- PDF: `raw/sources/2510.11977-kapoor-holistic-agent-leaderboard.pdf`.

## Referencia ABNT (como citada no PCC)

KAPOOR, Sayash *et al.* **Holistic Agent Leaderboard**: the missing infrastructure for AI agent evaluation. arXiv:2510.11977, 2025. *Preprint*, nao revisado por pares. Disponivel em: https://arxiv.org/abs/2510.11977. Acesso em: 28 ago. 2026.

## Escala

*Harness* padronizado orquestrando avaliacoes paralelas em centenas de VMs: **21.730 rollouts**, 9 modelos x 9 benchmarks (codigo, web, ciencia, atendimento), ~$40.000, 2,5B tokens de logs abertos. Achado (verbatim): "Agent scaffolds create drastic differences in cost and accuracy."

## Numeros

- Pareto: so 1/9 benchmarks tem o modelo mais caro na fronteira; Gemini 2.0 Flash aparece em 7/9, GPT-5 em 4/9; fronteira em tokens != fronteira em dolares.
- Mesmo modelo, outro *scaffold* (SWE-bench Verified Mini, 50 tarefas, SWE-Agent vs HAL Generalist, Tabela A19): **34 pp** GPT-5 Medium (46,0% -> 12,0%), **48 pp** o4-mini Low (54,0% -> 6,0%) e o4-mini High (50,0% -> 2,0%), **30 pp** Claude 3.7 Sonnet High (54,0% -> 24,0%). O par "Claude Sonnet 4.5 68% -> 34%" que circulava aqui nao consta do PDF v1 (13 out 2025) e foi retirado.
- Mind2Web: SeeAct+GPT-5 $171 vs Browser-Use+Claude $1.577 (**9x**) para ~2 pp; Claude vai melhor com BrowserUse, OpenAI com SeeAct (**interacao**).
- Generalista (smolagents) vs especifico: perde 9/12 (CORE-Bench Hard) e 11/12 (SWE Mini); mais barato em 20/24 comparacoes.
- Raciocinio maior reduz acuracia em 21/36 combinacoes; correlacao tokens-acuracia positiva em 6/9.
- Gaming auditado: buscar o gabarito no HuggingFace, hard-codar solucoes, vazamento few-shot do TAU ($1k perdidos).

## Verificacao no PDF (2026-09-14)

Conferido em `raw/sources/2510.11977-kapoor-holistic-agent-leaderboard.pdf` (pdftotext); VERIFICADO com correcao acima.

- Tabela A19 "SWE-bench Verified Mini Leaderboard" (p. 58): SWE-Agent GPT-5 Medium 46.0% / $162.93; HAL Generalist Agent GPT-5 Medium 12.0% / $57.58; SWE-Agent o4-mini Low 54.0% / $259.20; HAL Generalist o4-mini Low 6.0% / $87.03; SWE-Agent o4-mini High 50.0%; HAL Generalist o4-mini High 2.0%; SWE-Agent Claude-3.7 Sonnet High 54.0%; HAL Generalist Claude-3.7 Sonnet High 24.0%.
- Achado 6 (Secao 4): "on Online Mind2Web, SeeAct with GPT-5 Medium costs $171 while Browser-Use with Claude Sonnet 4 costs $1,577: a 9x difference in cost despite just a two-percentage-point difference in accuracy. [...] Claude models perform better with BrowserUse, while OpenAI models achieve higher accuracy with SeeAct."
- Achado 7: "task-specific CORE-Agent outperforms the generalist scaffold on 9 of 12 runs. A similar gap appears on SWE-bench Verified Mini (11 of 12). The generalist scaffolds also cost less in 20 of 24 model comparisons".
- Caveat de n (Secao 6): "For HAL, we were forced to rely on single runs without statistical validation for most evaluations." Apendice: "We use SWE-Bench Verified Mini (50 tasks) rather than the full". Todos os gaps acima sao de uma execucao, sem IC.

## Limitacoes (Apendice A3-A5)

Majoritariamente single-run sem IC (custo); provedores trocam pesos por tras do endpoint; niveis de reasoning incomparaveis; latencia nao medida sob paralelismo; 142/186 matriz (Opus 4.1 Mind2Web omitido por ~$20k).

## Uso no PCC

- Precedente de H1 em fronteira custo: Pareto USD + tokens; o mais barato domina a fronteira.
- Desenho fatorial modelo x *scaffold* x benchmark com contraste generalista — prefigura H2; priors de effect-size.
- Taxonomia failed/discarded/tampered + auditoria de trajetorias (licao TAU/HuggingFace).
- Checklist de ameacas: pinar endpoints, datar precos, pre-registrar n, nao comparar reasoning cross-provider.
- Ressalva permanente do PCC (efeito especifico do modelo, pode inverter): BrowserUse x SeeAct.

### Auditoria de conteudo 2026-09-11

- Citada em: §2 [54], [55].
- Afirmacao sustentada: custos raramente relatados, comparacoes entre *scaffolds* raras (§1); Claude melhor com BrowserUse, OpenAI com SeeAct em Online Mind2Web (§4.1).
- Veredito: CONCRETA. Detalhe em [[2026-09-11-auditoria-conteudo-referencias-pcc]].

## Contradictions

- Com DeepSWE sobre tokens x acuracia (positivo em 6/9 vs sem correlacao no DeepSWE): ver [[atribuicao-harness-vs-modelo]].
