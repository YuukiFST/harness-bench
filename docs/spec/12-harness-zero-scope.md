# 12 — Harness zero: the scope of the control

Ticket [#12](https://github.com/YuukiFST/harness-bench/issues/12). Implemented in [#17](https://github.com/YuukiFST/harness-bench/issues/17).

Harness zero is the only arm this project authors, and it exists to answer one question: **how much does *any* harness add over the crudest loop that can still finish the job?**
That makes it a scientific control, and a control has two failure modes that are equally fatal. Too thin and it cannot complete a task, so it produces no reference envelope and every other arm's timeout rests on a guess. Too generous and it stops being a floor.

This document draws the line, and — more importantly — fixes the rules that keep the line from moving once results start arriving.

## 1. Where it runs and what it is

Harness zero is a **Python `BaseAgent` subclass** entering Pier through `--agent-import-path` (#33, adapters in #40). It has no CLI arm adapter, because it does not need one: it is the only arm whose source this project controls.

It ships one additional entry point, `python -m harness_zero`, taking the same arguments the Layer 1 arm adapters take. That exists solely so harness zero appears in the Layer 1 request-shape table as the fourth arm — #41 currently lists three and names the missing control as a limitation.

It satisfies the map's arm-eligibility rule by construction: pointable at an arbitrary OpenAI-compatible base URL, reachable from inside an air-gapped container through the squid sidecar on 443 (#38), and able to commit.

## 2. The tool set: three tools

`read_file`, `write_file`, `bash`.

`bash` runs in the task workspace with a per-command timeout, and it subsumes everything else — listing, searching, running tests, `git commit`. The file tools exist despite that redundancy, and the reason is stated because it is the one place this scope is not simply "the minimum".

### The single-bash alternative, and why it was rejected

`mini-swe-agent` — the harness every published DeepSWE baseline uses (#33) — gives the model exactly one bash tool. Adopting it would buy something real: harness zero's numbers would be the one row in this project's results that *is* comparable to published DeepSWE baselines, and the DeepSWE authors' own concession that a single-bash-tool harness "may hold model families below their native ceiling" would be instantiated by this project's control rather than merely quoted at it.

It was rejected anyway. With one bash tool the model must write files through heredocs and `cat >` redirection, which small models get wrong for reasons of **output formatting**, not of capability. A control that floors because a free-tier model mis-escapes a heredoc has measured the tool interface, not the harness floor — and it would floor *hardest* on exactly the multi-file edits DeepSWE tasks consist of (reference solutions run 526–847 lines across 3–17 files, #33). The failure would then be attributed to minimalism, which is the one claim this arm exists to support.

Running both variants as two control arms was also rejected: #11's budget arithmetic puts the four-arm matrix at 115–518 hours against a one-batch-per-day cadence, and a fifth arm is not affordable at any rung of that ladder.

Three tools also lands harness zero where the calibration note in this ticket asks it to land — just below pi's four (#41 measured pi at 4 schemas, 2,900 tool-schema bytes) rather than far below it. pi is already close to minimal, and a control crippled to manufacture a contrast against it would be a straw man.

## 3. The loop

Plain observe/act, and nothing else:

1. Send the conversation to `/v1/chat/completions` with the three tool schemas.
2. If the reply carries tool calls, execute them in order, append each result as a `tool` message, go to 1.
3. If the reply carries no tool call, stop.

Native tool calling, never an XML-in-prompt fallback — that fallback is the validity threat #2 raised against Cline, and the control must not carry it.
Streaming, through the measuring proxy, with `stream_options` forced by the proxy (#25).

### Terminating conditions

- The model returns a reply with no tool call.
- The enforced wall clock expires (#11). There is **no step cap**, for any arm, by #11's decision.
- The next request would exceed the tier's context window. The loop then stops. **It does not compact, summarise or truncate** — compaction is a harness feature, and a control that has one is not a floor.

Harness zero does **not** commit on the agent's behalf under any of these. DeepSWE collects the answer with `git diff --binary <base> HEAD`, so committing is part of what is measured; a run that ends with nothing committed is classified `no_commit` and scores 0, by the same rule that applies to every other arm (#36, #11).

### What it must not have

Written as a list because #17 will otherwise drift toward it one reasonable feature at a time:

no planning or todo phase · no memory compaction or summarisation · no retry or backoff on a tool error or an HTTP error · no context-file discovery · no skills, extensions or plugins · no auxiliary model call of any kind · no sub-agents · no diff or patch tool · no test-runner integration · no permission prompting · no session persistence.

Two of those are worth their own sentence.

**No retries.** #25 measured a missing `finish_reason` producing four retried requests for one turn, a 4x token inflation, and exit code 0. Retry logic is a reliability feature, and #30's taxonomy makes `reliability` one of the three mechanism classes this project reports — the control must sit at zero on that axis so the axis has an origin.

**No context-file discovery.** #41 measured OpenCode walking up to the enclosing git root and injecting the context files it found — 4,918 bytes of a repository the arm was never pointed at. A DeepSWE task workspace *is* a git checkout, so #43 owns that confound for the third-party arms. Harness zero is immune to it by construction, which makes it the reference row that isolates the effect rather than merely avoiding it.

**No auxiliary model call.** #41 measured OpenCode spending an unreported 2,526-byte title-generation call per session. Harness zero's `side_call_requests` (#25) is zero by design, which is what makes the column meaningful for everyone else.

## 4. The system prompt

It contains only what is mechanically required: the tool contract, the working directory, and the instruction to commit when finished. The commit instruction is a property of DeepSWE's collection mechanism, not a harness feature, and every arm needs it.

It carries **no task-specific content, ever** — a control adjusted to suit a task is not a control, and the reference envelope it produces would encode our tuning rather than the task's shape.

### The anti-tuning gate

A minimal prompt is easy to write and easy to quietly improve after seeing a bad result. The gate is mechanical rather than a matter of discipline:

- The prompt lives in one file, committed with its `sha256`.
- The sha is recorded in **every** run record.
- **Any change to the file after the first archived run invalidates every run that preceded it.** There is no path where a prompt edit and an old result coexist in the dataset.
- #19's analysis reports the sha alongside the results.

Its size is **not budgeted, it is measured**: harness zero's system-prompt bytes and tokens appear in the Layer 1 table (#41) next to pi's 2,499, OpenCode's 9,738 and oh-my-pi's 25,395. A stated token budget would invite writing to the budget; a measured number reported in the same table as every other arm cannot be written to without it showing.

The expectation, stated as a prediction rather than a target: materially below pi's sub-1,000 tokens.

## 5. Alignment with the other arms

Every limit in #11 applies to harness zero unchanged: one enforced wall clock, no step cap, `max_tokens` forced identical by the proxy, sampling parameters logged but not forced.

There is one ordering subtlety, and it is not circular. #11 sets the enforced wall clock at `3 × (median wall clock harness zero needs on the pilot tasks)`, so the control produces the bound that later constrains it. The sequence is:

1. #39 runs harness zero on three pilot tasks under **Pier's own default bound**, disclosed as provisional.
2. That produces the median, and therefore the enforced value.
3. The matrix runs with the enforced value applied identically to every arm, harness zero included.

Harness zero is also the instrument for the reference envelope inherited from #10. That requirement carries over to DeepSWE unchanged in substance: **harness zero must actually be able to complete tasks**, and it must never be tuned per task. What changed is the suite it must survive — #36 replaced #10's synthetic families with 8 Python DeepSWE tasks over real repositories, and #10's suite is now the fallback.

`partial` scoring (#36) is what makes that survivable: harness zero does not need to solve a DeepSWE task to produce an envelope, it needs to work the task and pass some tests. Flash-class models scored 0–36% on DeepSWE v1 (#33), so a low score is the expected result and not a defect of the control.

## 6. The size gate

**≤ 400 lines of Python, excluding tests**, measured over the `harness_zero` package.

Dependencies for HTTP and SSE handling are permitted and do not count — the budget is on harness logic, which is the thing that must stay small. The number is a **CI gate**, not an aspiration: when a change pushes the package over it, a feature comes out. That is the operational definition of "minimal", and it is the only real defence against the control quietly becoming an arm over the life of the project.

## 7. What this leaves open

- **Whether the final arm set makes harness zero the only control** — #23 owns the arm set, and if Cline is dropped for the XML fallback the taxonomy's upper end loses a rung.
- **The provisional bound's exact value** — Pier's default, read from Pier at implementation time in #17, not guessed here.
