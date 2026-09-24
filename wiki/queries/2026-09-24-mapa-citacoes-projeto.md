---
title: Mapa das citacoes do projeto por trecho e prova na fonte
type: query
summary: 14 entradas, cada citacao ligada ao paragrafo do projeto e ao trecho verbatim da fonte que a sustenta
tags: [auditoria, referencias, citacoes, nbr, projeto]
created: 2026-09-24
updated: 2026-09-24
sources: [wiki/sources/harnesstax-pan-2026.md, wiki/sources/code-as-agent-harness-ning-2026.md, wiki/sources/agentic-harness-engineering-lin-2026.md, wiki/sources/stop-comparing-harness-zhang-2026.md, wiki/sources/sol-pi-liu-2026.md, wiki/sources/adding-error-bars-miller-2024.md, wiki/sources/effective-harnesses-young-2025.md, wiki/sources/pi-earendil-2026.md, wiki/sources/zen-opencode-2026.md, wiki/sources/llm-wiki-karpathy-2026.md, wiki/sources/helmsman-skill-yuukifst-2026.md, wiki/entities/opencode.md, wiki/entities/finn.md]
---

# Mapa das citacoes do projeto — as of 2026-09-24

Pergunta: que parte do projeto cada referencia sustenta, e onde esta a prova na obra?
Indices `[n]` sao os do `python tools/docx_prose.py dump dist/projeto-de-pesquisa.docx` depois de `tools/docx_edits_2026-09-24f.py` (lista em [148]-[161]).
Cada trecho foi conferido na fonte bruta (`raw/sources/`, PDFs via `pdftotext`) ou, para fontes sem copia bruta, na pagina publica acessada em 2026-09-24.
Resultado: 14 entradas, 14 citadas, nenhuma entrada sem citacao, nenhuma citacao sem entrada, todas no tema do *harness* salvo as duas excecoes autorizadas em [74].

## Por referencia

### Pan et al. (2026), HarnessTax — [[harnesstax-pan-2026]]

- [43] Berkeley; sete modelos, tres *harnesses*; Fable 5 no SWE-bench Lite 97,8% no Claude Code e 96,7% no Pi, US$ 1,33 contra US$ 0,67. Fonte, Finding 1: "Claude Fable 5 solves 97.8% of attempts in Claude Code, 96.7% in Codex and 96.7% in Pi". Cinco dos seis autores sao da UC Berkeley; Chiang e da Arena Intelligence.
- [44] "imposto do *harness*": Finding 1 usa "Harness Tax" (termo que os autores tomam da ref. 10, Portkey). Benchmarks possivelmente vistos no treino e proximo passo em fluxos reais de varias sessoes: Ending Notes, "natural next step is to evaluate harnesses [...] in real development workflows".
- [68] efeito medio dentro de ±2% e custo ~2,0x: Finding 1, "Claude Code costs about 2.0× as much as Pi [...] using geometric means of cost ratios". Por isso o texto diz "em media".
- [69] primeira requisicao: Finding 2, "A harness tax can begin with the first model call. Across all seven models, Claude Code's mean initial context is over 10× Pi's". Turnos 15,3 (Claude Code) e 15,4 (Pi) sao so do Fable 5 no SWE-bench Lite.
- [70] definicao de turno varia: "though turn definitions vary across harnesses".
- [71] nove de doze: Finding 3, "an alternative harness achieves the highest observed success rate in nine of twelve comparisons" (seis modelos Anthropic e OpenAI, dois *benchmarks*).

### Ning et al. (2026), Code as agent harness — [[code-as-agent-harness-ning-2026]]

- [65] citacao direta, p. 7 (§2): "A harness turns a stateless language model into a functional agent by grounding its outputs in external execution, persistent state, and verifiable feedback." Traducao fiel.
- [69] citacao direta, p. 66 (§5.2.7): "metrics that isolate harness components". Sustenta a motivacao de H2.

### Lin et al. (2026), Agentic harness engineering — [[agentic-harness-engineering-lin-2026]]

- [66] citacao longa, p. 1 (§1; a pagina nao traz numero impresso, a numeracao impressa comeca em 2): "such progress relies not only on the underlying language model, but equally on the surrounding engineering components [...] collectively referred to as the agent's harness". Traducao fiel; os numeros de referencia entre colchetes foram omitidos.
- [68] Tabela 1, p. 6: pass@1 no Terminal-Bench 2 (89 tarefas), GPT-5.4, *harnesses* humanos de 47,2% (OpenCode) a 71,9% (Codex).
- [71] Succ/Mtok, Apendice A, Eq. 2, p. 16: "the expected number of successes per million tokens". Ver [[succ-mtok]].

