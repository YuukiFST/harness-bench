# 09 — Methodological lessons from Fabio Akita's LLM coding benchmark

Research ticket #9.
Question: what can a practitioner-built, iterated LLM coding benchmark teach this project about task-suite design, grading oracles, repetitions, failure handling and results presentation?

Retrieval date for every claim below: **2026-08-07**.

Sources actually read:

- Blog post (Portuguese): https://akitaonrails.com/2026/07/30/novo-llm-benchmark-refiz-todos-os-testes/ — "Novo LLM Benchmark: refiz todos os testes!", 2026-07-30.
- Repository: https://github.com/akitaonrails/llm-coding-benchmark, branch `master`.
- Repository files read individually: `README.md`, `CLAUDE.md`, `docs/success_report.v2.md`, `docs/audit_prompt_template.md`, `docs/IDEA.md`, `prompts/benchmark_prompt_v2.txt`, `prompts/benchmark_followup_v2.txt`, `scripts/run_benchmark_v2.py`, `scripts/verify_scores.py`, `results-v2/v2_claude_opus_5/result.json`.
- Repository metadata via the GitHub REST API: directory listings for `results-v2/`, `docs/`, `scripts/`, plus `/languages` and `/license`.

## Fidelity caveat — read this before trusting any quotation

Two different retrieval channels were used, and they do not have the same reliability.

The GitHub REST API results are **exact**: directory listings, file sizes, the language byte counts, the 404 on the licence endpoint, and the full body of `results-v2/v2_claude_opus_5/result.json` are reproduced here byte-for-byte.

Everything else came through a fetch tool that renders a page and then answers a prompt against it with a small model, and that tool **summarizes even when instructed not to**.
Repeated attempts to obtain the blog post verbatim returned a summary each time; the Portuguese quotations below are what that tool returned when asked for direct quotes, and short quotes may be abridged at their edges.
The same applies to the repository Markdown files.
Consequently this document cites **file paths and section headings**, not `file:line`, for prose sources — the line numbers were not obtainable through that channel and are not invented here.
Two line counts are reported because the tool stated them: `scripts/verify_scores.py` at 177 lines and `scripts/run_benchmark_v2.py` at 341 lines.

Where a question in the ticket is not answered by either source, it is marked **NOT ADDRESSED** rather than filled in by inference.

Throughout, `#### What he did` and `#### What this project should take from it` are kept as separate subsections, and are never blended.

---

## Section 0 — What this source actually is

It is not one benchmark; it is two, plus a documented migration between them.

Version 1 ran from roughly 2026-04 to 2026-06 and is the subject of the repository `README.md` and of `docs/success_report.md`, `docs/success_report.nvidia.md`, `docs/success_report.multi_model.md`, `docs/success_report.multi_model_forced.md`, `docs/success_report.manual_orchestration.md` and `docs/success_report.deepclaude.md`.
Version 2 is the subject of the 2026-07-30 blog post and of `docs/success_report.v2.md`.

The blog post is the announcement of v2 and the retirement of v1.
That makes this source unusually valuable for this project: it contains a benchmark author's own list of what his first design got wrong, which is exactly the artifact Section 9 below extracts.

The repository also carries `docs/report.md`, `docs/report.nvidia.md` and `docs/report.claude-code.md` (auto-generated tables), `docs/cost_analysis.md` and `docs/pricing.md` (both dated 2026-07-09 per `CLAUDE.md`), `docs/orchestration_traces.md`, and integration guides for Codex, deepclaude and llama-swap.

---

## Section 1 — What he measures, and how

#### What he did

**The unit of evaluation is one whole task: a single Rails application built end to end by an autonomous agent.**
It is not a per-file diff and it is not a test-suite pass rate.
`README.md` states the premise plainly: "This repository benchmarks autonomous coding runs against one fixed Rails application brief."

In v2 that one task is decomposed into three phases and fourteen numbered goals, per `docs/success_report.v2.md`:

> "**Three phases** (session-independent — each phase is a fresh CLI invocation continuing via the workspace):
> 1. **Build** against 14 explicitly numbered goals (G1-G14, `prompts/benchmark_prompt_v2.txt`)
> 2. **Runtime validation** — boot, TRUE streaming proof, live tool-call proof, `WEB_CONCURRENCY=2` + restart-survival proof, gates, Docker, compose e2e (`prompts/benchmark_followup_v2.txt`)
> 3. **Self-review** — goal-by-goal PASS/FAIL with evidence + code quality / test coverage / clean-code assessment, written to `SELF_REVIEW.md`"

**He is benchmarking models primarily, with the harness pinned per model — and this is the mirror image of this project, so the transfer is not automatic.**
The main ranking table in `docs/success_report.v2.md` carries a `Harness` column, and different models are ranked while running under different harnesses (Claude Code, Codex, opencode, kimi CLI, grok CLI, agy).
The stated comparability rule is explicit about this:

> "Within-v2 comparability = every model in its natural habitat. v2 scores are NOT comparable to v1 scores (different brief, different harnesses)."

**However, he also runs a genuine harness-with-model-fixed experiment as a sub-campaign**, described in Section 5 below.
That sub-campaign, not the main ranking, is the part of his design that is structurally analogous to this project.

**What he reports per run**, read directly from `results-v2/v2_claude_opus_5/result.json` (exact, via the API):

```json
{
  "billing": "Claude Max subscription",
  "cost_usd_total": 38.9115,
  "elapsed_seconds_total": 4695.04,
  "harness": "claude",
  "label": "Claude Opus 5 (Claude Code)",
  "phases": [ { "phase": "phase1", "cost_usd": 27.019069249999994,
                "elapsed_seconds": 2598.16, "exit_code": 0,
                "file_count_after": 1846, "harness": "claude",
                "session_id": "...", "started_at": "...", "ended_at": "...",
                "timed_out": false,
                "tokens": { "cache": { "read": 41597946, "write": 283129 },
                            "input": 6809, "output": 176597,
                            "total": 42064481 } } ],
  "self_review_present": true,
  "slug": "v2_claude_opus_5",
  "tokens_total": 56814102
}
```

The published table adds the rubric score, the tier, the v1 score and the delta between them; the blog post's "Afinal, qual é o melhor" section shows the shape as, for example, "Fable 5 | 96 | 46 min | $26,03".

**He separates recorded cost from API-equivalent cost.**
The blog names both "Custo registrado" and "Equivalente em API" as distinct reported quantities, and the `billing` field in `result.json` records "Claude Max subscription" — that is, the money actually spent was a flat subscription, while the comparable figure is reconstructed from token counts and public rates.

**There is no composite score.**
The 0-100 rubric score is the only scalar; cost and wall time are reported alongside it and left for the reader to trade off.
The blog's cost-benefit discussion is prose, not a formula.

#### What this project should take from it

The `result.json` shape is the most directly reusable artifact in the entire source, and `harness` being a first-class top-level *and* per-phase field is the single most relevant detail — he arrived at that field because he discovered the harness was a variable, which is this project's premise from the start.

The recorded-cost-versus-API-equivalent split is precisely this project's simulated-cost problem in a different costume: he pays a subscription and reconstructs an API-equivalent figure, this project pays nothing locally and reconstructs a frontier-API figure from `docs/research/04-measuring-tokens-steps-time.md` §8.
Presenting them as two labelled columns rather than one number is his solution and should be this project's too.

Refusing a composite score is the right call for a 5-7 page ABNT paper as well: a weighted blend of tokens, steps and time would be an unfalsifiable invention, whereas three labelled columns are defensible.

