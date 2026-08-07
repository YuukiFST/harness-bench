# 10 — PI: measurement and configuration surface

Research ticket #10.
Question: what is pi's measurement and configuration surface, and can it be wired as an arm against an arbitrary OpenAI-compatible gateway?

pi is the largest gap in the project.
Doc 06 established OpenCode and Cline against pinned commits; doc 07 established oh-my-pi by installing and running it, and used pi only as a comparison baseline.
This document does for pi what doc 07 did for OMP: install, configure, run, capture the wire, and read the source for everything the wire cannot show.

Retrieved 2026-08-07.

## What was pinned, and how the evidence was gathered

| Artifact | Pin |
|---|---|
| `@earendil-works/pi-coding-agent` | `0.80.10`, installed at `C:\Users\tisao\AppData\Local\pi-node\current\node_modules\@earendil-works\pi-coding-agent\`, executed locally |
| Node runtime | `v22.23.1` (`node.exe --version`), bundled alongside the shim |
| npm registry metadata | fetched 2026-08-07 |

All `file:line` references are to the installed `dist/` tree of that version unless another package is named.
pi ships no source map-free obfuscation — `dist/` is readable TypeScript output, and `docs/` ships inside the npm tarball, so both are primary sources.

pi was **exercised, not just read**.
A mock OpenAI-compatible server was run on `127.0.0.1:11435` — the benchmark's actual proxy port — which answers `GET /v1/models`, streams a chat completion, logs every inbound request (headers plus full body) to JSONL, and deliberately reproduces the three OpenCode Zen quirks that matter:

1. an unknown `reasoning_content` field inside `choices[].delta`;
2. `usage` attached to a chunk that **still carries `finish_reason`**;
3. a `data: {"choices":[],"cost":"0"}` frame arriving **after** `data: [DONE]`.

A second mock on `127.0.0.1:11436` returns two rounds of `tool_calls` before a final text answer, so the agent loop could be counted rather than inferred.
A third configuration points at a dead port, `127.0.0.1:11499`, for the failure path.

No request was sent to `https://opencode.ai/zen/v1` or any other third-party endpoint.

The authoring machine is Windows 11; the experiment machine is NixOS.
Process-level behaviour transfers; the Windows-specific half of the isolation finding in §7 does not, and is called out where it applies.

---

## 1. Canonical identity

| Field | Value | Source |
|---|---|---|
| Package | `@earendil-works/pi-coding-agent` | `package.json:2` |
| Binary | `pi` | `package.json:9-11` — `"bin": { "pi": "dist/cli.js" }` |
| Installed version | **0.80.10** | `node dist/cli.js --version` → `0.80.10` |
| npm `latest` | **0.84.1**, published 2026-08-07T06:01:32Z | `registry.npmjs.org/@earendil-works/pi-coding-agent`, `dist-tags.latest` |
| 0.80.10 published | 2026-07-16T22:05:04Z | same, `time["0.80.10"]` |
| Total published versions | 40 | same |
| Repository | `git+https://github.com/earendil-works/pi.git` | `package.json`, confirmed by the registry |
| Runtime | Node **≥ 22.19.0** | `package.json` — `"engines": {"node": ">=22.19.0"}` |
| Licence | **MIT** | `package.json` `"license": "MIT"`, `"author": "Mario Zechner"`; confirmed by the registry |
| nixpkgs | `pi-coding-agent` 0.84.0 | given in the ticket; corroborated by doc 07 §7, not re-derived here |

Note the upstream repo moved: doc 07 quoted OMP's porting guide referring to `badlogic/pi-mono`, and `docs/json.md` still links to `github.com/earendil-works/pi-mono` for type definitions, but `package.json` points at `earendil-works/pi`.

The local install is a Node shim, not a compiled binary.
`C:\Users\tisao\AppData\Local\pi-node\current\pi:12-16` execs a bundled `node.exe` against `dist/cli.js`:

```sh
if [ -x "$basedir/node" ]; then
  exec "$basedir/node"  "$basedir/node_modules/@earendil-works/pi-coding-agent/dist/cli.js" "$@"
```

This matters for the NixOS gate: pi's install is plain JS on a Node runtime, with no Bun requirement and no eagerly-loaded native `.node` addons on the startup path — the three obstacles doc 07 recorded for OMP do not apply.
The runtime is the one hard constraint, and nixpkgs already carries a derivation.

**The local install is four minor versions behind and 0.84.x is moving daily.**
Pin the version and record it; `0.80.10` is what this document establishes, and every number below is for that version.

---

## 2. Custom base URL — VERIFIED WORKING

**pi can be pointed at an arbitrary OpenAI-compatible endpoint, and it was.**

### Config file and schema

The mechanism is a JSON file, `<agentDir>/models.json`, default `~/.pi/agent/models.json`.
`docs/models.md:3`: "Add custom providers and models (Ollama, vLLM, LM Studio, proxies) via `~/.pi/agent/models.json`."

The path is computed in `dist/config.js:423-426`:

```javascript
/** Get path to models.json */
export function getModelsPath() {
    return join(getAgentDir(), "models.json");
}
```

and `getAgentDir()` at `dist/config.js:391-397` is env-redirectable:

```javascript
export function getAgentDir() {
    const envDir = process.env[ENV_AGENT_DIR];
    if (envDir) {
        return expandTildePath(envDir);
    }
    return join(homedir(), CONFIG_DIR_NAME, "agent");
}
```

with `ENV_AGENT_DIR` derived at `dist/config.js:396` as `` `${APP_NAME.toUpperCase()}_CODING_AGENT_DIR` `` → **`PI_CODING_AGENT_DIR`**.
`CONFIG_DIR_NAME` comes from the package's own `piConfig.configDir`, `.pi` (`dist/config.js:394`, `package.json:6-8`).

Provider fields, from `docs/models.md:136-145`: `baseUrl` (API endpoint URL), `api`, `apiKey`, `oauth`, `headers`, `authHeader`, `compat`, `models`.
`docs/models.md:145`: "For providers with `models`, non-built-in provider configs need `baseUrl` and `api`."

The exact config verified end to end:

```json
{
  "providers": {
    "mockollama": {
      "baseUrl": "http://127.0.0.1:11435/v1",
      "api": "openai-completions",
      "apiKey": "mock",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [
        {
          "id": "MOCK-2.6B",
          "name": "Mock 2.6B",
          "reasoning": false,
          "input": ["text"],
          "contextWindow": 32768,
          "maxTokens": 4096,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
        }
      ]
    }
  }
}
```

Registration confirmed:

```
$ PI_CODING_AGENT_DIR=<tmp>/agentdir pi --list-models
provider    model      context  max-out  thinking  images
mockollama  MOCK-2.6B  32.8K    4.1K     no        no
```

Note that the isolated agent directory **replaced** the machine's real provider list entirely — only the mock appears.
And the traffic actually arrived at `127.0.0.1:11435`, which is the whole question: the mock's request log recorded a single `POST /v1/chat/completions` with a well-formed OpenAI Chat Completions body.

The `compat` block is not optional for a strict gateway.
`docs/models.md:39` states it directly: "Some OpenAI-compatible servers do not understand the `developer` role used for reasoning-capable models. For those providers, set `compat.supportsDeveloperRole` to `false` so pi sends the system prompt as a `system` message instead."
With `supportsDeveloperRole: false` the captured request used `role: "system"`, confirmed on the wire.

### An API key is required

**This is a real difference from OMP and it will bite anyone porting the doc-07 config.**
OMP has `auth: none`; pi has no such option.
`docs/models.md:37`: "The `apiKey` value is a placeholder because Ollama ignores it. pi still treats models as requiring auth before they appear in `/model`, so keyless local servers should keep a dummy value, save a key for that provider with `/login`, or pass `--api-key` when selecting the model."

Verified by removing `apiKey` from an otherwise identical provider block:

```
$ pi --list-models
No models available. Use /login to log into a provider via OAuth or API key.

$ pi --mode json --model mockollama/MOCK-2.6B "Say hi"
Use /login to log into a provider via OAuth or API key.
exit 1
```

The mock's request log was **empty** — the model is invisible, and no HTTP request is issued at all.
Both `apiKey` in `models.json` and the `--api-key` flag work; with `--api-key dummy` against the keyless config the run completed normally and the mock recorded `authorization: Bearer dummy`.

`apiKey` also supports indirection (`docs/models.md:149-169`): `$VAR` / `${A}_${B}` environment interpolation, `!command` shell execution, `$$`/`$!` literal escapes.
For a benchmark, a literal dummy string is the least surprising choice.

### No `/v1/models` probe

Across every run in this session — six successful chat runs plus the tool-loop and dead-endpoint runs — the mock logged **only** `POST /v1/chat/completions`.
pi never issued `GET /v1/models`.
This is a difference from OMP, which doc 07 §4 observed probing `/v1/models` once per session; the proxy still needs no `/v1/models` handler for pi.

### Environment-variable shortcuts exist but should not be used

`pi --help` lists a per-vendor API-key variable for roughly 30 providers, including `OPENCODE_API_KEY - OpenCode Zen/OpenCode Go API key`, and a base-URL variable only for Azure (`AZURE_OPENAI_BASE_URL`).
There is **no** generic `OPENAI_BASE_URL` override.
pi does have a built-in `opencode` provider, so pointing the arm straight at Zen without the proxy is possible — but that defeats the measurement instrument and is not what this arm is for.
Use the explicit custom provider: it pins the context window and the model list, and it keeps the proxy URL out of a variable another arm might also read.

---

## 3. Headless invocation

Working command, verified end to end against the mock:

```bash
cd /path/to/workspace
HOME=/run/bench/home \
PI_CODING_AGENT_DIR=/run/bench/pi \
PI_OFFLINE=1 \
pi --mode json \
   --no-session --no-extensions --no-skills --no-context-files \
   --model mockollama/MOCK-2.6B \
   "your task prompt here" < /dev/null
```

`--mode <mode>` accepts `text` (default), `json`, or `rpc` (`pi --help`).
`--print` / `-p` is the text-mode non-interactive switch; `--mode json` implies non-interactive.
pi has **no `--cwd` flag** — the runner must `chdir` — and **no `--max-time`**, which OMP has; an external `timeout --kill-after` is mandatory rather than merely warranted.

Flags that matter for a boxed-in run, all from `pi --help` (help text at `dist/cli/args.js:250-378`):

| Flag | Effect |
|---|---|
| `--no-session` | ephemeral, writes no transcript |
| `--no-extensions`, `-ne` | disable extension discovery |
| `--no-skills`, `-ns` | disable skills discovery and loading |
| `--no-context-files`, `-nc` | disable `AGENTS.md` and `CLAUDE.md` discovery |
| `--no-prompt-templates`, `-np` | disable prompt templates |
| `--no-themes` | disable theme discovery |
| `--tools`, `-t <list>` | allowlist of tool names |
| `--exclude-tools`, `-xt <list>` | denylist |
| `--no-builtin-tools`, `-nbt` / `--no-tools`, `-nt` | drop built-ins / all tools |
| `--offline` | "Disable startup network operations (same as `PI_OFFLINE=1`)" |
| `--api-key <key>` | supply the credential inline |
| `--session-dir <dir>` | transcript location, overrides `PI_CODING_AGENT_SESSION_DIR` |

**There is no max-turns or max-iterations cap of any kind** — see §6.

One caution the help text does not make obvious: pi's own `--help` on this machine printed extension-contributed flags (`--fff-mode`, `--cursor-fast`, `--cursor-no-fast`) sourced from packages listed in the ambient `~/.pi/agent/settings.json`.
Ambient state reaches pi before argument parsing finishes; §7 is not optional reading.

### `--mode json` output

JSONL, one object per line.
The schema is documented in `docs/json.md` and matches what was captured.
Verified event sequence for a one-turn, no-tool success:

```
session, agent_start, turn_start,
message_start, message_end,                       ← the user message
message_start, message_update ×4, message_end,    ← the assistant message
turn_end, agent_end, agent_settled
```

Observed record types and their top-level keys, from the captured stream:

| `type` | Keys |
|---|---|
| `session` | `type, version, id, timestamp, cwd` |
| `agent_start` | `type` |
| `turn_start` | `type` |
| `message_start` | `type, message` |
| `message_update` | `type, assistantMessageEvent, message` |
| `message_end` | `type, message` |
| `turn_end` | `type, message, toolResults` |
| `tool_execution_start` | `type, toolCallId, toolName, args` |
| `tool_execution_end` | `type, toolCallId, toolName, result, isError` |
| `agent_end` | `type, messages, willRetry` |
| `agent_settled` | `type` |
| `auto_retry_start` | `type, attempt, maxAttempts, delayMs, errorMessage` |
| `auto_retry_end` | `type, success, attempt, finalError?` |

The header line, verbatim:

```json
{"type":"session","version":3,"id":"019fdc7f-961a-75e0-9a71-131effde9e4d","timestamp":"2026-08-07T13:52:56.858Z","cwd":"C:\\Users\\tisao\\AppData\\Local\\Temp\\pi-bench\\work"}
```