### Zhang et al. (2026), Stop comparing — [[stop-comparing-harness-zhang-2026]]

- [68] p. 4, Binding Constraint Thesis: "HV is often comparable to or larger than MV", para "long-horizon tasks with comparable frontier models". A afirmacao e sobre variancia, num *position paper*; o texto agora diz "variacao de desempenho" e "em tarefas longas". Ver [[binding-constraint-thesis]].

### Liu et al. (2026), SoL-Pi — [[sol-pi-liu-2026]]

- [69] p. 1 (resumo): "Four mechanisms [...] spanning action execution, context compaction, observation handling, and delegated reading". O texto anterior listava tres; a leitura delegada foi incluida.
- [69] p. 6: "1.10 B tokens, 49.0% fewer than Pi, while retaining 93.7%" (GPT-5.6 Sol) e "retains 94.3% [...] reducing token traffic by 44.7%" (Opus 5), EdgeBench, 51 tarefas.

### Miller (2024), Adding error bars — [[adding-error-bars-miller-2024]]

- [83] p. 7, §4.2: "reduce the variance with paired differences as long as the conditional means [...] are correlated", "We therefore recommend using the paired version". Miller nao diz que a dificuldade e a *maior* fonte de variacao, e usa erro padrao pareado, nao Wilcoxon. O texto agora diz so que o pareamento remove a dificuldade comum aos dois bracos.

### Young (2025), Effective harnesses — [[effective-harnesses-young-2025]]

- [77] formato da lista de funcionalidades: secao "Feature list", exemplo JSON com `"passes": false` e "we landed on using JSON for this".

### Earendil (2026), Pi — [[pi-earendil-2026]]

- [67] "It comes out of the box with only 4 tools"; "its system prompt and tool definitions come in below 1,000 tokens". Citacao acrescentada em 24f.
- [76] identificacao do *harness*. O post nao fala de licenca, modo sem interface ou URL base; esses fatos estao em pi.dev ("`pi -p`", MIT, provedores via `models.json`), nao citado.
- Titulo "Pi, Minimal and Performant", 4 ago. 2026; a URL com `pi-autoresearch-and-databricks` e a do proprio post.

### Opencode (2026a), repositorio — [[opencode]]

- [67] README lista os agentes build/plan, o subagente general e o pedido de permissao do modo plan. Citacao acrescentada em 24f.
- [76] identificacao do *harness*. URL base compativel com OpenAI: opencode.ai/docs/providers ("baseURL"), nao citado.

### Opencode (2026b), Zen — [[zen-opencode-2026]]

- [79] "OpenCode Zen is an AI gateway"; modelos "free on OpenCode for a limited time". Os *endpoints* variam por modelo (responses, messages, chat/completions): os modelos escolhidos precisam usar chat/completions para passar pelo *proxy* de [76]. Teste anonimo de 2026-09-24: `hy3-free` "not supported"; chamada sem cabecalho de cliente recusada ("from within OpenCode"), mas o Pi, que se identifica como cliente, usa o nivel gratuito (ver `_review.md`).

### Karpathy (2026), LLM Wiki — [[llm-wiki-karpathy-2026]]

- [74] excecao autorizada: origem do metodo do repositorio. "A pattern for building personal knowledge bases using LLMs".

### YuukiFST (2026a), Helmsman — [[helmsman-skill-yuukifst-2026]]

- [74] excecao autorizada: metodo que mapeou as decisoes do Finn. URL publica (HTTP 200).

### YuukiFST (2026b), Finn — [[finn]]

- [77] objeto do estudo: *issue* #1 "Mapa Finn - SaaS universal de financeiro por voz", decisoes nas *issues* #2-#22 (21 *tickets*). O repositorio tambem tem #23-#40, de implementacao.
- Repositorio privado em 2026-09-24, por decisao do autor, ate ficar pronto.

### YuukiFST (2026c), harness-bench

- [74], [76] repositorio do projeto e onde as versoes serao registradas; objetivo 6 [57] promete publicar.
- Repositorio privado em 2026-09-24, por decisao do autor, ate ficar pronto.

## Afirmacoes sem citacao que ficam

- [73] "nao se encontrou comparacao publicada [...] do mesmo produto completo": afirmacao negativa, nao citavel. O precedente mais proximo e [[sol-pi-liu-2026]], Tabela 1, que compara OpenCode e Pi sob o GPT-5.6 Sol no EdgeBench, com tarefas isoladas.
- [76] licenca aberta, modo sem interface e URL base: fatos das documentacoes (pi.dev, opencode.ai/docs/providers), nao das obras citadas.

## Pendencias para o autor

Registradas em `_review.md`, entrada 2026-09-24 "revisao do projeto contra fontes e apostilas".
