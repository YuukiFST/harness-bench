# 07 — Candidate arms: oh-my-pi (OMP) and Cursor CLI

Research ticket #7.
Question: can oh-my-pi and the Cursor CLI serve as arms in a headless, proxy-measured harness benchmark with the model held fixed?

The measurement instrument is a local reverse proxy on `http://localhost:11435/v1` that fronts an OpenAI-compatible endpoint, forces `stream_options: {"include_usage": true}`, swallows the usage frame and logs one JSONL record per request.
One requirement therefore decides everything: **the arm must be pointable at an arbitrary OpenAI-compatible base URL, headlessly, without routing through a vendor backend.**
Each candidate is judged on that first.

## What was pinned, and when

Retrieved 2026-08-07.

| Artifact | Pin |
|---|---|
| `can1357/oh-my-pi` git clone | HEAD `39477ba39bfbdc6be2cfff0efde979dd32bd7eb7`, committed 2026-08-07T14:50:17+02:00 |
| `@oh-my-pi/pi-coding-agent` (npm) | `17.2.10`, installed and executed locally |
| `@earendil-works/pi-coding-agent` (baseline for comparison) | `0.80.10`, already installed on this machine |
| Cursor CLI docs | fetched live from `cursor.com/docs/cli/*` on 2026-08-07 |

All file:line references for OMP are relative to the repo root at that SHA.

## How the evidence was gathered

OMP was installed and exercised, not just read.
`bun add @oh-my-pi/pi-coding-agent` into a throwaway directory pulled `17.2.10` and 138 packages in 22 s, and `omp --version` printed `omp/17.2.10`.

Because no real Ollama runs on the authoring machine, a mock OpenAI-compatible server was run on `127.0.0.1:11435` — the benchmark's actual proxy port — that answers `GET /v1/models`, streams a three-chunk SSE chat completion, emits a trailing usage-only frame, and appends every inbound request (headers plus full body) to a JSONL log.
Both OMP `17.2.10` and pi `0.80.10` were then pointed at that same endpoint with equivalent configs and the same prompt (`"Say hi"`), which makes the request-shape numbers below a genuine head-to-head rather than two separately-sourced figures.

This proves the wiring, the exit codes, the JSON event shapes and the on-the-wire request size.
It proves nothing about how either harness behaves with a real 2.6B model that emits malformed tool calls.

The authoring machine is Windows 11; the experiment machine is NixOS.
Process-level behaviour transfers; binary packaging does not.

Cursor was researched from documentation only — the CLI was not installed, because question 2 below makes installing it pointless.

---

## Candidate 1 — oh-my-pi (OMP)

### 1. What it actually is

**A hard fork of pi that vendors the entire source tree, not a wrapper, plugin layer or config distribution.**

The README says so in its own words, twice.
Under the hero image: "Fork of [Pi](https://github.com/badlogic/pi-mono) by [@mariozechner](https://github.com/mariozechner)" (`README.md:23`).
And in the body: "Originally built on [Mario Zechner](https://github.com/mariozechner)'s wonderful [Pi](https://github.com/badlogic/pi-mono), omp adds everything you're missing" (`README.md:108`).

The dependency evidence confirms it is a vendored fork rather than a dependent.
The root `package.json` declares a Bun workspace over `packages/*` and a catalog in which every pi-lineage package is re-scoped and re-versioned: `@oh-my-pi/pi-agent-core`, `@oh-my-pi/pi-ai`, `@oh-my-pi/pi-catalog`, `@oh-my-pi/pi-coding-agent`, `@oh-my-pi/pi-natives`, `@oh-my-pi/pi-tui`, `@oh-my-pi/pi-utils`, `@oh-my-pi/pi-wire`, all pinned to `17.2.10` (`package.json:16-30`).
Grepping `bun.lock` for `earendil`, `@mariozechner`, `badlogic` or `pi-mono` returns **zero matches** — OMP depends on no upstream pi package at any version.

The versioning is independent too: pi is at `0.80.10` (npm) / `0.84.0` (nixpkgs), OMP at `17.2.10`.
The binary is `omp`, not `pi`: `"bin": { "omp": "src/cli.ts" }` (`packages/coding-agent/package.json:31-33`).

The fork's own porting guide states the mechanical rule: upstream imports are rewritten scope-by-scope, `@mariozechner/pi-coding-agent` → `@oh-my-pi/pi-coding-agent` and so on, with a note that "Some upstream packages publish under the `@earendil-works/*` scope instead of `@mariozechner/*`. Map it the same way" (`docs/porting-from-pi-mono.md:40-55`).

Upstream changes are pulled in as periodic manual syncs, and the guide records the last one:

> **Commit:** `b21b42d032919de2f2e6920a76fa9a37c3920c0a`
> **Date:** 2026-03-22
>
> — `docs/porting-from-pi-mono.md:6-12`

So as of 2026-08-07 the fork has been diverging without a recorded upstream sync for roughly four and a half months.

The repo is much larger than pi's: 17 TypeScript workspace packages plus a Rust workspace ("~80k lines of Rust core" per `README.md:27`), a Bazel build, a Python subtree, and a Dockerfile.

### 2. Its relationship to pi in concrete terms

This is the part with benchmark value, so it is enumerated rather than summarised.

#### 2a. Tool set — 4 exposed tools become 11, out of a registry of 29

