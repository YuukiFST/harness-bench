---
title: Verificacao de uso real de cada referencia do projeto
type: query
summary: 14 entradas citadas e sustentadas na obra; ressalvas corrigidas no docx, deck e roteiro em 2026-09-25
tags: [auditoria, referencias, citacoes, nbr, projeto]
created: 2026-09-25
updated: 2026-09-25
sources: [wiki/sources/harnesstax-pan-2026.md, wiki/sources/code-as-agent-harness-ning-2026.md, wiki/sources/agentic-harness-engineering-lin-2026.md, wiki/sources/stop-comparing-harness-zhang-2026.md, wiki/sources/sol-pi-liu-2026.md, wiki/sources/adding-error-bars-miller-2024.md, wiki/sources/effective-harnesses-young-2025.md, wiki/sources/pi-earendil-2026.md, wiki/sources/zen-opencode-2026.md, wiki/sources/llm-wiki-karpathy-2026.md, wiki/sources/helmsman-skill-yuukifst-2026.md, wiki/entities/opencode.md, wiki/entities/finn.md, wiki/queries/2026-09-24-mapa-citacoes-projeto.md]
---

# Verificacao de uso real de cada referencia — as of 2026-09-25

Pergunta: cada referencia de `6 REFERENCIAS` e de fato usada no projeto, ou esta la a toa?
Texto conferido: `python tools/docx_prose.py dump dist/projeto-de-pesquisa.docx` no commit 9c0fe11 (edicao manual do autor em 2026-09-24, depois de [[2026-09-24-mapa-citacoes-projeto]]).
Os indices `[n]` nao mudaram em relacao ao mapa de 2026-09-24; a lista vai de [148] a [161].

## Metodo

1. Fechamento mecanico: regex sobre os paragrafos [41]-[146] contra as 14 entradas (Aula 3: nenhuma entrada sem citacao, nenhuma citacao sem entrada).
2. Cada afirmacao atribuida a uma obra foi procurada na obra, nao na wiki: PDFs de `raw/sources/` via `pdftotext -enc UTF-8 -layout`, com a pagina do PDF conferida no rodape; `raw/sources/*.md` para HarnessTax, Young, Karpathy e Helmsman; paginas publicas baixadas com `curl` em 2026-09-25 para Earendil, OpenCode (README, API do GitHub e pasta `packages/opencode/src/tool`) e Zen; `gh` para as *issues* do Finn.
3. Metadados das entradas (titulo, primeiro autor, identificador) conferidos na API do arXiv e nas paginas.

## Resultado

- 14 entradas, 14 citadas no corpo, nenhuma citacao sem entrada.
- Nenhuma referencia esta a toa: cada uma sustenta pelo menos uma afirmacao concreta que se acha na obra.
- Titulos, primeiros autores e identificadores arXiv das cinco entradas arXiv batem com a API do arXiv.
- Ressalvas de precisao abaixo; nenhuma delas torna uma referencia inutil.

| Entrada | Paragrafos | Uso | Veredito |
|---|---|---|---|
| Pan *et al.*, 2026 | [43], [68], [69], [70], [71] (+ [44] sem nome) | numeros e achados centrais da justificativa e do referencial | usada; ressalva em [69] |
| Ning *et al.*, 2026 | [65], [69] | duas citacoes diretas, p. 7 e p. 66 | usada; exata |
| Lin *et al.*, 2026 | [65], [66], [68], [71] | citacao longa p. 1, Tabela 1, Succ/Mtok | usada; ressalva em [68] |
| Zhang *et al.*, 2026 | [68] | tese de variancia do *harness* | usada; ressalva |
| Liu *et al.*, 2026 | [69] | quatro mecanismos, 44,7-49,0% e 93,7-94,3% | usada; exata |
| Miller, 2024 | [83] | justificativa do pareamento | usada; exata no sentido |
| Young, 2025 | [77] | formato JSON da lista de funcionalidades | usada; exata |
| Earendil, 2026 | [67], [76] | 4 ferramentas, *system prompt* curto; identificacao do Pi | usada; ressalva em [76] |
| Opencode, 2026a | [67], [76] | subagentes, permissoes, ferramentas; identificacao | usada; exata no repositorio |
| Opencode, 2026b | [79] | *gateway* com modelos gratuitos | usada; exata |
| Karpathy, 2026 | [74] | origem do metodo da wiki (excecao autorizada) | usada |
| YuukiFST, 2026a | [74] | Helmsman mapeou o Finn (excecao autorizada) | usada |
| YuukiFST, 2026b | [77] | objeto do estudo | usada; numero de *tickets* desatualizado |
| YuukiFST, 2026c | [74], [76] | repositorio do projeto | usada |