`docs/json.md:6-22` defines `AgentSessionEvent` as `AgentEvent` plus `queue_update`, `compaction_start`, `compaction_end`, `auto_retry_start`, `auto_retry_end`; `docs/json.md:26-42` defines the `AgentEvent` base.
`compaction_start` / `compaction_end` were not observed — the mock never filled a 32 K context — but they are on the schema and a long task will emit them.

**`agent_end` carries `willRetry`, and a separate `agent_settled` event follows.**
This is the divergence doc 07 §3 recorded from the OMP side, now confirmed from pi's: OMP emits `isTerminal` and no `agent_settled`; pi 0.80.10 emits `willRetry` and does emit `agent_settled`.
A shared classifier must branch on the arm.

### Exit codes — the JSON-mode asymmetry, with a correction

The ticket's premise is confirmed and refined.

| Situation | `--mode text` | `--mode json` |
|---|---|---|
| Success | 0 | 0 |
| Dead endpoint, retries exhausted | **1** | **0** |
| Missing credential (never issued a request) | **1** | **1** |
| Unrecognised flag | 1 | 1 |

Measured:

```
=== TEXT MODE, DEAD ENDPOINT ===
Connection error.
PI_TEXT_DEAD_EXIT=1

=== JSON MODE, DEAD ENDPOINT ===
PI_JSON_DEAD_EXIT=0
```

The `stopReason` check that sets exit 1 is guarded by `if (mode === "text")` in `dist/modes/print-mode.js`, exactly as the ticket states, and exactly as OMP inherited it.

**The correction is worth having: exit 1 in JSON mode is still meaningful — it means pi never started.**
A missing credential exits 1 in *both* modes because it fails before the agent loop, upstream of the mode-guarded check.
So for a runner: `exit != 0` in JSON mode is an unambiguous configuration/startup failure worth aborting the whole matrix on, while `exit 0` means "pi ran" and says nothing about the outcome.
That is a genuinely useful signal doc 07 did not extract for OMP.

Unlike OMP, **pi does not exit 2 on a bad flag** — `--totally-bogus-flag` exited 1, indistinguishable from a task error in text mode.

Classify outcomes from the stream, never the exit code: the discriminator is the last assistant message's `stopReason` (`"stop"`, `"toolUse"`, `"error"`, `"aborted"`), with `agent_end.willRetry` as the companion flag.

The dead-endpoint JSON run terminated on its own after the retry budget — nothing hung.
It emitted three `auto_retry_start` events at 2 s / 4 s / 8 s, an `agent_end` with `willRetry: true` after each of the first three attempts, then a final `agent_end` with `willRetry: false`, `auto_retry_end`, `agent_settled`, and exit 0.

**Note the retry structure carefully: pi emits one `agent_start`/`agent_end` pair per retry attempt, not one per run.**
A naive "count `agent_end` events" run-counter will over-count by the retry factor. Take the last one.
The default is `retry.maxRetries: 3` (`dist/core/settings-manager.js:553-558`, `dist/core/agent-session.js:2095`, `docs/settings.md:139`) against OMP's 10 — the ~3× amplification doc 07 §2d flagged, confirmed from pi's side at 3.

---

## 4. Token and usage reporting

### `stream_options` is set by pi itself, by default

`pi-ai/dist/api/openai-completions.js:462`:

```javascript
if (compat.supportsUsageInStreaming !== false) {
    params.stream_options = { include_usage: true };
}
```

The gate defaults to `true` for every provider (`pi-ai/dist/api/openai-completions.js:1043`, inside `detectCompat()`), and is only overridden by an explicit model-level `compat.supportsUsageInStreaming` (`:1088`).

Confirmed on the wire: the captured body contains `"stream_options":{"include_usage":true}`.
The proxy's rewrite is therefore **idempotent for this arm rather than corrective** — the same useful property doc 07 established for OMP.
Leave `compat.supportsUsageInStreaming` unset in `models.json`.

### Usage is reported per assistant message

There is no per-run aggregate object in the JSON stream.
Usage rides on each assistant `message_end` (and on the `partial` inside every `message_update`), verified against the mock's `prompt_tokens: 1234 / completion_tokens: 7 / total_tokens: 1241`:

```json
{"type":"message_end","message":{"role":"assistant","content":[{"type":"text","text":"Task complete."}],
 "api":"openai-completions","provider":"mockollama","model":"MOCK-2.6B",
 "usage":{"input":1234,"output":7,"cacheRead":0,"cacheWrite":0,"reasoning":0,"totalTokens":1241,
          "cost":{"input":0,"output":0,"cacheRead":0,"cacheWrite":0,"total":0}},
 "stopReason":"stop","timestamp":1786110505623,"responseId":"chatcmpl-mock1"}}
```

Fields: `input`, `output`, `cacheRead`, `cacheWrite`, `reasoning`, `totalTokens`, and a nested `cost` object with the same breakdown plus `total`.
`cost` is computed from the `cost` block in `models.json`, so a benchmark that sets those to zero gets zeros and must derive spend from the proxy.

`agent_end.messages` repeats the full message array, so per-run totals can be summed from the final `agent_end` alone.
The three-request tool loop produced assistant usages of `{input:100,output:5}`, `{input:200,output:5}`, `{input:999,output:3}` — one per request, summing cleanly.

**One correction to doc 07.** Doc 07 §5 wrote that `duration` and `ttft` "per message are a bonus pi's stream also carries."
pi 0.80.10 did **not** emit them.
Every `message_end` captured here had exactly `role, content, api, provider, model, usage, stopReason, timestamp, responseId` — no `duration`, no `ttft`.
Those two fields appear to be an OMP addition; pi gives only a millisecond `timestamp` per message, from which per-step wall time can be differenced but time-to-first-token cannot.

### Persisted totals exclude compaction — see §8

`dist/core/agent-session.js:2471-2494` (`getSessionStats()`) sums usage only over entries with `type === "message"` and `role === "assistant"`.
Anything that is not an assistant message is invisible to pi's own totals.
That is exactly where the side-call tokens go.

---

## 5. On-disk artifacts

pi writes a session transcript by default; `--no-session` suppresses it.

Location resolution, in precedence order: `--session-dir <dir>`, then `PI_CODING_AGENT_SESSION_DIR` (`ENV_SESSION_DIR`, derived at `dist/config.js:397`), then `<agentDir>/sessions/` (`dist/config.js:448-450`).
Under the default agent dir, sessions are bucketed per project — `~/.pi/agent/sessions/--C--Users-tisao-Desktop-my-harness-config--/` on this machine.
With `PI_CODING_AGENT_SESSION_DIR` set, the file lands flat in that directory.