pi `0.80.10` describes itself as "AI coding assistant with read, bash, edit, write tools" (`pi --help`, first line), with `grep`/`find`/`ls` present but off by default.
Measured on the wire, pi sent exactly four tool schemas: `read, bash, edit, write`.

OMP declares 29 built-ins plus 2 hidden ones (`packages/coding-agent/src/tools/builtin-names.ts:1-38`):

```
read, bash, edit, ast_grep, ast_edit, ask, debug, eval, github, glob, grep, lsp,
inspect_image, browser, computer, checkpoint, rewind, security_scan, task, hub,
todo, web_search, write, memory_edit, retain, recall, reflect, learn, manage_skill
```
plus hidden `yield`, `goal`.

It does **not** send all 29 as native tool schemas.
A mechanism called `xd://` mounts most built-ins as virtual devices reachable by writing a JSON args object to `xd://<tool>` through the ordinary `write` tool, gated on the `tools.xdev` setting (`packages/coding-agent/src/tools/index.ts:676-700`):

```typescript
// Ordinary sessions use xd:// for discoverable built-ins, custom tools, and
// MCP tools. ...
const xdevEnabled =
    !restrictToolNames && session.settings.get("tools.xdev") && tools.some(tool => tool.name === "write");
```

The wire capture shows the result: 11 native tool schemas (`read, bash, edit, eval, glob, grep, task, hub, todo, web_search, write`), with the rest described in prose inside the system prompt under a `# xd:// Tool Devices` heading.
This is a real architectural divergence — a benchmark must pin `tools.xdev`, because flipping it changes the tool-schema token cost by a large factor.

#### 2b. System prompt and request size — measured head-to-head

Same mock endpoint, same prompt, same model id, both harnesses run with their ambient environment disabled:

| First `POST /v1/chat/completions` | pi 0.80.10 | omp 17.2.10 | ratio |
|---|---|---|---|
| native tool schemas | 4 | 11 | 2.8× |
| `tools` array, JSON bytes | 2,900 | 38,973 | 13.4× |
| system message, JSON-encoded chars | 2,610 | 22,909 | 8.8× |
| total request body bytes | 5,739 | 62,111 | **10.8×** |
| `stream_options` | `{"include_usage":true}` | `{"include_usage":true}` | — |

The OMP system prompt opens with an RFC-2119 conventions block, a `ROLE` section, `# Engineering Principles`, an `# Internal URLs` registry (`skill://`, `rule://`, `agent://`, `history://`, `artifact://`, `local://`, `mcp://`, `issue://`, `pr://`, `omp://`), a `# Tool Inventory`, and the `# xd:// Tool Devices` catalogue with per-tool schemas inline.
The prompt sources live in `packages/coding-agent/src/system-prompt.ts` (35.5 KB) and `packages/coding-agent/src/prompts/`.

That ~10.8× spread on the very first request, before any agent loop runs, is the single most important number in this document for the "is this cosmetic?" question.

#### 2c. Permissions model — pi has none, OMP has three modes

`docs/security.md` in pi's own tarball states pi has no approval gate at all, and doc 06 verified that grepping pi's `dist/` for approval symbols returns nothing.

OMP adds a full three-tier approval system (`docs/approval-mode.md`).
Every tool declares an `approval` tier of `read`, `write` or `exec`; tools may attach `policy: allow | deny | prompt`; users may override per tool via `tools.approval.<toolName>`.
The modes:

| Mode | Auto-approves | Prompts for |
|---|---|---|
| `always-ask` | `read` | `write`, `exec` |
| `write` | `read`, `write` | `exec` |
| `yolo` (default) | `read`, `write`, `exec` | none |

— `docs/approval-mode.md:19-25`

The default is `yolo`, so a headless run does not hang on approval out of the box, but `--approval-mode` and `--auto-approve`/`--yolo` exist and are applied as a settings override in `packages/coding-agent/src/main.ts:1283-1292`.
`bash` can force a prompt for critical destructive patterns via an `override: true` decision, and in `yolo` a bare critical override is ignored (`docs/approval-mode.md:47-51`).

#### 2d. Retry policy — 3 attempts becomes 10

pi defaults to `retry.maxRetries: 3` with `baseDelayMs: 2000`.
OMP defaults to `retry.maxRetries: 10` (`docs/settings.md:471`) with `retry.baseDelayMs` default `500` (`packages/coding-agent/src/config/settings-schema.ts:1516`).

Verified empirically against a dead endpoint: pi emitted three `auto_retry_start` events, OMP emitted ten.
That is a ~3× difference in requests-per-failed-turn, which directly inflates the proxy's request count on any transport hiccup and must be normalised before comparing.

#### 2e. Context management — LLM summarisation replaced by image compaction

OMP ships `@oh-my-pi/snapcompact`, described in its own README as:

> Bitmap-frame context compression for vision-capable LLMs.
> Instead of asking an LLM to summarize discarded conversation history, snapcompact serializes it and renders the text into dense PNG frames of pixel-font glyphs that vision models read back directly. The whole pass is local and deterministic — no LLM call, no API key, no latency beyond rendering.
>
> — `packages/snapcompact/README.md:1-7`

`docs/compaction.md` is 27.9 KB and `docs/non-compaction-retry-policy.md` another 12.9 KB.

For this benchmark that path is almost certainly inert — LFM2.5-2.6B is not vision-capable and tasks should be sized below the context window — but it is a genuine, non-cosmetic difference in the compaction stage and would need to be confirmed disabled rather than assumed so.

