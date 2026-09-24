---
title: Adequacao do Oraculo
type: concept
summary: Verificador captura a tarefa ou so um proxy executavel estreito
tags: [oraculo, verificador, gaming, held-out]
created: 2026-09-10
updated: 2026-09-24
sources: [wiki/sources/effective-harnesses-young-2025.md, wiki/sources/code-as-agent-harness-ning-2026.md, wiki/sources/deepswe-huang-2026.md, wiki/sources/holistic-agent-leaderboard-kapoor-2025.md, wiki/sources/ai-agents-that-matter-kapoor-2024.md, wiki/sources/scaffolding-matters-alier-forment-2026.md]
---

# Adequacao do Oraculo

Gargalo central (source: [[code-as-agent-harness-ning-2026]], Secao 5.2.1): "*oracle adequacy*: whether the evaluator captures the intended task rather than only a narrow executable proxy." Problema aberto nao e so benchmark mais dificil, mas avaliar o *harness* como runtime executavel.

## Padroes

- Verificadores funcionais escritos a mao + auditoria por juiz independente: 1,4% vs 32,4% de desacordo (source: [[deepswe-huang-2026]]). Taxa de desacordo entre leitores, nao erro ground-truth.
- Patologias de testes herdados: vazamento por git log (87% dos cheats lendo gold), stubs que passam, falhas de helpers/privados/testes alheios (source: [[deepswe-huang-2026]]).
- Gaming mesmo com checks: buscar gabarito no HuggingFace, hard-codar solucoes, few-shot vazado do TAU (source: [[holistic-agent-leaderboard-kapoor-2025]]).
- Verificacao e camada V do ETCSOVG a divulgar (source: [[stop-comparing-harness-zhang-2026]]).
- Regra de [[scaffolding-matters-alier-forment-2026]]: nunca perguntar ao agente se venceu; inspecionar o estado.

## Resposta do projeto

Oraculo proprio executado pelo runner, nunca a suite do agente (modelo que alucina API escreve testes que mocam a alucinacao). Desde 2026-09-14: testes de aceitacao Vitest escritos pelo autor por unidade da especificacao do [[finn]], antes da execucao, mantidos fora do espaco de trabalho (held-out) e rodados sobre uma copia dele ao fim de cada unidade; a fracao aprovada e o escore e todos aprovados = unidade concluida. Desde 2026-09-24 o oraculo e validado antes da coleta: os testes das unidades 1..k precisam passar no Finn de referencia do autor na *tag* da unidade k, e um teste que falha la ou que usa identificador fora do contrato de interface da especificacao e lacuna a corrigir antes do congelamento. Isso mostra que todo teste e satisfazivel pela especificacao; nao mostra que os testes cobrem tudo que a especificacao pede. A lista de funcionalidades segue [[effective-harnesses-young-2025]], mas sem o campo `passes`: la o proprio agente marca o que passou, e a fonte relata que ele marcava pronto sem teste ponta a ponta. Auditoria de logs; taxonomia nao-concluida/descartada/adulterada. Holdouts no nivel certo de generalidade (source: [[ai-agents-that-matter-kapoor-2024]]).

## Contradictions

- Verificadores suficientes? [[deepswe-huang-2026]] (1,4%: bons) vs [[holistic-agent-leaderboard-kapoor-2025]] (mesmo tarefas checadas sao gameaveis fora da vista do verificador). Leitura: combinar funcional + regressao + auditoria + divulgacao da camada V; pre-definir tratamento de tampered. Juizes LLM sem execucao ([[harness-handbook-wang-2026]]) nao substituem verificacao para H1/H2.
