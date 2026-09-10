---
title: Holistic Agent Leaderboard (Kapoor et al., 2025)
type: source
summary: HAL com 21.730 rollouts; scaffolds movem 34-48 pp e front open-source vence
tags: [leaderboard, hal, pareto, scaffold, generalista, gaming]
created: 2026-09-10
updated: 2026-09-10
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
- Mesmo modelo, outro *scaffold* (SWE-bench Verified Mini): **34 pp** Claude Sonnet 4.5 (68%->34%), **34 pp** GPT-5 Medium (46%->12%), **~48 pp** o4-mini.
- Mind2Web: SeeAct+GPT-5 $171 vs Browser-Use+Claude $1.577 (**9x**) para ~2 pp; Claude vai melhor com BrowserUse, OpenAI com SeeAct (**interacao**).
- Generalista (smolagents) vs especifico: perde 9/12 (CORE-Bench Hard) e 11/12 (SWE Mini); mais barato em 20/24 comparacoes.
- Raciocinio maior reduz acuracia em 21/36 combinacoes; correlacao tokens-acuracia positiva em 6/9.
- Gaming auditado: buscar o gabarito no HuggingFace, hard-codar solucoes, vazamento few-shot do TAU ($1k perdidos).

## Limitacoes (Apendice A3-A5)

Majoritariamente single-run sem IC (custo); provedores trocam pesos por tras do endpoint; niveis de reasoning incomparaveis; latencia nao medida sob paralelismo; 142/186 matriz (Opus 4.1 Mind2Web omitido por ~$20k).

## Uso no PCC

- Precedente de H1 em fronteira custo: Pareto USD + tokens; o mais barato domina a fronteira.
- Desenho fatorial modelo x *scaffold* x benchmark com contraste generalista — prefigura H2; priors de effect-size.
- Taxonomia failed/discarded/tampered + auditoria de trajetorias (licao TAU/HuggingFace).
- Checklist de ameacas: pinar endpoints, datar precos, pre-registrar n, nao comparar reasoning cross-provider.
- Ressalva permanente do PCC (efeito especifico do modelo, pode inverter): BrowserUse x SeeAct.

## Contradictions

- Com DeepSWE sobre tokens x acuracia (positivo em 6/9 vs sem correlacao no DeepSWE): ver [[atribuicao-harness-vs-modelo]].