#### 2f. Agent loop and session runtime

The agent loop lives in a separate package, `packages/agent/src/agent-loop.ts`, and gained a deadline abort path that pi has no equivalent for (`packages/agent/src/agent-loop.ts:929-1010`): a `config.deadline` installs an `AbortController` and an `AbortSignal.any` composition, with `isDeadlineExceeded` checks at two loop checkpoints.

Other loop-adjacent additions with no pi counterpart: an advisor runtime that "passively reviews each turn and injects notes" (`--advisor`), `--prewalk` (switch to a cheaper model at the first edit once a todo list exists), `--plan-yolo`, auto-thinking difficulty classification (`src/auto-thinking/`), and a `task`/`hub` subagent system.

#### 2g. Other divergences the fork records about itself

`docs/porting-from-pi-mono.md:302-397` is an explicit "Intentional Divergences" register.
The load-bearing entries:

| Area | Upstream pi | OMP |
|---|---|---|
| Credential storage | `proper-lockfile` + `auth.json` | `agent.db` (bun:sqlite), multi-credential with round-robin |
| Extension TS loading | `jiti` | native Bun `import()` |
| Manifest field | `pkg.pi` | `pkg.omp` preferred, `pkg.pi` fallback |
| Extension architecture | resource/package/settings managers | capability-based discovery + `Settings` singleton + `EventBus`; upstream classes survive only as shims in `legacy-pi-coding-agent-shim.ts` |
| Tool factories | `createTool(cwd, options?)` | `createTools(session)` via a `BUILTIN_TOOLS` registry |
| Test framework | `vitest` | `bun:test` |

Plus a "Features We Added (Preserve These)" list: multi-credential auth with session affinity, the capability-discovery system, MCP/Exa/SSH integrations, LSP writethrough for format-on-save, bash interception, fuzzy path suggestions in `read` (`docs/porting-from-pi-mono.md:380-397`).

#### 2h. Ambient-environment surface — larger than pi's, and it bit during testing

OMP discovers and loads **Claude Code's** directories as well as its own: `packages/coding-agent/src/discovery/claude.ts:572` registers a provider described as "Load custom tools from .claude/tools/", and `packages/coding-agent/src/discovery/claude-plugins.ts:4-5` loads `~/.claude/plugins/cache/` from `installed_plugins.json`.

This is not theoretical.
The first headless run on this machine died before reaching the model, on an unrelated tool that happens to live in `~/.claude/tools/`, **despite `--no-extensions`**:

```
C:\Users\tisao\.claude\tools\rgr\docs\reports\rgr-harness-evals-smoke-20260807T130414Z.json
Unknown command: mockollama/MOCK-2.6B

[Unhandled Rejection] ExtensionExitError: Module called process.exit(1) during guarded
extension/hook loading; OMP extension/hook modules must not terminate the host process.
OMP_TEXT_EXIT=1
```

The same command with an isolated `HOME`/`USERPROFILE` ran clean.
This is OpenCode's `--pure` lesson repeating: **a benchmark runner must give OMP a dedicated `HOME` as well as a dedicated `PI_CODING_AGENT_DIR`**, because `--no-extensions` alone does not fence off Claude Code's tool directory.

Not established: exactly which discovery provider bypassed `--no-extensions` here.
`main.ts:1259-1263` shows `--no-extensions` switching `injectOmpExtensionCliRoots` to `"explicit-only"` mode, so the leak is presumably in a discovery provider that does not route through that injection, but I did not trace it to a line.

### 3. Headless invocation

Working command, verified end to end against the mock endpoint:

```bash
cd /path/to/workspace
HOME=/run/bench/home \
PI_CODING_AGENT_DIR=/run/bench/omp \
omp --mode json \
    --no-session --no-extensions --no-skills --no-rules --no-lsp --no-title \
    --auto-approve \
    --model mockollama/MOCK-2.6B \
    --max-time 900 \
    "your task prompt here" < /dev/null
```

Mode resolution differs from pi and the difference matters (`packages/coding-agent/src/main.ts:1272-1274`):

```typescript
const pipedInput = isProtocolMode ? undefined : await logger.time("readPipedInput", readPipedInput);
const autoPrint = pipedInput !== undefined && !parsedArgs.print && parsedArgs.mode === undefined;
const isInteractive = !parsedArgs.print && !autoPrint && parsedArgs.mode === undefined;
```

pi drops to print mode whenever **stdin or stdout** is not a TTY.
OMP only auto-prints when stdin actually carries piped input; a redirected stdout with a TTY stdin leaves OMP interactive.
A runner must therefore pass `-p` or `--mode json` explicitly and not rely on pipe detection.

`--mode` accepts `text | json | rpc | acp | rpc-ui` in source (`packages/coding-agent/src/cli/flag-tables.ts:124-127`), though `--help` advertises only `text, json, rpc, or rpc-ui`; `acp` is also a subcommand.
Unrecognised flags exit **2** ("command line usage error"), added because an unknown token used to leak as the initial prompt and start a real LLM session — see the comment at `packages/coding-agent/src/main.ts:1631-1639`.

Flags OMP has that pi does not, all benchmark-relevant:

