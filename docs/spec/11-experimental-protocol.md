# 11 — The experimental protocol

Ticket [#11](https://github.com/YuukiFST/harness-bench/issues/11).
This is the protocol for **Layer 2**, the quota-bound task-outcome layer of [#37](https://github.com/YuukiFST/harness-bench/issues/37).
Layer 1 has its own protocol and is already built ([#41](https://github.com/YuukiFST/harness-bench/issues/41), [`41-layer1-request-shape.md`](41-layer1-request-shape.md)); the two layers are reported separately and never combined into one number.

Every rule below is either decided here or inherited from a closed ticket with the ticket named.
Where a number cannot be fixed without a run that has not happened, this document fixes the **rule that produces it** and says plainly what run produces it.
A number with no run behind it does not go in this file.

## 1. Unit of analysis

A **run** is one execution of one arm, on one task, at one tier, producing one result record.
A **cell** is one `(arm, task, tier)` triple and holds *n* runs.

- **Arms** — harness zero (the in-house ReAct control, #12/#17) plus the third-party set settled in #23.
- **Tasks** — the 8 Python DeepSWE tasks frozen in #36, pinned by commit `0b9fabb` plus per-task `sha256`.
- **Tiers** — primary `mimo-v2.5-free`, robustness `hy3-free`, both on `https://opencode.ai/zen/v1` (#35). Reported separately, never averaged.

## 2. What is counted, and where

### 2.1 The token counts, and which one is the metric

Three closed tickets constrain this and they do not agree with each other's assumptions, so the resolution is stated explicitly.

#25 made `total_prefill_tokens` — the sum of every request's `prompt_tokens` — the basis for simulated cost.
#34 then measured that the gateway's `prompt_tokens` **includes gateway-injected cached content that was never sent** (192 of 248 tokens on a cold first call), and #35 restricted `prompt_tokens` to same-gateway differences only.
An additive per-request offset does not cancel in a ratio: an arm that takes more steps accrues more offset, so a denominator built on gateway `prompt_tokens` would charge arms for content none of them sent, in proportion to a behaviour under test.

**Decision.** The reported token counts are measured **at the proxy**, on the bytes actually on the wire, with one disclosed tokenizer for every arm and every tier:

| Field | Definition |
|---|---|
| `hb_prefill_tokens` | Σ over requests of the tokenized request body, counted at the proxy |
| `hb_completion_tokens` | Σ over responses of the tokenized completion text, reassembled from the SSE frames at the proxy |
| `hb_total_tokens` | `hb_prefill_tokens + hb_completion_tokens` |
| `final_context_tokens` | the last request's proxy-counted prefill — the conversation's actual size |
| `gateway_prompt_tokens`, `gateway_completion_tokens` | as reported by the gateway, recorded for cross-check and for cost |

The tokenizer is `cl100k_base`, named in every record, exactly as in Layer 1 — a **disclosed proxy**, comparable between arms and never against a vendor's own billing count.
The gateway's tokenizer is unpublished for both tiers, so there is no version of this measurement that is simultaneously vendor-exact and cross-arm comparable; this choice takes cross-arm comparability, which is the only thing #9 asks about.

Two consequences worth stating in the methodology:

- **The divergence `gateway_prompt_tokens − hb_prefill_tokens` is itself reported per arm.** It quantifies #34's injected offset, and it is a number no harness's own reporting can produce.
- **harnessrank.net's "exclude cached tokens" rule is satisfied by construction**, not by filtering: a count taken on the bytes the arm sent cannot include content the gateway injected downstream.

`hb_total_tokens` is the denominator of the primary metric. `gateway_completion_tokens` is the billing-truth number and is what simulated cost is computed from (§6).

### 2.2 The primary metric

**Succ/Mtok**, adopted from AHE in #2, computed on `partial` per #36:

```
Succ/Mtok = (Σ partial over the cell's runs) / (Σ hb_total_tokens over the cell's runs / 1e6)
```

`partial` — DeepSWE's test-fraction field — replaces binary `reward` because at this tier binary reads 0 for every arm and measures nothing (#36).
The substitution is disclosed wherever the metric appears, and our absolute Succ/Mtok is **not** leaderboard-comparable: every published DeepSWE baseline uses `mini-swe-agent` (#33), so the comparison this project makes is between its own arms.

Reported alongside, never collapsed into it:

- **Counts** (#25): `proxy_requests`, `proxy_steps`, `tool_invocations`, and on their own lines `side_call_requests` and `retry_requests`. #41 measured why the separation matters: OpenCode spends an unreported 2,526-byte title call per session, and it is a side call, not a step.
- **Timing**: `Σ inter_request_gap` is the headline timing metric — it isolates harness overhead and tool execution from model time, and it is invisible to every harness's own reporting. `Σ request_latency` is reported only with an explicit contention caveat (58% spread on byte-identical requests, #28). **Time to first token is not reported.** Wall time is never presented as a harness property; harnessrank.net excludes speed rankings for the same reason.
- **Mechanism class**: every observed harness effect is classified `none` / `scaffolding` / `reliability`, so "the harness made the model produce better code" and "the harness stopped the run from dying" are not merged into one score column.

## 3. Run classification

One class per run, assigned in this precedence. Exit codes are **never** used: #6 established they cannot classify outcome, and #25 found exit code 0 accompanying a 4x token inflation from silent retries.

| # | Class | Rule | Enters statistics |
|---|---|---|---|
| 1 | `discarded` | any of #25's nine faults, including a mid-run 429 (#34). **Never repaired, never retried** — retrying converts an outage into an apparent harness difference | no; counted and reported |
| 2 | `spawn_failed` | the arm never started | no; counted and reported |
| 3 | `timeout` | exceeded the enforced wall clock (§4) | yes, scores 0 |
| 4 | `no_commit` | `git diff --binary <base> HEAD` is empty, so DeepSWE collects nothing (#36) | yes, scores 0, as its own failure class and never as a task failure |
| 5 | `tampered` | the agent edited a shipped test. Agent behaviour, not a measurement fault, so #25's discard rules do not apply | yes; affected goals score 0 |
| 6 | `completed` | scored on `partial` | yes |

A timeout is a **result, not a retry** (harnessrank.net rule 2, and directly relevant given the OpenCode hangs of #6): a harness that hangs has failed, and retrying it launders a real cost out of the data.

**n is budgeted in completed runs, after discards.** The attempt count exceeds *n* by a discard rate only the pilot (#39) can measure.

## 4. Hard limits, identical for every arm

**Wall clock — enforced, and the only limit imposed.**
pi has no iteration bound at all (#26), so this bound is load-bearing rather than a safety net.
The value is `3 × (median wall clock harness zero needs on the pilot tasks of #39)`, rounded up to the next 15 minutes, and never below Pier's own default.
The factor of 3 is chosen to bound cost without truncating a slow-but-working arm; a timeout below the reference envelope silently converts a design decision into a "failure".
**Until #39 has run, this number is unset and no run is archived.**

**Step count — not capped.**
An imposed step cap is itself a harness design decision, and capping it would erase the difference under test: an arm taking twelve small steps and one taking five large steps are the two behaviours #4 warns cannot be compared on a single "tokens" figure.
The wall clock bounds cost; step count is a dependent variable.

**`max_tokens` — forced identical by the proxy**, at the model's published output cap read from the **upstream, not from `models.dev`**, whose `limit` fields were wrong in both directions (#31).
Forcing it is not optional: #31 measured a model copying its whole chain of thought into `content` when `max_tokens` truncates, which is a *model* behaviour that would present as a *harness* difference.
The proxy already forces `stream_options` (#25), so the mechanism exists.

**Context window** — a property of the tier, recorded per tier, not pinned. (The Ollama context-pinning control inherited from #5 is superseded: #24 removed local inference from the reported experiment.)

**Sampling parameters — logged, reported, not forced.**
Zen accepts `temperature` and `seed` with HTTP 200 and does not honour them (#28, #34), so #4's requirement to *assert* parameter equality is unfalsifiable here.
The proxy logs the effective parameters per request and reports any divergence between arms as a limitation.
They are not normalised, because normalising would create an appearance of control the gateway does not provide.

**Environment isolation is a gate, not a checklist item.**
#26 measured a 2.48x request inflation produced entirely by the operator's home directory, and #41 measured the same class of contamination three more times — the workspace path, the directories above it, and the arms' own install path — each of which produced a wrong number before a run caught it.
Every archived run asserts a boxed-in environment and fails closed if the assertion does not hold.
The unresolved case is the task workspace itself, which for DeepSWE *is* a git checkout: #43 owns it, and it must close before the matrix runs.

## 5. Sizing: repetitions, tasks, and the reduction ladder

### 5.1 The floor

**n ≥ 3 completed runs per cell** (#36), because #34 measured 2.4x completion-token variance on byte-identical requests and there is no deterministic tier to fall back on (#24).
When the budget does not fit, **drop coverage, never repetitions** — the threat is variance, not coverage.

### 5.2 Why the budget is the binding constraint

From measured numbers only: the free tier caps at roughly 10 requests per 6 minutes with no `Retry-After` (#34), i.e. ~100 requests/hour, and one DeepSWE task costs 60–270 model requests (#33).
One run is therefore 0.6–2.7 hours of wall clock at the cap.
A four-arm matrix at n = 3 over 8 tasks and two tiers is 192 completed runs, or **115–518 hours** before discards — between two weeks and two months of continuous running, against a cadence of one batch per day.

The matrix does not fit, and the exact shape that does fit is not decidable from these figures: the 60–270 range is DeepSWE's own, measured with a different agent.
**#39 measures the real per-run request cost.** This section fixes the ladder so that the dev never has to make a scope choice mid-experiment.

### 5.3 The reduction ladder, in order

1. **Narrow the robustness tier to the flagship pairing** — pi vs oh-my-pi only, all tasks, full n. Cuts the matrix from 192 to 144 runs. The cross-model check exists because harness effects invert in sign across models — the Holistic Agent Leaderboard measures Anthropic models scoring higher under one scaffold and OpenAI models under another on the same benchmark (arXiv:2510.11977); that risk is concentrated on H2, which *is* the flagship pairing, so the check is preserved exactly where it matters and H1 becomes a primary-tier claim.
2. **Drop tasks from the tail of the documented draw.** #36's draw is an ordered procedure (`random.Random(0).shuffle`, take 8), so dropping from the tail keeps the remaining set exactly reproducible and the drop itself documented as a truncation rather than a re-draw.
3. **Drop the robustness tier entirely**, reported as not-run. A tier with one arm or one task is not a robustness check and would read as a result while being none.
4. **Never below n = 3, and never below 6 tasks.** The task floor is not a preference — see below.

### 5.4 Why 6 tasks is a hard floor

The comparison in §7 is paired by task, and at this scale the appropriate test is the **Wilcoxon signed-rank test** on per-task Succ/Mtok.
Its smallest attainable two-sided *p* with *k* pairs is `2 / 2^k`:

| k tasks | smallest attainable two-sided p |
|---|---|
| 8 | 0.0078 |
| 7 | 0.0156 |
| 6 | 0.031 |
| 5 | **0.0625** |

At five tasks **no dataset whatsoever can reach p < 0.05** — the experiment would be unable to refute its own hypotheses regardless of how large the effect turned out to be.
Six is the floor; eight leaves margin for tied pairs, which reduce the effective *k*.

### 5.5 What the design can detect

For a paired two-sided comparison at α = 0.05 with 80% power, the minimum detectable difference is approximately `2.80 · σ · sqrt(2 / (n·k))`:

| design | δ detectable |
|---|---|
| n = 3, k = 8 | 0.81 σ |
| n = 3, k = 6 | 0.93 σ |

This is a planning approximation that treats each run as a replicate; the analysis in #19 uses the paired-by-task form.
**σ is not known and is not guessed here** — it is the per-task dispersion of Succ/Mtok, and #39 is the run that produces the first estimate of it.
If that estimate makes the design underpowered and the budget cannot absorb a larger *n*, the shortfall is reported as a stated limitation with the minimum detectable effect given, not smoothed over.

Repeated measures with a reported dispersion is the cheapest rigour available here, and Miller (arXiv:2411.00640) is the source for both halves of it: resample rather than chase a point estimate, and do not touch the temperature to reduce variance. Results are reported as **median with spread, never as a point estimate**.

## 6. Simulated cost

Both reported tiers are free, so cost is a counterfactual computed from published paid rates, and it is labelled as one wherever it appears.

- **Primary tier.** MiMo's paid equivalent is **$0.14 / $0.28 per 1M** (#31). Cost is computed from `gateway_completion_tokens` and `gateway_prompt_tokens` — the vendor's own counts, which is what a bill would be raised on — with the retrieval date recorded next to the figure.
- **No cached-read rate is published for MiMo**, so its cost is computed flat. The primary's split-rate formula is **not** silently applied to a model with no published cache rate (#31).
- **Robustness tier.** #35 chose `hy3-free` without recording a paid rate. If no published rate is found for that exact model, the tier reports tokens and no dollars. A substituted rate would be a fabricated number.
- The frontier price table in `docs/research/04-measuring-tokens-steps-time.md` §8 stays as a clearly-labelled secondary extrapolation ("what this would have cost on Opus 5"), carrying its own stated ~30% tokenizer-mismatch bias.

Simulated cost is presented as an **order-of-magnitude comparison**, never as a precise dollar figure. harnessrank.net's "actual costs, not estimates" rule cannot be honoured here, and the divergence is stated plainly rather than glossed.

## 7. Pre-registration and analysis

Registered **per tier**, because harness effects invert in sign across models (arXiv:2510.11977).

- **H1** — the arms differ. Refuted if the arms' Succ/Mtok intervals overlap across the whole suite. Registered on the **primary tier**; under ladder step 1 the robustness tier no longer carries the full arm set.
- **H2** — the difference survives between a harness and a direct fork of it. Refuted if **pi and oh-my-pi do not differ significantly on Succ/Mtok**, despite the 11.4x first-request payload difference #41 measured. Registered on **both tiers**.

**Direction, registered separately for pass rate and for Succ/Mtok**, so #19 can state plainly whether it held:

- Pass rate — the taxonomy-derived ordering `ReAct mínimo < PI < OpenCode ≈ Cline` (#2).
- Succ/Mtok — the same ordering **may invert**, per the Databricks result (pi beating Claude Code and Codex on cost at equal or better quality, ~3x less context per turn).
- For the flagship pairing, the naive prediction from payload alone is that oh-my-pi costs more per completed task — and that is exactly what H2 puts at risk, since oh-my-pi could recover the payload in fewer steps.

**A null H2 is a reportable finding, not a failed experiment** (#9), and the analysis plan is written so it can say so: an 11.4x payload difference that does not move Succ/Mtok is a result about how little request size predicts outcome, which is a stronger claim than the one the project set out to make.

**The test.** Wilcoxon signed-rank on per-task Succ/Mtok, paired by task, two-sided, α = 0.05 — non-parametric because 8 pairs cannot support a distributional assumption, and paired because task difficulty is the largest nuisance factor in the design. Effect size is reported as the median per-task ratio with its range, alongside the *p*.

## 8. Inherited items that this ticket retires

Stated so they are not re-litigated downstream:

- **Ollama context-window pinning** (#5) — superseded by #24. Local inference contributes no reported result.
- **"Cached tokens are structurally zero"** (#4, true of Ollama) — superseded by #34, which found gateway-injected cached content. §2.1 replaces the property with a construction.
- **Cline's XML tool-call fallback as a validity threat** (#2) — deferred to #23, which owns the arm set. On free Zen models the fallback would apply to Cline regardless of the whitelist, so the choice is declare-or-drop, and it belongs with the arm decision rather than here.
- **Task retirement keyed on Succ/Mtok** (#10, executed by #32) — applies to the **fallback** suite only. #36 froze the DeepSWE subset at adoption, so nothing is retired on the primary route.
- **Self-review fidelity as a reported axis** (#10) — a property of the fallback suite's oracle. DeepSWE has no self-review step, so the axis exists only if the fallback is taken.

## 9. What this protocol still owes, and to which run

| Owed | Produced by |
|---|---|
| the enforced wall-clock value | #39 (median harness-zero wall clock on the pilot tasks) |
| the real per-run request cost, and therefore the matrix shape | #39 |
| the discard rate, and therefore attempts per completed run | #39 |
| σ for the power calculation | #39, refined by #32 |
| the arm set | #23 |
| the task workspace's ancestor-context handling | #43 |

None of these is a decision. Each is a measurement, and none of them is written into this file before the run that produces it.
