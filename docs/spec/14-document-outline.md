# 14 — The document outline and its page budget

Ticket [#14](https://github.com/YuukiFST/harness-bench/issues/14). Drafted against in [#20](https://github.com/YuukiFST/harness-bench/issues/20); the *cronograma* it budgets space for is built in [#15](https://github.com/YuukiFST/harness-bench/issues/15).

The deliverable is the IFMT **Projeto de Conclusão de Curso (PCC)**, following the department's own template — *Normas básicas e padrões para a elaboração do Projeto de Conclusão de Curso*, Instituto Federal de Mato Grosso, Campus Octayde Jorge da Silva, Departamento de Área de Informática.

Three sources govern the document and they disagree; §0 states which one wins. In short: the professor's handouts, then the template, then the current ABNT editions.

At well under ten pages the risk this outline exists to prevent is not omission — it is every section arriving as a stub. So the budget is paragraph-level, and each paragraph names what it must carry and which ticket produced it.

The section text itself is Portuguese. This file is the plan, so it is English, with the headings in the exact form the template gives them.

## 0. Which source wins

Three sources govern this document, and they disagree. In descending order:

1. **The course handouts in `files/`** — *Aula 2*, *Aula 3* and *Aula 5*, written by the professor who grades the work. They are the most specific statement of what is expected, and they are the only source that can override the template.
2. **The department template**, `files/Template projeto novo3.pdf`. Binding for structure and formatting wherever the handouts are silent.
3. **The current ABNT editions** — NBR 15287:2025, NBR 6023, NBR 10520 — which fill the gap where both of the above are silent or self-contradictory.

The handouts outrank the template because the template is a skeleton with formatting notes, while the handouts state the reasoning and the order. Where the template shows something the handouts do not mention, the template still wins: it is the artefact the work is compared against.

**`files/` is tracked.** It was not: the handouts and the template are the professor's material and #22 opens this repository to the public, so they were kept as local copies excluded by `.gitignore`. The author reversed that and published three of them — *Aula 3*, *Aula 5* and the template. Every decision they forced is still quoted here with the sentence that forced it, so this file stands on its own for a reader who does not have them, and restoring the `.gitignore` line reverses the reversal.

Three places where the handouts decided against the earlier reading of this file, each recorded at its section below: the *folha de rosto* (§1), the order of the *introdução* (§3.1), and the citation rules (§1).

## 1. The template, and where it overrides the norms

### Structure — six numbered sections, and no others

The template's *sumário* fixes the document at:

```
1 INTRODUÇÃO
2 REFERENCIAL TEÓRICO
3 MATERIAL E MÉTODO
4 ORÇAMENTO
5 CRONOGRAMA
6 REFERÊNCIAS
```

Three consequences, each of which overrides an earlier assumption in this ticket:

- **"Material e Método", not "Metodologia".** The template's own heading.
- **"Orçamento", not "Recursos necessários".** A budget, which changes what the section contains — see §3.4.
- **`REFERÊNCIAS` is numbered section 6**, so it sits *inside* the body and inside the page count. The earlier version of this outline treated it as a post-textual element outside the count; that was wrong, and the budget in §3 is rebuilt around it.

There is **no numbered section for preliminary results**, so Layer 1 does not get one. It becomes the closing subsection of *Material e Método* (§3.3).

### Formatting the template specifies literally

| Element | Rule |
|---|---|
| author name (cover) | bold, 14 pt, centred, uppercase |
| work title (cover) | bold, 16 pt, centred, line spacing 1.5, uppercase |
| section headings | bold, 14 pt, uppercase |
| cover footer | city and year (`Cuiabá` / year) |
| pre-textual | cover page, then *sumário* — the template shows no other pre-textual element, but see *Folha de rosto* below |

### Citations and references

The template's reference examples predate the current norms and use conventions that were dropped: angle brackets around URLs (`Disponível em: <http://…>`) and `Acessado em:` alongside `Acesso em:` in different examples.

**Decision.** The template's *structure* of the reference list is followed. Its *internal inconsistencies* are resolved toward **NBR 6023:2025** — no angle brackets, `Acesso em:` throughout — because the template contradicts itself there and one of the two forms has to be picked. Author surnames stay uppercase **in the reference list**, which both the template and NBR 10520:2023 agree on.

In-text citations follow **NBR 10520:2023**: `(Prodanov; Freitas, 2013, p. 51)`, with all-caps surviving only in the reference list. The template gives no in-text example, so the norm fills the gap with nothing to override it.

**One footnote covers the whole divergence**, placed at its first occurrence.

*Aula 5* is the handout on citations, and it settles four things the template does not:

- **No caps inside parentheses.** `(Silva, 2023)`, not `(SILVA, 2023)` — NBR 10520:2023. Uppercase survives only in the reference list.
- **No `< >` around URLs**, which is where the template contradicts itself.
- **Latin expressions in italic** in the reference list: *et al.*, *in*, *apud*.
- **Four or more authors: all of them, or the first followed by *et al.*** Five names and then *et al.* is neither, and two entries did that.

It also fixes what a direct quotation costs. Over three lines it needs a 4 cm indent, a smaller size, single spacing, no quotation marks, and a locator. The Ning definition ran to about four lines with none of that, so it is a **citação indireta** — the idea in the document's own words, author and year only.

### The norm that governs the genre

**NBR 15287:2025** — 3rd ed., 18.03.2025, which cancels and replaces NBR 15287:2011 — is the norm for a *projeto de pesquisa*, and it is cited in the document's own reference list.
An audit found the text claiming ABNT conformity while citing only NBR 6023 and NBR 10520, which govern references and citations, not the genre.
Two ABNT entries now share the year 2025, so they carry the distinguishing letters `2025a` (NBR 6023) and `2025b` (NBR 15287), and the in-text citation reads `(ABNT, 2023, 2025a, 2025b)`.

Its §4.2.2 is the checklist the document is audited against, and the wording is identical in the 2011 and 2025 editions:

> O texto deve ser constituído por uma parte introdutória, na qual devem ser expostos o tema do projeto, o problema a ser abordado, a(s) hipótese(s), quando couber(em), bem como o(s) objetivo(s) a ser(em) atingido(s) e a(s) justificativa(s).
> É necessário que sejam indicados o referencial teórico que o embasa, a metodologia a ser utilizada, assim como os recursos e o cronograma necessários à sua consecução.

Two consequences for the text, both already enforced:

- **No *resumo*, no *palavras-chave*, no *considerações finais*.** None is listed by NBR 15287; *considerações finais* is a mandatory element of the **article** norm (NBR 6022:2018, 5.2.3). Any of the three appearing here would mean the document was built on an article template.
- **No past tense for the project's own procedure.** No ABNT norm prescribes tense, so the evidence is the norm's own wording: §4.2.2 describes the project in four prospective constructions in a row (*a ser abordado*, *a serem atingidos*, *a ser utilizada*, *necessários à sua consecução*), against NBR 14724:2024, which speaks of *estudo realizado*. Layer 1 is the one exception, and §3.3 gives the reason it survives.

### What the template does not mention

**Folha de rosto.** NBR 15287:2025 makes exactly three elements mandatory — *folha de rosto* (4.2.1.1), *sumário* (4.2.1.6) and *referências* (4.2.3.1) — and makes the **capa optional** (4.1.1).
The template inverts that: it shows a cover and a *sumário*, and no *folha de rosto*.

**Decision: the document carries both.**
This is the one place where the template does not win, and the reason is that it is not a divergence — it is an omission.
The template never says a *folha de rosto* is excluded; it simply shows a model that does not have one, and §1's own rule is that where the template is silent the current norm fills the gap.
Adding the page is **additive**: it removes nothing the template asks for, contradicts no rule it states, and can be deleted in one commit if the professor objects.

It also carries information the cover has no slot for and a PCC proposal is expected to state — the **tipo de projeto and the entity it is submitted to**, and the **orientador**.
Those arrive as bracketed placeholders, so `collect_markers()` reports them and no unfilled field can ship silently.

The page sits between the cover and the *sumário*, and costs nothing against the budget in §3: both are pre-textual and outside the page count.

**Hipótese.** The template's *introdução* lists justificativa, tema, problema, objetivo geral and objetivos específicos, with no hypothesis heading — yet its *referencial teórico* section says that section exists to raise what is needed "para testar a hipótese e solucionar o problema". The hypothesis is therefore expected and simply not enumerated.

It goes in the *introdução* immediately after the *problema*, as a labelled paragraph rather than a numbered subsection. H1 and H2 are the spine of this project (#9), and burying them would gut the document.

## 2. Page budget

**5–7 pages covering sections 1–6**, with the cover and the *sumário* outside the count. Target **6.4 pages**, which writes to neither edge.

| § | Section | Pages | Paragraphs | Source |
|---|---|---|---|---|
| — | Capa, sumário | — | — | template |
| 1 | **Introdução** | 2.0 | 11 | #9, aula 3 |
| 2 | **Referencial Teórico** | 1.0 | 5 | #2, #3 |
| 3 | **Material e Método** | 2.2 | 12 + 1 table | #11, #12, #36, #37, #41 |
| 4 | **Orçamento** | 0.3 | 1 + 1 table | #11, #33, #34 |
| 5 | **Cronograma** | 0.5 | 1 + 1 table | #15 |
| 6 | **Referências** | 0.7 | ~18 entries | #2, #3 |

## 3. Section by section

### 3.1 Introdução — 2.0 pages, 11 paragraphs

**The template fixes the internal order, and it is not the conventional one**: the *justificativa* comes **first**, before the tema. Its stated purpose is to convince the reader the work is worth reading, so the section opens with the argument rather than the context.

The *tema*, *problema*, *hipótese* and *objetivos* are already written in final Portuguese in #9's resolution. **They are budgeted here, not drafted again.** #20 pastes them.

| ¶ | Content |
|---|---|
| 1–3 | **Justificativa.** Template constraint: 2–3 paragraphs, **maximum 12 lines total** |
| 4 | **Tema.** Exactly one paragraph, per the template — the justificativa has already given the context, so this only has to name the object of study |
| 5 | **Problema**, quoted verbatim from #9. **Both clauses** — dropping the second turns the project back into a replication |
| 6 | **Objetivo geral**, quoted from #9 |
| 7 | **Objetivos específicos** 1)–7) as a numbered list, quoted from #9 — the template asks for topics, not prose, and writes them `1) 2) 3)` |
| 8 | **Metodologia**, one short paragraph. *Aula 3* puts it here, "apenas para citar o que vai fazer": how the data is collected, what result is expected, and what method systematises it. §3 carries the full treatment; this one only names it |
| 9–10 | **Hipótese**: H1 and H2, one paragraph each, each stating what refutes it |
| 11 | **How the work is organised.** The template requires this as the closing paragraph of the introdução |

