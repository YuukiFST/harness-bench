---
title: SWE-bench (Jimenez et al., 2023)
type: source
summary: 2.294 issues reais em 12 repos Python; Claude 2 resolve 1,96%
tags: [benchmark, swe-bench, github-issues, baseline]
created: 2026-09-10
updated: 2026-09-11
dated: 2024-11-11
sources: []
---

# SWE-bench (Jimenez et al., 2023)

## Identificacao

- Titulo: *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*
- Autores: Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan (Princeton, Chicago).
- arXiv:2310.06770v3 [cs.CL], 11 nov 2024. Publicado na **ICLR 2024** (conferencia revisada por pares).
- PDF: `raw/sources/2310.06770-jimenez-swe-bench.pdf`.

## Referencia ABNT (como citada no PCC)

JIMENEZ, Carlos E.; YANG, John; WETTIG, Alexander; YAO, Shunyu; PEI, Kexin; PRESS, Ofir; NARASIMHAN, Karthik. **SWE-bench**: can language models resolve real-world GitHub issues? arXiv:2310.06770, 2023. Trabalho apresentado na International Conference on Learning Representations (ICLR), 2024. Disponivel em: https://arxiv.org/abs/2310.06770. Acesso em: 28 ago. 2026.

## Desenho

2.294 problemas de engenharia de issues + PRs reais em 12 repositorios Python (django 850, sympy 386, ..., flask 11). Modelo recebe texto da issue + codebase e edita o codigo; resolve se o patch aplica e todos os testes (fail-to-pass + pass-to-pass) passam. Metrica: % de instancias resolvidas.

## Numeros

- Melhor modelo nao-interativo: **Claude 2, 1,96%** (com retriever BM25).
- Estatisticas: issue media 195 palavras; codebase media 3.010 arquivos / 438K linhas; gold patch medio 32,8 linhas, 1,7 arquivos; 9,1 testes fail-to-pass medios.
- Split temporal pre/pos-2023 sem gap (controle de contaminacao).

## Limitacoes declaradas

So Python; baselines intencionalmente mais simples (retrieval, sem agentes — convite a agentes); testes de execucao sozinhos nao garantem qualidade (legibilidade, eficiencia).

## Uso no PCC

- Contraste fixo: teto nao-interativo ~2-4% define o piso que qualquer *harness* precisa bater com interacao.
- Split fail-to-pass/pass-to-pass como modelo de atribuicao ao *harness*.
- Diagnosticos de dificuldade (contexto longo, patches multi-arquivo) motivam H1.

### Auditoria de conteudo 2026-09-11

- Citada em: §3 [60] (comparador).
- Afirmacao sustentada: 2.294 instancias, 32,8 linhas por patch de referencia.
- Veredito: CONCRETA, uso minimo. Detalhe em [[2026-09-11-auditoria-conteudo-referencias-pcc]].