---

## Section 2 — The task suite

This is the part of the source with the highest information density for this project's open ticket on the task suite and its oracle.

#### What he did

**There is no suite. There is one task.**
Every model, in both versions, builds the same application from the same brief.
`README.md`: "one fixed Rails application brief".

**The task is a greenfield Rails 8-style SPA chat application in Ruby**, using Hotwire (Turbo Streams + Stimulus), Tailwind, and the `ruby_llm` gem pointed at OpenRouter.
`prompts/benchmark_prompt_v2.txt` requires, among the fourteen goals: newest Ruby/Rails via `mise`, no Active Record / Action Mailer / Active Job, TRUE per-token streaming via Turbo Stream broadcasts, multi-turn payload correctness with a mandated unit test, bounded persistence surviving restart and `WEB_CONCURRENCY=2`, two named tools (`server_time` and `calculator`), structured output for conversation titles, token budgeting with a friendly UI refusal, system prompt via the gem's instructions API, preflight API-key validation, Minitest coverage with mocks mirroring the real gem surface, clean Brakeman / RuboCop / bundle-audit, and a production Dockerfile plus docker-compose.
One constraint is stated as a hard rule: "Failed turns must never be stored into the history that gets replayed to the provider."

**The brief is hand-written by the author.**
`docs/IDEA.md` is the original specification he wrote for the harness itself, listing the local and cloud models to cover and the required deliverables.
It is not drawn from a public benchmark set, not generated, and has no relationship to HumanEval / SWE-bench / anything comparable.

**Difficulty calibration is discussed explicitly, and it is the stated reason v1 was retired.**
The blog's "Por que aposentei o v1" section:

> "Quinze dos quarenta resultados já estavam comprimidos no Tier A, com o topo entre 92 e 97."
> ("Fifteen of the forty results were already compressed into Tier A, with the top between 92 and 97.")

and

> "os modelos novos chegaram ao teto daquela prova"
> ("the new models had hit that test's ceiling")

That is a textbook ceiling effect stated in the author's own words, and his response was to replace the brief with a harder one rather than to add models or rescale the rubric.

**The v2 brief demonstrably restored discrimination.**
Scores in `docs/success_report.v2.md` span from 18 (Grok 4.3 on clean opencode, which "built nothing, twice") to 96 (Claude Fable 5), and the tier bands are populated across their whole range.

**The fourteen numbered goals are themselves the calibration instrument.**
Because G1-G14 are separately checkable, a model that achieves nine of fourteen gets a score in the middle of the range instead of a binary fail, which is what keeps a hard task from collapsing into a floor effect.

**On tasks every model can do or no model can do:** NOT ADDRESSED as a general policy.
He handles the specific instance — a saturated v1 — by retiring the whole brief, but there is no per-goal rule for dropping or replacing a goal that stops discriminating.

**The discriminator that carried v1 was library-API recall on a comparatively obscure gem.**
`README.md`, "Key findings": "**Hallucinated APIs + tests that mock the hallucination is a benchmark-killing pattern.**"
The catalogue of confirmed hallucinations is `RubyLLM::Client.new`, `Openrouter::Client` (wrong casing), `c.user`/`c.assistant` fluent DSL, `response.text` / `response.output_text` / `response.choices`, and the batch form `RubyLLM.chat(messages:)`.
`docs/success_report.nvidia.md` carries the sharpest observation about why this discriminates so well: a Qwen 3.5 27B distilled from Claude reasoning traces "produced code that _looks_ Claude-shaped but still hallucinated the RubyLLM API in the same way", from which he concludes "API correctness is binary recall, not a reasoning skill."

#### What this project should take from it

The numbered-goal decomposition is the transferable idea, not the Rails brief.
A task defined as *n* independently checkable goals gives partial credit for free, and partial credit is the only thing that prevents a weak local model from scoring 0 on everything and producing no discrimination — which is the exact failure mode named in this project's open ticket.

The library-API-recall discriminator is unusually well suited to a 2.6B model.
It is binary, mechanically checkable by grep against real library source, requires no reasoning depth to *measure*, and — per his distillation finding — does not correlate with the general capability that a small model most conspicuously lacks.
A task family of the form "use API *X* correctly, where *X* is real but not in the top thousand most-trained-on libraries" would produce a spread at 2.6B where a general coding task produces a floor.

His ceiling-effect experience argues for calibrating this project's suite *before* the real runs, on the actual LFM2.5-2.6B model, and being willing to replace tasks that land at 0% or 100%.
The cost of not doing so is his v1: months of runs that no longer discriminate.

One task is not enough here.
He can afford a single brief because his dependent variable is a 100-point quality score with effect sizes in the tens of points; this project's dependent variables are token counts and step counts, where a single task gives no way to distinguish a harness effect from a task-specific quirk.

---

## Section 3 — The grading oracle

#### What he did

**The oracle has three layers, and no layer is the model's own test suite passing.**

