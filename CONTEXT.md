# Context — harness-bench

Glossary for this experiment.
Terms only: no implementation detail, no specification, no decisions.
The decisions live in the tickets of [the map](https://github.com/YuukiFST/harness-bench/issues/1); the specifications live in `docs/spec/`.

## Arm

One harness under test, driven headlessly against a fixed model.
An arm must be pointable at an arbitrary OpenAI-compatible base URL without a wrapper hack, or it cannot traverse the measuring proxy and cannot be measured.

## Harness zero

The in-house minimal ReAct loop that serves as the scientific control.
It is an arm, and it is the only arm this project authors.

## Tier

One model configuration every arm is measured against, reported on its own and never averaged with another tier.
There are two: a **primary tier** and a **robustness tier**, the second existing because a harness effect is model-specific and can invert in sign.

## Run

One execution of one arm, on one task, at one tier.
A run produces one result record.

## Cell

One (arm, task, tier) triple.
A cell holds *n* runs, because the tiers do not honour a fixed seed and a single run per cell measures noise.

## Step

One LLM round trip, counted at the measuring proxy.
Counted at the proxy rather than reported by the arm, because every arm omits a different set of real calls from its own reporting.

## Failed run

A run whose agent did not accomplish the task.
This is an outcome, it is data, and it is reported.

## Discarded run

A run whose *measurement* is untrustworthy, per the faults enumerated in `docs/spec/25-measuring-proxy.md`.
It is never repaired into a valid sample and never silently dropped: the dataset records that it happened.
The distinction from a failed run is load-bearing — one is a result, the other is the absence of one.

## Tampered run

A run in which the agent modified something it was shipped and told not to touch.
It is agent behaviour rather than a measurement fault, so unlike a discarded run it stays in the dataset and is reported.

## Task

One unit of work handed to an arm, in its own workspace, independent of every other task.

## Task manifest

The machine-readable declaration of what a task is: its goals, the mechanism checking each one, what ships with it, and what is withheld.
It is the contract between the design of a task and the runner that executes it.

## Reference envelope

The step count and wall clock a task was designed to fit, measured on harness zero.
It exists so that a run cut short by an enforced timeout is distinguishable from a run that genuinely failed — without it the two are the same row in the dataset.

## Goal

One independently checkable requirement of a task, stated in the task's own prompt and numbered.
Goals exist so that a task the agent does not finish still yields a distribution rather than a zero, which is what lets the suite discriminate between arms at both ends of the difficulty range.

## Family

A group of tasks sharing a shape and a difficulty axis.
A family is the unit of retirement: a family that stops discriminating after calibration is dropped whole, rather than task by task.

## Oracle

What decides whether a goal was met.
It is authored by this project, executed by the runner, and is never the agent's own test suite — a model that hallucinates an API also writes tests that mock the hallucination, so a green suite can sit over code that crashes.

## Visible test

A test shipped inside the workspace, which the agent may read and run.
It exists so that a harness which runs tests and iterates is credited for doing so, and it is never what decides a goal.

## Held-out test

A test the oracle owns, which never enters the workspace.
The agent cannot read it, run it, or write against it, and it is one of the mechanisms by which a goal is decided.

## Synthetic library

A library written by this project for the tasks to be grounded in.
Its purpose is that the fact the agent needs is present in the workspace and absent from the model's weights, so that what varies between arms is whether the harness lets the agent go and read it.

## Self-review

The agent's own verdict on each goal, emitted as a machine-readable artifact and scored against the oracle's verdict.
It measures whether a harness gives its agent the means to know whether it succeeded, and is kept separate from the task score rather than folded into it.
