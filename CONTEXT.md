# Context — harness-bench

Glossary for this experiment.
Terms only: no implementation detail, no specification, no decisions.
The decisions live in the tickets of [the map](https://github.com/YuukiFST/harness-bench/issues/1); the specifications live in `docs/spec/`; the product's decisions live in the tickets of [Finn](https://github.com/YuukiFST/Finn/issues/1).

## Arm

One harness under test, driven headlessly against a fixed model.
There are exactly two: **OpenCode** and **Pi** (written "Pi" in prose, as in its own title; `pi` only as the CLI command).
An arm must be pointable at an arbitrary OpenAI-compatible base URL without a wrapper hack, or it cannot traverse the measuring proxy and cannot be measured.
This project authors no arm.

## Tier

One model configuration every arm is measured against, reported on its own and never averaged with another tier.
There are two: a **primary tier** and a **robustness tier**, the second existing because a harness effect is model-specific and can invert in sign.

## Product

The one piece of software both arms build: Finn, a multi-tenant voice-driven finance SaaS.
It was decided before the experiment, in closed tickets, and those decisions do not change during it.

## Reference build

The Finn the author builds first, outside both arms, until it is the product the author wants, with the end of each stage tagged in git.
It is where the specification and the acceptance tests come from, and the acceptance tests of each unit must pass on it at that unit's tag before anything is frozen.
Its code never enters an arm's workspace.

## Specification

The one document set both arms build from, extracted from the reference build before any run and frozen by hash: a text with the product, its stack, its locks and the interface the acceptance tests touch, and a feature list in JSON where every feature names its unit.
Both arms receive the same bytes; the acceptance tests and the reference code are not in it.
It exists so that the input is identical and the difference in tokens can be attributed to the harness rather than to what each arm was told.

## Unit

One part of the specification handed to an arm as one prompt, byte-identical for both arms: the features of one stage of the reference build, in the order the author built them.
There are as many units as stages, and at least six, the fewest at which a two-sided Wilcoxon signed-rank test can reach p < 0.05.
A unit is what the previous design called a ticket (one of nine Finn tickets), and the design before that a task.

## Initial workspace

The directory a construction starts from: the specification and the pinned toolchain files, nothing else, frozen by hash.
From then on the workspace is the arm's own: what it built for one unit is what the next unit starts from, and nothing the author wrote enters it.

## Acceptance test

A test the author writes for a unit before any run, kept outside the workspace, that decides the unit's score on a copy of the workspace after the arm exits.
It is the oracle of this design.
It is never the agent's own test suite — a model that hallucinates an API also writes tests that mock the hallucination, so a green suite can sit over code that crashes.

## Construction

One execution of one arm, at one tier, that builds the whole product from the initial workspace, unit by unit, one fresh arm process per unit.
It is the run of this design and produces one result record per unit and one for the whole.

## Cell

One (arm, tier) pair.
A cell holds *n* constructions, because the tiers do not honour a fixed seed and a single construction per cell measures noise.

## Step

One LLM round trip, counted at the measuring proxy.
Counted at the proxy rather than reported by the arm, because every arm omits a different set of real calls from its own reporting.

## Fixed load

The bytes an arm sends in every request regardless of the conversation: its system prompt and its tool schemas.
Measured in Layer 1 against a mock endpoint; multiplied by the step count it is the part of a run's tokens that the harness design, not the task, decides.

## Concluded unit

A unit in which every acceptance test of that unit passes when the arm exits it.
A construction is concluded when every test of every unit passes at the end.
Tokens per construction, always reported next to the acceptance fraction, is the primary metric; tokens per unit is the paired one.

## Unconcluded unit

A unit whose agent did not conclude it.
It is an outcome, it is data, it enters the statistics with the fraction of acceptance tests it passed, and the construction goes on to the next unit from that workspace.

## Discarded construction

A construction in which any unit's *measurement* is untrustworthy, per the faults enumerated in `docs/spec/25-measuring-proxy.md`.
It is never repaired into a valid sample and never silently dropped: the dataset records that it happened.
The distinction from an unconcluded unit is load-bearing — one is a result, the other is the absence of one.

## Tampered unit

A unit in which the agent modified something it was shipped and told not to touch, the specification included.
It is agent behaviour rather than a measurement fault, so unlike a discarded construction it stays in the dataset and is reported.

## Pilot unit

One of the first units, run before the matrix to fix the numbers the protocol leaves open: the wall-clock limit per unit, the free-tier quota per unit, and the construction-to-construction variance.
