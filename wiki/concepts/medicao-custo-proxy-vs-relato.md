---
title: Medicao de Custo Proxy vs Relato
type: concept
summary: Proxy externo conta tudo igual; cada harness omite chamadas diferentes
tags: [proxy, medicao, tokens, custo, instrumentacao]
created: 2026-09-10
updated: 2026-09-23
sources: [wiki/sources/ai-agents-that-matter-kapoor-2024.md, wiki/sources/scaffolding-matters-alier-forment-2026.md, wiki/sources/harnessrank-2026.md, wiki/sources/frontierharness-runta-2026.md, wiki/sources/harnesstax-pan-2026.md, wiki/sources/sol-pi-liu-2026.md]
---

# Medicao de Custo Proxy vs Relato

A segunda pendencia do projeto e de instrumentacao: o que um *harness* relata diverge do que gasta, e cada um omite um conjunto diferente de chamadas reais (source: [[ai-agents-that-matter-kapoor-2024]]: avaliacoes ignoram custo e erram a origem dos ganhos).

## Vazamentos conhecidos (pesquisa propria, `docs/research/04-measuring-tokens-steps-time.md`)

- OpenCode: chamada de titulo (primeiro passo, toda sessao) nunca registrada; retries sem teto aparentemente perdidos; compactacao **contada**.
- Cline: compactacao agentica descarta o chunk de uso (invisivel em toda superficie); retries contam tokens mas nao passos.
- PI: superficie de reporte nao verificada.
- Regra: proxy reverso entre braco e gateway, forca `stream_options: {include_usage: true}`, engole o frame de uso (harness ve stream identico), conta no proxy com um so tokenizador. Passo = um POST /v1/chat/completions 2xx com `finish_reason` terminal.

## Regras de medida (das fontes)

- Condicionar custo a conclusao; conclusao em separado; indefinido onde zero conclusoes (source: [[scaffolding-matters-alier-forment-2026]], Secao 2.8).
- Verificar comportamento real (aderencia a interface), nao auto-relato (sources: [[scaffolding-matters-alier-forment-2026]], [[frontierharness-runta-2026]]).
- Tokens sem cache para eficiencia; custo reportado, nao estimado; velocidade fora do ranking (source: [[harnessrank-2026]]).
- Custo como tokens x lista de precos fixa, igual para o mesmo modelo em todos os *harnesses* (precos de API direta de 1 set. 2026); contexto inicial pelos tokens de entrada relatados pelo provedor na primeira chamada; turnos pela definicao de cada *harness*, que os autores admitem nao ser comparavel (source: [[harnesstax-pan-2026]]).
- Trafego de tokens registrado em quatro parcelas (*input*, leitura de *cache*, escrita de *cache*, *output*) e custo por tabela de precos de 17 ago. 2026; eficiencia = custo por ponto de *score*. Cortar contexto reduz leitura de *cache* e aumenta escrita (GPT-5.6 Sol, EdgeBench: leitura 2,1326 -> 1,0605 B, escrita 0,0141 -> 0,0316 B, custo $1.339 -> $894), por isso a fonte pede custo total da tarefa, nao so taxa de reaproveitamento de *cache* (source: [[sol-pi-liu-2026]]).
- Objetivo (6) do projeto quantifica a divergencia relato-vs-proxy por braco.

## Armadilhas

- Gateway injeta conteudo e conta a mais (deslocamento aditivo por requisicao nao se cancela em razao); contagens do gateway ficam para verificacao cruzada e custo.
- Temperatura/seed omitidos viram defaults silenciosos distintos; `num_ctx` nao vai por /v1 (fixar `OLLAMA_CONTEXT_LENGTH`, verificar `ollama ps`).
- Cache: hit mediano != custo; falha longa cacheada queima mais que acerto curto (source: [[frontierharness-runta-2026]]).

## Contradictions

Tensao pratica: instrumentar custa (handbook corta 8-13% de tokens do planner — reportar overhead em separado).

- Custo relatado vs estimado, e *cache* dentro ou fora da eficiencia. [[harnessrank-2026]] adota custo reportado, nao estimado, e eficiencia por tokens sem *cache* (leituras de *cache* excluidas). [[harnesstax-pan-2026]] e [[sol-pi-liu-2026]] estimam custo por tabela de precos fixa, e [[sol-pi-liu-2026]] soma leitura de *cache* no trafego e argumenta que so o custo total da tarefa, com *cache*, mostra o efeito de compactar contexto. Registrado em `_review.md`.
