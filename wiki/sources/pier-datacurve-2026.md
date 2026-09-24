---
title: Pier (Datacurve, 2026)
type: source
summary: Fork Harbor para DeepSWE; docker ou modal, custo zero, agentes CLI isolados
tags: [pier, executor, docker, deepswe, air-gapped]
created: 2026-09-10
updated: 2026-09-14
dated: 2026-08-28
sources: []
---

# Pier (Datacurve, 2026)

## Identificacao

- *Pier: a Harbor fork built for DeepSWE*. Repositorio: https://github.com/datacurve-ai/pier (183 stars, 50 forks; 109 commits na leitura). Licenca Apache-2.0.
- Repositorio de codigo (nao revisado por pares).

## Referencia ABNT (como citada no projeto)

DATACURVE. **Pier**: a Harbor fork built for DeepSWE. 2026. Repositorio de codigo. Disponivel em: https://github.com/datacurve-ai/pier. Acesso em: 28 ago. 2026.

## O que e

Framework compativel com tarefas Harbor para avaliar agentes de codigo em *sandbox*: `pier run -p path/to/task --agent <nome> --env modal|docker`. Fork menor e opinativo do Harbor, com: agentes instalados em tarefas air-gapped (`allow_internet=false`, allowlist de rede honrada por docker e modal); ATIF v1.7 aumentado (1 passo por turno, separacao reasoning/mensagem, `peak_context_tokens`, `llm_call_count`, timestamps reais); viewer de trajetoria (`pier view`); `pier critique run`.

## Relevante ao projeto

- Agentes hoje: nop, oracle, antigravity-sdk, claude-code, codex, cursor-cli, gemini-cli, **opencode**, **mini-swe-agent**. **Sem adaptador para Pi nem oh-my-pi** — os dois (e o *harness* zero) sao escritos neste projeto.
- Este projeto usa **docker**; GPU da estacao irrelevante para resultados.
- Trials em `jobs/<ts>/<trial_id>/`; datasets Harbor via download previo.

## Uso no projeto

- Retirada da lista de referencias em 2026-09-14: o executor do DeepSWE nao faz parte do desenho com o [[finn]].

### Auditoria de conteudo 2026-09-11

- Citada em: §3 [59]; §4 [75].
- Afirmacao sustentada: sem adaptador para pi/oh-my-pi (lista do README); Apache-2.0.
- Veredito: CONCRETA. Detalhe em [[2026-09-11-auditoria-conteudo-referencias]].