Format: **JSONL, one record per event**, filename `<ISO-timestamp>_<uuid>.jsonl`.
A complete captured transcript for a one-turn run:

```json
{"type":"session","version":3,"id":"019fdc7f-961a-75e0-9a71-131effde9e4d","timestamp":"2026-08-07T13:52:56.858Z","cwd":"..."}
{"type":"model_change","id":"9427ac2a","parentId":null,"timestamp":"2026-08-07T13:52:56.906Z","provider":"mockollama","modelId":"MOCK-2.6B"}
{"type":"thinking_level_change","id":"af86b425","parentId":"9427ac2a","timestamp":"2026-08-07T13:52:56.906Z","thinkingLevel":"off"}
{"type":"message","id":"2a0bbef4","parentId":"af86b425","timestamp":"2026-08-07T13:52:56.922Z","message":{"role":"user",...,"timestamp":1786110776920}}
{"type":"message","id":"c9b68af1","parentId":"2a0bbef4","timestamp":"2026-08-07T13:52:57.105Z","message":{"role":"assistant",...,"usage":{"input":1234,"output":7,"cacheRead":0,"cacheWrite":0,"reasoning":0,"totalTokens":1241,"cost":{...}},"stopReason":"stop","timestamp":1786110777057,"responseId":"chatcmpl-mock1"}}
```

**Records carry both token counts and timestamps**, and there are two clocks: an ISO-8601 `timestamp` on the outer record and a millisecond epoch `timestamp` inside `message`.
Records also carry `id` / `parentId`, forming a tree rather than a flat log — pi supports branching and `/tree` navigation, so a transcript reader must follow the parent chain rather than assume linear order.
`docs/session-format.md` (14.6 KB) documents the format; `docs/sessions.md` the lifecycle.

For a benchmark this is a usable secondary record, redundant with the proxy log but useful for attributing tokens to steps after the fact.
Set `PI_CODING_AGENT_SESSION_DIR` per run so transcripts are trivially collectable, rather than passing `--no-session`.

---

## 6. Step semantics and the missing loop bound

### What counts as one iteration

The loop is `runLoop()` in `pi-agent-core/dist/agent-loop.js:77`.

- One iteration = **one assistant LLM request plus the execution of the tool calls it returned**.
  The request is issued at `agent-loop.js:105` (`streamAssistantResponse(...)`, LLM call at `:194`); tool calls execute at `:116-129`, setting `hasMoreToolCalls = !executedToolBatch.terminate`.
- Inner loop condition, `agent-loop.js:87`: `while (hasMoreToolCalls || pendingMessages.length > 0)` — it continues as long as the model keeps emitting tool calls or steering messages arrive.
- The outer `while (true)` at `:84` restarts the inner loop when `getFollowUpMessages()` returns queued user messages (`:162-167`).

Confirmed empirically against the tool-calling mock, which returns two rounds of `read` tool calls and then a text answer:

```
requests seen by mock: 3
  req 0  5757 bytes  msgs=2  roles=system,user
  req 1  6099 bytes  msgs=4  roles=system,user,assistant,tool
  req 2  6441 bytes  msgs=6  roles=system,user,assistant,tool,assistant,tool
```

and the corresponding stream:

```
agent_start
turn_start  message_start/message_end (assistant, stop=toolUse, usage i=100)  tool_execution_start/end  turn_end
turn_start  message_start/message_end (assistant, stop=toolUse, usage i=200)  tool_execution_start/end  turn_end
turn_start  message_start/message_end (assistant, stop=stop,    usage i=999)                            turn_end
agent_end (willRetry=false)  agent_settled
```

**So `turn_start`/`turn_end` maps one-to-one onto an upstream request, and onto an assistant `message_end` carrying that request's usage.**
`turn_end` is the correct step counter for this arm.
`agent_start`/`agent_end` is the run boundary — but see §3: on the retry path pi emits one pair per attempt, so take the last.

### There is no max-iterations bound

`grep -rniE "maxiterations|maxturns|maxsteps|maxloops|iterationlimit|maxToolRounds"` over `pi-agent-core/dist/`, `pi-coding-agent/dist/` and `docs/` returns **zero matches**.
No such flag exists in `dist/cli/args.js` (parser at `:19-248`, help at `:250-378`).

The only exits are `stopReason === "error" | "aborted"` (`agent-loop.js:107-111`), the model emitting no further tool calls, or the optional `config.shouldStopAfterTurn` hook (`agent-loop.js:150-158`).
**`shouldStopAfterTurn` is never set by pi's own code** — no assignment exists anywhere in `pi-coding-agent/dist/`.

This is the same hole doc 07 found in OMP, but worse: OMP at least has `--max-time`.
pi has neither a turn cap nor a wall-clock deadline.
The loop is bounded only by the model deciding to stop calling tools — which is precisely the assumption a 2.6B-class model breaks.
**An external `timeout --kill-after` and a proxy-side request-count kill switch are load-bearing for this arm, not belt-and-braces.**

`UNVERIFIED:` whether a third-party extension can set `shouldStopAfterTurn` through the extension API to impose a cap.
The type exists (`pi-agent-core/dist/types.d.ts:183`) and `docs/extensions.md` is 112 KB, which was not audited for it.
The built-in tree sets it nowhere.

---

## 7. Isolation — `PI_CODING_AGENT_DIR` is not enough, and this was measured

### The env vars that redirect pi

| Variable | Redirects | Source |
|---|---|---|
| `PI_CODING_AGENT_DIR` | the whole agent directory: `models.json`, `settings.json`, `auth.json`, `sessions/`, `skills/`, `extensions/`, `prompts/`, `themes/`, `bin/`, debug log | `dist/config.js:391-397`, and the getters at `:423-450` |
| `PI_CODING_AGENT_SESSION_DIR` | session storage only (overridden by `--session-dir`) | `dist/config.js:397`, `pi --help` |
| `PI_PACKAGE_DIR` | package directory, "for Nix/Guix store paths" | `dist/config.js`, `pi --help` |
| `PI_OFFLINE` | disables startup network operations | `dist/utils/version-check.js`, `dist/core/package-manager.js`, `dist/core/model-runtime.js`, `dist/main.js` |
| `PI_TELEMETRY` | telemetry override — see §10 | `dist/core/telemetry.js:6-7` |
| `PI_SKIP_VERSION_CHECK` | update check | `dist/utils/version-check.js:3,21` |
| `HTTP_PROXY` / `HTTPS_PROXY` | outbound HTTP | `dist/core/http-dispatcher.js` |

