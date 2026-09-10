---
title: Agent Harness
type: concept
summary: Definicao canonica e componentes; o que varia com o modelo fixo
tags: [harness, definicao, componentes]
created: 2026-09-10
updated: 2026-09-10
sources: [wiki/sources/agentic-harness-engineering-lin-2026.md, wiki/sources/code-as-agent-harness-ning-2026.md, wiki/sources/meta-harness-lee-2026.md, wiki/sources/harness-handbook-wang-2026.md]
---

# Agent Harness

Definicao a citar (source: [[code-as-agent-harness-ning-2026]]): a camada de software que envolve um LLM com ferramentas, APIs, *sandboxes*, memoria, validadores, fronteiras de permissao, lacos de execucao e canais de realimentacao, convertendo um modelo sem estado em agente funcional de longo horizonte.

Definicao operacional (source: [[agentic-harness-engineering-lin-2026]]): o conjunto de componentes externos ao modelo e editaveis — system prompt, ferramentas, middleware de contexto/execucao/recuperacao. Definicao formal (source: [[meta-harness-lee-2026]]): programa com estado que envolve o modelo e determina o contexto que ele ve a cada passo.

## Componentes

Sete tipos ortogonais (NexAU, source: [[agentic-harness-engineering-lin-2026]]): system prompt, descricao e implementacao de ferramenta, middleware, skill, configuracao de subagente, memoria de longo prazo. Onze itens granulares (source: [[code-as-agent-harness-ning-2026]], Secao 3.5): schemas, artefatos de planejamento, politicas de memoria, retrieval, *sandbox*, sensores de verificacao, niveis de permissao, roteamento, workflows multiagente, gates humanos.

## Tres camadas (source: [[code-as-agent-harness-ning-2026]])

Interface (raciocinio/acao/ambiente), mecanismos (planejamento, memoria, ferramenta, controle PEV, otimizacao), escala (multiagente). O laco ReAct minimo e *harness* legitimo, o mais raso (source: [[react-yao-2022]]).

## O que varia no PCC

Com o modelo fixo, varia so o *harness*: prompt de sistema, numero/tamanho dos schemas, compactacao, permissoes, verificacao. Ver [[atribuicao-harness-vs-modelo]], [[medicao-custo-proxy-vs-relato]] e [[desenho-experimental-harness-fixo]].

## Contradictions

Ver [[atribuicao-harness-vs-modelo]] (tensao modelo-dirige vs *harness*-domina).
