"""Revise docs/spec/11-experimental-protocol.md for the construction design (2026-09-14).

Each arm builds the whole product from one frozen specification, unit by unit
in one workspace; the tokens per construction are compared. Reference states
and isolated tickets leave the protocol; the nine tickets become the nine
units of the specification. Exact-string replacements; each must match once.

Usage:
    python tools/protocol_edits_2026-09-14.py
"""

from pathlib import Path

PATH = Path("docs/spec/11-experimental-protocol.md")

R: list[tuple[str, str]] = [
(
"""Rewritten on 2026-09-14 when the object of the experiment changed: instead of a DeepSWE suite run through harness zero, pi, oh-my-pi and third-party arms, the two arms now build the same product, [Finn](https://github.com/YuukiFST/Finn/issues/1), ticket by ticket.
""",
"""Rewritten on 2026-09-14 when the object of the experiment changed: instead of a DeepSWE suite run through harness zero, pi, oh-my-pi and third-party arms, the two arms now build the same product, [Finn](https://github.com/YuukiFST/Finn/issues/1).
Revised the same day: the arms no longer run isolated tickets from author-written reference states; each arm builds the whole product **from scratch, from one frozen specification**, unit by unit in one workspace, and the comparison is on the tokens each harness spends to get there.
The author's first proposal was to let OpenCode build Finn, have it emit a specification, and hand that to pi; it was replaced because the two arms would then receive different inputs (issues vs. a specification distilled from a finished system) and the token difference could not be attributed to the harness.
""",
),
(
"""A **run** is one execution of one arm, on one ticket, at one tier, producing one result record.
A **cell** is one `(arm, ticket, tier)` triple and holds *n* runs.
""",
"""A **construction** (the run) is one execution of one arm, at one tier, that builds the whole product from an empty workspace, unit by unit, producing one result record per unit and one per construction.
A **cell** is one `(arm, tier)` pair and holds *n* constructions.
""",
),
(
"""- **Tickets** — the nine technical tickets of Finn, in dependency order: #15 tenant, #16 governança, #17 flags, #14 pipeline de voz, #20 confirmação, #21 log, #19 relatório, #18 agendador, #22 cobrança. Each becomes one prompt, byte-identical for both arms: the ticket's `## Decision`, its locks, and the owner's stack from the Finn map. The Finn issues are closed and do not change during the experiment.
- **Reference states** — the workspace each ticket starts from is the product as the author left it after the previous ticket, committed to `layer2/tasks/<ticket>/reference/` and pinned by SHA-256 over the tree. Both arms start every ticket from that tree; nothing an arm produced enters the next ticket.
- **Acceptance tests** — one Vitest suite per ticket, written by the author before any run, stored outside the workspace and copied in only by the runner after the arm exits. Score = fraction passed; `concluded` = all passed.
""",
"""- **The specification** — one frozen document set, `layer2/spec/`, written by the author from the closed Finn issues (#2–#22) before any run, with agent help and the author's review, and pinned by SHA-256 over the tree. `00-produto.md` carries the product, the stack and the locks that hold for every unit; `01-tenant.md` … `09-cobranca.md` carry one unit each: the decision, its locks and the acceptance criteria in prose. The Vitest acceptance tests are **not** in it. The same bytes go to both arms.
- **Units** — the nine technical tickets of Finn, in dependency order, become the nine units of the specification: #15 tenant, #16 governança, #17 flags, #14 pipeline de voz, #20 confirmação, #21 log, #19 relatório, #18 agendador, #22 cobrança. Each becomes one prompt, byte-identical for both arms: "implement unit *k* as specified in `spec/0k-*.md`, honouring `spec/00-produto.md`".
- **The workspace** — one directory per construction, starting from the frozen initial tree: the specification, `package.json` and `.nvmrc` with the pinned toolchain, nothing else. The arm is invoked once per unit, as a fresh process, in that same directory; what it built for unit *k* is what unit *k+1* starts from. No conversation carries across units (the harness's session features are not part of what is measured); the code does. Nothing the author wrote enters the workspace after the start.
- **Acceptance tests** — one Vitest suite per unit, written by the author before any run, stored outside the workspace. After the arm exits on unit *k* the runner copies the workspace to a scratch directory, copies in the suites of units 1..*k*, and runs them. Unit score = fraction of unit *k*'s tests passed; regression = fraction of units 1..*k−1*'s tests still passed; `concluded` unit = all of unit *k*'s tests pass; `concluded` construction = every test of every unit passes at the end.
""",
),
(
"""| `hb_fixed_tokens` | `steps × fixed_load_tokens(arm)`, with `fixed_load_tokens` the Layer 1 first-request prompt tokens of the arm (system prompt + tool schemas) |""",
"""| `hb_fixed_tokens` | `steps × fixed_load_tokens(arm)`, with `fixed_load_tokens` the Layer 1 first-request prompt tokens of the arm (system prompt + tool schemas) |
| `unit` | the unit the request belongs to: every request between the runner launching the arm for unit *k* and the process exiting is unit *k*'s |""",
),
(
"""- **Primary: tokens per concluded ticket** — median `hb_total_tokens` over the cell's `concluded` runs. A cell with no concluded run reports the median over all runs and is flagged; H1 is tested on concluded cells only.
- **Secondary: Succ/Mtok** (AHE, #2), computed on the acceptance-test fraction: `Σ fraction / (Σ hb_total_tokens / 1e6)` over the cell's runs. It carries the unconcluded runs that the primary metric leaves out.
- **For H2: fixed-load share** — `hb_fixed_tokens / hb_total_tokens` per run, and the decomposition of the between-arm difference in `hb_total_tokens` into a fixed-load part and a conversation part, per ticket.
""",
"""- **Primary: tokens per construction** — `hb_total_tokens` summed over the nine units, reported per cell as median with dispersion over its *n* constructions, always next to the final acceptance fraction. Tokens are never reported without the fraction: an arm that fails cheaply must not read as the cheaper arm.
- **Paired: tokens per unit** — `hb_total_tokens` of unit *k*, cell median over the *n* constructions; nine pairs `(opencode, pi)` per tier, the basis of the test in §7.
- **Secondary: Succ/Mtok** (AHE, #2), per construction: `Σ unit fraction / (hb_total_tokens / 1e6)`; and per unit.
- **For H2: fixed-load share** — `hb_fixed_tokens / hb_total_tokens` per unit, and the decomposition of the between-arm difference in `hb_total_tokens` into a fixed-load part and a conversation part, per unit and per construction.
""",
),
(
"""One class per run, in this precedence. Exit codes are never used (#6, #25).
""",
"""One class per unit-run, in this precedence. Exit codes are never used (#6, #25).
A construction is `discarded` when any of its units is; otherwise its class is the worst class among its units, and it is `concluded` only when every unit is.
""",
),
(
"""| 3 | `timeout` | exceeded the enforced wall clock (§4) | yes, scored on the fraction the tests pass over what is in the workspace |""",
"""| 3 | `timeout` | exceeded the enforced wall clock (§4) for the unit | yes, scored on the fraction the tests pass over what is in the workspace; the construction continues to the next unit from that workspace |""",
),
(
"""| 4 | `tampered` | the agent edited or deleted a shipped file marked read-only, or touched the acceptance tests once copied in | yes; affected tests score 0 |""",
"""| 4 | `tampered` | the agent edited or deleted `spec/` or another shipped file marked read-only | yes; affected tests score 0 |""",
),
(
"""- **Wall clock — enforced, and the only limit.** `3 × max(median wall clock of opencode, median wall clock of pi)` on the pilot tickets (§5.3), rounded up to the next 15 minutes. Until the pilot has run, this number is unset and no run is archived.""",
"""- **Wall clock per unit — enforced, and the only limit.** `3 × max(median wall clock of opencode, median wall clock of pi)` on the pilot units (§5.3), rounded up to the next 15 minutes. Until the pilot has run, this number is unset and no construction is archived.""",
),
(
"""- **Environment isolation is a gate.** Every archived run asserts a boxed-in `HOME`, agent directory and workspace path (#26, #41) and fails closed. The workspace is a plain directory, not a git checkout: the reference state is unpacked from the pinned tree, and a fresh `git init` inside it belongs to the arm.
- **Stack services.** PostgreSQL runs in a container started by the runner per run with a fresh database; the connection string is part of the prompt. Node.js and pnpm are pinned by version in the reference state's `package.json` and `.nvmrc`.""",
"""- **Environment isolation is a gate.** Every archived construction asserts a boxed-in `HOME`, agent directory and workspace path (#26, #41) and fails closed. The workspace is a plain directory, not a git checkout: the initial tree is unpacked from the pinned specification, and a fresh `git init` inside it belongs to the arm.
- **Stack services.** PostgreSQL runs in a container started by the runner per construction with a fresh database; the connection string is part of `spec/00-produto.md`. Node.js and pnpm are pinned by version in the initial tree's `package.json` and `.nvmrc`.""",
),
(
"""**n ≥ 3 statistical runs per cell** (#36), because #34 measured 2.4x completion-token variance on byte-identical requests.""",
"""**n ≥ 3 statistical constructions per cell** (#36), because #34 measured 2.4x completion-token variance on byte-identical requests.""",
),
(
"""2 arms × 9 tickets × 2 tiers × n = 3 = **108 statistical runs**, plus discards.
At the measured free-tier cap of ~100 requests/hour (#34), the wall-clock cost per run is unknown until the pilot measures how many requests a Finn ticket takes; the DeepSWE figure of 60–270 requests per task (#33) is a different agent on a different task and is not carried over.
""",
"""2 arms × 2 tiers × n = 3 = **12 constructions**, i.e. 108 unit-runs, plus discards.
At the measured free-tier cap of ~100 requests/hour (#34), the wall-clock cost per construction is unknown until the pilot measures how many requests a unit takes; the DeepSWE figure of 60–270 requests per task (#33) is a different agent on a different task and is not carried over. A construction spans days when the quota says so; the runner resumes at the next unit boundary.
""",
),
(
"""Two tickets (#15 tenant and #20 confirmação, the smallest and a mid-sized one), both arms, primary tier, n = 3, run before anything is archived.
It produces: the wall-clock limit (§4), the requests per ticket, the discard rate, and the first estimate of σ (§5.5).
""",
"""The first two units (tenant and governança), both arms, primary tier, n = 3 constructions truncated after unit 2, run before anything is archived.
It produces: the wall-clock limit per unit (§4), the requests per unit, the discard rate, and the first estimate of σ (§5.5).
""",
),
(
"""1. Drop tickets from the **end** of the dependency order on the robustness tier only.
2. Drop the robustness tier entirely, reported as not-run.
3. Never below n = 3, and never below 6 tickets on the primary tier.
""",
"""1. Truncate constructions after unit 6 on the robustness tier only (units are never skipped from the middle: the construction is the object).
2. Drop the robustness tier entirely, reported as not-run.
3. Never below n = 3, and never below the full nine units on the primary tier.
""",
),
(
"""σ is the per-ticket dispersion of the metric and is not guessed; the pilot produces the first estimate.""",
"""σ is the per-unit dispersion of the metric and is not guessed; the pilot produces the first estimate.""",
),
(
"""- **H1** — OpenCode and pi differ in tokens per concluded ticket by a practically relevant margin. Refuted if the two arms' intervals of tokens per concluded ticket overlap across the whole suite.
""",
"""- **H1** — building Finn from the same specification, OpenCode and pi differ in tokens per construction by a practically relevant margin. Refuted if the two arms' intervals of tokens per construction overlap and the paired test on tokens per unit does not reject.
""",
),
(
"""- Tokens per concluded ticket — the naive prediction from Layer 1 alone is `pi < opencode`.""",
"""- Tokens per construction — the naive prediction from Layer 1 alone is `pi < opencode`.""",
),
(
"""**The test.** Wilcoxon signed-rank, paired by ticket, two-sided, α = 0.05, on (a) the cell median of tokens per concluded ticket and (b) the cell Succ/Mtok; critical *W* for *k* = 9 is 5.
For H2, the per-ticket decomposition of §2.2 is reported as a table and the share is tested against 0.5 with the same paired test.
""",
"""**The test.** Wilcoxon signed-rank, paired by unit, two-sided, α = 0.05, on (a) the cell median of tokens per unit and (b) the cell median of Succ/Mtok per unit; critical *W* for *k* = 9 is 5.
Units are paired, not independent: unit *k* starts from what the same arm built in units 1..*k−1*, so a bad unit costs the arm again later. That path dependence is part of what a harness costs and is reported per unit, not corrected away.
For H2, the per-unit decomposition of §2.2 is reported as a table and the share is tested against 0.5 with the same paired test.
""",
),
(
"""- **Goals, families, reference envelope, synthetic library, self-review** (`CONTEXT.md` before 2026-09-14) — not part of this design.""",
"""- **Goals, families, reference envelope, synthetic library, self-review** (`CONTEXT.md` before 2026-09-14) — not part of this design.
- **Reference states and isolated tickets** (this document earlier on 2026-09-14) — replaced by one construction per arm from the frozen specification; the nine tickets survive as the nine units of that specification.""",
),
]


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    for old, new in R:
        if text.count(old) != 1:
            raise SystemExit(f"expected 1 match, found {text.count(old)}:\n{old[:100]}")
        text = text.replace(old, new)
    PATH.write_text(text, encoding="utf-8")
    print(f"{PATH}: {len(R)} replacements")


if __name__ == "__main__":
    main()