### What pi discovers outside its own directory

Three things, and one of them is not fenced off by `PI_CODING_AGENT_DIR`.

**a) `AGENTS.md` / `CLAUDE.md`, walked up from cwd to the filesystem root.**
`dist/core/resource-loader.js:46-71` (`loadProjectContextFiles`) loads `<agentDir>/AGENTS.md` as global context, then walks every ancestor of cwd, breaking only when `dirname(currentDir) === currentDir`:

```javascript
let currentDir = resolvedCwd;
while (true) {
    const contextFile = loadContextFileFromDir(currentDir);
    if (contextFile && !seenPaths.has(contextFile.path)) {
        ancestorContextFiles.unshift(contextFile);
        seenPaths.add(contextFile.path);
    }
    const parentDir = dirname(currentDir);
    if (parentDir === currentDir) break;
    currentDir = parentDir;
}
```

Candidates per directory are `["AGENTS.md", "AGENTS.MD", "CLAUDE.md", "CLAUDE.MD"]` (`resource-loader.js:31`).
There is no repo-root stop.
Suppressed by `--no-context-files` / `-nc`.

**b) `~/.agents/skills/` — the cross-harness skills directory, keyed off `HOME`, not off the agent dir.**
`dist/core/package-manager.js:1927`:

```javascript
const userAgentsSkillsDir = join(getHomeDir(), ".agents", "skills");
```

with `getHomeDir()` at `dist/core/package-manager.js:77-79`:

```javascript
function getHomeDir() {
    return process.env.HOME || homedir();
}
```

registered as skills at `package-manager.js:1975`.

**c) `<ancestor>/.agents/skills/`, walked up from cwd to the git repo root — or to the filesystem root if there is no git repo.**
`dist/core/package-manager.js:273-290`:

```javascript
function collectAncestorAgentsSkillDirs(startDir) {
    const skillDirs = [];
    const resolvedStartDir = resolve(startDir);
    const gitRepoRoot = findGitRepoRoot(resolvedStartDir);
    let dir = resolvedStartDir;
    while (true) {
        skillDirs.push(join(dir, ".agents", "skills"));
        if (gitRepoRoot && dir === gitRepoRoot) break;
        const parent = dirname(dir);
        if (parent === dir) break;
        dir = parent;
    }
    return skillDirs;
}
```

registered at `package-manager.js:1959`.
The `gitRepoRoot` guard only fires inside a git repo; a task workspace that is not a git checkout gets the full walk to `/`.

### Measured: what leaks, and how much

This is the OMP `~/.claude/tools/` lesson repeating for pi, and unlike doc 07's version it is quantified rather than anecdotal.

Four runs, same prompt (`"Say hi"`), same mock endpoint, same isolated `PI_CODING_AGENT_DIR` containing only `models.json` and an empty `settings.json`, cwd `C:\Users\tisao\Desktop\harness-bench` — varying only the environment:

| Run | First `POST /v1/chat/completions` body | System message chars |
|---|---|---|
| A — `PI_CODING_AGENT_DIR` only | **14,209 bytes** | **10,805** |
| B — `+ HOME=<tmp>` | 5,737 | 2,547 |
| C — `+ HOME + USERPROFILE=<tmp>` | 5,737 | 2,547 |
| D — `PI_CODING_AGENT_DIR + --no-skills` | 5,737 | 2,547 |

**A correctly-configured `PI_CODING_AGENT_DIR` still produced a request 2.48× larger than the boxed-in one, and a system prompt 4.24× larger.**
The 8,258 extra characters were an `<available_skills>` XML block enumerating every skill in `C:\Users\tisao\.agents\skills\` — a directory pi has no business reading in a benchmark, injected verbatim into the system prompt with `<name>`, `<description>` and `<location>` per skill.
`--no-extensions` did **not** suppress it (run with `--no-extensions` alone: still 14,209 bytes); only `HOME` or `--no-skills` did.

That number is the whole point.
It is the same order of magnitude as the pi-vs-OMP gap doc 07 built its headline on.
A run matrix that gets isolation wrong on the pi arm would report a 2.5× input-token inflation that is an artefact of the operator's home directory, not a property of the harness.

**Windows caveat, for completeness:** `getHomeDir()` prefers `process.env.HOME`, so on POSIX setting `HOME` alone is sufficient (run B). On Windows `homedir()` derives from `USERPROFILE`, so `HOME` happens to win here too — but set both. The experiment machine is NixOS, where `HOME` is the operative one.

### A fully boxed-in run

Belt and braces, since the failure mode is silent inflation rather than a crash:

```bash
env -i \
  PATH="$PATH" \
  HOME=/run/bench/home \
  PI_CODING_AGENT_DIR=/run/bench/pi \
  PI_CODING_AGENT_SESSION_DIR=/run/bench/sessions/$RUN_ID \
  PI_OFFLINE=1 \
  PI_TELEMETRY=0 \
  PI_SKIP_VERSION_CHECK=1 \
  timeout --kill-after=30s 900s \
  pi --mode json --no-extensions --no-skills --no-context-files --no-prompt-templates --no-themes \
     --model bench/MODEL "$PROMPT" < /dev/null
