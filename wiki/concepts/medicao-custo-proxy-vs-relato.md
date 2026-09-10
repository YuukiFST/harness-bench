---
title: Medicao de Custo Proxy vs Relato
type: concept
summary: Proxy externo conta tudo igual; cada harness omite chamadas diferentes
tags: [proxy, medicao, tokens, custo, instrumentacao]
created: 2026-09-10
updated: 2026-09-10
sources: [wiki/sources/ai-agents-that-matter-kapoor-2024.md, wiki/sources/scaffolding-matters-alier-forment-2026.md, wiki/sources/harnessrank-2026.md, wiki/sources/frontierharness-runta-2026.md]
---

# Medicao de Custo Proxy vs Relato

A segunda pendencia do PCC e de instrumentacao: o que um *harness* relata diverge do que gasta, e cada um omite um conjunto diferente de chamadas reais (source: [[ai-agents-that-matter-kapoor-2024]]: avaliacoes ignoram custo e erram a origem dos ganhos).

## Vazamentos conhecidos (pesquisa propria, `docs/research/04-measuring-tokens-steps-time.md`)

- OpenCode: chamada de titulo (primeiro passo, toda sessao) nunca registrada; retries sem teto aparentemente perdidos; compactacao **contada**.
- Cline: compactacao agentica descarta o chunk de uso (invisivel em toda superficie); retries contam tokens mas nao passos.
- PI: superficie de reporte nao verificada.
- Regra: proxy reverso entre braco e gateway, forca `stream_options: {include_usage: true}`, engole o frame de uso (harness ve stream identico), conta no proxy com um so tokenizador. Passo = um POST /v1/chat/completions 2xx com `finish_reason` terminal.

## Regras de medida (das fontes)

- Condicionar custo a conclusao; conclusao em separado; indefinido onde zero conclusoes (source: [[scaffolding-matters-alier-forment-2026]], Secao 2.8).
- Verificar comportamento real (aderencia a interface), nao auto-relato (sources: [[scaffolding-matters-alier-forment-2026]], [[frontierharness-runta-2026]]).
- Tokens sem cache para eficiencia; custo reportado, nao estimado; velocidade fora do ranking (source: [[harnessrank-2026]]).
- Objetivo (6) do PCC quantifica a divergencia relato-vs-proxy por braco.

## Armadilhas

- Gateway injeta conteudo e conta a mais (deslocamento aditivo por requisicao nao se cancela em razao); contagens do gateway ficam para verificacao cruzada e custo.
- Temperatura/seed omitidos viram defaults silenciosos distintos; `num_ctx` nao vai por /v1 (fixar `OLLAMA_CONTEXT_LENGTH`, verificar `ollama ps`).
- Cache: hit mediano != custo; falha longa cacheada queima mais que acerto curto (source: [[frontierharness-runta-2026]]).

## Contradictions

Nenhuma entre fontes; tensao pratica: instrumentar custa (handbook corta 8-13% de tokens do planner — reportar overhead em separado).
