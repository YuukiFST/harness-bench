# 41 — Layer 1: the request-shape instrument

Ticket [#41](https://github.com/YuukiFST/harness-bench/issues/41), specified by [#37](https://github.com/YuukiFST/harness-bench/issues/37).
Code in [`layer1/`](../../layer1), operating instructions in [`layer1/README.md`](../../layer1/README.md).

Layer 1 measures what each harness sends **before the model has done anything**, against a mock endpoint that never forwards a request upstream.
It costs zero free-tier quota, needs no Docker, no gateway and no proxy on 443, and it is the result no outage can take away.

## What is measured

Every inbound `POST /v1/chat/completions` body is decomposed into four buckets that **partition the raw bytes exactly**:

| Bucket | Definition |
|---|---|
| `system_bytes` | the spans of the messages whose role is `system` or `developer` |
| `conversation_bytes` | the spans of every other message |
| `tools_bytes` | the span of the `tools` array |
| `envelope_bytes` | everything else — the enclosing punctuation, `model`, `stream`, `stream_options`, `max_tokens` |

`system + conversation + tools + envelope == total`, and the identity is asserted in the test suite.
The buckets are taken as **byte spans of the body as received**, not as re-serialised JSON: `json.dumps` of a parsed body differs from the original in whitespace, key order and escaping, which would silently move bytes between buckets and make two arms incomparable.
Spanning is done by a small recursive-descent scanner (`layer1/src/hb_layer1/json_spans.py`) because no stdlib JSON parser exposes offsets.

Alongside the bytes, each record carries the tool-schema count, the tool names as offered, and a token count.

### The token count is a disclosed proxy

The gateway's own tokenizer is not published for `mimo-v2.5-free` or `hy3-free`, and #34 established that its `prompt_tokens` carries a gateway-injected offset for content that was never sent.
Layer 1 therefore tokenises with `cl100k_base` and records the encoding name in **every** record.
The rule that follows: Layer 1 token counts are compared **between arms only**, and never against a `prompt_tokens` value returned by the real gateway.

### Two environment profiles

- **`isolated`** — a fresh `HOME` and fresh XDG directories. The cross-arm table is built from this profile.
- **`ambient`** — the machine's real `HOME`. This is where #26 found pi injecting `$HOME/.agents/skills` into its system prompt.

The ambient-state delta is `ambient − isolated` on the first request.

Both profiles keep the arm's agent directory inside the run sandbox, so the mock provider can be registered without writing into the dev's real `~/.pi`.
The discovery-disabling flags the research docs recommend for a benchmark run — `--no-skills`, `--no-extensions`, `--no-context-files`, `--no-rules`, and OpenCode's `--pure` in the ambient profile — are deliberately **not** passed, because they erase the exact effect this profile exists to measure.

### Per-step growth

The mock answers from a fixed script: four tool calls, then a final text answer, so five agent-loop requests per run.
The tool call is built from the schema the arm itself sent, filling required properties from one shared argument table; an unknown required property raises rather than being guessed, because a wrong argument produces a tool error, and a tool error changes the next step's conversation bytes.

## Four decisions the instrument turns on

**The workspace path is part of the measurement.**
Arms put the working directory into their system prompt, so the staged workspace has one fixed path, rebuilt per run.
This was not theoretical: the first pass reported a phantom **−1 byte** ambient delta for pi purely because `ambient` is one character shorter than `isolated`, and the second reported a phantom **4-token** delta because a per-run hex digest tokenised differently between runs.
Both vanished once the path was held byte-identical.

**And so are the workspace's ancestor directories.**
OpenCode walks up from the working directory to the enclosing git root and injects the context files it finds there.
While the workspace was staged under `layer1/data/ws/`, OpenCode was reading **harness-bench's own `CONTEXT.md`** into every request: 14,656 system-prompt bytes instead of 9,738, a **4,918-byte** inflation in which the instrument was measuring its own repository.
The default workspace root is therefore outside any repository and outside `$HOME` (`C:\hb`, `/tmp/hb`), which is also what keeps the machine's username out of the published captures (#22).
The same reasoning applies to the arms themselves: pi writes its own npm package directory into its system prompt, so the arms are installed under a neutral root (`HB_ARMS_DIR`) rather than taken from a global install under the dev's home, and a local install wins over `PATH`.

**A tool-less request is auxiliary, not step 0.**
OpenCode opens every session with a title-generation call that carries no tool schemas.
It is recorded and reported — it is a real cost of that harness design, and #4 warned that the arms' own reporting omits exactly this class of call — but it does not advance the script, or one arm's titling prompt would be compared against another arm's system prompt.

**A run the instrument cannot make is left as a failed run, never as a number.**
Two of the six runs below produced no request at all, for reasons in the machine's ambient state.
They are reported as failures with their exit code and stderr, and no delta is imputed for them.

## What is pinned

| Artifact | Pin |
|---|---|
| `pi` | `0.80.10` (npm `@earendil-works/pi-coding-agent`) |
| `omp` | `17.2.10` (npm `@oh-my-pi/pi-coding-agent`) |
| `opencode` | `1.17.9` (npm `opencode-ai`) |
| arms install root | `C:\hbarms`, via `HB_ARMS_DIR`; never a global install under `~` |
| workspace root | `C:\hb`, outside every git repository |
| tokenizer | `cl100k_base` |
| task | `layer1/tasks/probe`, one 83-byte prompt, byte-identical across arms |
| machine | Windows 11, the authoring box |

Measured 2026-08-28. Raw dataset: `layer1/data/records.jsonl` with the raw bodies under `layer1/data/bodies/`.

## Results

### First request, isolated

| arm | tool schemas | tools bytes | system bytes | conversation bytes | envelope | total bytes | prompt tokens |
|---|---|---|---|---|---|---|---|
| omp 17.2.10 | 11 | 39,273 | 25,395 | 135 | 142 | **64,945** | 16,714 |
| opencode 1.17.9 | 9 | 20,007 | 9,738 | 114 | 138 | **29,997** | 6,659 |
| pi 0.80.10 | 4 | 2,900 | 2,499 | 135 | 142 | **5,676** | 1,228 |

### pi vs oh-my-pi — #27's finding, independently reproduced

| metric | pi | omp | ratio |
|---|---|---|---|
| total request bytes | 5,676 | 64,945 | **11.4x** |
| tool-schema bytes | 2,900 | 39,273 | 13.5x |
| system-prompt bytes | 2,499 | 25,395 | 10.2x |
| tool schemas | 4 | 11 | 2.75x |
| prompt tokens | 1,228 | 16,714 | 13.6x |

#27 measured 10.8x total bytes, 13.4x tool-schema bytes and 4 vs 11 tool schemas with a throwaway mock, a different prompt and different measurement code.
This instrument gets 11.4x, 13.5x and 4 vs 11.
The tool-schema count is **identical**, and pi's tool-schema payload is **2,900 bytes in both** — the same figure doc 10 reproduced independently, now on a third measurement.
The total-bytes ratio moves with the prompt (a shorter prompt is a smaller shared addend, which raises the ratio), which is why the ratio is only ever reported alongside the task it was measured on.

The flagship claim of #9 therefore stands on an instrument in the repo rather than on an afternoon's scratch work: with harness lineage held fixed — a hard fork against its upstream — the fork sends **11x** the bytes of its parent on the first request of the same task.

### Ambient-state delta

| arm | isolated | ambient | delta | ratio |
|---|---|---|---|---|
| pi | 5,676 | 5,676 | **0** | 1.000 |
| omp | 64,945 | — | not measurable on this machine | — |
| opencode | 29,997 | — | not measurable on this machine | — |

pi's delta is **exactly zero bytes and zero tokens on this machine**, and that does not contradict #26.
#26 measured a 2.48x inflation caused by `$HOME/.agents/skills`; that directory does not exist on this box today, so there is no ambient state for pi to inject.
The measurement is that *this machine's* ambient state costs pi nothing right now — the delta is a property of the machine as much as of the harness, and the number must be re-measured on the NixOS experiment box, where the arms' real configuration lives.

The other two arms could not be measured in the ambient profile, and the reasons are findings rather than defects of the instrument:

- **omp** aborts before issuing any request: `Unknown command: json`, then `ExtensionExitError: Module called process.exit(1) during guarded extension/hook loading`, raised by an extension discovered in the real `HOME`. Ambient state does not merely inflate this arm's request, it prevents the run.
- **opencode** exits 1 with a SQLite migration failure against the real `~/.local/share/opencode/opencode.db`. Verified to be independent of this instrument: a plain `opencode run` with no Layer 1 configuration fails the same way on this machine. It is the first evidence for the open hypothesis in #23, that OpenCode's ambient SQLite state is a preventable failure mechanism; the source that first claimed it left the project in #50, so the claim now rests on this run and is confirmed on the rig.

### Per-step growth (isolated)

| arm | step 0 | step 1 | step 2 | step 3 | step 4 | steady per-step |
|---|---|---|---|---|---|---|
| omp | 64,945 | 65,273 | 65,898 | 66,523 | 67,148 | +625 |
| opencode | 29,997 | 30,695 | 31,393 | 32,091 | 32,789 | +698 |
| pi | 5,676 | 6,231 | 6,786 | 7,341 | 7,896 | +555 |

All three arms resend the full history and growth is linear, with a constant increment per step after the first.

**Two arms resend it intact; one does not.** At step 4, pi carries four tool results of 303 characters each and opencode three of 435, all whole. omp has replaced its *oldest* tool result with a 54-character reference stub — `[shaken ~84 tokens — recover: artifact://0 (region 1)]` — and renamed the duplicate `tool_call_id`s to `call_layer1_dup1..3`. So omp compacts, and it does so at the first opportunity rather than under context pressure. That is what its first increment of +328 against a steady +625 is: the stub replacing the first result, not a different framing of it.

**The trigger is not characterised, and the probe is a plausible cause.** The script sends four byte-identical `read` calls carrying the same `tool_call_id` (#55), which is not what a real provider emits. Whether omp shakes because the content repeats, because the ids collide, or on a rule of its own cannot be told from this run. Reported as observed, not as a mechanism.

The steady increment is the arm's own framing of one tool call plus one tool result, and it differs by 26% between the cheapest and the most expensive arm — small next to the 11x standing difference in the first request. Part of that spread is the instrument's own: the mock fills each arm's required schema fields, and omp's `read` requires one more than pi's, so roughly 29 bytes per step of the gap is server-injected rather than the arm's (#55).
The consequence for Layer 2 is that at this horizon the arms' *relative* cost is set almost entirely by what they send before the loop starts.

### Auxiliary model calls

| arm | calls per run | bytes |
|---|---|---|
| opencode | 1 | 2,526 |
| pi | 0 | — |
| omp | 0 | — |

OpenCode spends one extra model call, of 2,526 bytes, generating a session title before the task begins.
On a paid tier that call is billed; in the arm's own reporting it does not appear.
This is #4's argument for measuring at the proxy rather than trusting native totals, observed directly.

## Limitations

- **One task, one machine.** The `probe` task exists so the instrument has something to run today; the DeepSWE workspaces of #36 are not staged yet, and every ratio above is specific to this prompt.
- **The fourth arm does not exist yet.** Harness zero, the in-house ReAct control, is scoped in #12 and built in #17. Until then the table has three arms, not four.
- **The token count is a proxy** (`cl100k_base`), comparable between arms and never against the gateway.
- **The ambient profile is a property of the machine.** All three ambient results above must be re-measured on the NixOS experiment box before they enter the document.
- **OpenCode's number is a property of where the task sits.** It is measured with the workspace outside any repository. A DeepSWE task workspace *is* a git checkout, so #36 has to decide what context files that checkout carries before Layer 2 numbers are comparable to these.
- **Layer 1 says nothing about task success.** A harness sending 11x the bytes is not thereby 11x worse; #26 recorded a null H2 as an explicitly reportable finding, and the two layers are never combined into one number (#37).

## Reproducing

```bash
cd layer1
uv venv && uv pip install -e . --group dev
export HB_ARMS_DIR=C:/hbarms
npm i --prefix "$HB_ARMS_DIR" @earendil-works/pi-coding-agent@0.80.10 \
                              @oh-my-pi/pi-coding-agent@17.2.10 \
                              opencode-ai@1.17.9
uv run pytest          # 37 tests, no network, no arms required
hb-collect && hb-report
```

Two consecutive `pi` runs produced a byte-identical first request — same 5,676 bytes, same `sha256 2d3920264e84d2c4…` — which is the empirical form of #37's "n = 1 suffices".