*Layer 1 — an automated structural scanner.*
`CLAUDE.md` documents `.agents/skills/benchmark-audit/scripts/benchmark_audit_scan.py`, run as `python .agents/skills/benchmark-audit/scripts/benchmark_audit_scan.py results/<slug>`.
It emits JSON covering: required artifacts present, gems (including Tailwind v4 cssbundling detection), Ruby version resolved from the Dockerfile `ARG`, the Gemfile directive or `.ruby-version`, RubyLLM usage patterns split into valid entry forms versus hallucinations (`chat.user(...)`, the paren-less `chat.user msg` form, `chat.assistant`, `chat.system`, `RubyLLM::Client.new`, the batch form, `response.text`), test mocks, error-handling rescue counts, and the model slug the generated app pins.
The scanner was contributed externally (PR #3, @Tavernari) and its regexes were later hardened against real outputs.

*Layer 2 — live runtime proof, executed inside phase 2.*
`prompts/benchmark_followup_v2.txt` forbids regenerating the app and requires, in order: local boot answering over HTTP; a chat message proving the response arrives incrementally through Turbo Stream broadcasts rather than as one completed post-request; a `server_time` call and an arithmetic request proving both tools actually fire; a `WEB_CONCURRENCY=2` launch with a conversation, a restart, and a check that history survived; a full test / RuboCop / Brakeman / bundle-audit pass; `docker build`; and `docker compose up --build` with a real chat end to end.

*Layer 3 — a hand-read audit against a written rubric.*
`docs/audit_prompt_template.md` is the audit contract.
Its core rule is that the auditor must verify against the actual RubyLLM 1.14.1 gem source before flagging any API usage as incorrect, and its output contract is: a one-sentence summary, per-dimension scores with justifications, a total, a tier, a verification section carrying grep evidence for every hallucination claim, one strength and one weakness, under 800 words, with no speculation.

**The v1 rubric was 8 dimensions / 100 points; the v2 rubric is 10 dimensions / 100 points.**
The v2 weights, from `docs/success_report.v2.md` → "Scoring methodology":

| Dimension | Weight | Verified by |
|---|---:|---|
| Goal gates G1-G3, G13-G14 (stack, structure, artifacts) | 15 | scanner + hand-read |
| TRUE streaming (G4) | 10 | phase-2 proof + hand-read of mechanism |
| Multi-turn payload correctness (G5, incl. the required outgoing-array test) | 10 | hand-read + the model's own test |
| Concurrency-safe bounded persistence (G6) | 10 | phase-2 `WEB_CONCURRENCY=2` + restart proof |
| Tool calling (G7) | 10 | phase-2 live proof + hand-read vs gem source |
| Structured output (G8) | 5 | hand-read vs gem source |
| Token budgeting (G9) | 5 | hand-read |
| Robustness (G10: system prompt, preflight, degraded states) | 10 | hand-read |
| Test quality + gates (G11-G12) | 10 | hand-read; mock fidelity vs real gem |
| **Self-review fidelity** (SELF_REVIEW.md verdicts vs audit ground truth) | 15 | audit cross-check of every claimed PASS/FAIL |

**There is a written deduction catalog, applied uniformly.**
From the same section: stale model pin is "−1 gates, and −1 fidelity if the review claims G3 PASS anyway"; an `eval`-based calculator is "−2 tools. A hand-written parser or parsing gem takes no deduction"; a token budget enforced only between turns is "−1 budget, cohort-wide"; a missing required G5 test caps the payload dimension at ~6; "**Unproven runtime claims**: the affected dimension is scored on hand-read evidence only, capped roughly at 60% of max".

**The anti-gaming design is the most important single idea in this source.**
The model writes its own tests, and he treats those tests as evidence about the *model*, never as the oracle.
`README.md`, "What We Learned": "**Benchmark metrics lie about runtime correctness.** Test counts, file counts, and artifact checklists do not measure whether the generated code actually works. A model can write 37 test methods and still call a hallucinated API."
And in the per-model analysis instructions: "Tests that mock a hallucinated API will pass _and_ lie about the code's correctness."
The concrete cases named are DeepSeek V3.2 mocking `RubyLLM::Client.any_instance` (a class that does not exist) and MiniMax M2.7 stubbing a batch signature that does not exist — green suites over code that crashes at runtime.

**The self-review phase turns honesty into a scored dimension.**
The model writes `SELF_REVIEW.md` claiming PASS/PARTIAL/FAIL per goal, and the auditor scores those claims against ground truth, worth 15 of 100.
The blog's "A prova nova" section: "A terceira fase pede que o próprio modelo revise cada objetivo como `PASS`, `PARTIAL` ou `FAIL`… Essa honestidade vale 15 pontos." ("The third phase asks the model itself to review each objective as PASS, PARTIAL or FAIL… That honesty is worth 15 points.")

**The rubric itself is under version control and has a consistency gate.**
`scripts/verify_scores.py` (177 lines, exit 0 on clean) checks, per its own docstring, for "the exact slippage classes that bit us on 2026-07-30": a dimension breakdown that does not sum to the stated total; an explicit "Total NN" that disagrees with the section header; a FINAL STANDINGS row whose score no section supports; rank numbers that do not follow score order or tie rules; and A/B rows whose stated delta does not match `baseline → result`.
Tier assignment is hardcoded in the same script as `"A" if sc >= 83 else "B" if sc >= 73 else "C" if sc >= 51 else "D"`.

**`CLAUDE.md` carries an eight-rule "Scoring discipline" section written after a full-matrix re-audit found six non-directional scoring slips** — some raising scores, some lowering them — "that single-model attention had missed".
Rule 1 is "Score every dimension against the written deduction catalog, not by feel."
Rule 2 requires cross-checking each new model against at least two prior models on the same evidence before locking a dimension.
Rule 5 makes `verify_scores.py` a blocking gate: "Treat a non-zero exit as blocking."

#### What this project should take from it

The principle "the oracle must live outside the artifact the model produces" is the single most reusable idea here, and it transfers exactly.
If this project's tasks are graded by tests, those tests must be held by the runner, never written into the workspace where the agent can edit them — and the runner must diff the test files after each run to prove they were not touched.

The scanner-plus-rubric split maps cleanly onto this project's needs, with the weighting inverted.
He can afford to make the hand-read layer dominant because he is one person judging fifty runs of frontier models; this project needs the mechanical layer to be dominant because a 5-7 page academic artifact cannot defend a subjective 100-point score, and because the number of runs is repetitions × tasks × harnesses.

The written deduction catalog plus an automated verifier over the *report* is a pattern worth stealing wholesale even at small scale: it makes the results table testable rather than merely proofread, and it exists precisely because he discovered drift after the fact.

His self-review dimension is elegant and should be noted as such, but see Section 11 — it does not survive contact with a 2.6B model.

---

## Section 4 — Repetitions, variance and determinism

This is where the source is weakest, and knowing that is itself useful.

#### What he did

**Each model × harness condition is run once.**
There is no repetition protocol, no *n* per cell, and no averaging.
The phrase "single run" never appears; runs are discussed as "runs", "sessions" and "attempts".

**Re-runs happen only as failure handling, and the policy is written down.**
`docs/success_report.v2.md`: "one clean retry for suspicious sub-5-minute phase-1 exits or infrastructure failures; one fresh-session retry for a phase 3 that errors/loops".
And the rule that resolves what a retry means for the score: "Behavior that reproduces on retry is the model's official result."

**Temperature, seed and sampling parameters: NOT ADDRESSED.**
Neither the blog post nor any repository document read here mentions temperature, seed, top-p or any sampling control.
`scripts/run_benchmark_v2.py` sets none — it shells out to vendor CLIs (`claude`, `codex`, `kimi`, `grok`, `agy`, `opencode`), each of which owns its own sampling defaults, so sampling is not merely unreported but not controlled.

**No dispersion measure is reported anywhere.**
No standard deviation, no min/max, no error bars, no confidence intervals — point estimates only, for score, cost, tokens and time alike.

**In place of statistics he declares a noise band by fiat.**
`docs/success_report.v2.md`: "per the standing 2026-06-11 decision, 1-point gaps are within audit noise — read adjacent scores as ties."
That band is then applied as a decision rule, for example on the Grok 4.5 native-CLI A/B: "Δ−1 is inside the stated ±1 noise band".
**How the ±1 band was estimated is NOT ADDRESSED** — it is asserted as a standing decision, with no repeated-run data cited to support it.
Note also that this band is about *audit* noise (two hand-reads of the same artifact disagreeing), not about *run-to-run* noise (the same model producing a different artifact twice), and he does not distinguish the two.

**Run-to-run nondeterminism is nonetheless visible in his prose, qualitatively.**
Gemini 3.5 Flash at high effort: "three attempts… phase 3 failed twice, differently each time".
Qwen3.7 Max: "Three attempts, three failure shapes, one outcome".
Grok 4.3 on clean opencode: "built nothing, twice", with a 48-second stub-quit both times.
So he observed nondeterminism repeatedly, described it, and did not quantify it.

#### What this project should take from it

Take the retry rule and reject the rest.
"Behavior that reproduces on retry is the official result" is a good, cheap, stateable policy and it should go into this project's protocol close to verbatim.

His design gets away with *n*=1 for one reason that does not hold here: his effect sizes are enormous.
The isolation campaign deltas are +67, +37, +29, −22 and −39 points on a 100-point scale, and no plausible run-to-run variance threatens a conclusion at that magnitude.
This project's expected effects — a token-count or step-count difference between two harnesses on the same model and task — are entirely capable of being smaller than the run-to-run spread, so repetitions are not optional here in the way they were optional for him.

His unestimated ±1 band is a cheap win this project can convert into a real one.
Running the *same* harness on the *same* task *k* times and reporting the observed spread costs nothing but GPU time on a local model, produces an empirically grounded noise floor instead of an asserted one, and lets every between-harness difference be reported as inside or outside that floor.
That single step makes this project methodologically stronger than its source on the axis where the source is weakest.

Sampling must be pinned and verified at the wire.
`docs/research/04-measuring-tokens-steps-time.md` §5.6 already establishes that a harness which omits `temperature` silently gets `1.0` from Ollama rather than a Modelfile default, so two harnesses can differ purely because one was silent — the exact class of confound Akita never controlled and never had to notice, because his cost per run made repetition unaffordable anyway.

---

## Section 5 — Harness effects: direct third-party corroboration of this project's thesis

This section exists because the ticket asked for verbatim quotation if a practitioner observed the tooling mattering as much as the model.
He did, repeatedly, across both versions, and it is the headline finding of his v2.

#### What he did

**The v1 observation, from `README.md` → "Key findings":**

> "**The harness matters for correctness.** The same Opus 4.7 model produced Tier A code (correct RubyLLM API) in opencode and Tier 2/3 code (hallucinated `chat.complete`) in Claude Code. Same model, different harness, different correctness."

**The v2 statement of the general claim, from `docs/success_report.v2.md` → harness-isolation campaign:**

> "Agent scaffolding is a model-specific multiplier, not a neutral wrapper. The same plugin shifted scores across a 106-point spread."

**The blog's formulation, from "Por que aposentei o v1":**

> "resultado = modelo + harness + prompt + tools + contexto + execução + auditoria"
> ("result = model + harness + prompt + tools + context + execution + audit")

**And the necessary counterweight, from "O harness também entrou no teste":**

> "O harness nativo não joga pó mágico no modelo. Grok 4.5 praticamente não ligou. Grok 4.3 precisava da estrutura."
> ("The native harness doesn't sprinkle magic dust on the model. Grok 4.5 barely cared. Grok 4.3 needed the structure.")

**The isolation campaign itself: 11 re-runs, started 2026-07-28, model held fixed and harness varied.**
The trigger was a discovered contamination, documented in `CLAUDE.md`: the user's dev environment loaded the `oh-my-opencode-slim` plugin from `~/.config/opencode/` **regardless of `OPENCODE_CONFIG`**, replacing opencode's built-in agents with an "orchestrator" whose delegation machinery contaminated every run — delegation-prone models delegated and exited, producing empty phase 1s.
The fix was to redirect `XDG_CONFIG_HOME` to `config/opencode.xdg-isolated/` for every opencode phase in `run_benchmark_v2.py`, and — critically — the pre-fix results were **kept**, as `results-v2/<slug>.orchestrator/`, so the contamination became a controlled A/B instead of discarded data.
The API listing of `results-v2/` confirms both members of each pair exist on disk, for example `v2_deepseek_v4_flash.orchestrator` alongside `v2_deepseek_v4_flash`.

**The A/B produced a three-way taxonomy of harness effect**, from `docs/success_report.v2.md`:

| Pattern | Models | Effect |
|---|---|---|
| Suppressed by orchestrator | MiniMax M3, Qwen, Kimi, Nex | Triggered delegation, lowered scores |
| Propped up by orchestrator | Gemini 3.1 Pro, Grok 4.3 | Used scaffolding as crutch, lost capability without it |
| Insensitive to harness | Grok 4.5, GLM 5.2, DeepSeek Flash | Scores within ±1 noise |

The deltas, clean minus orchestrator, sorted:

> "M3 +67 · Qwen3.7 +29 · K2.6 +14 · Nex +10 · Flash@high +3 · Grok 4.5 +1 · GLM 5.2 +1 · DeepSeek Flash −1 · Gemini 3.1 Pro −22 · Grok 4.3 −39."

The extreme case: MiniMax M3 scored 24 (DNF) under the orchestrator and 91 clean.
"Under OMO-slim orchestrator, M3 delegated to phantom lanes and produced literally zero code in two attempts. Under vanilla opencode it worked synchronously for 56 minutes and delivered a 91-grade app."

**A second A/B, "Wave 4", compared clean opencode against each model's native vendor CLI:**

| Model | opencode clean | native CLI | Δ | verdict |
|---|---:|---:|---:|---|
| Grok 4.5 | 92 | 91 (grok CLI) | −1 | within noise |
| Grok 4.3 | 18 (built nothing) | 55 (grok CLI) | +37 | out of margin |
| Gemini 3.1 Pro @ high | 62 (opencode, bug-capped) | 88 (agy) | +26 | harness reliability effect |

**The mechanism taxonomy is the most methodologically sophisticated thing in the source**, from `CLAUDE.md` → "Wave 4 native harnesses":

> "**Native-harness A/B verdict**: harness choice is never neutral but the mechanism differs — none (Grok 4.5, within noise), scaffolding (Grok 4.3, +37), reliability (Gemini 3.1 Pro, +26, agy escapes the OpenRouter thought-signature bug). Only a controlled A/B separates them."

That distinguishes a harness helping because it *scaffolds better* from a harness helping because it *fails less often* — two completely different claims that a raw score delta conflates.

**A third, earlier harness effect, from v1**: routing Claude Code's tool loop to DeepSeek V4 Pro via the `deepclaude` shim lifted that model from 69 (Tier B, solo opencode) to 84-89 (Tier A) — "the harness change alone lifted DeepSeek V4 Pro by **+15-20 points**".

**He also publishes the confound that undercuts his own harness comparison**, in `README.md` under "Known confound: opencode dispatches per-family system prompts":

> "`opencode run` substring-matches the model ID and injects a _family-specific_ built-in system prompt — Claude, GPT/Codex, Gemini, and Kimi models each get bespoke prompts while everything else (DeepSeek, Qwen, GLM, MiniMax, Grok, Step, …) receives the generic `default.txt`. opencode-harness scores therefore do not run under literally identical system instructions".

He resolves it by scope rather than by correction: "v2 treats the harness as part of the measured system and documents conditions explicitly; a uniform-prompt condition (as prototyped in PR #13) is earmarked for a possible v3."

#### What this project should take from it

This is the strongest available third-party corroboration of the project's central thesis, and it is worth more than a paper because it is an accidental finding from someone who set out to benchmark models and was forced by his own data to conclude that the harness is a variable.
The 106-point spread on a 100-point scale, and MiniMax M3 moving from 24 to 91 with the model held fixed, are quotable in the paper's justification section exactly as they stand.

The mechanism taxonomy — none / scaffolding / reliability — should be adopted as this project's reporting framework, because this project will produce harness deltas and will need to say *why*.
In this project's metric space the analogue is direct: a harness that uses fewer tokens because its prompts are leaner is a scaffolding effect; a harness that uses fewer tokens because it retries less often, or hangs less often, is a reliability effect; and `docs/research/04-measuring-tokens-steps-time.md` §1.8, §3.6 and §6.3 already provide the instruments to tell them apart (unbounded retries, empty-response retry middleware, identical `messages`-hashes at the proxy).

The `XDG_CONFIG_HOME` contamination is a live warning, not a historical one.
He set `OPENCODE_CONFIG` correctly and was still running under someone else's plugin, and the failure mode was silent — delegation-prone models simply produced nothing.
This project runs OpenCode as an arm on a machine whose user has a populated `~/.config`, and must redirect the entire config surface per run, not just the documented config variable.

Keeping the contaminated runs and reframing them as an A/B arm, instead of deleting them, is a discipline worth copying: a discovered confound is a free experimental condition if the data survives.

Publishing the family-specific-system-prompt confound rather than burying it is the right move and applies here with a twist.
For him it is a confound, because he wants to compare models and the harness varies the prompt underneath him.
For this project it is not a confound at all — the system prompt *is* part of the harness, and comparing harnesses means comparing their prompts.
That inversion is worth one sentence in the paper, because a reader who knows his post will otherwise assume the same objection applies.

---

## Section 6 — Automation and reproducibility

#### What he did

**One command per model.**
`python scripts/run_benchmark_v2.py --model <slug>`, with flags `--config` (default `config/models_v2.json`), `--results-dir` (default `results-v2`) and `--phases` (default `"1,2,3"`, and resumable — passing `"2,3"` continues an existing workspace).
The v1 runner is richer: `--model` (repeatable), `--force`, `--max-runs`, `--timeout-minutes` (default 90), `--report-only`, `--sync-ollama-contexts-only`, `--local-backend`, `--local-api-base`, `--opencode-config`, `--results-dir`, `--report`.

**Language and dependencies.**
`CLAUDE.md`: "All Python scripts use only stdlib (Python 3.10+ required for `X | None` union syntax)."
The GitHub `/languages` endpoint returns Python 228,352 bytes, JavaScript 9,922 bytes, Ruby 2,400 bytes — so it is a Python project with one Node helper (`scripts/browser_probe.mjs`, a Chromium CDP driver for runtime validation).

**Repository layout**, from the API listing of the repository root: directories `.agents/skills/benchmark-audit/`, `config/`, `docs/`, `prompts/`, `results/`, `results-nvidia/`, `results-claude-code/`, `results-v2/`, `scripts/`; files `.ai-jail`, `.gitignore`, `CLAUDE.md`, `README.md`, `llama.md`.
`scripts/` contains `run_benchmark.py`, `run_benchmark_v2.py`, `run_claude_code_benchmark.py`, `manual_dispatch.py`, `analyze_results_runtime.py`, `browser_probe.mjs`, `verify_scores.py`, `warmup_llama_swap.py`, `warmup_ollama_models.py`, and a `benchmark/` package.
The v1 logic is factored into that package as `util.py`, `backends.py` (a `LocalModelBackend` ABC with `OllamaBackend` and `LlamaSwapBackend` implementations), `config.py`, `runner.py` and `report.py`, with `scripts/run_benchmark.py` as a thin CLI over it.

**There is no licence.**
The GitHub licence API returns 404 for this repository, and no `LICENSE` file appears in the root listing.

**Raw per-run records are committed selectively, and the reason is stated.**
`results-v2/v2_claude_opus_5/` contains exactly five files, per the API: `result.json` (2,076 bytes), `phase1.result.json` (501), `phase2.result.json` (497), `phase3.result.json` (488), and `SELF_REVIEW.md` (27,095).
The same five-file shape holds for `results-v2/v2_deepseek_v4_flash/`.
The NDJSON event stream, the generated project tree, the prompt file, the stderr log and the session export are all gitignored, and `README.md` gives the reason: "those files often contain raw env captures including secrets, so do not force-add them."

**Reports split cleanly into auto-generated and hand-written.**
`docs/report.md`, `docs/report.nvidia.md`, `docs/report.claude-code.md`, `docs/ollama_warmup.md` and `docs/llama_swap_warmup.nvidia.md` are rebuilt from `result.json` on every run.
`docs/success_report*.md` are hand-written and are, per `README.md`, "the substance of this repo".
`python scripts/run_benchmark.py --report-only` rebuilds the generated tables from artifacts already on disk without running any model.

**Two hardware profiles are supported by the same scripts with different flags**, per `README.md`: an AMD Strix Halo server (`config/models.json`, `results/`, `docs/report.md`, llama-swap at `192.168.0.90:11435`) and an NVIDIA RTX 5090 workstation (`config/models.nvidia.json`, `results-nvidia/`, `docs/report.nvidia.md`, llama-swap at `localhost:11435`), the latter a strict subset with reduced `benchmark_context_override` values to fit 32 GB of VRAM.

**Two reproducibility bugs he found are directly relevant to this project.**

*The metrics extraction bug.*
`CLAUDE.md`, "opencode metrics: accumulate ALL step_finish events (fixed 2026-08-01, issue #14/PR #15)":

> "`extract_metrics` (scripts/benchmark/runner.py) MUST sum tokens and `part.cost` across **every** `step_finish` event in an opencode phase, not just the last one — each step_finish carries only that step's usage. The original last-step-only version understated opencode cost/tokens by ~40-90× (a 159-step K2.5 phase recorded 1 step)."

The correction banner at the top of `docs/success_report.v2.md` restates it: "A bug in `extract_metrics` recorded only the *last* `step_finish` event of each opencode phase, understating opencode-harness token counts and costs by ~40-90×."
He was able to recompute historical figures only because the NDJSON streams for those runs had been committed.

*The workspace contamination bug.*
`CLAUDE.md`: "**`--force` does NOT wipe `results/<slug>/project/`** — a forced re-run starts with the previous run's completed app in the workspace and the model just polishes it (contaminated result: K3 'finished' in 8 min at 625K tokens). For a clean re-run: `rm -rf results/<slug>` first."

#### What this project should take from it

Adopt his `result.json` schema, adapted: one JSON object per run carrying `slug`, `harness`, `label`, `elapsed_seconds_total`, `cost_usd_total`, `tokens_total`, and a `phases` array whose elements each carry `exit_code`, `timed_out`, `started_at`, `ended_at`, `elapsed_seconds`, `session_id` and a nested `tokens` object.
For this project the `phases` array becomes the task array or the repetition array, and the nested `tokens` object gains the three separately-labelled figures from `docs/research/04-measuring-tokens-steps-time.md` §6.4.

Adopt the generated-versus-hand-written split.
A results table rebuilt from artifacts by a script, plus a separate prose analysis file, is exactly the structure a research artifact plus a written report needs, and `--report-only` makes the table cheap to regenerate as the analysis is revised.

Commit the normalized records; his selective-commit policy is right and his stated reason — raw agent transcripts capture environment variables — applies identically to a local run.
This project's JSONL proxy log is the equivalent risk surface, and while a local Ollama endpoint needs no API key, the harnesses under test may still be configured with real keys for other providers.

His `extract_metrics` bug is independent, real-world corroboration of `docs/research/04-measuring-tokens-steps-time.md` §1.2 and §1.5: OpenCode emits no run-total event, per-step usage must be summed, and a runner that reads only the final event is wrong by up to two orders of magnitude while looking entirely plausible.
It also strengthens the proxy argument in that document's Section 7 more than any code reading could: a native-reporting parser was silently wrong by 40-90× for months, across a published benchmark, and was caught only by an external contributor.
A proxy count is the cross-check that would have caught it on day one.

Wipe the workspace between runs, unconditionally, and treat a run that starts against a non-empty workspace as invalid.
His K3 case — 8 minutes and 625K tokens for what should have been a full build — is exactly the shape of a contaminated result that passes every automated check.

The absence of a licence means none of his code can be vendored into this project.
Reimplement the patterns, cite the repository as the source of the idea, or ask him.

---

## Section 7 — Failures, retries and timeouts

#### What he did

**A hard per-phase timeout, and nothing else, in v2.**
`scripts/run_benchmark_v2.py` defines `PHASE_TIMEOUT = 5400` — 90 minutes per phase — plus `KIMI_TERMINAL_GRACE = 8` seconds for one vendor CLI that lingers after its terminal event.
On timeout the phase loop stops and subsequent phases do not run: `if results[-1]["timed_out"]: print(f"[{model['slug']}] {phase_name} timed out; stopping"); break`.

**The v2 runner does not retry.**
Phases execute once, sequentially.
Retries are a human decision, governed by the written policy quoted in Section 4, and the decision is documented per model in `docs/success_report.v2.md`.

**The v2 runner has no stall detection and no speed gate** — only the hard timeout and a selector-based I/O loop.
The v1 runner did have both: a speed gate that auto-killed a run averaging under 10 tok/s over the first three steps (Qwen 3 32B was killed at 7.32 tok/s), and a 6-minute no-progress timeout sized specifically to tolerate llama-swap's KV-cache cold start, which "can pin the GPU at 100% for 1-3 minutes before inference begins".

**v1 classified every run into one of five statuses**, per `README.md` → "Interpreting Results": `completed`, `completed_with_errors`, `failed`, `timeout`, `not_run`.

**Exit code is explicitly not the classifier.**
The v1 analysis recipe checks `status`, `finish_reason` and `works_as_intended` together, and states: "Look for `status=completed` (or `completed_with_errors`), `finish=stop`, and `works=yes`. Anything else is a structural failure."
The GPT 5.4 Pro case is the worked example: two runs generating 1,278 and 1,118 files, both ending `finish_reason: tool-calls` rather than `stop`, with only 624 output tokens recorded against 1,118 files created — "suggesting event capture was incomplete."

**A failed run is scored, not discarded.**
MiniMax M3 under the orchestrator scored 24 and is labelled DNF; Qwen3.7 Max under the orchestrator scored 22 after three attempts.
Both numbers appear in the A/B tables and both carry the analysis.

**But infrastructure failures are exempt from scoring**, per `docs/success_report.v2.md`:

> "Infrastructure failures (auth, provider bugs) are never charged to the model; provider-side bugs that block validation are documented and cap the affected dimensions instead."

`CLAUDE.md` rule 7 states the consequence: "**Provisional / infra-blocked / DNF runs get NO rankable total on the same scale** — infrastructure failures (quota, provider bugs, auth) are never charged to the model; cap the affected dimensions or mark the run provisional, and keep it out of the ranked table until it completes."
The named instances are a prepaid balance exhausting mid-campaign, Google's non-retryable `Corrupted thought signature` 400, and the Antigravity free preview quota that "one 3-phase run exhausts".

**Stale processes are a documented, recurring failure class.**
`README.md`: "When a benchmark run is killed or times out, opencode child processes can remain alive and hold a SQLite lock on `~/.local/share/opencode/opencode.db`. This causes all subsequent opencode instances to hang silently with zero output. Before re-running benchmarks, always kill stale processes: `pkill -f 'opencode.*run.*agent'`."
`CLAUDE.md` notes the runner now does this automatically before each model run.

**Unparseable or absent output** is handled at the summary level rather than as a status: `run_benchmark_v2.py` records `self_review_present` and flags a missing `SELF_REVIEW.md`, and per-harness metric extractors (`extract_codex_metrics`, `extract_kimi_metrics`, `extract_opencode_metrics`) fall back to a rates-based cost reconstruction when a native cost figure is unavailable.

#### What this project should take from it

The exemption rule is the important one and it needs a local translation.
His categories — quota, auth, provider bug — mostly vanish against a local Ollama endpoint, but the underlying principle does not: an outcome caused by the *measurement apparatus* must not be charged to the arm under test.
For this project the analogous exempt classes are the proxy crashing, Ollama evicting the model mid-run, and the machine thermally throttling; the analogous *non*-exempt classes are the harness hanging, the harness looping, and the harness exhausting its context — because those are properties of the harness, which is exactly what is being measured.
Drawing that line explicitly, in advance and in writing, is the transferable act.

Scoring DNF runs rather than discarding them is right and matters more here than for him.
A harness that fails to complete a task while burning 200K tokens is a *result about that harness*, and dropping it would launder the exact behaviour the study exists to expose.

His stale-`opencode.db`-lock finding is independent confirmation of `docs/research/04-measuring-tokens-steps-time.md` §1.8, which recorded reproduced OpenCode headless hangs producing zero bytes of output and no exit.
That document treated the cause as unknown; this source supplies a concrete mechanism and a concrete mitigation, and the runner should `pkill` stale OpenCode processes and verify no lock is held before every run.

The v1 speed gate is worth reviving in a modified form.
He killed runs below 10 tok/s because they were economically pointless; this project's concern is different — a 2.6B model that is producing tokens but making no progress will otherwise consume the full timeout on every task, multiplied by repetitions and harnesses.
A no-progress detector keyed on the proxy's inter-request gap (no new `POST /v1/chat/completions` for *n* minutes) is a better instrument here than a tok/s threshold, and the proxy already produces the signal.

Adopt the multi-signal outcome classification, and note that both this source and `docs/research/04-measuring-tokens-steps-time.md` §7 arrived at it independently: OpenCode and PI both return exit 0 on failure, and he found `finish_reason: tool-calls` runs that exited cleanly with plausible artifacts.
Classify from task artifacts and from the proxy's terminal `finish_reason`, never from the process exit status.

---

## Section 8 — His own stated limitations

#### What he did

He is franker than most papers, though the limitations are scattered rather than gathered into one section.

**On generality, from the blog's "Afinal, qual é o melhor":**

> "Esta é uma leitura deste projeto. Troque o workload e a ordem pode virar."
> ("This is one reading of this project. Change the workload and the ordering can flip.")

**On scope, from "O que os tiers querem dizer agora":**

> "A prova não mede tudo isso"
> ("The test doesn't measure all of that")

— said of refactoring, debugging, frontend work and domain-specific tasks, which the benchmark does not cover.

**On what a tier means, from `docs/success_report.v2.md`:**

> "**Harness caveat on tiers:** a model's tier is a property of *model × harness*, not the model alone"

`CLAUDE.md` rule 8 spells out the consequence with examples: "Tier is a property of *model × harness* — a native harness can move a model's tier (Gemini 3.1 Pro C on opencode → A on agy; Grok 4.3 D on bare opencode → C on grok CLI)."

**On cross-version comparability:**

> "Within-v2 comparability = every model in its natural habitat. v2 scores are NOT comparable to v1 scores (different brief, different harnesses)."

**On a known uncorrected confound:**

> "**Known engine-level confound**: even vanilla opencode dispatches a family-specific built-in system prompt by model-ID substring"

**On his own metrics, from `README.md` → "Key findings":**

> "**File count and test count are misleading metrics.** Kimi K2.5 wrote 37 tests; none mock RubyLLM. Gemini 3.1 Pro wrote 11 tests with a correctly-signatured `FakeChat` — Gemini scored higher on test quality with fewer tests."

**On refusing to attribute a harness failure to a model**, from `README.md` → "GPT 5.4 Pro: Tool Calling Incompatibility":

> "**Important caveat:** This failure reflects an **opencode/OpenRouter tooling limitation**, not a GPT 5.4 Pro model capability issue… The benchmark's opencode-through-OpenRouter path cannot handle OpenAI's function calling response format, making this an unfair test of GPT's coding ability."

**On the epistemic status of the whole exercise**, from the blog:

> "Só traga artefato e dado. Opinião de ranking já tem demais."
> ("Just bring artifacts and data. There are already plenty of ranking opinions.")

#### What this project should take from it

Four of these are directly reusable in this project's own limitations section, with the roles swapped where appropriate.

The workload-dependence caveat transfers unchanged: a harness ranking on this project's task suite is a ranking on *this* suite, and a different suite may reorder it.

The `model × harness` caveat transfers *inverted* and becomes the project's core claim rather than a caveat — but it must still be stated as a limitation in one direction, because a harness result obtained on LFM2.5-2.6B is a property of *harness × model* and does not automatically extend to a frontier model.
His own data proves this is not a hypothetical: the same harness change was worth +67 for one model, −39 for another, and +1 for a third.

The cross-version incomparability caveat becomes: results are comparable only within one pinned set of harness versions, and `docs/research/04-measuring-tokens-steps-time.md` §1.2 already requires pinning OpenCode's version because its event schema is undocumented and unstable.

His refusal to charge a tooling failure to the model is the single most quotable line for this project's limitations section, because it is the same distinction running the other way: he protects the model from the harness's failures, and this project must protect the harness from the model's failures — a 2.6B model that cannot complete a task at all tells you nothing about the harness driving it.

---

## Section 9 — v1 → v2: what he changed and why

This is the highest-value content in the source, because it is a benchmark author's own list of what his first design got wrong.
Each item below is presented as: what he changed, why, and what failure mode this project can therefore pre-empt.

#### What he did

**1. He retired the entire task brief because it saturated.**
Fifteen of forty results were compressed into Tier A with the top between 92 and 97, so the instrument had stopped discriminating at the high end.
He replaced the brief rather than rescaling the rubric or adding harder models.

**2. He stopped treating the harness as a neutral wrapper.**
The blog's stated reason for retiring v1 includes operational inconsistency — different models ran under different harnesses, distorting comparisons — and v2's answer is to make the harness an explicit, recorded condition and to run a controlled A/B over it.
The reformulation `resultado = modelo + harness + prompt + tools + contexto + execução + auditoria` is the v2 premise.

**3. He added a phase-2 live runtime proof.**
v1's oracle was "does the code look right when read"; v2 requires the run to demonstrate streaming, tool invocation, restart survival under two workers, clean gates, a Docker build and a compose end-to-end chat.
The v1 finding that forced this: "structural completeness does not predict runtime correctness. A model can produce a 9/9 artifact checklist with 37 test methods and still call a non-existent gem API."

**4. He added a phase-3 self-review scored against ground truth, worth 15 of 100.**
This makes over-claiming a scored failure rather than a free option.

**5. He grew the rubric from 8 dimensions to 10 and wrote a deduction catalog**, after a full-matrix re-audit found six non-directional scoring slips that per-model attention had missed.
`CLAUDE.md` rule 1: "Score every dimension against the written deduction catalog, not by feel. … If a deduction you want to apply isn't in the catalog, either don't apply it or add it to the catalog first (and re-check prior models against the new rule)."

**6. He automated consistency checking of the report itself** with `scripts/verify_scores.py`, and made a non-zero exit blocking.

**7. He fixed a metrics-extraction bug that had understated opencode token counts and costs by 40-90×**, then recomputed the historical figures from committed NDJSON and put a correction banner at the top of the report.

**8. He isolated `XDG_CONFIG_HOME` per phase** after discovering that his own machine's opencode plugin was replacing the agent under test, regardless of `OPENCODE_CONFIG`.

**9. He discovered that `--force` re-runs inherited the previous run's finished workspace**, producing a fast, cheap, high-looking result that was entirely contaminated.

**10. He added per-vendor native CLI runners** (`codex`, `kimi`, `grok`, `agy`, `claude`) rather than forcing every model through opencode, after finding that models fail through translation layers for reasons unrelated to their coding ability — GPT 5.4 Pro through opencode-over-OpenRouter, DeepSeek V4 Pro's `reasoning_content` echo requirement, and Kimi K3's rejection of opencode's root-level `anyOf` tool schemas.

#### What this project should take from it

Items 1, 5, 6, 7, 8 and 9 are pre-emptable failure modes, and each maps to a specific decision this project can make now rather than after a wasted campaign.

Calibrate the task suite against the actual model before the real runs, and be willing to replace tasks (item 1).
Write the scoring rules down before scoring anything, and re-check earlier results whenever a rule is added (item 5).
Make the results table machine-checkable (item 6).
Cross-check native token reporting against an independent count — which is precisely what this project's proxy already is (item 7).
Isolate the entire configuration surface per run, not just the documented config variable (item 8).
Wipe the workspace between runs and treat a non-empty starting workspace as a hard error (item 9).

Item 10 is a warning against a design this project should not adopt: he solved harness-model incompatibility by giving each model its own harness, which is exactly the confound this project exists to eliminate.

---

## Directly transferable

Each item names the decision, a one-line justification, and the open ticket it feeds.
Tickets: **[suite]** = task suite and oracle, **[protocol]** = repetitions and metrics protocol, **[presentation]** = results presentation.

1. **Decompose each task into numbered, independently checkable goals (G1..Gn) and score per goal.** **[suite]**
   Partial credit is the only mechanism that stops a hard task collapsing into a floor at 2.6B, and it is how he kept a much harder v2 brief from producing all-zeros.

2. **Hold the oracle outside the workspace: the runner owns the tests, the agent never sees or edits them, and the runner diffs the test files after every run.** **[suite]**
   His single strongest finding is that model-written tests mocking a hallucinated API pass green over code that crashes — "Tests that mock a hallucinated API will pass _and_ lie about the code's correctness."

3. **Use library-API recall as at least one task family: require correct use of a real but not heavily-trained-on library, graded by grep against the library's actual source.** **[suite]**
   Binary, mechanically checkable, and — per his distillation finding — "binary recall, not a reasoning skill", so it discriminates at 2.6B where general coding tasks will not.

4. **Write a deduction catalog before scoring anything, and re-check earlier runs whenever a rule is added.** **[suite]**
   His full-matrix re-audit found six scoring slips in both directions that per-model attention had missed.

5. **Make the results table machine-verifiable: a script that checks per-row arithmetic, totals against headers, ordering, and every stated delta, exiting non-zero on failure.** **[suite] [presentation]**
   `verify_scores.py` is 177 lines of stdlib and turns a proofreading task into a gate.

6. **Adopt his `result.json` shape, with `harness` as a first-class field at both run and phase level.** **[protocol] [presentation]**
   It already carries `elapsed_seconds`, `exit_code`, `timed_out`, `started_at`/`ended_at`, `session_id` and a nested `tokens` object with input/output/cache-read/cache-write/total — nearly a one-to-one fit for this project's needs.

7. **Report recorded cost and reconstructed API-equivalent cost as two separately labelled columns.** **[presentation]**
   He faces the identical problem from the subscription side and solves it by refusing to merge the two numbers; this project's local-cost-zero plus simulated-frontier-cost is the same split.

8. **Split auto-generated tables from hand-written analysis, and make table regeneration a single `--report-only` command.** **[presentation]**
   Lets the prose be revised repeatedly without re-running anything, which matters when the paper goes through review cycles.

9. **Commit normalized per-run records; gitignore raw transcripts, and state the secret-leak reason in the repository.** **[protocol]**
   His NDJSON exclusion is justified by real env captures in tool output, and the same risk exists in this project's proxy log.

10. **Adopt "behavior that reproduces on retry is the official result" as the written retry rule, with a bounded retry allowance for suspicious sub-threshold exits.** **[protocol]**
    A short, stateable policy that prevents ad-hoc re-running from quietly laundering failures out of the data.

11. **Score DNF runs rather than discarding them; exempt only failures of the measurement apparatus, and define those classes in advance.** **[protocol]**
    A harness that burns 200K tokens and fails is a result about the harness; his exemption line (infra never charged to the arm under test) is the right principle with locally-translated categories.

12. **Classify outcomes from artifacts and `finish_reason`, never from process exit status.** **[protocol]**
    Independently confirms `docs/research/04-measuring-tokens-steps-time.md` §7, and his GPT 5.4 Pro case shows a clean exit with 1,118 files, 624 recorded output tokens and `finish_reason: tool-calls`.

13. **Sum every per-step usage event; treat the proxy count as the cross-check that catches a parser bug.** **[protocol]**
    His `extract_metrics` bug understated opencode tokens and cost by 40-90× for months, and corroborates §1.2/§1.5 of the measurement document from outside.

14. **Wipe the workspace between runs, and fail hard on a non-empty starting workspace.** **[protocol]**
    His K3 case finished in 8 minutes on 625K tokens by polishing the previous run's finished app, and passed every automated check.

15. **Redirect `XDG_CONFIG_HOME` (and the whole config surface) to a per-run scratch directory for every harness.** **[protocol]**
    He set `OPENCODE_CONFIG` correctly and still ran under a personal plugin that silently replaced the agent under test.

16. **Kill stale harness processes and verify no SQLite lock is held before each run.** **[protocol]**
    Supplies the mechanism for the zero-output OpenCode hangs recorded as unexplained in §1.8 of the measurement document.

17. **Adopt the none / scaffolding / reliability taxonomy when reporting any harness delta.** **[presentation]**
    "Only a controlled A/B separates them" — and a token or step delta that is really a retry-rate delta is a different claim from one that is really a prompt-size delta.

18. **State the noise band explicitly and read differences inside it as ties — but estimate it from repeated runs instead of asserting it.** **[protocol] [presentation]**
    He declares ±1 by standing decision with no supporting data; a handful of repeated identical-configuration runs on a free local model turns that assertion into a measurement, and is the cheapest place this project can be stronger than its source.

19. **Publish confounds rather than hiding them, including ones that are not fixed.** **[presentation]**
    He documents opencode's family-specific system prompts in the README and defers the fix to a future version; for this project the same fact is not a confound at all, since the system prompt is part of the harness — which is worth one explicit sentence for readers who know his post.

20. **Report score, cost and time side by side without folding them into a composite.** **[presentation]**
    Three labelled columns are defensible in an ABNT paper; a weighted blend of tokens, steps and seconds is an unfalsifiable invention.

---

## Deliberately not transferable

1. **His main ranking varies the model and pins the harness per model; this project does the exact reverse.**
   "Every model in its natural habitat" deliberately confounds model and harness, which is fine for his question and fatal for this one.
   Only the isolation campaign and the Wave 4 A/B are structurally analogous to this project — the ranking table is not a template.

2. **The single-brief design does not survive the change of dependent variable.**
   One task suffices when the outcome is a 100-point quality score with 40-point effects; it cannot support a claim about token or step cost, where a single task's idiosyncrasies are indistinguishable from a harness property.

3. **`n`=1 per condition is affordable for him and is not affordable here.**
   His deltas are +67, +37, −39 — immune to any plausible run-to-run variance — whereas this project's expected effects may be smaller than the noise, so repetitions are mandatory rather than optional.

4. **The scale and cost are out of reach.**
   `results-v2/v2_claude_opus_5/result.json` records a single model's three phases at 4,695 seconds and $38.91, and the campaign spans 50 result directories; this project runs a 2.6B local model at zero budget.

5. **The task itself is far too hard for the model under test.**
   A greenfield Rails 8 application with true token streaming, two working tools, structured output, concurrency-safe persistence and a passing compose end-to-end is a task LFM2.5-2.6B will score zero on, in every harness, producing no discrimination whatsoever — the floor-effect mirror of the ceiling effect that killed his v1.

6. **The 90-minute-per-phase, three-phase budget is incompatible with a repeated-measures design.**
   Repetitions × tasks × harnesses at his time budget is weeks of GPU time; this project's tasks must be minutes, not hours.

7. **The hand-read LLM-judge rubric cannot be the primary oracle here.**
   He is one expert judging fifty runs at 800 words each and can defend a subjective 100-point score by authority; a university research artifact cannot, and needs a mechanical oracle with the human read as a secondary check.

8. **The phase-3 self-review dimension is unusable at 2.6B.**
   Fifteen of a hundred points for goal-by-goal PASS/FAIL honesty presupposes a model that can produce a coherent self-assessment; LFM2.5-2.6B would score uniformly near zero, so the dimension would carry no information while consuming 15% of the scale.

9. **The phase-2 live runtime proof, as he implements it, is too heavy.**
   Having the agent itself drive boot, Docker, compose and a browser is a large extra workload whose failures are mostly not about the harness; a runner-executed test command is the right analogue here.

10. **The per-vendor native CLI runner zoo is the wrong direction for this project.**
    `runner_type` / `harness` values of `codex`, `kimi`, `grok`, `agy` and `claude` exist because he needed each model in its best environment; this project points every harness at one local OpenAI-compatible endpoint on purpose, and adding vendor-specific paths would reintroduce the confound.

11. **His cost measurement has no local analogue.**
    `billing: "Claude Max subscription"` and vendor-reported `cost_usd` come from paid APIs; this project's cost is zero by construction and simulated from the price table in `docs/research/04-measuring-tokens-steps-time.md` §8.

12. **His code cannot be reused directly.**
    The GitHub licence endpoint returns 404 and no `LICENSE` file exists in the repository root, so the patterns can be reimplemented and cited but the source cannot be vendored.

---

## Summary of what could not be established

- **Temperature, seed and any other sampling control: NOT ADDRESSED** in either source. `run_benchmark_v2.py` sets none, delegating entirely to the vendor CLIs, so sampling is uncontrolled rather than merely unreported.
- **A stated repetitions-per-condition policy: NOT ADDRESSED.** Runs are single by default; the only written repetition rule is the failure-retry policy.
- **Any dispersion measure: NOT ADDRESSED.** No standard deviation, min/max, error bars or intervals appear anywhere.
- **How the ±1 noise band was derived: NOT ADDRESSED.** It is cited as a "standing 2026-06-11 decision" with no supporting data, and it conflates audit-reread noise with run-to-run noise.
- **A policy for a goal that every model passes or no model passes: NOT ADDRESSED.** He retires the whole brief on saturation but states no per-goal rule.
- **Total campaign cost and total campaign tokens: NOT ADDRESSED** in the blog post. Per-run figures are available in the committed `result.json` files and could be summed from them.
- **The exact number of models in v2: NOT ADDRESSED** in the blog post. The API shows 50 directories under `results-v2/`, but that count includes `.orchestrator` A/B variants and so overstates the number of distinct models.
- **Licence: absent.** The GitHub licence API returns 404 and no `LICENSE` file exists.
- **How a disagreement between the automated scanner and the hand-read audit is adjudicated: NOT ADDRESSED.** `CLAUDE.md` states only that on a rubric conflict "the project doc wins", which resolves rubric-copy drift, not scanner-versus-human disagreement.
- **Exact `file:line` citations for prose sources: not obtainable.** As stated in the fidelity caveat, the fetch channel for Markdown and HTML returns rendered or summarized content; only the JSON artifacts and directory metadata retrieved through the GitHub API are exact.

The most consequential gap is the complete absence of a variance treatment.
It does not weaken his conclusions, because his effect sizes are large enough to survive almost any plausible noise, but it means this source offers **no** guidance on the repetitions question in this project's open ticket beyond a negative example — and that a repeated-measures design with an empirically estimated noise floor is the clearest axis on which this project can exceed its most useful practitioner reference.
