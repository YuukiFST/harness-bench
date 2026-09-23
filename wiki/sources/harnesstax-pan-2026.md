---
title: HarnessTax (Pan et al., 2026)
type: source
summary: 7 modelos x Claude Code/Codex/Pi; sucesso muda ate ~5%, custo ate 5x; CC ~2x Pi no SWE-bench Lite
tags: [harness, custo, modelo-fixo, claude-code, codex, pi, swe-bench-lite, terminal-bench]
created: 2026-09-23
updated: 2026-09-23
dated: 2026-09-22
sources: []
---

# HarnessTax (Pan et al., 2026)

## Identificacao

- Titulo: *HarnessTax: How Much Does the Harness Matter for Coding Agents?*
- Autores: Melissa Z. Pan, Shuo Yang, Negar Arabzadeh, Wei-Lin Chiang, Ion Stoica, Matei Zaharia (UC Berkeley; Chiang pela Arena Intelligence Inc.).
- Blogue de pesquisa em https://harnesstax.github.io/ (pagina renderizada em JS; texto integral no JSON `data/blog/harness-x-model.0af74054a7.json`).
- *Blog post* de pesquisa, nao revisado por pares; sem *venue*. Os autores prometem liberar os *traces* de *profiling*.
- Texto extraido: `raw/sources/harnesstax-pan-2026.md` (coletado em 23 set. 2026; os graficos interativos, figuras 1-4, nao foram capturados, so as legendas).
- Data: o rodape da pagina traz "2026-09-22 00:47 UTC" e o JSON tem Last-Modified de 22 set. 2026; `dated` usa essa data. O anuncio no X foi em 16 set. 2026 (informado pelo pedido de *ingest*, nao conferido aqui); as referencias do texto dizem "Accessed September 16, 2026".

## Escopo que a fonte declara

Estudo de 21 pares modelo-*harness*: 7 modelos x 3 *harnesses* (Claude Code, Codex CLI, Pi), em dois benchmarks abertos (SWE-bench Lite e Terminal-Bench 2.0). Os autores limitam as conclusoes a esses dois benchmarks, que os modelos podem ter visto no treino, e dizem que o resultado pode mudar em outros benchmarks e cargas de trabalho.

## Metodo

- 30 tarefas sorteadas de cada benchmark, as mesmas para os 21 pares; 3 execucoes por tarefa.
- Configuracao nativa de cada *harness*, esforco *high*, teto de 100 turnos por tentativa; turno e esforco seguem a definicao de cada *harness*.
- Sucesso pelo avaliador oficial de cada benchmark.
- Media das 3 tentativas por tarefa, depois das 30 tarefas; IC de 95% por *bootstrap* com 10.000 reamostragens de 30 medias por tarefa.
- Custo em tokens calculado com uma lista de precos de API direta fixa, datada de 1 set. 2026, igual para o mesmo modelo em todos os *harnesses* (custo estimado de tokens x preco, nao fatura).
- SWE-bench Lite sem rede: *web tools* desligadas no Claude Code e no Codex, declaracoes de *hosted tools* rejeitadas na requisicao.
- Pi recebe dois pacotes (chaves de assinatura e controle de turnos). Kimi K3 via Fireworks AI, modo *thinking* nativo unico nos tres *harnesses*.
- Modelos citados no texto: Claude Fable 5, Sonnet 4.6, Opus (versao nao dita no texto extraido), GPT-5.6 Sol, GPT-5.6 Luna, Kimi K3; seis sao da Anthropic e da OpenAI. A lista completa dos 7 esta nos graficos, nao no texto.

## Achados (numeros exatos, denominador junto)

1. O *harness* muda mais o custo que o acerto. Efeito medio do *harness* na taxa de sucesso: dentro de +-2% no SWE-bench Lite e de cerca de +-5% no Terminal-Bench 2.0. O mesmo modelo chega a taxas parecidas com ate 5x de custo.
   - Claude Fable 5, SWE-bench Lite: 97,8% no Claude Code, 96,7% no Codex, 96,7% no Pi; custo medio por tentativa $1,33 no Claude Code vs $0,67 no Pi.
   - Nos modelos em comum, media geometrica das razoes de custo: Claude Code custa ~2,0x o Pi e 1,6x o Codex no SWE-bench Lite, e 1,5x o Pi no Terminal-Bench 2.0.
   - Nome do efeito: "harness tax", pagar mais pela mesma qualidade ao aceitar o *harness* padrao sem comparar.
2. Um *harness* simples compete. Pi fica na fronteira de Pareto nos dois benchmarks com quatro ferramentas (read, write, edit, bash).
   - Fable 5, SWE-bench Lite: Pi e Claude Code fazem 15,4 e 15,3 turnos por tentativa, e o Claude Code custa cerca de 2x por 1,1% a mais de sucesso. Ou seja, o gasto por turno e maior, embora turno seja definido de forma diferente em cada *harness*.
   - Contexto da primeira chamada, SWE-bench Lite: nos 7 modelos, o contexto inicial medio do Claude Code passa de 10x o do Pi (instrucoes mais longas e *schemas* de ferramentas maiores; tokens de entrada relatados pelo provedor). Os autores ressalvam que o custo total depende tambem de *cache*, tokens gerados e chamadas seguintes.
3. O modelo pode ir melhor fora do *harness* do proprio fornecedor. Nos seis modelos Anthropic e OpenAI e nos dois benchmarks, um *harness* alternativo tem a maior taxa de sucesso observada em 9 de 12 comparacoes.
   - Sonnet 4.6, SWE-bench Lite: 68,9% no Codex vs 66,7% no Claude Code, custo parecido.
   - GPT-5.6 Sol, Terminal-Bench 2.0: 83,3% no Pi vs 78,9% no Codex, $0,42 vs $0,76.

## Proximo passo declarado

Avaliar *harnesses* e automatizar sua escolha em fluxos reais de desenvolvimento, em que os requisitos mudam, o desenvolvedor da *feedback* e as tarefas atravessam varias sessoes. Esse e o recorte do [[desenho-experimental-harness-fixo]] (construcao inteira de um produto, varias unidades), que a fonte deixa em aberto.

## O que acrescenta a wiki

- Primeira fonte com modelo fixo, 3 execucoes por tarefa e IC por *bootstrap* que compara Claude Code, Codex e Pi lado a lado em varios modelos. Reforca com repeticao o que [[pi-earendil-2026]] relatava *apud* Databricks (mais de 2x de custo com qualidade igual).
- Separa custo e acerto como eixos independentes, como [[frontierharness-runta-2026]], mas com o sucesso quase constante entre *harnesses*.
- Nao mede OpenCode, o outro braco do projeto.
- Mede contexto inicial em caracteres e tokens relatados pelo provedor; custo e estimado por tabela de precos (ver [[medicao-custo-proxy-vs-relato]]).

## Paginas afetadas

[[pi-coding-agent]], [[binding-constraint-thesis]], [[especificidade-modelo-inversao]], [[medicao-custo-proxy-vs-relato]].

## Contradictions

Nenhuma interna. Os conflitos com outras fontes ficam em [[binding-constraint-thesis]] (efeito pequeno no acerto) e [[especificidade-modelo-inversao]] (Claude Code caro tambem no fornecedor nativo).