**The hipótese closes the introdução; it does not follow the problema.** An earlier version of this file put it immediately after the *problema*, reasoning that the template omits it and H1/H2 are the spine of the project. Both handouts say otherwise, in the same words: *"Por fim, no encerramento da introdução você deve lançar pelo menos uma hipótese."* The handouts outrank the template (§0), so the hypothesis goes last, after the metodologia paragraph.

**The *justificativa* is the hardest constraint in the document**: 12 lines to carry the whole case. The template asks for data and statistics from authoritative sources, and says so explicitly. What goes in, in this order:

1. **The magnitude is established, with numbers**: AHE Table 1's 24.7 percentage points of spread on a *frozen* model, and the Databricks study's >2x cost variation at equal quality.
2. **This project's own measured number**: **11.4x** first-request payload between a harness and a direct fork of it, measured in #41 on an instrument in this repository — the lineage-fixed case none of the published sources report.
3. **The applied stake**, in one sentence: *"você está mesmo extraindo o máximo do modelo que está pagando para usar?"*

The fourth candidate — that a harness's own cost reporting diverges from what it spends — **does not fit in 12 lines** and moves to the *referencial teórico*, where it supports objective (f).

### 3.2 Referencial Teórico — 1.0 page, 5 paragraphs

**The template defines this section differently from a conventional one**, and the difference is useful: it is explicitly *not* a complete theory of the topic. It exists "para levantar pendências" — to raise what is not yet known but is needed to test the hypothesis and solve the problem.