## Evidencia por referencia

### Pan et al. (2026) — [[harnesstax-pan-2026]]

- [43] "sete modelos em tres *harnesses*": "21 model–harness pairs spanning seven models and three harnesses—Claude Code, Codex CLI, and Pi".
- [43] "influencia notavelmente o custo": "can significantly affect the cost on the benchmarks we test". A fonte diz "pode" e restringe aos *benchmarks* testados.
- [43] 97,8% / 96,7% / US$ 1,33 contra US$ 0,67, SWE-bench Lite: Finding 1, "Claude Fable 5 solves 97.8% of attempts in Claude Code, 96.7% in Codex and 96.7% in Pi, yet Claude Code costs about twice as much as Pi ($1.33 vs $0.67)". O *benchmark* se confirma no Finding 2: "For Fable 5 on SWE-bench Lite [...] a 1.1% increase in the success rate" (97,8 − 96,7 = 1,1).
- [43] Berkeley: cinco dos seis autores sao da UC Berkeley; Chiang e da Arena Intelligence.
- [44] vies de treino e proximo passo: Ending Notes, "which the models may have encountered during training" e "evaluate harnesses [...] in real development workflows, where requirements evolve [...] and tasks extend across sessions". "Tarefas isoladas" e glosa do projeto, nao frase da fonte.
- [68] "dentro de ±2%" e "cerca de 2,0 vezes": "the average harness effect on success rate stays within ±2% on SWE-bench Lite" e "Claude Code costs about 2.0× as much as Pi [...] using geometric means of cost ratios".
- [69] "o imposto pode comecar na primeira requisicao" e "passa de dez vezes": Finding 2, "A harness tax can begin with the first model call. Across all seven models, Claude Code’s mean initial context is over 10× Pi’s". A Figura 3 e so do SWE-bench Lite.
- [69] 15,3 contra 15,4: "Pi and Claude Code average 15.4 and 15.3 turns per attempt" (Fable 5, SWE-bench Lite).
- [70] "a definicao de turno varia": "though turn definitions vary across harnesses".
- [71] nove de doze: "an alternative harness achieves the highest observed success rate in nine of twelve comparisons" (seis modelos Anthropic e OpenAI, dois *benchmarks*).
- Ressalva: desde 9c0fe11 o [44] nao nomeia mais o "imposto do *harness*", e o [69] fala de "o imposto" sem antecedente. O leitor nao sabe que imposto e.

### Ning et al. (2026) — [[code-as-agent-harness-ning-2026]]

- [65] p. 7 do PDF (rodape "7"), §2: "A harness turns a stateless language model into a functional agent by grounding its outputs in external execution, persistent state, and verifiable feedback." Traducao fiel.
- [69] p. 66 (rodape "66"): "metrics that isolate harness components". Traducao fiel.
- Entrada: a API do arXiv da o titulo "Code as Agent Harness"; o subtitulo "Toward Executable, Verifiable, and Stateful Agent Systems" aparece so no PDF. A entrada segue o arXiv.

### Lin et al. (2026) — [[agentic-harness-engineering-lin-2026]]

- [66] p. 1 (sem numero impresso; rodape "Preprint."): "such progress relies not only on the underlying language model, but equally on the surrounding engineering components: the system prompt that shapes work style, the tools that expose the file system and shell, and the middleware that controls context, execution, and recovery. This collection of model-external, editable components is collectively referred to as the agent’s harness". Traducao fiel.
- [68] Tabela 1, p. 6: OpenCode 47,2%, Terminus-2 62,9%, Codex 71,9%, pass@1, Terminal-Bench 2, 89 tarefas.
- [71] Apendice A, Eq. 2, p. 16: "Succ/Mtok = pass@1 × 10^6 / mean tokens per trial, the expected number of successes per million tokens".
- Ressalva: o artigo nao diz com todas as letras que os tres *harnesses* humanos da Tabela 1 rodaram no GPT-5.4. O paragrafo "Models" (§4.1) fala dos tres agentes do AHE ("all three role agents [...] share one base model, GPT-5.4"); a legenda da Tabela 2 diz "all four columns run on GPT-5.4", mas a Tabela 1 nao. O "sobre o GPT-5.4" de [68] e inferencia plausivel, nao citacao.

