# 11 — The experimental protocol

Ticket [#11](https://github.com/YuukiFST/harness-bench/issues/11).
This is the protocol for **Layer 2**, the quota-bound outcome layer.
Layer 1 has its own protocol and is already built ([#41](https://github.com/YuukiFST/harness-bench/issues/41), [`41-layer1-request-shape.md`](41-layer1-request-shape.md)); the two layers are reported separately and never combined into one number, but Layer 1 supplies the fixed load that H2 is tested on.

Rewritten on 2026-09-14 when the object of the experiment changed: instead of a DeepSWE suite run through harness zero, pi, oh-my-pi and third-party arms, the two arms now build the same product, [Finn](https://github.com/YuukiFST/Finn/issues/1).
Revised the same day: the arms no longer run isolated tickets from author-written reference states; each arm builds the whole product **from scratch, from one frozen specification**, unit by unit in one workspace, and the comparison is on the tokens each harness spends to get there.
The author's first proposal was to let OpenCode build Finn, have it emit a specification, and hand that to pi; it was replaced because the two arms would then receive different inputs (issues vs. a specification distilled from a finished system) and the token difference could not be attributed to the harness.
Every rule below is either decided here or inherited from a closed ticket with the ticket named.
Where a number cannot be fixed without a run that has not happened, this document fixes the **rule that produces it** and says plainly what run produces it.

## 1. Unit of analysis

A **construction** (the run) is one execution of one arm, at one tier, that builds the whole product from an empty workspace, unit by unit, producing one result record per unit and one per construction.
A **cell** is one `(arm, tier)` pair and holds *n* constructions.

- **Arms** — `opencode` (`opencode run --pure --format json`, custom provider in `opencode.json` pointed at the proxy; #6) and `pi` (`pi --mode json`, custom provider in `<PI_CODING_AGENT_DIR>/models.json` pointed at the proxy; #10). Versions pinned at adoption and recorded in every result record. No arm is written by this project.
- **The specification** — one frozen document set, `layer2/spec/`, written by the author from the closed Finn issues (#2–#22) before any run, with agent help and the author's review, and pinned by SHA-256 over the tree. `00-produto.md` carries the product, the stack and the locks that hold for every unit; `01-tenant.md` … `09-cobranca.md` carry one unit each: the decision, its locks and the acceptance criteria in prose. The Vitest acceptance tests are **not** in it. The same bytes go to both arms.
- **Units** — the nine technical tickets of Finn, in dependency order, become the nine units of the specification: #15 tenant, #16 governança, #17 flags, #14 pipeline de voz, #20 confirmação, #21 log, #19 relatório, #18 agendador, #22 cobrança. Each becomes one prompt, byte-identical for both arms: "implement unit *k* as specified in `spec/0k-*.md`, honouring `spec/00-produto.md`".
- **The workspace** — one directory per construction, starting from the frozen initial tree: the specification, `package.json` and `.nvmrc` with the pinned toolchain, nothing else. The arm is invoked once per unit, as a fresh process, in that same directory; what it built for unit *k* is what unit *k+1* starts from. No conversation carries across units (the harness's session features are not part of what is measured); the code does. Nothing the author wrote enters the workspace after the start.
- **Acceptance tests** — one Vitest suite per unit, written by the author before any run, stored outside the workspace. After the arm exits on unit *k* the runner copies the workspace to a scratch directory, copies in the suites of units 1..*k*, and runs them. Unit score = fraction of unit *k*'s tests passed; regression = fraction of units 1..*k−1*'s tests still passed; `concluded` unit = all of unit *k*'s tests pass; `concluded` construction = every test of every unit passes at the end.
- **Tiers** — primary `mimo-v2.5-free`, robustness `hy3-free`, both on `https://opencode.ai/zen/v1` (#35). Reported separately, never averaged.

## 2. What is counted, and where

### 2.1 Token counts

Unchanged from the previous design (#25, #34, #35): the reported counts are measured **at the proxy**, on the bytes on the wire, with `cl100k_base` disclosed for every arm and tier.

| Field | Definition |
|---|---|
| `hb_prefill_tokens` | Σ over requests of the tokenized request body, counted at the proxy |
| `hb_completion_tokens` | Σ over responses of the tokenized completion text, reassembled from the SSE frames |
| `hb_total_tokens` | `hb_prefill_tokens + hb_completion_tokens` |
| `hb_fixed_tokens` | `steps × fixed_load_tokens(arm)`, with `fixed_load_tokens` the Layer 1 first-request prompt tokens of the arm (system prompt + tool schemas) |
| `unit` | the unit the request belongs to: every request between the runner launching the arm for unit *k* and the process exiting is unit *k*'s |
| `hb_conversation_tokens` | `hb_total_tokens − hb_fixed_tokens` |
| `gateway_prompt_tokens`, `gateway_completion_tokens` | as reported by the gateway, recorded for cross-check and for cost |

The divergence `gateway_prompt_tokens − hb_prefill_tokens` is reported per arm (objective 6).

### 2.2 The metrics

- **Primary: tokens per construction** — `hb_total_tokens` summed over the nine units, reported per cell as median with dispersion over its *n* constructions, always next to the final acceptance fraction. Tokens are never reported without the fraction: an arm that fails cheaply must not read as the cheaper arm.
- **Paired: tokens per unit** — `hb_total_tokens` of unit *k*, cell median over the *n* constructions; nine pairs `(opencode, pi)` per tier, the basis of the test in §7.
- **Secondary: Succ/Mtok** (AHE, #2), per construction: `Σ unit fraction / (hb_total_tokens / 1e6)`; and per unit.
- **For H2: fixed-load share** — `hb_fixed_tokens / hb_total_tokens` per unit, and the decomposition of the between-arm difference in `hb_total_tokens` into a fixed-load part and a conversation part, per unit and per construction.

Reported alongside, never collapsed into a metric: `proxy_requests`, `proxy_steps`, `tool_invocations`, `side_call_requests`, `retry_requests`, `Σ inter_request_gap`, `Σ request_latency`.

## 3. Run classification

One class per unit-run, in this precedence. Exit codes are never used (#6, #25).
A construction is `discarded` when any of its units is; otherwise its class is the worst class among its units, and it is `concluded` only when every unit is.

| # | Class | Rule | Enters statistics |
|---|---|---|---|
| 1 | `discarded` | any of #25's nine faults, including a mid-run 429 (#34). Never repaired, never retried | no; counted and reported |
| 2 | `spawn_failed` | the arm never started | no; counted and reported |
| 3 | `timeout` | exceeded the enforced wall clock (§4) for the unit | yes, scored on the fraction the tests pass over what is in the workspace; the construction continues to the next unit from that workspace |
| 4 | `tampered` | the agent edited or deleted `spec/` or another shipped file marked read-only | yes; affected tests score 0 |
| 5 | `unconcluded` | acceptance fraction < 1 | yes, on the fraction |
| 6 | `concluded` | acceptance fraction = 1 | yes |

A timeout is a result, not a retry.
**n is budgeted in runs that enter the statistics, after discards.**

## 4. Hard limits, identical for both arms

- **Wall clock per unit — enforced, and the only limit.** `3 × max(median wall clock of opencode, median wall clock of pi)` on the pilot units (§5.3), rounded up to the next 15 minutes. Until the pilot has run, this number is unset and no construction is archived.
- **Step count — not capped.** A step cap is a harness design decision and would erase the difference under test.
- **`max_tokens` — forced identical by the proxy**, at the model's published output cap read from the upstream (#31).
- **Sampling parameters — logged, reported, not forced** (#28, #34: Zen accepts and does not honour them).
- **Environment isolation is a gate.** Every archived construction asserts a boxed-in `HOME`, agent directory and workspace path (#26, #41) and fails closed. The workspace is a plain directory, not a git checkout: the initial tree is unpacked from the pinned specification, and a fresh `git init` inside it belongs to the arm.
- **Stack services.** PostgreSQL runs in a container started by the runner per construction with a fresh database; the connection string is part of `spec/00-produto.md`. Node.js and pnpm are pinned by version in the initial tree's `package.json` and `.nvmrc`.

## 5. Sizing

### 5.1 The floor

**n ≥ 3 statistical constructions per cell** (#36), because #34 measured 2.4x completion-token variance on byte-identical requests.
When the budget does not fit, **drop coverage, never repetitions**.

### 5.2 The matrix

2 arms × 2 tiers × n = 3 = **12 constructions**, i.e. 108 unit-runs, plus discards.
At the measured free-tier cap of ~100 requests/hour (#34), the wall-clock cost per construction is unknown until the pilot measures how many requests a unit takes; the DeepSWE figure of 60–270 requests per task (#33) is a different agent on a different task and is not carried over. A construction spans days when the quota says so; the runner resumes at the next unit boundary.

### 5.3 Pilot

The first two units (tenant and governança), both arms, primary tier, n = 3 constructions truncated after unit 2, run before anything is archived.
It produces: the wall-clock limit per unit (§4), the requests per unit, the discard rate, and the first estimate of σ (§5.5).

### 5.4 The reduction ladder, in order

1. Truncate constructions after unit 6 on the robustness tier only (units are never skipped from the middle: the construction is the object).
2. Drop the robustness tier entirely, reported as not-run.
3. Never below n = 3, and never below the full nine units on the primary tier.

Six is the Wilcoxon floor: with *k* pairs the smallest attainable two-sided *p* is `2 / 2^k`, which is 0.031 at *k* = 6 and 0.0625 at *k* = 5.
Nine leaves margin for tied pairs.

### 5.5 What the design can detect

Paired two-sided comparison at α = 0.05, 80% power, minimum detectable difference ≈ `2.80 · σ · sqrt(2 / (n·k))`:

| design | δ detectable |
|---|---|
| n = 3, k = 9 | 0.76 σ |
| n = 3, k = 6 | 0.93 σ |

σ is the per-unit dispersion of the metric and is not guessed; the pilot produces the first estimate.
If the design is underpowered and the budget cannot absorb a larger *n*, the shortfall is reported as a limitation with the MDE stated.

## 6. Simulated cost

Both tiers are free; cost is a counterfactual from published paid rates, labelled as such wherever it appears.
Primary tier: MiMo's paid equivalent, $0.14 / $0.28 per 1M (#31), on gateway counts.
Robustness tier: tokens and no dollars unless a published rate for `hy3` is found.

## 7. Pre-registration and analysis

Registered **per tier**, because harness effects invert in sign across models (arXiv:2510.11977).

- **H1** — building Finn from the same specification, OpenCode and pi differ in tokens per construction by a practically relevant margin. Refuted if the two arms' intervals of tokens per construction overlap and the paired test on tokens per unit does not reject.
- **H2** — the fixed load explains the larger part of that difference. Refuted if the conversation part (equivalently, the step count) explains the larger part. A null H2 is a reportable finding: OpenCode's 5.3x first-request payload (#41) recovered in fewer steps is a result about how little request size predicts.

**Direction, registered separately:**

- Tokens per construction — the naive prediction from Layer 1 alone is `pi < opencode`.
- Acceptance fraction — the taxonomy-derived ordering `pi < opencode` (#2), which may invert on the free tiers.
- Succ/Mtok — undetermined; whichever of the two effects above dominates.

**The test.** Wilcoxon signed-rank, paired by unit, two-sided, α = 0.05, on (a) the cell median of tokens per unit and (b) the cell median of Succ/Mtok per unit; critical *W* for *k* = 9 is 5.
Units are paired, not independent: unit *k* starts from what the same arm built in units 1..*k−1*, so a bad unit costs the arm again later. That path dependence is part of what a harness costs and is reported per unit, not corrected away.
For H2, the per-unit decomposition of §2.2 is reported as a table and the share is tested against 0.5 with the same paired test.

## 8. Items the previous design retires

- **Harness zero** (#12, #17) — no control arm; the comparison is between the two arms themselves.
- **The pi / oh-my-pi fork pair** (#41, H2 of the previous design) — replaced by the fixed-load decomposition.
- **DeepSWE, Pier, `partial` from the DeepSWE verifier** (#33, #36) — replaced by Finn tickets and author-written acceptance tests.
- **Goals, families, reference envelope, synthetic library, self-review** (`CONTEXT.md` before 2026-09-14) — not part of this design.
- **Reference states and isolated tickets** (this document earlier on 2026-09-14) — replaced by one construction per arm from the frozen specification; the nine tickets survive as the nine units of that specification.