- `--cwd <path>` — pi has no working-directory flag at all and requires the runner to `chdir`.
- `--max-time <value>` — accepts seconds or `5s`/`10m`/`1h` (`packages/coding-agent/src/cli/flag-tables.ts:92-104,153-154`), converted to `options.deadline = Date.now() + parsed.maxTime * 1000` (`packages/coding-agent/src/main.ts:908-910`) and enforced inside the agent loop. pi has no built-in timeout.
- `--approval-mode`, `--auto-approve` — no pi equivalent.
- `--add-dir`, `--config`, `--profile`, `--no-lsp`, `--no-pty`, `--no-rules`, `--advisor`, `--print-thoughts`, `--smol`, `--slow`, `--plan`, `--prewalk`, `--plan-yolo`, `--service-tier`.

Flags pi has that OMP drops: `--offline`, `--exclude-tools`/`-xt`, `--no-builtin-tools`/`-nbt`, `--no-context-files`/`-nc` (OMP has `--no-rules` instead), `--api-key` is present in both.

**There is no max-turns cap in headless mode.**
An iteration-based loop limit type exists (`packages/coding-agent/src/modes/loop-limit.ts:1-9`, `kind: "iterations"`), but it is imported only by `interactive-mode.ts` and the status line — it is a `/loop` slash command, not a CLI flag.
`--max-time` is the only headless bound, and an external `timeout --kill-after` is still warranted.

#### JSON output

`--mode json` emits JSONL, one object per line, serialised in `packages/coding-agent/src/modes/print-mode.ts:191-193`.
Verified event sequence for a one-turn success:

```
session, agent_start, turn_start, message_start, message_end,
message_start, message_update ×3, message_end, turn_end, agent_end
```

The `session` header carries `version`, `id`, `timestamp`, `cwd` — identical in shape to pi's.

**The terminal event schema differs from pi's and this will break a shared classifier.**
pi `0.80.10` emits `agent_end` with keys `type, messages, willRetry`, followed by a distinct `agent_settled` event.
OMP `17.2.10` emits `agent_end` with keys `type, messages, isTerminal` and **no** `agent_settled`.
Both were captured on the same mock endpoint minutes apart, so this is a real divergence, not a version-reporting artefact.

### 4. Custom base URL — VERIFIED WORKING

**OMP can be pointed at an arbitrary OpenAI-compatible endpoint, and it was.**

The mechanism is inherited from pi's custom-provider file but the format and location changed.
pi reads `~/.pi/agent/models.json`; OMP reads `~/.omp/agent/models.yml` (then `models.yaml`), migrating a legacy `models.json` at the same location if both YAML files are absent (`docs/models.md:17-27`).
The loader is `packages/coding-agent/src/config/model-registry.ts` (`docs/models.md:7-9`).

Validation rules for a full custom provider: `baseUrl` required, `apiKey` required unless `auth: none`, and `api` at provider level or on every model (`docs/models.md:104-113`).
`auth: none` is the clean choice for a keyless local endpoint — pi requires a dummy `apiKey` placeholder instead.

The config that was verified, written to a throwaway `PI_CODING_AGENT_DIR`:

```yaml
providers:
  mockollama:
    baseUrl: http://127.0.0.1:11435/v1
    api: openai-completions
    auth: none
    models:
      - id: MOCK-2.6B
        name: Mock 2.6B
        api: openai-completions
        reasoning: false
        input: [text]
        cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }
        contextWindow: 32768
        maxTokens: 4096
        compat:
          supportsDeveloperRole: false
          supportsReasoningEffort: false
```

Registration confirmed:

```
$ PI_CODING_AGENT_DIR=... omp models
mockollama (1)
│ MOCK-2.6B │     33K │    4.1K │ -        │ no     │
```

And the traffic actually arrived at `127.0.0.1:11435`, which is the whole question — the mock's request log recorded `POST /v1/chat/completions` with a 62,111-byte body and a well-formed OpenAI Chat Completions payload.

`PI_CODING_AGENT_DIR` is the env var that relocates the whole agent directory, still under pi's name (`omp --help` environment section: "PI_CODING_AGENT_DIR — Session storage directory (default: ~/.omp/agent)"; also `packages/utils/src/dirs.ts:5,326`).
`OMP_PROFILE`/`--profile` gives an alternative isolated-state mechanism (`packages/utils/src/dirs.ts:35,87`).

Built-in local engines exist as a shortcut but are worse for this purpose: `ollama` reads `OLLAMA_BASE_URL` then `OLLAMA_HOST`, `llama.cpp` reads `LLAMA_CPP_BASE_URL`, `lm-studio` reads `LM_STUDIO_BASE_URL` (`docs/providers.md:188-190`).
Prefer the explicit custom provider — it pins the context window and the model list instead of relying on discovery, and it keeps the proxy URL out of a variable another arm might also read.

One operational note: OMP issued a `GET /v1/models` against the endpoint once across the test session but not on subsequent runs, so the proxy should answer `/v1/models` even though it is not hit per-run.
`UNVERIFIED:` the exact code path that issues that probe and its cache TTL — I confirmed the behaviour from the mock's request log but did not trace it to a source line, and a grep for `/v1/models` across `packages/ai` and `packages/coding-agent` returned 500+ matches across 347 files without an obvious single origin.

### 5. Token and usage reporting

**OMP sets `stream_options: {include_usage: true}` itself, by default**, for the `openai-completions` API (`packages/ai/src/providers/openai-completions.ts:1555-1557`):

```typescript
if (initialCompat.supportsUsageInStreaming !== false) {
    params.stream_options = { include_usage: true };
}
```

