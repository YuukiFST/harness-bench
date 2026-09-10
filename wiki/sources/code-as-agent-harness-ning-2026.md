---
title: Code as Agent Harness (Ning et al., 2026)
type: source
summary: Survey que define harness em 3 camadas e pede metricas que isolem componentes
tags: [harness, survey, metricas, oracle, pexels-loop]
created: 2026-09-10
updated: 2026-09-10
dated: 2026-05-18
sources: []
---

# Code as Agent Harness (Ning et al., 2026)

## Identificacao

- Titulo: *Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems*.
- Autores: Xuying Ning *et al.* (lista longa, ver PDF).
- arXiv:2605.18747v1 [cs.CL], 18 maio 2026. 102 paginas no PDF (survey).
- *Preprint*, nao revisado por pares.
- PDF: `raw/sources/2605.18747-ning-code-as-agent-harness.pdf`. HTML: <https://arxiv.org/html/2605.18747v1>.
- O Secao 3.5 do survey resume o proprio AHE (citado como `lin2026agentic`): os dois artigos-ancora **nao** sao confirmacoes independentes.

## Referencia ABNT (como citada no PCC)

NING, Xuying *et al.* **Code as agent harness**. arXiv:2605.18747, 2026. *Preprint*, nao revisado por pares. Disponivel em: https://arxiv.org/abs/2605.18747. Acesso em: 28 ago. 2026.

## Definicao a citar (verbatim EN, Secao 1)

> "An agent harness refers to the software layer that surrounds an LLM with tools, APIs, sandboxes, memory, validators, permission boundaries, execution loops, and feedback channels, thereby turning a stateless model into a functional agent capable of long-running task execution."

Traducao de trabalho: um *agent harness* e a camada de software que envolve um LLM com ferramentas, APIs, *sandboxes*, memoria, validadores, fronteiras de permissao, lacos de execucao e canais de realimentacao, convertendo um modelo sem estado em agente funcional de longo horizonte.

Tres elementos (Secao 1): *model-internal capabilities* (raciocinio, percepcao, planejamento), *system-provided harness infrastructure* (ferramentas, APIs, *sandboxes*, memoria, validadores, permissoes, telemetria — o foco da engenharia de *harness*), *agent-initiated code artifacts* (objetos de codigo que o agente cria, executa, revisa, persiste e compartilha).

## Tres camadas do survey

1. **Secao 2 — *Harness Interface***: codigo para raciocinio, acao e modelagem de ambiente.
2. **Secao 3 — *Harness Mechanisms***: planejamento, memoria/engenharia de contexto, uso de ferramenta, controle (laco Plan-Execute-Verify), otimizacao (AHE).
3. **Secao 4 — *Scaling***: orquestracao multiagente sobre artefatos de codigo compartilhados.

Sobre ReAct (Secao 3.1.1): "A lightweight precursor of this pattern is ReAct, where the agent interleaves thoughts, actions, and observations in a serial trajectory." Autorizacao textual para tratar o laco ReAct minimo como *harness* legitimo.

## Metricas de nivel de harness (verbatim, Secao 5.2.1)

> "Useful dimensions include: (i) *trajectory efficiency*, such as number of tool calls, tokens, edits, executions, and wall-clock time; (ii) *verification strength*; (iii) *recovery ability*; (iv) *state consistency*; (v) *safety compliance*; (vi) *replayability*."

Grade de metricas adotada pelo PCC: custo fica em (i), reprodutibilidade em (vi).

## Lacunas nomeadas (verbatim)

- Secao 5.2.1: "most existing evaluations measure end-task success... Such metrics conflate the capabilities of the base model, the quality of the harness, the reliability of tools, the informativeness of feedback, and the difficulty of the environment."
- Secao 5.2.1: "A central bottleneck in this agenda is *oracle adequacy*."
- Secao 5.2.7: pede "metrics that isolate harness components" — a frase mais curta para justificar o PCC.
- Atribuicao de falhas em lacos longos: precisao 14-53% no nivel de passo.

## Uso no PCC

- Referencial: definicao canonica de *harness*; distincao dos tres elementos (recorte: capacidades internas constantes, infraestrutura varia).
- Referencial: lacuna de atribuicao (Secao 5.2.1) e pedido de metricas por componente (Secao 5.2.7) — o par pi/oh-my-pi responde a 5.2.7.
- Material e metodo: dimensoes (i) e (vi); adequacao do oraculo como ameaca declarada.

## Contradictions

- Nenhuma interna registrada. Ver [[adequacao-oraculo]] e [[atribuicao-harness-vs-modelo]] para tensoes entre fontes.
