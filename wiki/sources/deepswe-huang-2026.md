---
title: DeepSWE (Huang et al., 2026)
type: source
summary: Benchmark de 113 tarefas originais longas; verifiers escritos a mao, 1,4% vs 32,4%
tags: [benchmark, deepswe, verificador, contaminacao, pass-at-1]
created: 2026-09-10
updated: 2026-09-14
dated: 2026-07-08
sources: []
---

# DeepSWE (Huang et al., 2026)

## Identificacao

- Titulo: *DeepSWE: Measuring Frontier Coding Agents on Original, Long-Horizon Engineering Tasks*.
- Autores: Wenqi Huang, Charley Lee, Leonard Tng, Serena Ge (Datacurve).
- arXiv:2607.07946v1 [cs.SE], 8 jul 2026 (titulo data maio 2026). 32 paginas.
- *Preprint*, nao revisado por pares.
- PDF: `raw/sources/2607.07946-huang-deepswe.pdf`.

## Referencia ABNT (como citada no projeto)

HUANG, Wenqi; LEE, Charley; TNG, Leonard; GE, Serena. **DeepSWE**: measuring frontier coding agents on original, long-horizon engineering tasks. arXiv:2607.07946, 2026. *Preprint*, nao revisado por pares. Disponivel em: https://arxiv.org/abs/2607.07946. Acesso em: 28 ago. 2026.

## Desenho

113 tarefas originais escritas do zero em 91 repositorios ativos, 5 linguagens (TypeScript 35, Go 34, Python 34, Rust 5, JavaScript 5), nunca devolvidas ao upstream (solucoes fora do registro publico de treino). Cada tarefa tem verificador escrito a mao que aceita qualquer implementacao correta. Juiz LLM independente discorda do verificador em **1,4% [0,7-2,5%]** vs **32,4% [29,2-35,8%]** nos testes herdados do SWE-Bench Pro (n=735 vs 789 rollouts auditados). Solucoes de referencia tocam **~5,5x mais codigo** que as do SWE-Bench Pro com prompts de metade do tamanho.

## Protocolo travado (reutilizavel)

Todas as 16 configuracoes de fronteira rodam no mesmo *harness* (mini-swe-agent, commit adfe2023, prompt compartilhado, 1 ferramenta bash, shallow clone, timeout 9.000 s, sem teto de passos/custo): 113 tarefas x ~4 rollouts, 7.174 rollouts pontuados, maio 2026. Exclusoes (erros de provedor/verificador/rede, 0-5,3%) vs falhas (timeout, estouro de contexto). Incerteza run-to-run com SE (ex.: GPT-5.5 xhigh pass@1 70,0% [67,2-72,9], pass@4 88%).

## Piloto de *harness* (n=10, indicativo)

Mesmas 10 tarefas SWE-Bench Pro x 3 modelos x 2 *harnesses* (mini-swe-agent vs nativo): Opus 4.7 50% vs 40%; GPT-5.5 40% vs 40%; Gemini 3.1 Pro 40% vs 20%. Autores: nenhuma diferenca significativa (4/10 tem Wilson ~[17-69]%); checagem direcional, nao ranking.

## Custo vs acuracia

Medianas por trial de output tokens, wall-clock e dolares variam **ordem de grandeza** entre agentes **sem correlacao forte** com pass rate. Nao computa custo por tarefa concluida (o projeto computa).

## Verificacao no PDF (2026-09-14)

Conferido em `raw/sources/2607.07946-huang-deepswe.pdf` (pdftotext); VERIFICADO.

- Resumo: "DeepSWE is a benchmark of 113 original, long-horizon software engineering tasks"; "written from scratch across 91 active open-source"; "it disagrees with DeepSWE's verifier about an order of magnitude less often than with SWE-Bench Pro's inherited tests (1.4% versus 32.4%)"; "reference solutions touch 5.5x more code".
- Auditoria do verificador (Secao 4): "67 (false-positive) and 189 (false-negative) of 789 rollouts, 32.4% overall (95% Clopper-Pearson interval [29.2, 35.8]%), against 2 and 8 of 735 for DeepSWE, or 1.4% overall ([0.7, 2.5]%)."
- Protocolo (Secao 5): "9,000 seconds (2.5 hours) [...] we set no step or cost cap. The limit rarely binds: only 67 of the 7,174 scored rollouts (0.9%) reached it."; "mini-swe-agent commit adfe2023".
- Piloto de *harness* (Secao 5.2): "50% vs. 40% for Claude Opus 4.7, 40% vs. 40% for GPT-5.5, 40% vs. [20%]"; "a single 4/10 pass rate has a 95% Wilson interval of roughly [17, 69]%".
- Custo (Secao 6): "Output tokens, wall-clock duration, and dollar cost per trial all vary by an order of magnitude across the agents shown, but none correlates strongly with pass rate".
- Figura 2: linhas adicionadas na solucao de referencia: SWE-Bench Verified 9,9; SWE-Bench Pro 120; DeepSWE 668. O "32,8" da auditoria de 2026-09-11 vem de [[swe-bench-jimenez-2023]] (SWE-bench completo), nao deste PDF.
- Atribuicao (Secao 2): "recent cross-scaffold evaluation finds that the model itself drives task success more than the scaffold does [Merrill et al., 2026]" e Secao 9: "decomposed into the model itself versus the scaffolding around it."

## Limitacoes declaradas (Secao 8)

Pass/fail binario sem credito parcial; so correcao funcional; prompts ~2.000 chars; *harness* unico + misturas de esforco; auditoria pequena com juiz falivel; piloto n=10 no SWE-Bench Pro, nao DeepSWE.

## Uso no projeto

- Ate 2026-09-14 era a suite (8 tarefas Python). Desde entao a suite e o [[finn]] e a obra saiu da lista de referencias; segue como fonte de metodo (abaixo).
- Metodo: protocolo travado + regra de exclusao + SE run-to-run como modelo de H1/H2.
- Oraculo: verificadores funcionais + auditoria independente + taxonomia de patologias (vazamento por git log, stubs, testes alheios quebrando).
- Futuro declarado (§9): decompor escore em modelo vs *scaffolding* — exatamente H2 do projeto.

### Auditoria de conteudo 2026-09-11

- Citada em: §3 [60]; §4 [75].
- Afirmacao sustentada: 113/91, 5,5x vs SWE-Bench Pro, §8 sem credito parcial, 34 tarefas Python, mini-swe-agent em toda linha de base.
- Veredito: CONCRETA; Apache-2.0 so no repositorio; "ordem de grandeza ante SWE-bench" e inferencia (668 vs 32,8 linhas). Detalhe em [[2026-09-11-auditoria-conteudo-referencias]].

## Contradictions

- Minimiza *scaffold* como segunda ordem sob *harness* travado, contra [[stop-comparing-harness-zhang-2026]] e [[holistic-agent-leaderboard-kapoor-2025]]. Ver [[atribuicao-harness-vs-modelo]].