### Zhang et al. (2026) — [[stop-comparing-harness-zhang-2026]]

- [68] p. 4: "For LLM agents operating on long-horizon tasks with comparable frontier models [...] HV is often comparable to or larger than MV".
- Ressalva: o texto omite o "often" (frequentemente) e apresenta como constatacao o que a fonte chama de tese de um *position paper*. "Sustentam" cobre o carater argumentativo; falta o "frequentemente".

### Liu et al. (2026) — [[sol-pi-liu-2026]]

- [69] p. 1: "Four mechanisms survive selection and form SoL-Pi, spanning action execution, context compaction, observation handling, and delegated reading".
- [69] p. 6: "1.10 B tokens, 49.0% fewer than Pi, while retaining 93.7% of Pi’s average score" (GPT-5.6 Sol) e "On Opus 5, it retains 94.3% of Pi’s average score while reducing token traffic by 44.7%". EdgeBench, 51 tarefas.

### Miller (2024) — [[adding-error-bars-miller-2024]]

- [83] p. 8 (rodape "8"; a Eq. 7 do erro padrao pareado esta na p. 7): "We can thus reduce the variance with paired differences as long as the conditional means of the model scores are correlated; that is to say, if the two models have some amount of agreement on which questions are 'easy' and which questions are 'hard'" e "We therefore recommend using the paired version of the standard error estimate wherever practicable".
- Miller compara modelos, nao *harnesses*, e usa erro padrao pareado, nao Wilcoxon; o projeto usa so o argumento do pareamento, o que a fonte sustenta.

### Young (2025) — [[effective-harnesses-young-2025]]

- [77] secao "Feature list": exemplo JSON com `"passes": false` e "we landed on using JSON for this, as the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files". Publicado em 26 nov. 2025, "Written by Justin Young".

### Earendil (2026) — [[pi-earendil-2026]]

- [67] pagina baixada em 2026-09-25 (HTTP 200), titulo "Pi, Minimal and Performant", "Date: Tue, 04 Aug 2026": "It comes out of the box with only 4 tools, and its system prompt and tool definitions come in below 1,000 tokens".
- Ressalva em [76]: "Os dois sao de codigo aberto" nao tem apoio no post de Earendil (nenhuma ocorrencia de "open", "license" ou "MIT" ligada ao Pi). Pan *et al.* (2026), ja na lista, sustenta: "Pi, a minimal, open-source harness".

### Opencode (2026a) — [[opencode]]

- [67] README (`anomalyco/opencode`, ramo `dev`): "two built-in agents [...] build [...] plan", "Asks permission before running bash commands", "a **general** subagent for complex searches and multistep tasks".
- [67] "mais ferramentas": o README nao lista ferramentas; o repositorio sim. `packages/opencode/src/tool/` tem apply_patch, edit, glob, grep, lsp, plan, question, read, shell, skill, task, todowrite, webfetch, websearch e write, contra as 4 do Pi.
- [76] codigo aberto: API do GitHub, `"description": "The open source coding agent."`, licenca MIT, repositorio publico.

### Opencode (2026b) — [[zen-opencode-2026]]

- [79] pagina baixada em 2026-09-25: "OpenCode Zen is an AI gateway that gives you access to these models" e varios modelos "available on OpenCode for a limited time" na lista de gratuitos. Limite ja registrado em [[2026-09-24-mapa-citacoes-projeto]]: o nivel gratuito so atende clientes que se identificam como OpenCode ou Pi.

### Karpathy (2026) — [[llm-wiki-karpathy-2026]]

- [74] `raw/sources/karpathy-2026-llm-wiki.md`: "A pattern for building personal knowledge bases using LLMs". Excecao autorizada pelo autor em 2026-09-14.

### YuukiFST (2026a) — [[helmsman-skill-yuukifst-2026]]