```

Then **assert the first request body size against a recorded baseline** and fail the run if it differs.
A size assertion on request 0 catches every class of ambient leak at once, and is cheaper than auditing the discovery code after every version bump.

`/run/bench/home` must exist and be empty; `~/.agents` inside it must not.

Note that pi wrote a 2-byte `auth.json` into the isolated agent dir on first run.
Nothing was written to the machine's real `~/.pi/` during this session — verified with `find ~/.pi -newermt <session start> -type f`, which returned nothing.

---

## 8. Side-calls — compaction, and its tokens are discarded

**pi has no title generation.**
Grep across `dist/` finds no `generateTitle`, no `titleModel`, no classification, routing, or embedding call.
This is a clean win over OpenCode, which doc 06 established loses title-generation tokens entirely.

pi has exactly **three** LLM code paths outside the main agent turn, all summarisation.
Only two modules in the package import a completion function from `pi-ai` outside the loop, both via `import { completeSimple } from "@earendil-works/pi-ai/compat"`:
`dist/core/compaction/compaction.js:7` and `dist/core/compaction/branch-summarization.js:7`.

**a) Context compaction — history summary.**
`dist/core/compaction/compaction.js:122` (`generateSummary`), request issued at `:410-416`.
Same model, same provider, same thinking level as the main loop — `dist/core/agent-session.js:1427` and `:1662` both pass `this.model`.
There is no `compactionModel` / `smallModel` setting; `getCompactionSettings()` (`dist/core/settings-manager.js:526-532`) returns only `{enabled, reserveTokens, keepRecentTokens}`.

**On by default, in headless mode.**
`dist/core/settings-manager.js:509-511`: `getCompactionEnabled() { return this.settings.compaction?.enabled ?? true; }`, corroborated by `docs/settings.md:113` (`compaction.enabled | boolean | true`).
Defaults: `{ enabled: true, reserveTokens: 16384, keepRecentTokens: 20000 }` (`compaction.js:51-55`).
It fires when `contextTokens > contextWindow - reserveTokens` (`compaction.js:137-141`), and `_checkCompaction` is called from `agent-session.js:782` (after `agent_end`) and `:868` (before each prompt) — mode-agnostic, so `pi --mode json` runs it.

**b) Compaction split-turn prefix summary — a *second* call in the same compaction.**
`compaction.js:579-599` (`generateTurnPrefixSummary`).
When the cut lands mid-turn, `compact()` issues two LLM calls (`compaction.js:552-556`), the second with `maxTokens = 0.5 * reserveTokens`.

**c) Branch summarisation.** `dist/core/compaction/branch-summarization.js:187`, `maxTokens: 2048`.
Gated on `options.summarize` (`agent-session.js:2330`) and reachable only through `navigateTree` — the TUI `/tree` command, RPC, or an extension.
A plain `pi --mode json "prompt"` never hits it.

### The tokens are discarded, in all three cases

`generateSummary` reads `response.content` and throws away `response.usage` (`compaction.js:151-155`); `compact()` returns only `{summary, firstKeptEntryId, tokensBefore, details}` (`compaction.js:270-275`).
The session records a `type: "compaction"` entry with no usage field (`dist/core/session-manager.js:742-754`), and `getSessionStats()` sums only `type === "message"` entries with `role === "assistant"` (`agent-session.js:2471-2494`), as does the TUI footer (`dist/modes/interactive/components/footer.js:83-90`).
The `compaction_end` event's `result` is `{summary, firstKeptEntryId, tokensBefore, estimatedTokensAfter, details}` — no usage (`agent-session.js:1452-1465`, `:1694-1700`; schema at `docs/json.md:18`).
`generateTurnPrefixSummary` (`compaction.js:595-599`) and `generateBranchSummary` (`branch-summarization.js:243-247`) read only `content` likewise, and `branch_summary` is persisted as a non-`message` entry (`session-manager.js:991-1002`).

**Net: compaction input and output tokens are billed by the provider and are invisible in pi's `/stats`, its footer cost, and its JSON stream.**
This is Cline's behaviour exactly — doc 06 recorded Cline discarding its compaction summariser's usage — and it is the strongest argument for the proxy being the system of record rather than any arm's self-report.

Three consequences for the run matrix:

1. **The proxy sees these calls; pi's own numbers do not.** A pi-vs-anything comparison built on `agent_end.messages` usage will silently under-count long tasks. Use the proxy.
2. **Compaction requests are indistinguishable from loop requests at the proxy** unless something marks them. They are `POST /v1/chat/completions` to the same endpoint with the same model. `UNVERIFIED:` whether the compaction request carries any distinguishing header or body field — I read the call sites but did not capture a compaction request on the wire, because filling a 32 K context against a mock was out of scope for this pass. A benchmark that needs to separate loop tokens from compaction tokens should verify this before relying on it; the cheap alternative is to size tasks below the compaction threshold and assert `compaction_start` never appears in the stream.
3. **`compaction.enabled: false` in `settings.json` removes the whole class**, at the cost of hard-failing on context overflow instead of degrading. For fixed-size benchmark tasks that is the more honest configuration.

---

## 9. SSE parsing robustness — all three Zen quirks survived

pi does **not** hand-roll the chat-completions SSE parser.
It uses the `openai` npm SDK: `pi-ai/dist/api/openai-completions.js:1` imports `OpenAI`, and `:135` calls `client.chat.completions.create(params, requestOptions).withResponse()`, then iterates already-parsed objects at `:251`.
Confirmed on the wire — the mock recorded `user-agent: OpenAI/JS 6.26.0` and the full `x-stainless-*` header set.
(pi does have hand-rolled SSE parsers, at `pi-ai/dist/api/openai-codex-responses.js:533` and `pi-ai/dist/api/pi-messages.js:207`, but neither is on the `openai-completions` path.)

That is a good sign on its own: the parser is the reference implementation, not bespoke.
Each quirk, read in the source and then confirmed by running the mock that emits it:

**a) Unknown `reasoning_content` — read deliberately, not merely tolerated.**
`pi-ai/dist/api/openai-completions.js:296`:

```javascript
const reasoningFields = ["reasoning_content", "reasoning", "reasoning_text"];
```

First non-empty string wins; the result becomes a `thinking` block.
There is no schema validation anywhere on the chunk path — no zod, no typebox, no `Value.Check` — and the SDK does a bare `JSON.parse` with no validation, so genuinely unknown fields are ignored silently and never throw.

**b) Usage on a chunk that still carries `finish_reason` — recorded correctly.**
`pi-ai/dist/api/openai-completions.js:260-266`:

```javascript
if (chunk.usage) {
    output.usage = parseChunkUsage(chunk.usage, model);
}
const choice = Array.isArray(chunk.choices) ? chunk.choices[0] : undefined;
if (!choice) continue;
```

The usage read happens **before** the `choices` guard, so it does not require empty `choices`; `finish_reason` is handled independently at `:271`.
It is assignment, not accumulation, so there is no double-count.
Confirmed empirically: the mock attached `prompt_tokens: 1234 / completion_tokens: 7` to the `finish_reason: "stop"` chunk, and pi reported `{"input":1234,"output":7,"totalTokens":1241}`.

One caveat from those assignment semantics: **last usage chunk wins**. A gateway that sends full usage on the finish chunk and then a second, zeroed usage frame would under-report. Zen sends one.

**c) A frame after `data: [DONE]` — consumed and discarded by the SDK, never reaches pi.**
`openai/core/streaming.mjs:28-30` flips a `done` flag on the sentinel and **continues draining** rather than breaking, discarding every subsequent frame without parsing or yielding.
Confirmed: the mock's `data: {"choices":[],"cost":"0"}` after `[DONE]` caused no error, no stall, and no stray event.

Even if such a frame did reach pi, `choices: []` is safe — the guard at `:263` handles both non-array and empty-array.

**Two things a gateway must not do**, established from the same read:

- **Never attach `usage` to a post-`[DONE]` frame.** It is silently dropped at the SDK layer. Zen does not, but a proxy that rewrites the stream must not introduce this.
- **Never omit `finish_reason`.** `pi-ai/dist/api/openai-completions.js:375-376` throws `"Stream ended without finish_reason"`, and that message matches a retry pattern in `pi-ai/dist/utils/retry.js:59` (`"ended without"`), so a truncated stream burns the retry budget rather than failing loudly. This is the single most likely way for a proxy bug to masquerade as a model failure.

Parse errors are not swallowed: the SDK logs and rethrows (`streaming.mjs:40`), pi's outer catch at `openai-completions.js:381` converts the throw into a visible `{type: "error"}` stream event, and SDK-level HTTP retries are off by default (`maxRetries: options?.maxRetries ?? 0`, `:133`).
A `JSON.parse` `SyntaxError` matches none of the retry patterns in `pi-ai/dist/utils/retry.js:20-72`, so it surfaces rather than being retried away.

### First-request shape — the prior pi figures are CONFIRMED

Captured from the same isolated run described in §7 run C/D, against the mock on `127.0.0.1:11435`:

| First `POST /v1/chat/completions` | Prior work (doc 07) | This measurement | Verdict |
|---|---|---|---|
| native tool schemas | 4 | **4** (`read, bash, edit, write`) | confirmed exactly |
| `tools` array, JSON bytes | 2,900 | **2,900** | confirmed exactly |
| system message chars | 2,610 | **2,619** JSON-encoded / 2,558 raw | confirmed, ±9 |
| total request body bytes | 5,739 | **5,748** | confirmed, ±9 |
| `stream_options` | `{"include_usage":true}` | `{"include_usage":true}` | confirmed |

**The reproduction is exact on the two figures that do not depend on the environment, and off by 9 bytes on the two that do.**
The 9-byte delta is fully accounted for: the system prompt ends with `Current working directory: <cwd>`, and the cwd string differed in length between the two measurements by exactly that much.
Re-running from a different directory moved both numbers together (5,737 / 2,547 from `C:\Users\tisao\Desktop\harness-bench`), which confirms the cwd as the sole source of variance.

**So the project's headline pi-vs-OMP numbers stand: 4 vs 11 tool schemas, 2,900 vs 38,973 tool bytes, ~5,74x vs 62,111 total body bytes, a 10.8× spread on the first request.**
Independently reproduced, on a different day, with a different mock implementation.

Full top-level keys of the captured body: `model, messages, stream, stream_options, store, max_completion_tokens, tools`.
Two are worth flagging for the proxy:

- `"store": false` — an OpenAI-platform field. Harmless for a permissive gateway, but a strict OpenAI-compatible server that rejects unknown top-level fields will reject pi. Zen is permissive.
- `"max_completion_tokens": 4096` — pi sends the newer field name, not `max_tokens`, and its value comes straight from `maxTokens` in `models.json`. An older gateway that only understands `max_tokens` will silently ignore pi's output cap.

`UNVERIFIED:` whether Zen accepts `store` and `max_completion_tokens`.
Both were accepted by the mock, which accepts anything.
This is a five-minute check against the real gateway and should be done before the first real run.

---

## 10. Telemetry

`dist/core/telemetry.js` is eight lines and sends nothing — it is a flag resolver (`dist/core/telemetry.js:6-7`):

```javascript
export function isInstallTelemetryEnabled(settingsManager, telemetryEnv = process.env.PI_TELEMETRY) {
    return telemetryEnv !== undefined ? isTruthyEnvFlag(telemetryEnv) : settingsManager.getEnableInstallTelemetry();
}
```

Two consumers:

**a) Install/update ping — opt-out, default on, but interactive-only.**
`dist/modes/interactive/interactive-mode.js:738-753` fires `https://pi.dev/api/report-install?version=<v>` with a pi User-Agent and a 5 s timeout, guarded by `if (process.env.PI_OFFLINE) return;` and the telemetry flag.
Default is `true` (`dist/core/settings-manager.js:658-659`).
It is called only from `getChangelogForDisplay()` on a fresh install or first run after a version bump — **a headless `pi -p` / `--mode json` run never reaches it**, because the only call site is in `interactive-mode.js`.

