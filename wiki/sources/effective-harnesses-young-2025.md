---
title: Effective harnesses for long-running agents (Young, 2025)
type: source
summary: Anthropic; harness de agente longo com feature list em JSON, progresso em arquivo e git, teste E2E por navegador
tags: [harness, longo-horizonte, feature-list, especificacao, claude-agent-sdk, anthropic]
created: 2026-09-24
updated: 2026-09-24
dated: 2025-11-26
sources: []
---

# Effective harnesses for long-running agents (Young, 2025)

## Identificacao

- Titulo: *Effective harnesses for long-running agents*. Autor: Justin Young (secao Acknowledgements: "Written by Justin Young"), Anthropic, blogue de engenharia.
- URL: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Texto extraido do HTML em 24 set. 2026: `raw/sources/effective-harnesses-young-2025.md` (as capturas de tela do Puppeteer nao foram guardadas).
- `dated` = "Published Nov 26, 2025", linha sob o titulo da pagina.
- Publicacao de blogue de engenharia de empresa, nao revisada por pares; relato de experimento interno, sem n de execucoes, sem tabela de resultados e sem numeros de custo.

## Escopo que a fonte declara

Um estudo de caso: o Claude Agent SDK com Opus 4.5 construindo um clone do claude.ai ao longo de varias janelas de contexto. A fonte diz que a demonstracao e "optimized for full-stack web app development" e que e "one possible set of solutions".

## O que a fonte diz

- Problema: um agente longo trabalha em sessoes discretas, e cada sessao nova comeca sem memoria da anterior. Compactacao de contexto "isn't sufficient": com so um *prompt* de alto nivel, o agente tenta fazer tudo de uma vez ("one-shot the app") ou, mais tarde, declara o trabalho pronto cedo demais.
- Solucao em duas partes. Um agente inicializador escreve `init.sh`, um arquivo de progresso `claude-progress.txt` e um commit inicial. Um agente de codificacao avanca uma funcionalidade por sessao, faz commit com mensagem descritiva e atualiza o arquivo de progresso. Nota 1: os dois so diferem no *prompt* inicial do usuario; "The system prompt, set of tools, and overall agent harness was otherwise identical."
- Lista de funcionalidades: o inicializador expande o *prompt* numa lista completa, "over 200 features" no clone do claude.ai, todas marcadas como falhando. Formato JSON por funcionalidade: `category`, `description`, `steps` (passos de verificacao) e `passes: false`. O agente so pode mudar `passes`: "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality." JSON foi escolhido porque "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."
- Teste: sem instrucao explicita, o agente marcava funcionalidade como pronta depois de teste unitario ou `curl`, sem verificar ponta a ponta. Com automacao de navegador (Puppeteer MCP) e instrucao de testar "as a human user would", o desempenho melhorou "dramatically"; a fonte nao da numero.
- Inicio de sessao: `pwd`, ler progresso e `git log`, ler a lista e escolher a funcionalidade de maior prioridade ainda falhando, subir o servidor com `init.sh` e rodar um teste E2E basico antes de comecar.
- Em aberto, segundo a fonte: se um agente unico ou uma arquitetura multiagente (teste, QA, limpeza) rende mais; generalizar para outros dominios.

## O que acrescenta a wiki

- Unica fonte da wiki sobre *harness* de agente em tarefa de varias sessoes que constroi um produto inteiro, o recorte que [[harnesstax-pan-2026]] deixa como proximo passo.
- Da o formato da lista de funcionalidades que o projeto adota na especificacao do [[finn]] desde 2026-09-24 (ver [[desenho-experimental-harness-fixo]]), sem o campo `passes`: no projeto quem decide o escore e o teste de aceitacao do autor, nunca o relato do agente (ver [[adequacao-oraculo]]).
- Relato de falha que o projeto deve esperar dos bracos: declarar vitoria cedo e marcar pronto sem teste ponta a ponta. No desenho do projeto isso aparece como unidade nao concluida, pelo teste externo.

## Uso no projeto

Citada em `dist/projeto-de-pesquisa.docx` §3 [77] como origem do formato da lista de funcionalidades, com entrada na secao 6 (YOUNG, 2025), e em `docs/spec/11-experimental-protocol.md` §1.1. Esta no tema (componentes de *harness* de agente de codificacao), entao nao exige excecao no `AGENTS.md`; o autor liberou em 2026-09-24 passar do limite de paginas por referencias.

## Contradictions

Nenhuma registrada.
