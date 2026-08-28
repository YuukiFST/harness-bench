# 14 — The document outline and its page budget

Ticket [#14](https://github.com/YuukiFST/harness-bench/issues/14). Drafted against in [#20](https://github.com/YuukiFST/harness-bench/issues/20); the *cronograma* it budgets space for is built in [#15](https://github.com/YuukiFST/harness-bench/issues/15).

The deliverable is an ABNT *projeto de pesquisa* of 5–7 pages. That is a tight budget for a project carrying two measurement layers, two model tiers and four arms, so the risk this outline exists to prevent is not omission — it is every section arriving as a stub.

The section text itself is Portuguese. This file is the plan, so it is English, with the section headings in the form they take in the document.

## 1. Which norms are followed

**The current editions**, not the ones the course material cites. #3 established that four of them are superseded:

| Element | Norm |
|---|---|
| project structure | **NBR 15287:2025** (3rd ed., 18 Mar 2025) — *capa* optional, *folha de rosto* mandatory |
| general formatting | **NBR 14724:2024** (4th ed., errata Apr 2025) |
| references | **NBR 6023:2025** (3rd ed., 21 May 2025) |
| in-text citations | **NBR 10520:2023** — `(Prodanov; Freitas, 2013, p. 51)`; all-caps survives **only** in the reference list |

A document that follows a superseded edition is wrong on its face, and following the current one costs nothing.

**Where the professor's template diverges, the template wins**, and the divergence gets a single footnote at its first occurrence. #7 is the ticket that establishes what the template expects; it is assigned to the dev and does not block this outline, because the rule above resolves the conflict in advance either way.

The in-text casing change is the one most likely to bite: the course material's own examples predate it, so a reviewer comparing against them will see a difference. The footnote names NBR 10520:2023 and moves on.

## 2. What counts toward the 5–7 pages

**This budget assumes 5–7 pages of *elementos textuais*** — from *Introdução* through *Cronograma* — with *folha de rosto*, *sumário* and *referências* outside the count. That is the ordinary reading, and §6 gives the reduction ladder for the case where the professor counts everything.

Target **6.3 pages**, which leaves margin on both sides of the range rather than writing to either edge.

## 3. The budget

| § | Section | Pages | Paragraphs | Source |
|---|---|---|---|---|
| — | Folha de rosto, sumário | — | — | NBR 15287:2025 |
| 1 | **Introdução** | 1.6 | 9 | #9 |
| 2 | **Referencial teórico** | 1.2 | 6 | #2, #3, #30 |
| 3 | **Metodologia** | 2.0 | 11 | #11, #12, #36, #37 |
| 4 | **Resultados preliminares** | 0.7 | 3 + 1 table | #41 |
| 5 | **Recursos necessários** | 0.3 | 2 | — |
| 6 | **Cronograma** | 0.5 | 1 + 1 table | #15 |
| — | Referências | — | — | NBR 6023:2025 |

### 1. Introdução — 1.6 pages, 9 paragraphs

The *tema*, *problema*, *hipótese* and *objetivos* are already written in final Portuguese in #9's resolution. **They are budgeted here, not drafted again.** #20 pastes them.

| ¶ | Content |
|---|---|
| 1–2 | *Tema* and contextualisation. The harness as the layer between model and task, and why a fixed model does not fix the outcome |
| 3 | *Problema*, quoted verbatim from #9. **Both clauses** — dropping the second turns the project back into a replication |
| 4–5 | *Hipótese*: H1 and H2, one paragraph each, each with what refutes it |
| 6 | *Objetivo geral*, quoted from #9 |
| 7 | *Objetivos específicos* (a)–(g) as a list, quoted from #9 |
| 8–9 | *Justificativa* — see below |

**The *justificativa* leans on four things, in this order.** The ticket asks specifically what carries the evidence, and the answer is that three of the four are measured numbers rather than assertions:

1. **The magnitude is already established**: AHE Table 1's 24.7 percentage points of spread on a frozen model, and the Databricks study's >2x cost variation at equal quality.
2. **This project's own measured number**: **11.4x** first-request payload between a harness and a direct fork of it, measured in #41 on an instrument in this repo. It is ours, it is reproducible at zero cost, and it is the lineage-fixed case none of the published sources report.
3. **The applied stake, in the user's own framing**: *"você está mesmo extraindo o máximo do modelo que está pagando para usar?"*
4. **The reporting gap**: harnesses under-report their own cost, and #30 recorded a production benchmark understating it by **40–90x for months** through exactly that error (#4, objective (f)).

### 2. Referencial teórico — 1.2 pages, 6 paragraphs

**A positioning section, not a survey.** #9 fixes its argument, which is why it can be the tightest section in the document.

| ¶ | Content |
|---|---|
| 1 | Citable definition of *harness* and the three-layer taxonomy, with all four arms placed on it (#2) |
| 2 | The bare claim "the harness matters" is **settled**, with all four sources that settled it — AHE Table 1, arXiv 2605.23950's Binding Constraint Thesis, harnessrank.net's method statement, the Databricks study |
| 3 | The gap: every published comparison contrasts harnesses built by different teams on different foundations, so the measured spread bundles prompt, tool, context and loop design with no way to separate them. CaAH §5.2.3 and §5.2.7 name it |
| 4 | This work's answer: hold **lineage** fixed — a harness against a direct fork of it. §5.2.7 asks for "metrics that isolate harness components"; the pi vs oh-my-pi pairing is a direct response |
| 5 | Succ/Mtok as the primary metric, adopted from AHE so the numbers stay legible against published work (#2, #11) |
| 6 | Harness effects are **model-specific and can invert in sign** — #30's +67 / −39 / −22 / +1 across four models — which is why the design carries two tiers and why conclusions are stated per tier |

Stating that the bare claim is settled is a strength; rediscovering it would be a weakness.

### 3. Metodologia — 2.0 pages, 11 paragraphs

**The section least able to absorb a cut** (#9), and the one the reduction ladder in §6 never touches.

| ¶ | Content |
|---|---|
| 1 | Research classification: applied · exploratory · quali-quantitative · experimental |
| 2 | **Two measurement layers, reported separately and never combined** (#37). Layer 1 is quota-free and deterministic; Layer 2 is quota-bound and stochastic. Layer 1 names the mechanism, Layer 2 shows the effect |
| 3 | Arms: harness zero as the scientific control (#12), plus the third-party set (#23), with the flagship pairing identified |
| 4 | Suite: 8 Python DeepSWE tasks, frozen at adoption, pinned by commit and per-task `sha256`, scored on `partial` (#36) |
| 5 | Tiers: two free hosted models, reported separately, never averaged (#35) |
| 6 | The measuring instrument: a forcing reverse proxy, with the token counts taken **at the proxy** rather than from the gateway, and why (#11, #25, #34) |
| 7 | Limits: one enforced wall clock, **no step cap**, `max_tokens` forced identical, sampling parameters logged but not forced (#11) |
| 8 | Repetitions and dispersion: n ≥ 3 completed runs per cell, median with spread, never a point estimate (#11, #36) |
| 9 | The test: paired Wilcoxon signed-rank on per-task Succ/Mtok, and the pre-registered predictions per tier (#11) |
| 10 | Run classification, including that a **timeout is a result, not a retry**, and that a run carrying a measurement fault is discarded and never repaired (#11) |
| 11 | **Limitações e ameaças à validade** — mandatory, see below |

**The limitations paragraph is mandatory** (#9) and covers, in one paragraph:

- **Model specificity** — harness advantage can invert in sign across models (#30), so no conclusion is stated globally.
- **The small-model transfer question, deliberately left open** — the design originally aimed at it and #24 abandoned it because the only viable small model was trained inside one of the arms. Declared future work, citing CaAH §5.2.3. An honest scope boundary reads better than a silent omission.
- **Absolute results are not leaderboard-comparable** — every published DeepSWE baseline uses `mini-swe-agent` (#33).
- **Cost is a counterfactual** computed from published rates, presented as an order of magnitude and never as a dollar figure (#11).

### 4. Resultados preliminares — 0.7 pages, 3 paragraphs and one table

A *projeto de pesquisa* does not require results, and this section is included anyway, for a specific reason: **Layer 1 is already complete** (#41), it costs no quota, it is deterministic, and it is the result that no outage can take away (#37).

It carries **Layer 1 only**. Layer 2 stays in *metodologia* as planned work; presenting a partial Layer 2 would read as a thin experiment rather than as a proposal.

| ¶ | Content |
|---|---|
| 1 | What Layer 1 measures and against what — a mock endpoint, byte-exact partition of the request, one disclosed tokenizer |
| 2 | **The table**: first request per arm — tool schemas, tool-schema bytes, system-prompt bytes, total bytes, tokens |
| 3 | The lineage-fixed result: **11.4x** total request bytes between a harness and its own fork, reproducing #27 on independent code, plus the two findings that outrank it — every arm resends full history with a near-constant per-step increment, and one arm spends an unreported auxiliary model call per session |

**This section supplies the presentation's figure** (#21). The map fixes a figure as the atomic visual deliverable, and this is the one that exists today regardless of what the free tier does.

### 5. Recursos necessários — 0.3 pages, 2 paragraphs

| ¶ | Content |
|---|---|
| 1 | Hardware and software: a personal NixOS box for the experiment, a Windows box for authoring, Docker (mandatory — Pier hard-fails without it), the repo as the sync surface. The GPU is irrelevant to every reported result |
| 2 | **Monetary cost is zero and that is a design constraint, not a limitation**: both tiers are free, and the binding limit is quota rather than money — roughly 10 requests per 6 minutes against 60–270 requests per task, which is why the matrix is batched across days. The public repo (#22) is cited here by URL |

### 6. Cronograma — 0.5 pages, 1 paragraph and one table

One framing paragraph plus the table #15 produces. The paragraph states the cadence — **one matrix batch per day**, because the free cap is the binding constraint — so a schedule spanning weeks reads as a design consequence rather than as slippage.

## 4. No appendix

Decided, not deferred. *Apêndice* is optional under NBR 15287:2025, and this document does not take it:

- At 5–7 pages an appendix signals that the body could not hold its own argument.
- The artifact is a public repository (#22) with the raw dataset and the analysis scripts in it. A URL in *Referências* and in *Recursos necessários* is stronger than an appendix, because a reader can run it.
- Objective (g) is explicitly that the experiment be re-executable at zero monetary cost. An appendix does not advance it; a citable repository does.

## 5. Reference-list notes

Under NBR 6023:2025, with two cases that recur here:

- **arXiv preprints** are cited as electronic documents with the arXiv identifier and access date, and marked as preprints — they are not peer-reviewed and the document should not imply otherwise.
- **Web sources with no author** — harnessrank.net, earendil.com, akitaonrails.com — carry an access date, and the *referencial teórico* names what kind of source each is when it cites them. Two of the four sources establishing the settled claim are practitioner sources, and saying so is more credible than letting the reader discover it.

## 6. The reduction ladder

If the professor's template counts *folha de rosto*, *sumário* and *referências* toward the 5–7 pages, roughly 1.5 pages have to come out. In this order:

1. **Resultados preliminares** to one table and one paragraph (−0.4).
2. **Referencial teórico** to 1.0 page, merging the taxonomy paragraph into the definition (−0.2).
3. **Recursos necessários** to a four-line list (−0.15).
4. **Introdução** contextualisation to one paragraph (−0.2).

**Never cut:** the *metodologia*, the limitations paragraph, or either half of the *problema*. Those three are what make the document a research project rather than a report, and #9 fixes all three.

If the ladder still does not reach, the document goes to 7 pages and the overrun is raised with the professor. It does not reach by thinning *metodologia*.