**b) Provider attribution headers — opt-out, default on, and these DO fire on every main-loop request.**
`dist/core/provider-attribution.js:27-49`, wired at `dist/core/sdk.js:189`, injects `HTTP-Referer: https://pi.dev` / `X-OpenRouter-Title: pi` / `X-OpenRouter-Categories: cli-agent` for OpenRouter, `X-BILLING-INVOKE-ORIGIN: Pi` for NVIDIA NIM, `User-Agent: pi-coding-agent` for Cloudflare.
Not flag-gated at all: `x-opencode-session` / `x-opencode-client: pi` for opencode providers (`provider-attribution.js:50-58`).

These are per-provider and keyed on the provider *name*.
A custom provider named `mockollama` got none of them — the captured headers were the plain `openai` SDK set plus `authorization`.
**Do not name the benchmark's custom provider `opencode` or `openrouter`**, or pi will start attaching attribution headers that a strict gateway may reject or that may perturb routing.

**Disable, exactly:**

- `PI_TELEMETRY=0` (or `false` / `no`) overrides settings for both consumers. Help text at `dist/cli/args.js:366`.
- or `"enableInstallTelemetry": false` in `<agentDir>/settings.json` (`docs/settings.md:59`).
- `PI_OFFLINE=1` / `--offline` kills all startup network operations including the ping and the update check.
- `docs/settings.md:79` warns that opting out of telemetry does **not** disable update checks — pi can still fetch `https://pi.dev/api/latest-version`. That is disabled separately with `PI_SKIP_VERSION_CHECK=1` (`dist/utils/version-check.js:3,21`), and is also interactive-only.

**A dormant second analytics system exists but has no transmitter.**
`enableAnalytics` and `trackingId` are in settings (`dist/core/settings-manager.js:666-679`, default `false`), prompted for by the first-time-setup dialog.
No transmitter and no `/privacy` command exist in 0.80.10 — grep finds `enableAnalytics` only in `settings-manager.js`, `startup-ui.js:135`, and `first-time-setup.js`.
The dialog is additionally gated behind `PI_EXPERIMENTAL=1` (`dist/core/experimental.js:2`) and a missing `settings.json`.
Worth re-checking on a version bump.

**OpenTelemetry is present as a dependency but not wired.**
`@opentelemetry/api` 1.9.0 is installed and declared by `pi-ai/package.json`, but a recursive grep for `opentelemetry|getTracer|SpanKind|otel` across `pi-coding-agent/dist/`, `pi-ai/dist/`, `pi-agent-core/dist/` and `pi-tui/dist/` returns **zero hits**.
No tracer is initialised, no exporter configured, and there is no way to turn it on from pi.