- [74] `raw/sources/helmsman-skill-yuukifst-2026.md`: "Helmsman charts the way as a **shared map** of tickets on the repo's issue tracker". Repositorio `agent-dotfiles` publico em 2026-09-25. Excecao autorizada em 2026-09-15.

### YuukiFST (2026b) — [[finn]]

- [77] *issue* #1 "Mapa Finn - SaaS universal de financeiro por voz", destino: "qualquer empresa fala com seu financeiro por voz e recebe lancamento, relatorio e aviso no celular". Multiempresa: *issue* #15 "Multi-tenant com ID da empresa em tudo".
- Fato desatualizado: "decidido em 21 *tickets*" conta #2-#22. Em 2026-09-16 o mapa ganhou #23 (produto), #24 (pesquisa) e #25 (decisao), todas com "Part of #1" e fechadas; o mapa lista #23 entre as "Product decisions". Sao 24 *tickets* de decisao hoje.
- Repositorio privado em 2026-09-25 (`gh api repos/YuukiFST/Finn`: `"private": true`). O avaliador nao consegue abrir a URL da entrada.

### YuukiFST (2026c) — harness-bench

- [74], [76]: repositorio do projeto. Publico em 2026-09-25 (`"private": false`); o mapa de 2026-09-24 ainda o dava como privado.

## Fora das referencias, notado na leitura

- [44], texto editado em 9c0fe11: "Quem paga por tokens paga pagando tambem essa diferenca" (repeticao) e "e a conta de tokens fora do *harness*" (oracao sem verbo; a versao anterior dizia "e conta os tokens fora do *harness*").
- [83]: "comum em ambos *coding agents*" (antes "comum aos dois bracos").

## Correcoes aplicadas em 2026-09-25

A pedido do autor, `tools/docx_edits_2026-09-25.py` (fidelidade as fontes) e `tools/docx_edits_2026-09-25b.py` (passada do humanizer e orcamento de paginas):

- [44] "paga pagando" -> "paga"; a ultima oracao volta a ter verbo ("e conta os tokens fora do *harness*"), e o Finn ganha frase propria ("O produto e o Finn, um SaaS voltado para o setor financeiro das empresas.").
- [68] Zhang: "e frequentemente comparavel ou maior" (fonte: "often").
- [69] "o imposto do *harness* pode comecar".
- [76] "Os dois sao de codigo aberto (Opencode, 2026a; Pan *et al.*, 2026)."
- [77] "decidido em 24 *tickets*".
- [83] "comum aos dois *coding agents*"; [84] "fracao de testes aprovados".
- Orcamento: as correcoes custaram tres linhas e levaram 6 REFERENCIAS para a p. 9. Tres cortes de viuva devolveram as linhas: [65] "delimitam essa camada:", [74] "na obra", [75] "mede a construcao contra o modelo real". Word: 9 paginas, 6 REFERENCIAS na p. 8, linha 33, igual a 9c0fe11; sumario inalterado.
- Humanizer em [43]-[86]: nenhum "nao X, mas Y" fora da citacao de Lin, nenhum travessao, cerca de um dois-pontos por paragrafo; os fechos causais de [71], [73], [81] e [83] respondem a objecao real e ficam.
- Fechamento citacao <-> lista refeito: 14 entradas, 14 citadas; Pan passa a 6 paragrafos, Opencode (2026a) a 3 citacoes.
- [68] "sobre o GPT-5.4" saiu (segunda rodada, a pedido do autor): o artigo nao declara o modelo dos *harnesses* humanos da Tabela 1. Os numeros, o *benchmark* e a tabela ficam.
- Finn continua privado por decisao do autor (registrada em `AGENTS.md`): ele apresenta o produto sem abrir o repositorio.
- Deck (`tools/apresentacao_explainer/`) e roteiro (`tools/roteiro_2026-09-25.py`) realinhados ao docx: titulo e problema com "mesmo modelo", *coding agents* no lugar de "bracos", sem GPT-5.4 na Tabela 1 de Lin, Zhang com "frequentemente", 24 *tickets*, "na obra", [76] sem modo sem interface nem URL base, fecho sem "tudo publico nos dois repositorios". Verificacao no navegador: 27 slides sem transbordo nem sobreposicao, 1280x720 e 390x844.

## Pendencias para o autor

Nenhuma. A entrada de 2026-09-25 em `_review.md` esta resolvida.
