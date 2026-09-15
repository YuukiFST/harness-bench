---
title: Pi Minimal and Performant (Earendil, 2026)
type: source
summary: Pi com 4 ferramentas e prompt <1K tokens; 2x custo Databricks, 3x menos contexto
tags: [pi, minimalismo, custo, databricks, contexto]
created: 2026-09-10
updated: 2026-09-14
dated: 2026-08-04
sources: []
---

# Pi Minimal and Performant (Earendil, 2026)

## Identificacao

- Titulo: *Pi, Minimal and Performant*. De: Earendil <rfc@earendil.com>. 4 ago 2026.
- Blogue institucional: https://earendil.com/posts/pi-autoresearch-and-databricks/
- Verbatim do projeto (pi.dev): "Pi is a minimal agent harness."

## Referencia ABNT (como citada no projeto)

EARENDIL. **Pi, minimal and performant**. 2026. Publicacao de blogue institucional. Disponivel em: https://earendil.com/posts/pi-autoresearch-and-databricks/. Acesso em: 28 ago. 2026.

## Conteudo

- Pi sai com **4 ferramentas**; system prompt + definicoes **<1.000 tokens**. Sem MCP, sem subagentes, sem plan mode — por decisao (README: "No MCP... No sub-agents... No plan mode").
- **Databricks** (codebase multi-milhao de linhas, tarefas proprias): "the harness a model is called from dramatically impacts cost and quality"; mesmo modelo + mesmo esforco: "**cost per task differed significantly (more than 2x in some cases), while quality remained the same**"; "Pi sent about **3x less context per turn**... keeping a tighter working set and finishing the tasks in fewer runs." Pi + Opus 4.8 xhigh: maior pass-rate com custo bem menor que Claude Code e Codex.
- **Shopify pi-autoresearch**: extensao construida pelo proprio Pi; testes 300x mais rapidos, montagem React 20% mais rapida.
- Economia fim-a-fim: Haiku 4.5 em workflow complexo saiu mais caro que Sonnet 4.6 (mais turnos); modelo forte + *harness* performante pode sair mais barato que o inverso.
- Modelos locais: disciplina de contexto preserva prefixo de cache (prefill caro); prompt minimo + sem mudanca nao pedida.

## Uso no projeto

- Desde 2026-09-14 e a referencia do braco pi (Earendil, 2026) em §3 [60]: 4 ferramentas, <1K tokens, sem MCP/subagentes/plan.
- Justificativa: 2x Databricks com qualidade igual (fonte de pratica; citar como *apud* quando via este post).
- Camada 1: precedente dos 5,3x bytes de OpenCode sobre pi (prompt+schemas inchados custam antes do primeiro token).

### Auditoria de conteudo 2026-09-11

- Citada em: §2 [52] (*apud* Databricks).
- Afirmacao sustentada: custo por tarefa >2x "in some cases" com mesma qualidade.
- Veredito: CONCRETA; projeto omite "em alguns casos". Detalhe em [[2026-09-11-auditoria-conteudo-referencias]].