Confirmed on the wire: the captured request body contains `"stream_options":{"include_usage":true}`.
The proxy's rewrite is therefore idempotent for this arm rather than corrective — which is a useful property, since it means the proxy is not changing OMP's behaviour relative to how a user would run it.
The gate is `compat.supportsUsageInStreaming`, so a `models.yml` that sets it to `false` would suppress the flag; leave it unset.

Usage is reported **per assistant message**, on `message_end` and on `message_update`, verified against the mock's `prompt_tokens: 1234 / completion_tokens: 7 / total_tokens: 1241`:

```json
{"type":"message_end","message":{"role":"assistant","content":[{"type":"text","text":"Task complete."}],
 "api":"openai-completions","provider":"mockollama","model":"MOCK-2.6B",
 "usage":{"input":1234,"output":7,"cacheRead":0,"cacheWrite":0,"totalTokens":1241,
          "cost":{"input":0,"output":0,"cacheRead":0,"cacheWrite":0,"total":0}},
 "stopReason":"stop","timestamp":1786107900573,"responseId":"chatcmpl-mock1",
 "duration":26.07,"ttft":23.83}}
```

`duration` and `ttft` per message are a bonus pi's stream also carries.
`agent_end.messages` repeats the full message array, so per-run totals can be summed from a single event.
There is no run-level aggregate object equivalent to Cline's `run_result.aggregateUsage`.

### 6. Exit-code semantics

**OMP reproduces pi's asymmetry exactly: text mode exits 1 on failure, JSON mode always exits 0.**

The `stopReason` check that sets exit 1 is guarded by `if (mode === "text")` (`packages/coding-agent/src/modes/print-mode.ts:223-251`):

```typescript
if (mode === "text") {
    const assistantMsg = session.getLastAssistantMessage();
    if (assistantMsg) {
        if ((assistantMsg.stopReason === "error" || assistantMsg.stopReason === "aborted") && !isSilentAbort(assistantMsg)) {
            ...
            if (flushed) { process.exit(1); } else { process.stderr.once("drain", () => process.exit(1)); }
        }
```

Verified against a dead endpoint on `127.0.0.1:11435`:

```
=== TEXT MODE, DEAD ENDPOINT ===
Working...
Unable to connect. Is the computer able to access the url?
OMP_TEXT_DEAD_EXIT=1

=== JSON MODE, DEAD ENDPOINT ===
OMP_JSON_DEAD_EXIT=0
```

The JSON-mode run emitted ten `auto_retry_start` events, a final `message_end` with `stopReason: "error"` and `errorMessage: "Unable to connect. Is the computer able to access the url?"`, then `agent_end` with `isTerminal: true` — and exit 0.

So OMP joins OpenCode and pi in returning 0 on total failure.
The discriminator is the last assistant message's `stopReason`, exactly as for pi, but the companion flag is `agent_end.isTerminal` rather than pi's `agent_end.willRetry`.
Nothing hung; the process terminated on its own after the retry budget, which is better than OpenCode's indefinite hang.

Also note: unrecognised flags exit **2**, not 1, so a runner distinguishing argument errors from task errors gets that for free with OMP and does not with pi or OpenCode.

### 7. Install and runtime

Package `@oh-my-pi/pi-coding-agent`, binary `omp`, runtime **Bun ≥ 1.3.14** — enforced at process start with a hard exit (`packages/coding-agent/src/cli.ts:40-45`):

```typescript
if (Bun.semver.order(Bun.version, MIN_BUN_VERSION) < 0) {
    process.stderr.write(`error: Bun runtime must be >= ${MIN_BUN_VERSION} ...`);
    process.exit(1);
}
```

Not Node. This is a harder runtime constraint than pi (`"engines": {"node": ">=22.19.0"}`) or OpenCode.

Documented install paths (`README.md:37-70`): `curl -fsSL https://omp.sh/install | sh`, `brew install can1357/tap/omp`, `bun install -g @oh-my-pi/pi-coding-agent`, `irm https://omp.sh/install.ps1 | iex`, `mise use -g github:can1357/oh-my-pi`.
The install script supports `--source` (via bun), `--binary` (prebuilt) and `--ref <tag>`, installing into `${PI_INSTALL_DIR:-$HOME/.local/bin}` (fetched from `https://omp.sh/install`, lines 1-16).

#### NixOS obstacles — three, and they are real

**1. Not in nixpkgs.**
`pkgs/by-name/om/omp/package.nix` returns 404, and a GitHub code search for `oh-my-pi` or `can1357` across `NixOS/nixpkgs` returns 0 results.
There is no derivation to reuse.

Side finding that resolves an open question from doc 06: **pi *is* in nixpkgs**, as `pkgs/by-name/pi/pi-coding-agent/package.nix`, `version = "0.84.0"`, built with `buildNpmPackage` from `fetchFromGitHub` on `earendil-works/pi` tag `v0.84.0`, with the model catalog restored from the published `@earendil-works/pi-ai` npm tarball because it is gitignored upstream.
So the pi arm has a clean Nix path; the OMP arm does not.

**2. The prebuilt binaries are large, dynamically-linked Bun standalone ELFs.**
Release `v17.2.10` assets: `omp-linux-x64` (185 MB), `omp-linux-musl-x64` (152 MB), `omp-linux-arm64` (154 MB), `omp-linux-musl-arm64` (150 MB), plus darwin and windows.
The glibc build is exactly the artefact class that fails on NixOS without `nix-ld` or `autoPatchelf`, and the README already warns the musl one is not self-contained either:

