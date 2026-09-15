---
title: Helmsman (skill, YuukiFST, 2026)
type: source
summary: Skill do autor; mapa de decisoes em issues, humano responde produto, agente decide o tecnico e pesquisa via subagentes
tags: [helmsman, metodo, skill, declaracao-de-uso, finn, especificacao]
created: 2026-09-15
updated: 2026-09-15
dated: 2026-08-27
sources: []
---

# Helmsman (skill, YuukiFST, 2026)

## Identificacao

- Titulo: `helmsman` (`SKILL.md`), skill para Claude Code e OpenCode. Descricao no cabecalho: "Plan a huge chunk of work, more than one agent session can hold, as a shared map where the human answers only what the system should do, and the agent decides how it gets built, resolving the technical tickets alone and in cascade."
- Autor: YuukiFST (o autor deste projeto). Repositorio `agent-dotfiles`, pasta `skills/helmsman`.
- URL: https://github.com/YuukiFST/agent-dotfiles/tree/main/skills/helmsman (copia em `raw/sources/helmsman-skill-yuukifst-2026.md`, baixada de `main` em 2026-09-15).
- `dated` = data do primeiro commit do arquivo no repositorio (`2fc9f3a`, 27 ago. 2026, via API do GitHub); o texto nao traz data. Ultima alteracao lida: `6f91157`, 28 ago. 2026. Documento de metodo do proprio autor, nao revisado por pares.

## Referencia ABNT (como citada no projeto)

YUUKIFST. agent-dotfiles: skill Helmsman, mapa de decisoes para agentes de codificacao. 2026a. Repositorio de codigo. Disponivel em: https://github.com/YuukiFST/agent-dotfiles/tree/main/skills/helmsman. Acesso em: 15 set. 2026.

## O que a skill diz

- Problema: uma ideia grande demais para uma sessao de agente e "wrapped in fog". A skill transforma a ideia num **mapa compartilhado** de *tickets* no rastreador de issues do repositorio e trabalha os *tickets* "until nothing is left to decide".
- Divisao de trabalho: "the human is the product owner, the agent is the developer". Toda pergunta passa pelo *product-owner test*: "Would the answer change what a person using the finished system experiences, or what the business gets out of it?" Sim = pergunta do humano (`helmsman:po`); nao = pergunta do agente (`helmsman:dev`). Linguagem, framework, esquema de dados, autenticacao, testes e ordem do trabalho nunca vao ao humano.
- Tres excecoes voltam ao humano com recomendacao pronta: dinheiro, dado pessoal e *lock-in*. A resposta esperada e "go" ou "no, because". "Being unsure doesn't escalate, being unsure means you research."
- O mapa e uma issue (`helmsman:map`) com secoes Destination, Notes, Product decisions, Technical decisions (cada linha com clausula `locks:`), Waiting on you, Not yet specified (nevoa) e Out of scope. Os *tickets* sao sub-issues com dois rotulos: audiencia (`po`/`dev`) e metodo (`decision`, `research`, `prototype`, `grilling`, `task`).
- Pesquisa por subagentes: um *ticket* `research` "is resolved by a `/research` subagent"; no modo de mapeamento a skill manda "Fire the research subagents. For each `research` ticket, spin up a `/research` subagent to resolve it in parallel", com os achados num *branch* `research/<name>`. Decisoes que dependem de fato externo (preco de API, comportamento de biblioteca) esperam esse resultado.
- Resolucao de um *ticket* `dev` tem forma obrigatoria: Decision, Alternatives considered (minimo duas reais), Criterion (rastreavel a uma decisao de produto ou a um fato citado) e Consequence (a clausula `locks:`). Regras: "Boring wins by default" e "Reversibility is a tiebreaker".
- Tres modos: `/helmsman <ideia>` mapeia (grilling + domain-modeling, nenhuma pergunta tecnica ao humano); `/helmsman <mapa>` avanca em cascata sem o humano ate a fronteira ficar sem *ticket* `dev`; `/helmsman <mapa> --review` drena todos os *tickets* `po` numa conversa. Um agente que responde o proprio *ticket* `po` "has broken the skill". Toda sessao termina com o proximo comando exato para o humano colar.
- Fim: fronteira vazia nas duas audiencias e nevoa limpa; entrega para `/writing-plans` com o mapa como entrada. A skill "is planning", produz decisoes, nao entregaveis.

## O que este projeto instancia

O mapa do [[finn]] e a issue #1 do repositorio Finn, com 21 sub-issues fechadas: #2-#10 `po` (respondidas pelo autor em `--review`), #11-#22 `dev` (#11-#13 `research`, resolvidas por subagentes em `research/meta-billing`, `research/whisper-ptbr` e `research/custo-zero`; #14-#22 `decision`). Exemplo de resolucao `dev`: #15 multi-tenant, banco unico com `tenant_id` em tudo, tres alternativas rejeitadas, criterio em `MEMORIA_PO_FELIPE.md:59-65`, `locks: tenant_id-em-tudo + sender-para-user-tenant + central-roteia-por-remetente`. Estado em 2026-09-15: Waiting on you vazio, nevoa limpa; o mapa e a base da especificacao congelada que os dois bracos constroem.

## Uso no projeto

- §3 [58]: o paragrafo que declara o uso de IA (amparo: [[portaria-cnpq-2664-2026]]) cita a skill como metodo que registrou as decisoes de produto e de pilha do Finn antes do experimento, ao lado do [[llm-wiki-karpathy-2026]].
- Fora do tema do *harness*; entra na lista por excecao autorizada pelo autor em 2026-09-15 (`AGENTS.md`, Project documents). Mesmo autor e ano das outras duas entradas YUUKIFST: letras por ordem de titulo (agent-dotfiles 2026a, Finn 2026b, harness-bench 2026c).

## Contradictions

Nenhuma registrada.
