---
title: Lost in the Middle (Liu et al., 2023)
type: source
summary: Curva em U no uso de contexto longo; pior caso abaixo do closed-book
tags: [contexto, posicao, u-shape, recuperacao, compactacao]
created: 2026-09-10
updated: 2026-09-11
dated: 2023-11-20
sources: []
---

# Lost in the Middle (Liu et al., 2023)

## Identificacao

- Titulo: *Lost in the Middle: How Language Models Use Long Contexts*.
- Autores: Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang (Stanford, Berkeley, Samaya).
- arXiv:2307.03172v3 [cs.CL], 20 nov 2023. Publicado em **TACL**.
- PDF: `raw/sources/2307.03172-liu-lost-in-the-middle.pdf`.

## Referencia ABNT (como citada no projeto)

LIU, Nelson F.; LIN, Kevin; HEWITT, John; PARANJAPE, Ashwin; BEVILACQUA, Michele; PETRONI, Fabio; LIANG, Percy. **Lost in the middle**: how language models use long contexts. arXiv:2307.03172, 2023. Publicado em Transactions of the Association for Computational Linguistics (TACL). Disponivel em: https://arxiv.org/abs/2307.03172. Acesso em: 28 ago. 2026.

## Achado (verbatim, legenda Fig. 1)

> "Changing the location of relevant information within the language model's input context results in a U-shaped performance curve."

Modelos usam melhor o inicio (primazia) e o fim (recencia); o meio degrada mesmo em modelos de contexto longo. Pior caso do GPT-3.5-Turbo em 20-30 docs cai **>20% e abaixo do closed-book (56,1%)**.

## Numeros (QA multi-documento, 2.655 queries NQ-Open, greedy)

- GPT-3.5-Turbo 20 docs, ouro nas posicoes 0/4/9/14/19: 75,8 / 57,2 / 53,8 / 55,4 / 63,2%.
- Extendido ~= base (curvas sobrepostas; janela maior nao implica usar melhor).
- Chave-valor 300 pares: Claude ~perfeito; GPT-3.5-Turbo-16K com query antes+depois: perfeito vs 45,6% pior caso sem.
- Flan-UL2 dentro da janela de treino: so 1,9 pp best-worst (robusto); fora, vira U.
- Open-domain: >20 docs agregam ~1-1,5 pp ao leitor e muito custo/latencia — leitor satura antes do recall.

## Uso no projeto

- Camada 1 mediu compactacao silenciosa do oh-my-pi (troca de resultado antigo por referencia de 54 bytes no passo 5 sem pressao): este artigo da o mecanismo pelo qual isso pode custar desempenho alem do custo.
- Justifica condicoes de compactacao/truncacao e o padrao de reportar melhor/pior por posicao, nao so media.
- Mecanismo de H1: contexto maior eleva tokens e pode *reduzir* acuracia — Succ/Mtok precisa cair.

### Auditoria de conteudo 2026-09-11

- Citada em: nenhuma.
- Afirmacao sustentada: (nenhuma; gancho da Camada 1 removido em 2026-09-11).
- Veredito: NÃO CITADA; fora do tema. Detalhe em [[2026-09-11-auditoria-conteudo-referencias]].