> **Alpine / musl:** the prebuilt musl binary links `libstdc++`/`libgcc` dynamically, which stock Alpine does not ship. Install them first: `apk add libstdc++ libgcc`.
>
> — `README.md:45`

**3. Native addons and blocked postinstalls on the npm path.**
`bun add @oh-my-pi/pi-coding-agent` reported "Blocked 2 postinstalls" — `onnxruntime-node@1.24.3` (`node ./script/install`) and `protobufjs@7.6.5`.
The installed tree contains prebuilt `.node` binaries: `@oh-my-pi/pi-natives-win32-x64/pi_natives.win32-x64-baseline.node`, `@img/sharp-*`, `lightningcss-*`, `onnxruntime-node/bin/napi-v6/{linux,darwin,win32}/*/onnxruntime_binding.node`, `sherpa-onnx-*`.
On Linux the equivalents are prebuilt ELF `.node` files with the same dynamic-loader problem.

The best NixOS bet is probably: install `bun` from nixpkgs, `bun install -g @oh-my-pi/pi-coding-agent@17.2.10` under `nix-ld`, and accept the native addons.
`UNVERIFIED:` whether OMP runs on NixOS by any path.
It could not be tested from Windows, no issue was found either way, and the `@oh-my-pi/pi-natives` addon is loaded eagerly enough that a partial failure may be fatal rather than degraded.
**Test `omp --version` on the experiment machine before committing to this arm** — same five-minute gate doc 06 prescribed for Cline.

### 8. License and maintenance

**License: MIT**, with dual copyright acknowledging the fork lineage (`LICENSE:1-4`):

```
MIT License

Copyright (c) 2025 Mario Zechner
Copyright (c) 2025-2026 Can Bölük
```

Confirmed as `MIT` by the GitHub API, and `packages/coding-agent/package.json:11` declares `"license": "MIT"` with `"author": "Can Boluk"` and `"contributors": ["Mario Zechner"]`.

**Maintenance: extremely active, arguably too active to benchmark without a hard pin.**
Repo metadata (GitHub API, 2026-08-07): created `2025-12-31`, last push `2026-08-07T13:14:12Z`, 22,677 stars, 1,074 open issues, not archived, default branch `main`.
Release cadence is roughly daily:

```
v17.2.10  2026-08-06    v17.2.6  2026-08-03
v17.2.9   2026-08-05    v17.2.5  2026-08-03
v17.2.8   2026-08-04    v17.2.4  2026-08-01
v17.2.7   2026-08-03    v17.2.3  2026-08-01
```

Eight releases in six days.
Pin `17.2.10` and record the SHA; a benchmark whose arm ships a new version mid-run is not a benchmark.

`UNVERIFIED:` OMP's headless reliability track record.
The 1,074 open issues were not triaged for headless hangs, unbounded loops or local-model tool-call failures, which is the analysis doc 06 performed for OpenCode and Cline.
Everything I exercised terminated correctly, but that is four invocations against a mock, not evidence about a real 2.6B model.

### What a PI vs OMP comparison would isolate

**It is not cosmetic, and the spread will be large.**

The strongest evidence is the head-to-head wire capture in §2b: with the model, the endpoint, the prompt and the ambient environment all held fixed, OMP's first request is **10.8× larger** than pi's — 62,111 bytes against 5,739.
That is measured, not inferred, and it is the input-token axis of the benchmark's headline metric appearing before the agent loop has taken a single step.

What a pi-vs-OMP arm pair would isolate, ranked by how cleanly the benchmark can attribute it:

1. **Prompt and tool-schema overhead.** 4 tool schemas vs 11, 2,900 vs 38,973 bytes of schema, 2,610 vs 22,909 chars of system prompt. This is a pure harness-authoring choice with the agent lineage held constant, and it is the cleanest signal in the pair.
2. **Whether that overhead buys anything.** OMP's entire thesis is that it does — the README claims Grok Code Fast 1 goes from 6.7% to 68.3% pass rate and Grok 4 Fast drops 61% of output tokens once the edit format stops causing retry loops (`README.md:91-97`), attributed to a rewritten edit format, summarising `read`, and per-model prompt tuning. **A pi-vs-OMP benchmark on a 2.6B model is a direct test of that claim on the weakest model class**, which is precisely where the fork says the effect is largest. That is the publishable result.
3. **Retry amplification.** 3 vs 10 retries changes request count per failed turn by ~3×; on a flaky local endpoint this can dominate. It is also a confound: it must be normalised (set both to the same `maxRetries`) or reported separately, or it will be mistaken for a harness-efficiency difference.
4. **Tool-exposure architecture.** The `xd://` device mechanism trades native tool schemas for prose in the system prompt. Whether that is a net token win, and whether a 2.6B model can drive a `write`-to-`xd://<tool>` indirection at all, is a genuinely open question with a measurable answer.

Three honest caveats.

The fork has diverged so far that "the underlying agent lineage held fixed" is doing less work than it sounds.
The last recorded upstream sync is 2026-03-22 and the register of intentional divergences covers auth storage, extension loading, tool factories, the test framework, the agent loop and the compaction pipeline.
The comparison isolates *harness design* with the *model* fixed; it does not isolate a single variable.

