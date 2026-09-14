# Layer 1 — the request-shape instrument

Measures what each harness sends **before the model has done anything**: total
request bytes split into system prompt / tool schemas / conversation, the number
of tool schemas offered, a token count, the delta the machine's ambient state
adds, and how the request grows over the first five steps.

It spends **zero free-tier quota**, needs no Docker, no gateway and no proxy on
443, and runs on the Windows authoring box as well as on NixOS. Decided in
[#37](https://github.com/YuukiFST/harness-bench/issues/37), built in
[#41](https://github.com/YuukiFST/harness-bench/issues/41).

## Install

```bash
cd layer1
uv venv && uv pip install -e . --group dev
export HB_ARMS_DIR=C:/hbarms
npm i --prefix "$HB_ARMS_DIR" @earendil-works/pi-coding-agent@0.80.10 \
                              opencode-ai@1.17.9
```

The arms are resolved from `$HB_ARMS_DIR/node_modules/.bin` first and from
`PATH` only as a fallback, because an install under the dev's home ends up in
the measurement (see below). `HB_ARMS_DIR` defaults to `layer1/.arms`, which is
fine for `opencode` but not for `pi`. The first run fetches the
`cl100k_base` BPE file once and caches it.

## Run

```bash
hb-collect                    # every arm, both profiles, task `probe`
hb-collect --arm pi --profile isolated
hb-report                     # renders data/report.md and the CSVs
```

Two collections must not run at the same time: the staged workspace has one
fixed path, on purpose (see below).

## What it produces

| Path | Contents |
|---|---|
| `data/records.jsonl` | one record per request: the decomposition, the tokenizer, the sha256 of the body |
| `data/bodies/<run>/request-NN.json` | the raw bytes each record was derived from |
| `data/runs.jsonl` | one manifest per run: status, exit code, command, wall time |
| `data/report.md`, `data/*.csv` | the tables, rendered from the records with no manual step |

`data/runs/` (stdout, stderr, sandboxes) holds working files and is not
committed. The staged workspaces live under `--ws-root`, outside the repo
entirely.

## The two profiles

- **isolated** — fresh `HOME` and fresh XDG dirs. The cross-arm table is built
  from this profile.
- **ambient** — the machine's real `HOME`. The difference between the two *is*
  the ambient-state measurement.

Both keep the arm's agent directory inside the run sandbox, so the dev's real
`~/.pi` is never written to.

The flags that disable discovery (`--no-skills`, `--no-extensions`,
`--no-context-files`, `--no-rules`) are deliberately not passed: they would erase
the effect the ambient profile exists to measure.

## Four things the design turns on

**The path is part of the measurement.** Arms put the working directory into
their system prompt, so the staged workspace has one fixed path, rebuilt per run.
An earlier pass reported a phantom one-byte ambient delta purely because
`ambient` is one character shorter than `isolated`, and a later one reported a
phantom four-token delta because a per-run hex digest tokenised differently.

**So are the directories above it, and the arms' own install path.** OpenCode
walks up to the enclosing git root and injects the context files it finds; while
the workspace sat under `layer1/data/ws/`, OpenCode was reading harness-bench's
own `CONTEXT.md` into every request, 4,918 bytes of the instrument measuring
itself. `--ws-root` therefore defaults outside any repository and outside `$HOME`
(`C:\hb`, `/tmp/hb`). pi does the same thing with its own npm package directory,
which is why `HB_ARMS_DIR` exists and why a local install beats `PATH`.

**A tool-less request is auxiliary, not step 0.** OpenCode opens every session
with a title-generation call carrying no tool schemas. It is recorded — it is a
real cost of that design, and #4 warned the arms' own reporting omits exactly
this class of call — but it does not advance the script, or one arm's titling
prompt would be compared against another arm's system prompt.

**Arguments are filled from the arm's own schema.** The arms disagree on argument
names (`path`, and OMP additionally requires `i`, "concise intent"). An unknown
required argument raises rather than being guessed: a wrong argument produces a
tool error, which changes the next step's conversation bytes.

## n = 1

Two consecutive `pi` runs produced a byte-identical first request
(`sha256 2d3920264e84d2c4…`, 5,676 bytes both times). The mock is deterministic,
so a repetition adds nothing; any variation that *does* appear is a finding about
that harness, not noise to average away.
