---
title: Harness Zero
type: entity
summary: Laco ReAct minimo do PCC; controle cientifico sob 400 linhas
tags: [harness-zero, controle, react, bracos]
created: 2026-09-10
updated: 2026-09-10
sources: [wiki/sources/react-yao-2022.md, wiki/sources/agentic-harness-engineering-lin-2026.md]
---

# Harness Zero

*Harness* minimo de referencia do PCC: laco observar/agir com 3 ferramentas (ler/escrever arquivo, executar comandos). Sem planejamento, compactacao, retry automatico ou chamada auxiliar; <400 linhas de Python com portao de CI. Unico braco escrito pelo projeto alem das adaptacoes pi/oh-my-pi.

## Precedentes

Semente NexAU0 do AHE (1 ferramenta shell, sem middleware/skills/subagentes — source: [[agentic-harness-engineering-lin-2026]]) e loop [[react-yao-2022]] como *harness* legitimo minimo.

## No PCC

Controle cientifico: mede quanto qualquer *harness* acrescenta sobre o laco mais cru capaz de concluir a tarefa. Define o envelope de referencia (passos + wall-clock) que distingue timeout de falha genuina. Ver [[desenho-experimental-harness-fixo]].

## Contradictions

Nenhuma registrada.
