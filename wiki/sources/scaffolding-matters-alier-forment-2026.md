---
title: The Scaffolding Matters More Than the Interface (Alier Forment et al., 2026)
type: source
summary: 20x entre scaffoldings e 139x num modelo 27B fixo, com verificacao por estado
tags: [scaffolding, mcp, cli, custo, verificacao, resolucao]
created: 2026-09-10
updated: 2026-09-11
dated: 2026-08-09
sources: []
---

# The Scaffolding Matters More Than the Interface (Alier Forment et al., 2026)

## Identificacao

- Titulo: *The Scaffolding Matters More Than the Interface: A Controlled Comparison of MCP and CLI Tool Use Across Seven Agent Scaffoldings, Five Language Models, and One Software Task*.
- Autores: Marc Alier Forment, Maria Jose Casan Guerrero, Francisco Jose Garcia-Penalvo, Juanan Pereira (UPC, USAL, UPV/EHU).
- arXiv:2608.08654v1, 9 ago 2026. 27 paginas, 4 figuras, 8 tabelas. Sem versao HTML (so PDF).
- *Preprint*, nao revisado por pares.
- PDF: `raw/sources/2608.08654-alier-forment-scaffolding-matters.pdf`. Dataset + *harness*: `github.com/Lamb-Project/mcp-vs-cli-bench`, Zenodo 1.0.0 DOI 10.5281/zenodo.21851992.

## Referencia ABNT (como citada no projeto)

ALIER FORMENT, Marc; CASAN GUERRERO, Maria Jose; GARCIA-PENALVO, Francisco Jose; PEREIRA, Juanan. The scaffolding matters more than the interface: a controlled comparison of MCP and CLI tool use across seven agent scaffoldings, five language models, and one software task. arXiv:2608.08654, 2026. *Preprint*, nao revisado por pares. Disponivel em: https://arxiv.org/abs/2608.08654. Acesso em: 9 set. 2026.

## Tese (verbatim, Secao 3)

> "When the running cost of an agent is at issue, the scaffolding chosen to drive the model is a larger factor than the interface through which that model is given tools."

> "Between the cheapest and the most expensive lies a factor of 20. No comparison between tool interfaces reported later in this paper approaches that magnitude."

Definicao (Secao 1.1, verbatim): "a software harness that the industry is calling the agent scaffolding: it takes the user's request, sends it to the model, receives the model's output, executes whatever actions the model asks for, and feeds the results back so the model can continue."

## Numeros (modelo/tarefa fixos, verificacao por estado do repositorio, ago 2026)

- **20x**: mediana de input tokens por run concluida, mesma tarefa de 6 operacoes GitHub: Pi 14.660 (4/4) a qwen-code 288.808 (7/8).
- **5,0x a 28x** so no braco CLI, sem MCP anexado: Pi 14.660 a Claude Code 410.797.
- **139x** para o modelo local qwen3.6:27b fixo: Tau CLI 17.416 a Codex MCP 2.418.828 tokens.
- **13 razoes MCP/CLI pareadas: 0,43x a 29x, mediana 0,93** — comparacao declarada inconclusiva.
- **Custo da falha**: 12,9% do dinheiro em runs MCP nao comprou trabalho concluido vs 2,2% em CLI; frequencia de falha igual.
- **Limite de resolucao**: diferenca < ~2x nao se distingue de variacao run-to-run (21 configs com repeticao; hospedados majoritariamente single-run).

## Metodo reutilizavel

Custo condicionado a conclusao; conclusao reportada em separado; verificacao por estado (API do GitHub), nunca auto-relato; agentes ignoraram a interface designada (6/21 MCP exclusivo, 6 so shell, 6 misto) — medir comportamento real. Precos OpenRouter de 3 ago 2026.

## Limitacoes declaradas (verbatim, Secao 8)

- "What we cannot do is attribute the difference to MCP support specifically."
- "We therefore report the conventional within-scaffolding comparison as inconclusive on this evidence."
- "One task, in one domain. The task exercises GitHub, a service with both a mature command-line client and an official MCP server."
- "a difference smaller than roughly twofold cannot be distinguished from run-to-run variation."

## Uso no projeto

- Justificativa: unica evidencia controlada de custo por tarefa concluida com modelo fixo (20x, 139x) — sustenta H1.
- Material e metodo: as cinco regras (condicionar, separar, verificar, checar aderencia, repetir) viram protocolo do projeto.
- H2: Pi vs Tau (12% de diferenca, ambos 4/4) mostra que efeito minimalista sobrevive a reimplementacao independente — precedente do teste Pi vs oh-my-pi.
- Limitacoes: mesmas ressalvas de tarefa unica e atribuicao.

### Auditoria de conteudo 2026-09-11

- Citada em: §2 [52]; §1 [27].
- Afirmacao sustentada: 5,0x-28x entre *scaffoldings* sem e com MCP (Abstract); Tau e reimplementacao independente, nao *fork* (§2.3).
- Veredito: CONCRETA; razao e mediana sobre mix de modelos, nao modelo fixo. Detalhe em [[2026-09-11-auditoria-conteudo-referencias]].

## Contradictions

- Direcao oposta a [[meta-harness-lee-2026]] (subtrair vs adicionar complexidade): objetivos diferem (custo vs acuracia). Ver [[atribuicao-harness-vs-modelo]].
