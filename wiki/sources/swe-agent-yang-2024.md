---
title: SWE-agent (Yang et al., 2024)
type: source
summary: Agent-Computer Interface leva GPT-4 a 12,47% no SWE-bench com modelo fixo
tags: [harness, aci, interface, swe-bench, custo]
created: 2026-09-10
updated: 2026-09-11
dated: 2024-11-11
sources: []
---

# SWE-agent (Yang et al., 2024)

## Identificacao

- Titulo: *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*.
- Autores: John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press (Princeton).
- arXiv:2405.15793v3 [cs.SE], 11 nov 2024. Publicado na **NeurIPS 2024** (38th, revisada por pares).
- PDF: `raw/sources/2405.15793-yang-swe-agent.pdf` (118 paginas com apendices).

## Referencia ABNT (como citada no PCC)

YANG, John; JIMENEZ, Carlos E.; WETTIG, Alexander; LIERET, Kilian; YAO, Shunyu; NARASIMHAN, Karthik; PRESS, Ofir. **SWE-agent**: agent-computer interfaces enable automated software engineering. arXiv:2405.15793, 2024. Trabalho apresentado na Conference on Neural Information Processing Systems (NeurIPS), 2024. Disponivel em: https://arxiv.org/abs/2405.15793. Acesso em: 28 ago. 2026.

## Tese (verbatim, Secao 2)

> "We refer to the interface LM agents use to interact with computers as the agent-computer interface (ACI)."

> "In this paper, we assume a fixed LM and focus on designing the ACI to improve its performance."

O ACI especifica comandos disponiveis e como o estado volta ao modelo. Loop em ReAct (pensamento + comando + feedback). Poucas acoes simples (ver, buscar, editar com lint, executar) superam o shell granular.

## Numeros (orcamento $4 por instancia)

- SWE-bench full (2.294): SWE-agent + GPT-4 Turbo **12,47% (286/2.294)** vs 3,79% RAG previo (+8,7 pp, estado da arte nao-interativo anterior).
- Lite (300): 18,00% vs 11,00% shell-only (+64% relativo) vs 2,67% RAG (6,7x).
- Custo medio por resolvida: RAG $0,13 vs SWE-agent $1,59-1,67.
- Ablacoes (Lite, base 18,0%): sem lint 15,0 (-3,0); sem edicao 10,3 (-7,7); busca iterativa 12,0 (-6,0); viewer arquivo cheio 12,7 (-5,3).
- Comportamento: mediana resolvida $1,21/12 passos vs nao-resolvida $2,52/21 passos; 93% das resolvidas submetem antes do orcamento.

## Limitacoes (Apendice E.3)

Toolkit pequeno; desenho do ACI manual (automatizar e futuro); escopo so em tarefas programaticas.

## Uso no PCC

- Primeira evidencia *harness*-como-interface com LM fixo: 2,67% -> 11% -> 18% no Lite isolam a contribuicao do *harness* (H1).
- Reagentes de custo para H2 (Succ/Mtok, pass@1 por dolar).
- Ablacoes rankeiam alavancas (lint, busca, viewer, historico) — definicoes de bracos.

### Auditoria de conteudo 2026-09-11

- Citada em: §2 [52].
- Afirmacao sustentada: ACI como objeto de projeto sem mudar pesos (§1); 11,00% -> 18,00% Lite com GPT-4 Turbo (Tabela 1).
- Veredito: CONCRETA. Detalhe em [[2026-09-11-auditoria-conteudo-referencias-pcc]].