---

## Cleanup

Everything created for this pass lived under `C:\Users\tisao\AppData\Local\Temp\pi-bench\` and was removed: two mock servers (ports 11435, 11436), four throwaway agent directories, an isolated `HOME`, a scratch workspace, and all request/output logs.
Both mock server processes were stopped.

Nothing was written to `C:\Users\tisao\.pi\` — verified with `find "C:/Users/tisao/.pi" -newermt "<session start>" -type f`, which returned nothing.
No files outside `docs/research/10-pi-measurement-surface.md` were modified in the repository.

Nothing was left behind that could not be removed.

---

## Verdict

### PI — YES, with one hard prerequisite

**The deciding fact:** a custom provider in `<PI_CODING_AGENT_DIR>/models.json` with `baseUrl`, `api: openai-completions`, a dummy `apiKey` and `compat.supportsDeveloperRole: false` was verified to send a well-formed OpenAI Chat Completions request to `http://127.0.0.1:11435/v1` — the benchmark's own proxy port — from a fully headless `pi --mode json` run, and to drive a three-request tool-calling loop through it to completion.
Nothing routes through a vendor backend.

It is a good instrument on every axis the ticket asked about:

- it sets `stream_options: {include_usage: true}` itself, so the proxy's rewrite is idempotent rather than corrective;
- it reports per-message `usage` with `input` / `output` / `cacheRead` / `cacheWrite` / `reasoning` / `totalTokens` and a `cost` breakdown, and `agent_end.messages` lets a run be totalled from one event;
- `turn_start` / `turn_end` maps one-to-one onto an upstream request, so step counting needs no inference;
- it writes a JSONL session transcript with per-message usage and two clocks, redirectable with `PI_CODING_AGENT_SESSION_DIR`;
- it has **no title-generation side-call at all**, which is strictly better than OpenCode;
- its SSE parser is the `openai` SDK's, and it survived all three OpenCode Zen quirks unchanged — including recording usage correctly off a chunk that still carries `finish_reason`;
- telemetry is inert in headless mode and fully disableable;
- it is MIT, in nixpkgs, and runs on plain Node with no Bun requirement and no native-addon obstacles — the three NixOS blockers doc 07 raised for OMP do not apply.

**The one hard prerequisite: give pi a dedicated `HOME`, not just a dedicated `PI_CODING_AGENT_DIR`.**
This is not a theoretical hardening note.
Measured on this machine, a correctly-isolated `PI_CODING_AGENT_DIR` with an ambient `HOME` produced a **14,209-byte first request against 5,737 boxed-in — 2.48×, with a system prompt 4.24× larger** — because `dist/core/package-manager.js:1927` reads `$HOME/.agents/skills` and injects every skill found there into the system prompt.
`--no-extensions` does not stop it; only `HOME` or `--no-skills` does.
An arm configured the obvious way would report a 2.5× input-token inflation that belongs to the operator's home directory, not to pi.

Four conditions before it goes in the run matrix:

1. **Dedicated `HOME` *and* `PI_CODING_AGENT_DIR`**, plus `--no-skills --no-extensions --no-context-files`. Then **assert the first request body size against a recorded baseline** and fail the run on drift — one assertion catches every ambient-leak class at once, including ones a future version introduces.
2. **Wrap every invocation in an external `timeout --kill-after`.** pi has no max-turns cap, no max-iterations setting, and no `--max-time`; `shouldStopAfterTurn` exists in the type but is never set by pi's own code. The loop ends only when the model stops calling tools — the exact assumption a 2.6B-class model breaks.
3. **Classify from the stream, never the exit code, and use `agent_end.willRetry` — not OMP's `isTerminal`.** JSON mode returns 0 on total failure. Note the refinement: a *non-zero* exit in JSON mode still means something, namely that pi never started (a missing credential exits 1 in both modes), so treat `exit != 0` as a hard configuration abort. And take the **last** `agent_end` — pi emits one per retry attempt, three by default.
4. **Decide compaction policy explicitly.** It is on by default, uses the main model, and its tokens are discarded from pi's own reporting exactly as Cline's are. Either set `compaction.enabled: false`, or size tasks below the threshold and assert `compaction_start` never appears.

Two smaller items to settle before the first real run, both five-minute checks against the gateway rather than blockers:

- Confirm Zen accepts `"store": false` and `"max_completion_tokens"` — pi sends both, and neither was exercised against a strict server.
- Do not name the custom provider `opencode` or `openrouter`, or pi will attach attribution headers (`dist/core/provider-attribution.js:27-58`).

And pin the version.
The local install is `0.80.10`; npm `latest` is `0.84.1`, published the same day this was written, with 40 versions in the registry.
`0.80.10` is what every number in this document describes.

### Summary

| | pi 0.80.10 |
|---|---|
| Custom OpenAI-compatible base URL | **Yes — verified end to end** |
| Mechanism | `<PI_CODING_AGENT_DIR>/models.json`, `providers.<name>.baseUrl` + `api: openai-completions` |
| API key required | **Yes** — dummy value or `--api-key`; no `auth: none` equivalent |
| Headless entry point | `pi --mode json` / `pi -p` |
| Machine-readable output | JSONL, 13 record types |
| Token usage in output | per assistant message: input/output/cache/reasoning/total + cost |
| Sets `include_usage` itself | yes, by default |
| Run-level usage aggregate | no — sum `agent_end.messages` |
| Session transcript | JSONL tree with `id`/`parentId`, per-message usage, two clocks |
| Step boundary | `turn_start`/`turn_end`, 1:1 with an upstream request |
| Max-turns cap | **none** |
| Built-in wall-clock timeout | **none** |
| Default retries | 3 (2 s / 4 s / 8 s), one `agent_end` per attempt |
| Exit code on total failure | 0 in JSON mode, 1 in text mode; 1 in both on startup failure |
| Exit code on bad flag | 1 (not 2) |
| Side-calls | compaction only (×2 per compaction); **tokens discarded**. No title generation |
| SSE parser | `openai` SDK 6.26.0 — tolerates all three Zen quirks |
| Telemetry in headless mode | none fired; `PI_TELEMETRY=0`, `PI_OFFLINE=1` |
| Isolation | `PI_CODING_AGENT_DIR` + **`HOME`** both required (2.48× measured leak without `HOME`) |
| Runtime | Node ≥ 22.19.0 |
| In nixpkgs | yes, `pi-coding-agent` 0.84.0 |
| Licence | MIT |
| Verdict | **arm** |