That is a licence to keep it tight, and it aligns with #9's instruction that this is a positioning section rather than a survey.

| ¶ | Content |
|---|---|
| 1 | Citable definition of *harness*, and the three-layer taxonomy with the arms placed on it (#2) |
| 2 | The bare claim "the harness matters" is **settled**, with the four sources that settled it — AHE Table 1, arXiv 2605.23950's Binding Constraint Thesis, harnessrank.net, the Databricks study. Two of the four are practitioner sources and the text says so |
| 3 | **The pendência this work addresses**: every published comparison contrasts harnesses built by different teams on different foundations, so the measured spread bundles prompt, tool, context and loop design with no way to separate them. CaAH §5.2.1 and §5.2.7 name it; the pi vs oh-my-pi pairing answers §5.2.7 directly |
| 4 | **The second pendência**: what a harness reports about its own cost diverges from what it spends, and Kapoor et al. (2024) and the Holistic Agent Leaderboard (2025) both record that agent evaluations rarely report cost and that cross-harness comparisons are rare. This is objective (f), and it is why the measurement sits at a proxy rather than in the arms' own reporting (#4) |
| 5 | Succ/Mtok as the metric (#2, #11), and the standing caveat that harness effects are **model-specific and can invert in sign** — the Holistic Agent Leaderboard measures Anthropic models scoring higher under one scaffold and OpenAI models under another, on the same benchmark — which is why the design carries two tiers and states conclusions per tier |

Stating that the bare claim is settled is a strength; rediscovering it would be a weakness.

### 3.3 Material e Método — 2.2 pages, 12 paragraphs and one table

**The section the reduction ladder never touches.**

The template asks first for the research-type classification on four axes, and the project's answer maps onto them exactly:

| Axis | This project |
|---|---|
| finalidade | **aplicada** |
| abordagem | **quali-quantitativa** |
| objetivos | **exploratória** |
| procedimentos | **experimental** |

| ¶ | Content |
|---|---|
| 1 | The four-axis classification above, in the template's own vocabulary |
| 2 | **Two measurement layers, reported separately and never combined** (#37). Layer 1 is quota-free and deterministic; Layer 2 is quota-bound and stochastic. Layer 1 names the mechanism, Layer 2 shows the effect |
| 3 | Arms: harness zero as the scientific control (#12), the third-party set (#23), and the flagship pairing |
| 4 | Suite: 8 Python DeepSWE tasks, frozen at adoption, pinned by commit and per-task `sha256`, scored on `partial` (#36) |
| 5 | Tiers: two free hosted models, reported separately, never averaged (#35) |
| 6 | The measuring instrument: a forcing reverse proxy, with token counts taken **at the proxy** rather than from the gateway, and why (#11, #25, #34) |
| 7 | Limits: one enforced wall clock, **no step cap**, `max_tokens` forced identical, sampling parameters logged but not forced (#11) |
| 8 | Repetitions and dispersion: n ≥ 3 completed runs per cell, median with spread, never a point estimate (#11, #36) |
| 9 | The test: paired Wilcoxon signed-rank on per-task Succ/Mtok, and the pre-registered predictions per tier (#11) |
| 10 | Run classification, including that a **timeout is a result, not a retry**, and that a run carrying a measurement fault is discarded and never repaired (#11) |
| 11–12 + table | **Resultados preliminares do instrumento** — see below |
| — | **Limitações e ameaças à validade**, closing the section |

**Layer 1 lands here, not in a section of its own**, because the template has no numbered section for results. That placement is not a compromise: Layer 1's role in a *projeto* is evidence that the instrument works, which is a *method* claim. Two paragraphs and one table — the per-arm first-request decomposition, and the lineage-fixed **11.4x**, with the two findings that outrank it (every arm resends full history at a near-constant per-step increment; one arm spends an unreported auxiliary model call per session).

**This is also the presentation's figure** (#21). The map fixes a figure as the atomic visual deliverable, and this is the one that exists today regardless of what the free tier does.

**The limitations paragraph is mandatory** (#9): model specificity (#31); the small-model transfer question deliberately left open (#24, on this project's own grounds rather than on a citation); absolute results not being leaderboard-comparable, since every published DeepSWE baseline uses `mini-swe-agent` (#33); and cost as an order-of-magnitude counterfactual (#11).

### 3.4 Orçamento — 0.3 pages, one paragraph and one table

The template asks for a **budget**, which is a stronger framing than the "recursos necessários" this ticket originally assumed — and it happens to suit this project, because the answer is a number.

| Item | Cost |
|---|---|
| Model inference (both tiers, OpenCode Zen free) | R$ 0,00 |
| Runner and benchmark (Pier, DeepSWE — Apache-2.0) | R$ 0,00 |
| Machines (personal NixOS box, personal Windows box) | R$ 0,00 — already owned |
| **Total** | **R$ 0,00** |

The paragraph states the constraint that produced that number and why it shapes the method: **the binding limit is quota, not money** — roughly 10 requests per 6 minutes against 60–270 model requests per task (#34, #33) — which is why the matrix is batched across days rather than run in one sitting. It also names the counterfactual: what the same token volume would have cost at the vendors' published paid rates, presented as an order of magnitude (#11).

Docker is mandatory (Pier hard-fails without it, #33) and the GPU is irrelevant to every reported result — both worth one clause each, because they are the two pieces of infrastructure a reader would otherwise assume cost something.

### 3.5 Cronograma — 0.5 pages, one paragraph and one table

**The template gives the exact table format**: rows are `FASES`, columns are months. Its example rows are `LEITURA`, `DEFINIÇÃO DO TEMA`, `ESCREVENDO INTRODUÇÃO`, `ESCREVENDO REFERENCIAL TEÓRICO`, `ESCREVENDO MATERIAL E MÉTODO`, `ELABORANDO AS REFERÊNCIAS`, over `MARÇO`–`JULHO`.

#15 builds the real table. Two things it must carry beyond the template's example rows, because this project has an experiment the template's example does not: **executing the matrix** and **analysing the results**.

The framing paragraph states the cadence — **one matrix batch per day**, because the free cap is the binding constraint — so a schedule spanning weeks reads as a design consequence rather than as slippage.

The month columns cannot be filled until the submission date is known, which is [#7](https://github.com/YuukiFST/harness-bench/issues/7).

### 3.6 Referências — 0.7 pages, ~18 entries

Numbered section 6 per the template, and therefore inside the page count.

Formatted per **NBR 6023:2025** where the template contradicts itself (§1). Two cases recur here and the template covers neither:

- **arXiv preprints** — cited as electronic documents with the arXiv identifier and access date, and **marked as preprints**. They are not peer-reviewed and the document should not imply otherwise.
- **Authorless web sources** — harnessrank.net, earendil.com — carry access dates, and the *referencial teórico* names what kind of source each is when it cites them.

The public repository (#22) is cited here by URL. It is what makes objective (g) — re-execution at zero monetary cost — checkable rather than asserted.

## 4. No appendix

The template's *sumário* has six sections and no *apêndice*, so the question is settled by the template rather than by preference. It is also the right answer independently: the artifact is a public repository (#22) with the raw dataset and the analysis scripts in it, and a URL a reader can run is worth more than pages nobody can execute.

## 5. The reduction ladder

If the draft overruns 7 pages, cut in this order:

1. **Resultados preliminares** in §3.3 to one table and one paragraph (−0.3).
2. **Referencial teórico** to 0.8, merging the taxonomy into the definition paragraph (−0.2).
3. **Orçamento** prose to two sentences, keeping the table (−0.1).
4. **Referências** by dropping the complementary references that no in-text citation uses (−0.2). A reference list is not a bibliography.

**Never cut:** *Material e Método*, the limitations paragraph, the *justificativa* (already at the template's 12-line floor), or either half of the *problema*. Those are what make it a research project rather than a report, and #9 fixes three of the four.

If the ladder does not reach, the overrun is raised with the professor. It is not paid for by thinning the method.