Comparing default configurations compares products, not techniques.
Running OMP with `--tools read,bash,edit,write` and `tools.xdev` off would isolate the prompt from the tool set, and running both at matched retry budgets would isolate the loop from the transport.
Both configurations are worth running; only one of them answers "which harness should I use", and it is the default one.

The `xd://` indirection and the 39 KB of tool schema are exactly the kind of thing a 2.6B model may simply fail to execute.
A result where OMP scores worse than pi because the harness overwhelmed the model is a real and interesting finding, but it must not be reported as a token-efficiency result.

---

## Candidate 2 — Cursor CLI

All Cursor claims are from documentation retrieved 2026-08-07.
The CLI was not installed, for the reason in §2.

Note that Cursor moved its docs from `docs.cursor.com/en/...` to `cursor.com/docs/...`; the old paths 308-redirect.

### 1. A headless CLI exists

| Item | Value | Source |
|---|---|---|
| Install (macOS/Linux/WSL) | `curl https://cursor.com/install -fsS \| bash` | https://cursor.com/docs/cli/installation |
| Install (Windows) | `irm 'https://cursor.com/install?win32=true' \| iex` | same |
| Binary | `agent`, with `cursor-agent` kept as a backward-compatible alias | https://cursor.com/changelog/cli-jan-08-2026 |
| Status | announced 2025-08-07, "still in beta" | https://cursor.com/blog/cli |

Documented flags (https://cursor.com/docs/cli/reference/parameters): `-p/--print`, `--output-format text|json|stream-json`, `--stream-partial-output`, `--model`, `--list-models`, `-f/--force` (alias `--yolo`), `--workspace <path>`, `--trust` (headless only), `--sandbox enabled|disabled`, `--approve-mcps`, `--api-key`, `-H/--header`, `--resume`, `--continue`, `--mode plan|ask`, `-w/--worktree`, `--plugin-dir`.

Canonical non-interactive form:

```bash
agent -p "prompt" --output-format stream-json --model <m> --force --workspace /path --trust
```

`--force` is not optional for a benchmark: without it "changes are only proposed" (https://cursor.com/docs/cli/headless).

On its own merits this is a good headless CLI — cleaner than OpenCode's, with a real workspace flag and a documented streaming JSON format.

### 2. Custom base URL — DISQUALIFYING

**No. Requests route through Cursor's own servers, by Cursor's own statement, and the CLI exposes no base-URL override at all.**

The routing statement is from Cursor's own help centre, on the page that documents bringing your own API key (https://cursor.com/help/models-and-usage/api-keys):

> "Your API key is sent to our backend with every request because all requests are routed through Cursor's servers for final prompt building."

An older phrasing of the same sentence, from a documentation mirror (https://www.aidoczh.com/cursor/settings/api-keys.html):

> "All requests are routed through our backend where we do the final prompt building."

That alone ends it.
Even the desktop BYOK path — the only path that accepts a custom base URL — is server-mediated, so the "override OpenAI base URL" setting does not mean what a benchmark needs it to mean.

The CLI is worse still: it has no such setting.
The complete documented environment surface is `CURSOR_API_KEY` (a *Cursor account* key, not a provider key), `CURSOR_CONFIG_DIR`, `XDG_CONFIG_HOME`, and the corporate-proxy variables `HTTP_PROXY`, `HTTPS_PROXY`, `NODE_USE_ENV_PROXY`, `NODE_EXTRA_CA_CERTS` (https://cursor.com/docs/cli/reference/configuration).
`OPENAI_BASE_URL` and `OPENAI_API_KEY` appear nowhere in the CLI reference.
The `cli-config.json` keys are `version`, `editor.vimMode`, `permissions.allow`/`permissions.deny`, `sandbox.mode`, `sandbox.networkAccess`, `network.useHttp1ForAgent`, `attribution.*` — no endpoint field, no provider key.

The `HTTP_PROXY` variables do not rescue this.
They would proxy TLS traffic to Cursor's own API in Cursor's own wire protocol, which is not an OpenAI-compatible request Ollama could serve, and they do not change the upstream endpoint.

The help-centre page also never mentions the CLI or headless agents at all, and notes that custom keys "only work with chat models" while "Tab completion continues using Cursor's built-in models".

Corroborating, lower-confidence: an open feature request titled "[CLI] No way to override the base url used in cursor CLI" (https://forum.cursor.com/t/cli-no-way-to-override-the-base-url-used-in-cursor-cli/133409, filed 2025-09-13) states "there is currently no way to override the base url", and a Cursor staff member replied on 2025-09-14: "Hey, thanks for the feature request, we'll consider it."
A companion request asks for exactly this benchmark's use case — CI prompt-regression testing — and contrasts the desktop-only override against the CLI (https://forum.cursor.com/t/override-openai-base-url-for-headless-and-background-agents/132693).
Forum evidence is weak on its own; here it corroborates the docs' silence and carries a staff acknowledgement of the gap.

`UNVERIFIED:` https://cursor.com/security does not describe the model-request path — it says only that the app "makes requests to Cursor backend domains to deliver API, indexing, update, and marketplace functionality" — and `cursor.com/docs/account/privacy` returns 404.
The routing claim rests entirely on the api-keys help page quoted above, which is official and unambiguous.

### 3. JSON output mode — exists, carries no token usage

`--output-format json | stream-json` is documented (https://cursor.com/docs/cli/headless, https://cursor.com/docs/cli/reference/output-format).
Event types are `system` (carries `model`), `assistant` (carries `timestamp_ms`), `tool_call` (started/completed subtypes) and `result`.

The terminal `result` event, as documented:

```json
{
  "type": "result",
  "subtype": "success",
  "duration_ms": 1234,
  "duration_api_ms": 1234,
  "is_error": false,
  "result": "<full assistant text>",
  "session_id": "<uuid>",
  "request_id": "<optional request id>"
}
```

No `usage`, no `input_tokens`, no `output_tokens` — timing only.
There is also no `/usage` or `/cost` slash command (https://cursor.com/docs/cli/reference/slash-commands).
The docs note field additions may occur in a backward-compatible way, so this could change.

This is a second, independent disqualifier: with no proxy and no self-reported usage, there is no token measurement at all.

### 4. Exit-code semantics

`UNVERIFIED:` not documented.
The headless page shows a shell example checking `$?` where 0 means success, but no page enumerates non-zero codes.
`cli/headless`, `cli/reference/parameters` and `cli/reference/configuration` were all checked.
Establishing this would require running the binary.

### 5. Terms of Service — benchmark publication is conditionally permitted

Found, in §1.5 "Use Restrictions" of https://cursor.com/terms-of-service, clause (vii), under the preamble "Except and solely to the extent such a restriction is impermissible under applicable law, you may not":

> "provide to any third party the results of any benchmark tests of the Service, unless you include all necessary information for others to replicate the tests"

So publishing is allowed **provided the methodology is published in full** — which this project intends to do anyway.

Two adjacent clauses are worth reading before designing any Cursor measurement.
Clause (v) prohibits using the Service "to develop or train a model that is competitive with the Service, or engage in model extraction or theft attacks".
Clause (viii) prohibits "harvest, scrape, or extract data from the Service".
A cost benchmark with published methodology satisfies (vii); routing Cursor's traffic through a capture proxy to extract its prompts would sit uncomfortably close to (viii).

---

## Verdict

### oh-my-pi — YES

**The deciding fact:** a custom provider in `~/.omp/agent/models.yml` with `baseUrl`, `api: openai-completions` and `auth: none` was verified to send a well-formed OpenAI Chat Completions request to `http://127.0.0.1:11435/v1` — the benchmark's own proxy port — from a fully headless `omp --mode json` run.
Nothing routes through a vendor backend; OMP is a local process that talks to whatever URL you give it.

It is a stronger candidate than the decisive test alone suggests: it already sets `stream_options: {include_usage: true}` itself, it reports per-message `usage` with `input`/`output`/`cache` breakdowns plus `duration` and `ttft`, it has a built-in `--max-time` deadline, it exits 2 on argument errors, and it terminated cleanly on every path exercised including a dead endpoint.

Three conditions before it goes in the run matrix:

1. **Test `omp --version` on the NixOS experiment machine first.** Not in nixpkgs; prebuilt binaries are 150–185 MB dynamically-linked Bun ELFs; npm install pulls native `.node` addons and two blocked postinstalls. Bun ≥ 1.3.14 is a hard requirement. This is the gate.
2. **Give it a dedicated `HOME` as well as `PI_CODING_AGENT_DIR`.** `--no-extensions` did not stop OMP from loading a tool out of `~/.claude/tools/` and killing the run.
3. **Classify outcomes from the stream, never the exit code**, and use `agent_end.isTerminal` — not pi's `willRetry`, which OMP does not emit.

### Cursor CLI — NO

**The deciding fact:** Cursor states on its own help page that "all requests are routed through Cursor's servers for final prompt building" (https://cursor.com/help/models-and-usage/api-keys), and the CLI exposes no base-URL override of any kind — a gap Cursor staff acknowledged as an unimplemented feature request.
There is no configuration under which `agent` talks to `http://localhost:11435/v1`.

The arm is disqualified for this project.
It fails a second time independently: its `result` event carries `duration_ms` and `duration_api_ms` but no token counts, so even with wall-clock-only measurement there would be no cost axis.

If Cursor is wanted anyway, the only honest framing is a separate, clearly-labelled non-proxy-measured category — wall time and step count from the `stream-json` stream, token cost from Cursor's own dashboard, and an explicit note that the model is *not* held fixed with the other arms because it is Cursor's model on Cursor's infrastructure.
That is a different experiment, and it should not share a table with the proxy-measured arms.

### Summary

| | OMP 17.2.10 | Cursor CLI |
|---|---|---|
| Custom OpenAI-compatible base URL | **Yes — verified end to end** | **No — vendor-routed, no override** |
| Headless entry point | `omp --mode json` / `omp -p` | `agent -p --output-format stream-json` |
| Machine-readable output | JSONL, 10 event types observed | stream-json, 4 event types |
| Token usage in output | per message, input/output/cache/cost | **none** |
| Sets `include_usage` itself | yes, by default | n/a |
| Exit code on total failure | 0 in JSON mode, 1 in text mode, 2 on bad flags | undocumented |
| Built-in wall-clock timeout | `--max-time` | not documented |
| Max-turns cap | none headless | not documented |
| Runtime | Bun ≥ 1.3.14 | bundled binary |
| In nixpkgs | no (pi is, as `pi-coding-agent` 0.84.0) | no |
| License | MIT | proprietary |
| Verdict | **arm** | **excluded** |
