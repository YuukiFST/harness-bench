# 06 — Headless invocation and configuration per harness

Research ticket #6.
Question: what is the precise, non-interactive command line and configuration for each harness to run one task in one workspace against a local OpenAI-compatible endpoint, and then exit?

Target endpoint: Ollama at `http://localhost:11434/v1`, model id `LFM2.5-2.6B`.
Experiment machine: NixOS.

## How the evidence was gathered

Two of the three harnesses are installed on the authoring machine (Windows 11), so their facts come from running the binaries directly.
OpenCode `1.17.9` and pi `0.80.10` were exercised end to end.
Cline is **not** installed on the authoring machine (`Get-Command cline` → not found), so every Cline claim below is from source or docs, never from execution.

Ollama is not running on the authoring machine either (`Invoke-WebRequest http://localhost:11434/v1/models` timed out).
To test the success path I ran a throwaway mock OpenAI-compatible server on `127.0.0.1:11434` that answers `/v1/models` and streams a single SSE chat completion, then pointed both installed harnesses at it.
This proves the wiring, the exit codes and the output shapes; it does not prove anything about how a real 2.6B model behaves.

Caveat that applies to everything below: the authoring machine is Windows, the experiment machine is NixOS.
Process-level behaviour (exit codes, JSON shapes, config parsing) transfers.
Binary packaging and anything touching `uv_spawn`, signals or the dynamic loader does not.

---

## OpenCode

### Install pin

The repo `sst/opencode` now redirects to `anomalyco/opencode`; the GitHub API returns `full_name: anomalyco/opencode` and `default_branch: dev` (https://api.github.com/repos/sst/opencode).

The npm package is `opencode-ai`, latest `1.18.15` (https://registry.npmjs.org/opencode-ai/latest).
The npm package is a launcher; the real binaries ship as per-platform `optionalDependencies` (`opencode-linux-x64`, `opencode-linux-x64-musl`, `opencode-linux-arm64`), all pinned to the same version (same URL).
The in-repo workspace package is named `opencode`, not `opencode-ai` (https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/package.json).

```bash
npm install -g opencode-ai@1.18.15
```

**Prefer the nixpkgs pin on NixOS.**
OpenCode is packaged at `pkgs/by-name/op/opencode/package.nix`, attribute path `pkgs.opencode`, currently `version = "1.18.13"` on nixpkgs `master`, built from `fetchFromGitHub` on `anomalyco/opencode` tag `v1.18.13` and wrapped with `ripgrep` on PATH (https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/op/opencode/package.nix).
The npm artifact is a prebuilt dynamically-linked ELF and will need `nix-ld` or `autoPatchelf` on NixOS; the nixpkgs derivation avoids that and also supplies the `ripgrep` dependency the npm tarball does not.

Not established: the exact version on the `nixos-unstable` channel as opposed to nixpkgs `master`.
A flake pin therefore gives a build two patch versions behind npm at the time of writing.

The version exercised locally is older than both:

```
$ opencode --version
1.17.9
```

### Config

Sources load in this order, later overriding earlier, merged rather than replaced (https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/config.mdx):

1. Remote config (`.well-known/opencode`)
2. Global `~/.config/opencode/opencode.json`
3. `OPENCODE_CONFIG` env var path
4. Project `opencode.json` in the project root
5. `.opencode` directories (agents, commands, plugins)
6. `OPENCODE_CONFIG_CONTENT` env var (inline JSON)
7. Managed config files (system directories)
8. macOS managed preferences (MDM)

Note that `OPENCODE_CONFIG` sits *below* the project file, so a task repo's own `opencode.json` would still win over it.
`OPENCODE_CONFIG_CONTENT` beats every standard file and is the injection point a benchmark runner should use if it must not be overridden by the workspace.

Minimal working config, written as `opencode.json` in the workspace root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": {
        "baseURL": "http://localhost:11434/v1",
        "apiKey": "ollama",
        "timeout": 300000,
        "chunkTimeout": 60000
      },
      "models": {
        "LFM2.5-2.6B": { "limit": { "context": 32768, "output": 4096 } }
      }
    }
  },
  "model": "ollama/LFM2.5-2.6B",
  "small_model": "ollama/LFM2.5-2.6B",
  "permission": {
    "*": "allow",
    "external_directory": "deny",
    "question": "deny",
    "webfetch": "deny",
    "websearch": "deny",
    "doom_loop": "deny"
  }
}
```

This shape is the documented Ollama example with the model id substituted (https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/providers.mdx).
`npm` selects the AI-SDK adapter; use `@ai-sdk/openai-compatible` for `/v1/chat/completions` endpoints and `@ai-sdk/openai` only for `/v1/responses` (https://opencode.ai/docs/providers).
The docs say local providers need no API key, but `options.apiKey` is accepted and costs nothing, so set a dummy.
The `limit` block matters because a custom provider has no models.dev metadata to supply the context window.
`small_model` matters because OpenCode uses a separate cheap model for session titling and will otherwise try to resolve a different provider (https://opencode.ai/docs/config).

Verified locally that the provider block is parsed and the model registered:

```
$ opencode models ollama
ollama/LFM2.5-2.6B
```

The CLI model reference is `provider_id/model_id`, split on the first slash only, where `provider_id` is your `provider` block key (https://opencode.ai/docs/models).
Model resolution precedence is `-m`/`--model` flag, then the `model` config key, then most-recently-used, then internal rules (same URL).

### Headless invocation

```bash
cd /path/to/workspace
opencode run --pure --format json --dir /path/to/workspace \
             -m ollama/LFM2.5-2.6B \
             --auto \
             "your task prompt here" < /dev/null
```

`opencode run` is the documented non-interactive entry point (https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/cli.mdx).

`--pure` ("run without external plugins") is **not optional for a benchmark runner**, and this is the single most useful thing the local testing turned up.
Without it, OpenCode loads the machine's global plugins from `~/.config/opencode/plugins/`, and on this machine one of them killed the run outright:

```
$ opencode run --format json --print-logs --log-level ERROR -m ollama/LFM2.5-2.6B "Say hi"
level=ERROR message="failed to load plugin" path=file:///C:/Users/tisao/.config/opencode/plugins/crg-plugin.ts ...
level=ERROR message=process error="EFTYPE: inappropriate file type or format, uv_spawn"
  at <anonymous> (C:\Users\tisao\.config\opencode\plugins\axi-chrome-devtools-axi.js:12:19)
{"type":"error","timestamp":1786105210629,"sessionID":"ses_...","error":{"name":"UnknownError","data":{"message":"EFTYPE: inappropriate file type or format, uv_spawn"}}}
RUN_EXIT=1
```

The same command with `--pure` runs clean.
A benchmark must not inherit ambient user plugins in any case, so pass `--pure` and use a dedicated `HOME`/`XDG_CONFIG_HOME`.

Approval flag — this differs across the two versions I have evidence for.
Local `1.17.9` exposes `--dangerously-skip-permissions` ("auto-approve permissions that are not explicitly denied (dangerous!)") and has **no** `--auto`; verified from `opencode run --help` on 1.17.9.
The `dev` branch at `1.18.15` renames it: `--auto` is the visible flag with that same description, and `--dangerously-skip-permissions` and `--yolo` are present but `hidden: true` (https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/src/cli/cmd/run.ts).
Pin the version, then choose the flag that version actually has.

Prompt passing: positional argument, and stdin also works.
Only the positional form is documented, but the source reads piped stdin when stdin is not a TTY and *concatenates* it after the positional message (same `run.ts` URL):

```typescript
const piped = process.stdin.isTTY ? undefined : await Bun.stdin.text()
message = resolveRunInput(message, piped) ?? ""
```

Verified locally that pure stdin piping works and produces identical output to the positional form.
Consequence: do not mix the two, and redirect stdin from `/dev/null` when using the positional form, or the pipe contents get glued on with a newline.
An empty message with no `--command` and no `--interactive` calls `process.exit(1)`.

### Working directory

`--dir` sets it, implemented as a plain `process.chdir` with a hard `process.exit(1)` on failure (https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/src/cli/cmd/run.ts).
There is no `--cwd` and no `--project` flag on `run`.

Confinement is the `permission` block, not `--dir`.
Permission keys are `read`, `edit`, `glob`, `grep`, `bash`, `task`, `skill`, `lsp`, `question`, `webfetch`, `websearch`, `external_directory`, `doom_loop`, each resolving to `"allow"`, `"ask"` or `"deny"` (https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/permissions.mdx).
Defaults: most permissions default to `"allow"`, while `doom_loop` and `external_directory` default to `"ask"`, and `.env` reads default to `"deny"` (same URL).
Granular glob form is supported, e.g. `"bash": { "*": "ask", "git *": "allow", "rm *": "deny" }` (https://opencode.ai/docs/permissions).

**In headless mode `"ask"` is a hang, not a refusal.**
Because `external_directory` defaults to `"ask"` and there is no TTY to answer, any tool touching a path outside the project freezes the process; issue #36762 documents exactly this, with logs showing `message=asking` and then nothing (https://github.com/anomalyco/opencode/issues/36762).
Every permission class must therefore be pinned explicitly to `allow` or `deny`.

There is no OS-level sandbox — confinement is the in-process permission check plus `chdir`.
Not established: whether OpenCode has any sandbox feature at all; `permissions.mdx`, `config.mdx`, `tools.mdx` and `run.ts` were read and none was found.
On NixOS, add `bwrap` or `systemd-run` confinement around the process.

### Termination

Only two exit codes exist, 0 and 1 (https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/src/cli/cmd/run.ts).
Exit 1 covers session/transport errors *and* argument-validation failures alike, so the exit code alone cannot classify a failure; the `--format json` `error` event must be parsed.

A task the agent failed to accomplish still exits 0 — exit 1 means an API or session error, not a wrong or incomplete answer.
Success must be judged from the workspace diff, never from the exit code.

**A wall-clock timeout must be imposed externally, and this is not theoretical.**
Pointed at a dead `http://localhost:11434/v1`, `opencode run --pure --format json` produced **zero bytes of output and never exited**; I let it run past the 300 s tool timeout, checked the capture file again at roughly nine minutes (still 0 bytes), and finally killed the process:

```
RUN_EXIT=-1     # process killed by me, not a self-terminated exit
```

That is the behaviour described in open issue #40319, "Provider connection error retried indefinitely (hangs 60+s without displaying failure)".
There is no `--max-turns` flag; the nearest control is the agent-level `steps` key, "the maximum number of agentic iterations an agent can perform before being forced to respond with text only", with an unspecified default (https://opencode.ai/docs/agents/).
Provider-level `timeout` (default 300000 ms) and `chunkTimeout` exist in `provider.<id>.options` (https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/config.mdx), but neither covers the init-hang and permission-hang classes, which happen outside any HTTP request.
Wrap every invocation in `timeout --kill-after=30s <N>s`.

### Output

`--format` takes `default` or `json` (`choices: ["default","json"]`).
Default format is human prose; verified locally against the mock endpoint:

```
> build · LFM2.5-2.6B

Task complete.
RUN2_EXIT=0
```

`--format json` is JSONL, one object per line on stdout, every line carrying `type`, `timestamp`, `sessionID` plus event-specific keys.
Event types are `step_start`, `text`, `reasoning`, `tool_use`, `step_finish`, `error` (https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/src/cli/cmd/run.ts).
Verified locally against the mock endpoint (abridged):

```json
{"type":"step_start","timestamp":1786105643391,"sessionID":"ses_023cec97...","part":{"type":"step-start",...}}
{"type":"text","timestamp":1786105643391,"sessionID":"ses_023cec97...","part":{"type":"text","text":"Task complete.","time":{"start":...,"end":...}}}
{"type":"step_finish","timestamp":1786105643392,"sessionID":"ses_023cec97...","part":{"reason":"stop","type":"step-finish","tokens":{"total":13,"input":10,"output":3,"reasoning":0,"cache":{"write":0,"read":0}},"cost":0}}
OC_JSON_EXIT=0
```

Note the envelope `type` is underscored (`step_finish`) while the nested `part.type` is hyphenated (`step-finish`).
`--print-logs` and `--log-level` are global flags writing diagnostics to stderr; they do not change stdout format.

A more robust machine-readable path is `opencode serve` (default `--port 4096`, `--hostname 127.0.0.1`), with `POST /session` then `POST /session/:id/message` returning one synchronous typed JSON response, and an OpenAPI 3.1 spec at `GET /doc` (https://opencode.ai/docs/server).
`opencode run --attach http://localhost:4096` is the documented hybrid.

### Reliability — flagged

OpenCode has 4,963 open issues (https://api.github.com/repos/sst/opencode), including a large open cluster of headless hangs.
The ones that matter here:

- #38723 — `opencode run` intermittently hangs during init, reporter measures a ~44–56% failure rate, open since 2026-07-24.
- #36762 — headless hang whenever a permission resolves to `"ask"`, with no timeout and no way to answer in a non-TTY.
- #17516 — hangs after completing tool calls and never exits, open since 2026-03-14; the reporter's blocked use case is CLI loops that expect termination.
- #33319 and #29395 — concurrent/parallel startup deadlocks (futex, no timeout), so run tasks strictly serially.
- #40319 — provider connection errors retried indefinitely without surfacing failure (independently reproduced above).
- #39968 — silent SSE terminations: a stream that dies without a finish frame is scored as a completed turn.
- #40146 — turns truncated at the output limit are recorded as normal completions, which is exactly what a 2.6B model hitting its output cap will do constantly.
- #31435 — `--format json` drops `text` and `step-finish` events in containerized environments because the idle event races ahead of pending events.

Sources: https://api.github.com/search/issues?q=repo:anomalyco/opencode+is:issue+is:open+run+hang+in:title, https://github.com/anomalyco/opencode/issues/36762, https://github.com/anomalyco/opencode/issues/17516, https://github.com/anomalyco/opencode/issues/31435.

#39968 and #40146 are the dangerous pair: both turn a failed run into exit code 0 with a plausible-looking transcript, which corrupts benchmark results rather than failing loudly.

Not established: whether small models emitting malformed tool calls specifically break OpenCode.
Adjacent open issues exist (#39164 empty tools array for local OpenAI-compatible models, #40888 truncated streaming tool calls, #40468 "stuck in busy forever after toolcall") but none names malformed-tool-call parsing from a small local model.

---

## pi

### Install pin

The installed CLI is version `0.80.10`:

```
$ pi --version
0.80.10
```

The npm package is `@earendil-works/pi-coding-agent`, `"version": "0.80.10"`, `"bin": { "pi": "dist/cli.js" }`, `"engines": { "node": ">=22.19.0" }`, repository `github.com/earendil-works/pi`, directory `packages/coding-agent`.
Read directly from the installed `node_modules/@earendil-works/pi-coding-agent/package.json`.

```bash
npm install -g @earendil-works/pi-coding-agent@0.80.10
```

Not established: whether pi exists in nixpkgs; I did not search nixpkgs for it.
There is a Nix-relevant hook though — `PI_PACKAGE_DIR` is documented as "Override package directory (for Nix/Guix store paths)" in `pi --help`, so the authors anticipate store-path installs.

The package ships its own first-party docs inside the tarball under `docs/`, which is where most of the facts below come from; those are primary sources shipped with the exact installed version, not a website that may have drifted.

### Config

Two files, project overriding global (`docs/settings.md`):

| Location | Scope |
|---|---|
| `~/.pi/agent/settings.json` | Global (all projects) |
| `.pi/settings.json` | Project (current directory) |

Custom providers live in a separate file, `~/.pi/agent/models.json` (`docs/models.md`).
The whole config directory is relocatable via `PI_CODING_AGENT_DIR` (default `~/.pi/agent`), which is the clean way to give each benchmark run an isolated config.

Credential resolution order is: CLI `--api-key` flag, then `auth.json`, then environment variable, then custom provider keys from `models.json` (`docs/providers.md`).

Minimal `models.json` — this exact file was written to a throwaway `PI_CODING_AGENT_DIR` and verified to work:

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [
        { "id": "LFM2.5-2.6B", "contextWindow": 32768, "maxTokens": 4096 }
      ]
    }
  }
}
```

`docs/models.md` documents this as the minimal local-model shape and states the `apiKey` placeholder is required because "pi still treats models as requiring auth before they appear in `/model`, so keyless local servers should keep a dummy value".
The same page recommends `compat.supportsDeveloperRole: false` and `compat.supportsReasoningEffort: false` specifically for "Ollama, vLLM, SGLang, and similar OpenAI-compatible servers" that do not understand the `developer` role.
`api` must be `openai-completions` for Chat Completions endpoints; the other choices are `openai-responses`, `anthropic-messages`, `google-generative-ai`.

Companion `settings.json` for a benchmark run:

```json
{
  "quietStartup": true,
  "defaultProjectTrust": "never",
  "retry": {
    "enabled": true,
    "maxRetries": 3,
    "baseDelayMs": 2000,
    "provider": { "timeoutMs": 300000, "maxRetries": 0, "maxRetryDelayMs": 60000 }
  },
  "httpIdleTimeoutMs": 300000
}
```

`docs/settings.md` documents `retry.enabled` (default `true`), `retry.maxRetries` (default `3`), `retry.baseDelayMs` (default `2000`, backoff 2s/4s/8s), `retry.provider.timeoutMs`, `retry.provider.maxRetries` (default `0`, and the docs warn to keep it at `0`), `retry.provider.maxRetryDelayMs` (default `60000`), and `httpIdleTimeoutMs` (default `300000`, "Set to `0` to disable").
`defaultProjectTrust` is a global-only setting with values `"ask"` (default), `"always"`, `"never"`.

### Headless invocation

```bash
cd /path/to/workspace
PI_CODING_AGENT_DIR=/run/bench/pi \
pi --mode json --offline -ne -ns -nc --no-session \
   --provider ollama --model LFM2.5-2.6B \
   --tools read,write,edit,bash,grep,find,ls \
   "your task prompt here"
```

`-p`/`--print` is "Non-interactive mode: process prompt and exit"; `--mode json` selects the JSON event stream and *implies* non-interactive, so `-p` is redundant with it.
From `dist/main.js`:

```javascript
function resolveAppMode(parsed, stdinIsTTY, stdoutIsTTY) {
    if (parsed.mode === "rpc") return "rpc";
    if (parsed.mode === "json") return "json";
    if (parsed.print || !stdinIsTTY || !stdoutIsTTY) return "print";
    return "interactive";
}
```

Note the last clause: pi drops to print mode automatically whenever stdin or stdout is not a TTY, so a CI pipe alone is enough.

Prompt passing: positional argument (multiple positional messages are sent as successive prompts), `@file` arguments for file attachment, or piped stdin.
`readPipedStdin()` in `dist/main.js` returns `undefined` when `process.stdin.isTTY` and otherwise drains stdin.

**There is no approval prompt to disable.**
`docs/security.md` is explicit: "Pi does not include a built-in sandbox. Built-in tools can read files, write files, edit files, and run shell commands with the permissions of the pi process."
Grepping the shipped `dist/` for `requiresApproval|permissionRequest|askPermission|toolApproval` returns zero matches, and `pi --help` has no `-y`/`--yolo` flag.
Tool scope is controlled by allow/deny lists instead: `--tools`/`-t` (allowlist), `--exclude-tools`/`-xt` (denylist), `--no-tools`/`-nt`, `--no-builtin-tools`/`-nbt`.
Built-in tool names are `read`, `bash`, `edit`, `write`, `grep`, `find`, `ls`, with `grep`/`find`/`ls` off by default per `pi --help`.

The isolation flags matter for a benchmark: `-ne` (no extension discovery), `-ns` (no skills), `-nc` (no `AGENTS.md`/`CLAUDE.md` discovery), `--no-session` (ephemeral, nothing written to the session store), `--offline` (no startup network operations).
Without them pi loads the ambient user environment, which on this machine meant four installed model-catalog packages and a pile of skills.

Project trust in non-interactive mode never prompts: `docs/settings.md` states that `-p`, `--mode json` and `--mode rpc` "do not show a trust prompt", and without a saved decision `defaultProjectTrust` of `ask` or `never` simply ignores project-local resources.
So a hostile workspace cannot block the run by planting a `.pi/` directory; set `defaultProjectTrust: "never"` and it is ignored outright.

### Working directory

Process cwd only.
There is no `--cwd`, `--dir` or `--project` flag in `pi --help`, so the runner must `chdir` before exec.
The session header confirms cwd is captured from the process: `{"type":"session","version":3,"id":"...","cwd":"C:\\Users\\tisao\\AppData\\Local\\Temp\\ws-hb-bfed3ab5"}`.

There is no path confinement of any kind.
`docs/security.md`: "Real isolation needs to come from the operating system or a virtualization/container boundary", and it recommends a container/VM with only the required paths mounted.
The only in-process lever is the `--tools` allowlist — dropping `bash` and `write` makes a run read-only, but nothing stops `read` or `edit` from touching paths outside the workspace.
`docs/containerization.md` is the first-party guidance for wrapping the process.

### Termination

Exit codes come from `dist/modes/print-mode.js`, read in full.
Text mode sets `exitCode = 1` when the last assistant message has `stopReason === "error"` or `"aborted"`, otherwise 0.
Any thrown exception returns 1.
`SIGTERM` exits 143 and `SIGHUP` exits 129 (the latter only on non-Windows).

**Critical asymmetry: `--mode json` does not set a failure exit code.**
The `stopReason` check in `print-mode.js` is guarded by `if (mode === "text")`, so in JSON mode `exitCode` stays 0 unless an exception escapes.
Confirmed empirically against a dead endpoint:

```
=== TEXT MODE ===
Connection error.
EXITCODE=1
=== JSON MODE ===
... three failed attempts, auto_retry_start attempt 1/3, 2/3 ...
EXITCODE=0
```

A runner using `--mode json` must therefore classify outcomes by parsing the stream, not by the exit code.
The discriminator is the final assistant message's `stopReason` (`"stop"` on success, `"error"` on failure) plus `agent_end`'s `willRetry` flag.

Auto-retry is visible in the stream and is bounded: `{"type":"auto_retry_start","attempt":1,"maxAttempts":3,"delayMs":2000,...}`, then attempt 2 at 4000 ms, matching the documented `retry.maxRetries: 3` / `baseDelayMs: 2000` defaults.
A dead endpoint therefore costs roughly 14 s of backoff before pi gives up, rather than hanging.

Not established: whether pi has any max-turns or max-iterations cap.
`pi --help` shows no such flag and `docs/settings.md` lists none; I did not audit the agent loop for an internal bound.
Assume there is none and impose an external wall-clock timeout, as with the others.

### Output

Text mode (`-p`) prints only the final assistant text to stdout; verified against the mock endpoint:

```
$ pi -p --offline -ne -ns -nc --no-session --provider ollama --model LFM2.5-2.6B "Say hi"
Task complete.
PI_TEXT_EXIT=0
```

`--mode json` emits JSONL, one event per line, with a session header first (`docs/json.md`).
Event types are `agent_start`, `agent_end`, `turn_start`, `turn_end`, `message_start`, `message_update`, `message_end`, `tool_execution_start`, `tool_execution_update`, `tool_execution_end`, plus `queue_update`, `compaction_start`, `compaction_end`, `auto_retry_start`, `auto_retry_end`.
Verified against the mock endpoint (abridged):

```json
{"type":"session","version":3,"id":"019fdc30-cc09-7119-be23-59b191f04d19","timestamp":"2026-08-07T12:26:53.321Z","cwd":"..."}
{"type":"agent_start"}
{"type":"turn_start"}
{"type":"message_start","message":{"role":"user","content":[{"type":"text","text":"Say hi"}],...}}
{"type":"message_end","message":{"role":"assistant","content":[{"type":"text","text":"Task complete."}],"provider":"ollama","model":"LFM2.5-2.6B","usage":{"input":10,"output":3,"totalTokens":13,...},"stopReason":"stop",...}}
{"type":"turn_end","message":{...},"toolResults":[]}
{"type":"agent_end","messages":[...],"willRetry":false}
PI_JSON_EXIT=0
```

The stream is richer than OpenCode's: per-message `usage` with input/output/cache token counts and a `cost` breakdown arrives on every `message_update`, and `agent_end` carries the full message array.
There is also `--mode rpc` (bidirectional JSONL over stdin/stdout, documented in `docs/rpc.md`, 38 KB) if the runner ever needs to steer mid-task.

### Reliability

No blocking findings.
Every scenario I exercised behaved correctly and terminated: success (exit 0, clean stream), connection failure in text mode (exit 1 after bounded retries), connection failure in JSON mode (exit 0, but with an unambiguous `stopReason: "error"` in the stream).
Nothing hung.

The one sharp edge is the JSON-mode exit code, documented above.
Not established: pi's behaviour under a real small model that emits malformed tool calls; I did not review its issue tracker, and the mock endpoint never exercised tool calling.

---

## Cline

**All Cline claims are from source and docs. Cline is not installed on the authoring machine, so none of this is execution-verified.**

### Install pin

Latest published version is `3.0.51` (`dist-tags` at https://registry.npmjs.org/cline gives `{"nightly":"3.0.51-nightly.1786020258","latest":"3.0.51"}`).

```bash
npm i -g cline@3.0.51
```

The npm name `cline` is correct but it is a wrapper, not the CLI code.
The repo's `apps/cli/package.json` declares `"name": "@cline/cli"` (https://raw.githubusercontent.com/cline/cline/main/apps/cli/package.json), and that is not what you install.
`apps/cli/DISTRIBUTION.md` states the CLI is published under seven names: the `cline` wrapper plus `@cline/cli-{darwin,linux,windows}-{x64,arm64}` (https://raw.githubusercontent.com/cline/cline/main/apps/cli/DISTRIBUTION.md).
The published `cline@3.0.51` has `"bin": {"cline":"bin/cline"}` and optional dependencies pinning all six platform packages (https://registry.npmjs.org/cline/3.0.51).

**NixOS risk, and this is the first thing to test.**
`bin/cline` is only a Node resolver; the real binary is a **Bun standalone executable** built with `bun build --compile --target bun-{os}-{arch}`, "a single self-contained executable that includes the Bun runtime, all JS/TS code, and native addons" (DISTRIBUTION.md URL above).
That is a prebuilt dynamically-linked ELF from npm, exactly the artifact class that fails on NixOS without `nix-ld` or `patchelf` because `/lib64/ld-linux-x86-64.so.2` does not exist.
The documented escape hatch is the resolution chain `CLINE_BIN_PATH` env var → `bin/.cline` cached hard link → walk up `node_modules`.
Corroborating fragility: https://github.com/cline/cline/issues/13006 (Bun standalone binary crashes on non-AVX2 CPUs) and https://github.com/cline/cline/issues/11945 (crashes with no error inside a container).

Not established: whether the linux-x64 binary runs unpatched on NixOS.
No issue was found either way and it could not be tested here.
Not established: the npm publish timestamp for `3.0.51` — the registry `time` object was truncated by the fetch layer, npmjs.com returned 403 and the GitHub releases API returned 403.

The published package has no `engines` field; the repo's dev `apps/cli/package.json` declares `"node": ">=22"` and the docs say "Install Node.js 20+ (22 recommended)" (https://docs.cline.bot/getting-started/installing-cline).

### Config

Paths, verbatim from `sdk/packages/shared/src/storage/paths.ts` (https://raw.githubusercontent.com/cline/cline/main/sdk/packages/shared/src/storage/paths.ts):

```ts
export function resolveClineDir(): string {
  if (CLINE_DIR) return CLINE_DIR;
  const envDir = process.env.CLINE_DIR?.trim();
  if (envDir) return envDir;
  return join(HOME_DIR, ".cline");
}
export function resolveProviderSettingsPath(): string {
  const explicitPath = process.env.CLINE_PROVIDER_SETTINGS_PATH?.trim();
  if (explicitPath) return explicitPath;
  return join(resolveClineDataDir(), "settings", "providers.json");
}
```

Provider config is `~/.cline/data/settings/providers.json`; global settings are `~/.cline/data/settings/global-settings.json`.
Path precedence is `CLINE_PROVIDER_SETTINGS_PATH` → `CLINE_DATA_DIR` → `CLINE_DIR` → `$HOME/.cline`.
Value precedence is stated as "explicit CLI flag -> persisted global setting -> built-in default" (https://raw.githubusercontent.com/cline/cline/main/apps/cli/src/utils/startup-settings.ts), though that sentence is written about mode, auto-approve and compaction specifically.

Not established: a formal documented precedence chain covering provider/model/baseUrl.

**Do not trust the `--config` / `--data-dir` flag defaults.**
`program.ts` says `--config` defaults to `~/.cline` and `--data-dir` to `~/.cline/data` (https://raw.githubusercontent.com/cline/cline/main/apps/cli/src/commands/program.ts), while the docs' `--help` dump says the opposite (https://docs.cline.bot/cli/cli-reference), and there is an open issue for exactly this contradiction (https://github.com/cline/cline/issues/10858).
Use the env vars, which are unambiguous in source.

The generic OpenAI-compatible provider id is the literal string `openai-compatible`, from `sdk/packages/llms/src/providers/ids.ts` (https://raw.githubusercontent.com/cline/cline/main/sdk/packages/llms/src/providers/ids.ts):

```ts
export enum BUILT_IN_PROVIDER {
  OPENAI_COMPATIBLE = "openai-compatible",
  OPENAI_NATIVE = "openai-native",
  OLLAMA = "ollama",
  ...
}
```

`apps/cli/src/commands/auth.ts` gates `--baseurl` to `openai-compatible` and `openai-native` only.
A separate `ollama` provider exists, but 3.0.50 "switched Ollama to the native AI SDK provider" (`apps/cli/CHANGELOG.md`), so `openai-compatible` is the more predictable target.

**Config can be written non-interactively — there is no interactive-only path.**
`auth.ts` supports a fully flag-driven quick setup and only loads the TUI wizard when no flags are supplied:

```bash
cline auth --provider openai-compatible \
           --baseurl http://localhost:11434/v1 \
           --modelid LFM2.5-2.6B \
           --apikey ollama
```

Flags are `-p/--provider`, `-k/--apikey`, `-m/--modelid`, `-b/--baseurl` (https://raw.githubusercontent.com/cline/cline/main/apps/cli/src/main.ts).

The resulting `~/.cline/data/settings/providers.json`, written mode `0o600` via staged temp file plus atomic rename (https://raw.githubusercontent.com/cline/cline/main/sdk/packages/core/src/services/storage/provider-settings-manager.ts):

```json
{
  "version": 1,
  "lastUsedProvider": "openai-compatible",
  "providers": {
    "openai-compatible": {
      "settings": {
        "provider": "openai-compatible",
        "baseUrl": "http://localhost:11434/v1",
        "model": "LFM2.5-2.6B",
        "apiKey": "ollama"
      },
      "updatedAt": "2026-08-07T00:00:00.000Z",
      "tokenSource": "manual"
    }
  }
}
```

Field names come from `ProviderSettings` in `sdk/packages/core/src/services/llms/provider-settings.ts`; readiness for a baseUrl-style provider requires a non-empty `baseUrl` and a non-empty `model` (https://raw.githubusercontent.com/cline/cline/main/apps/cli/src/utils/provider-readiness.ts).

Not established: the verbatim `StoredProviderSettingsSchema` zod definition.
The nesting above is derived from on-disk fixtures in `provider-settings-manager.test.ts`, so treat `version: 1` as fixture-derived and prefer running `cline auth` then verifying with `cline config --json`.

### Headless invocation

```bash
cline --json \
      --auto-approve true \
      -c /path/to/workspace \
      -P openai-compatible \
      -m LFM2.5-2.6B \
      -t 900 \
      --retries 6 \
      "Implement the change described in TASK.md and run the tests"
```

The prompt is a single positional argument, `.argument("[prompt]", ...)`; there is no `--task` flag.
Piped stdin also works — `main.ts` reads it when `!process.stdin.isTTY && stdinHasPipedInput() && !args.interactive`.

The flag is `--json`, not `--output-format json`.
There is no `--headless`, `--non-interactive` or `--no-interactive` flag.

**Use `--auto-approve true`, not `-y`/`--yolo`.**
`--yolo` exists but is `hideHelp()` and its description reads "Enable yolo mode where agents can use tools without approval with only a small set of tools available" — it *restricts the toolset*, which would silently change what the harness is capable of and invalidate the comparison.
Cline's own CI samples use `--auto-approve true` (https://docs.cline.bot/cli/samples/github-integration).

**Two traps that produce exit 1 before the agent ever starts**, both verbatim from `main.ts` (https://raw.githubusercontent.com/cline/cline/main/apps/cli/src/main.ts):

```ts
function promptArgLooksQuoted(arg) { return !!arg && /\s/.test(arg); }
...
if (program.args.length > 1 || !promptArgLooksQuoted(program.args[0])) {
  writePromptArgError(program.args); process.exitCode = 1; return;
}
...
if (args.outputMode === "json" && (args.interactive || !args.prompt)) {
  writeErr("JSON output mode requires a prompt argument or piped stdin (interactive mode is unsupported)");
  process.exitCode = 1; return;
}
```

A single-word prompt is rejected as "Unknown command or unquoted prompt" — deliberate, added in 3.0.31 ("Require quoted prompts for one-shot mode").
The benchmark's task prompts must always contain whitespace.

Recommended environment isolation, mirroring the project's own e2e harness (https://raw.githubusercontent.com/cline/cline/main/apps/cli/src/cli.e2e.test.ts):

```bash
export HOME=/run/bench/home
export CLINE_DIR=/run/bench/cline
export CLINE_DATA_DIR=/run/bench/cline/data
export CLINE_PROVIDER_SETTINGS_PATH=/run/bench/cline/data/settings/providers.json
export CLINE_SESSION_BACKEND_MODE=local
```

`CLINE_SESSION_BACKEND_MODE` accepts `local`, `hub`, `remote`, `auto`; the e2e suite pins `local`, which avoids the hub daemon (https://docs.cline.bot/cli/cli-reference).
`CLINE_COMMAND_PERMISSIONS` takes a JSON shell policy, e.g. `{"allow": ["npm *", "git *"], "deny": ["rm -rf *", "sudo *"]}` (same URL).
Cline also self-updates (`--update`), with an open issue about disabling it (https://github.com/cline/cline/issues/10741) — pin the version and block the update path.

### Working directory

The flag is `-c, --cwd <path>` ("Working directory"), resolved as `const cwd = args.cwd ?? process.cwd();`.

**The workspace root the agent is told about is not necessarily your `--cwd`** (https://raw.githubusercontent.com/cline/cline/main/apps/cli/src/utils/helpers.ts):

```ts
export function resolveWorkspaceRoot(cwd: string): string {
  const result = spawnSync("git", ["-C", cwd, "rev-parse", "--show-toplevel"], { encoding: "utf8" });
  if (result.status === 0) { const value = result.stdout.trim(); if (value) return value; }
  return cwd;
}
```

If a per-task workspace is a subdirectory of a larger git repo, the agent's workspace root escapes upward to the repo root.
Each task must get a directory that is either not a git repo or is its own `git init` root — a real constraint on how the benchmark lays out workspaces.

There is no path sandboxing.
`apps/cli/src/runtime/tool-policies.ts` contains only approval automation, with `SAFE_AUTO_APPROVE_TOOL_NAMES` and no filesystem-path restriction logic (https://raw.githubusercontent.com/cline/cline/main/apps/cli/src/runtime/tool-policies.ts).
`CLINE_SANDBOX` / `CLINE_SANDBOX_DATA_DIR` only redirect state directories, not filesystem access.
`--worktree` auto-creates a detached git worktree under `~/.cline/worktrees/` and runs the task there, which is a useful containment primitive but not a security boundary.

### Termination

Exit codes are set in `apps/cli/src/runtime/run-agent.ts` (https://raw.githubusercontent.com/cline/cline/main/apps/cli/src/runtime/run-agent.ts):

```ts
if (result.finishReason !== "completed") { ...; process.exitCode = 1; return; }
```

So exit 0 ⇔ `finishReason === "completed"`, exit 1 otherwise, including the timeout path and the catch-all.
Argument-validation failures also exit 1 and are indistinguishable from task failure by exit code alone, so parse `run_result.finishReason` rather than relying on `$?`.

Cline is the only one of the three with a **built-in wall-clock timeout**: `-t, --timeout <seconds>`, default `0` meaning no timeout, implemented as a `setTimeout` that sets `timedOut = true` and calls `abortAll()`, producing `run timed out after Ns` and exit 1.

There is **no max-turns cap**.
`--retries` (default 6) is only "Number of maximum consecutive mistakes (retries) before exiting", a consecutive-mistake counter, not an iteration bound.
Open issue https://github.com/cline/cline/issues/11542 documents the CLI issuing **870 provider requests in one run** until externally killed, and the still-open fix PR https://github.com/cline/cline/pull/12398 states that "on a non-interactive CLI run, the agent loop has no upper bound", pointing at `while (maxIterations === undefined || iteration < maxIterations)` in `agent-runtime.ts`.
Set `-t` **and** an external hard kill: the in-process timeout depends on the loop reaching an abort checkpoint, and several open issues describe hangs that never reach one.

Not established: any documented exit-code contract.
Neither the CLI changelog nor the issue tracker defines one.

### Output

With `--json`, output is NDJSON on stdout, one object per line, each stamped with `ts` (https://raw.githubusercontent.com/cline/cline/main/apps/cli/src/utils/output.ts):

```ts
export function emitJsonLine(stream, record) {
  const line = `${JSON.stringify({ ts: nowIso(), ...record }, jsonReplacer)}\n`;
  ...
}
```

Run-level events from `run-agent.ts` are `run_start` (`providerId`, `modelId`, `catalog`, `thinking`, `mode`, `sessionId`), `run_result` (`finishReason`, `iterations`, `usage`, `aggregateUsage`, `durationMs`, `text`, `model`) and `run_aborted` (`reason: "local_abort" | "external_abort"`).
Streaming events come through `session-events.ts` as `agent_event` (subtypes `iteration_start`, `done`, `usage`), `chunk`, `pending_prompts`, `pending_prompt_submitted`.
Errors go to stderr as `{"type":"error","message":...}`.

`run_result` is the one event a benchmark runner needs — it carries `finishReason`, `iterations`, `usage`, `durationMs`, `text` and `model` in a single object.

Warning: the docs describe a *different* JSON shape (`{"type":"say"|"ask","text","ts","say","ask","reasoning","partial"}` at https://docs.cline.bot/cli/cli-reference) that does not match what `run-agent.ts` emits.
Trust the source.

Without `--json`, output is styled text; the docs note headless is also implicitly triggered "when stdin is piped, or when output is redirected" (https://docs.cline.bot/usage/cli-overview).

### Reliability — flagged, and the worst of the three on paper

- **Unbounded agent loop on non-interactive runs.** https://github.com/cline/cline/issues/11542 (open, label `CLI`) — 870 provider requests in one run. Fix PR https://github.com/cline/cline/pull/12398 still open.
- **Silent exits with no diagnostics in 3.0.51 itself** — the version you would pin. https://github.com/cline/cline/issues/13036 (open, filed 2026-08-07): an uncaught `TypeError: O.replace is not a function` exits to the shell with no user-facing error and leaves the session non-resumable.
- **Process leak after one-shot `--json` runs.** https://github.com/cline/cline/issues/10857 (open) — `cline` processes stay resident after completion, so a batch accumulates orphans.
- **Hangs with no human to unblock them.** https://github.com/cline/cline/issues/12220 (`ask_question` spins forever), https://github.com/cline/cline/issues/12417 (background `&` commands hang indefinitely), https://github.com/cline/cline/issues/10931 (pager-style commands hang).
- **False error output on successful runs.** https://github.com/cline/cline/issues/11821 — poisons log scraping.
- **Direct precedent for this exact setup.** https://github.com/cline/cline/issues/7928 (closed): one-shot `cline -o` against a **local gpt-oss:120b** hung waiting for a human plan→act toggle. https://github.com/cline/cline/issues/7771 (closed): `cline -o` did not exit after "Mistake Limit Reached".

Local OpenAI-compatible endpoint issues, all open:

- https://github.com/cline/cline/issues/12132 (CLI 3.0.38) is the highest-signal one: backends that omit the `content` key on empty deltas break **every** turn, reproduced "across CLI, `--tui`, and non-interactive one-shot". Fix PR https://github.com/cline/cline/pull/12134 unmerged. Ollama's `/v1` shim is usually well-formed, but a 2.6B model is exactly the regime where malformed deltas surface.
- https://github.com/cline/cline/issues/12520 (CLI 3.0.46): `openai-compatible` ignores the configured `contextWindow`, so auto-compaction fires at 115.2k (`DEFAULT_CONTEXT_WINDOW` 128000 × 0.9). For a small-context LFM2.5-2.6B, Cline will believe it has vastly more room than it does.
- https://github.com/cline/cline/issues/11263 and https://github.com/cline/cline/issues/10843: small local models without solid native tool-calling fall into infinite JSON tool loops or HTTP 400/500.

---

## Comparison

| | OpenCode | pi | Cline |
|---|---|---|---|
| Pin | `pkgs.opencode` 1.18.13 (nixpkgs master) / `opencode-ai@1.18.15` | `@earendil-works/pi-coding-agent@0.80.10` | `cline@3.0.51` |
| Verified by execution | Yes (1.17.9) | Yes (0.80.10) | **No** |
| NixOS packaging | nixpkgs derivation exists | not checked; `PI_PACKAGE_DIR` hook exists | prebuilt Bun ELF, **untested on NixOS** |
| Config file | `opencode.json` (8-level precedence) | `~/.pi/agent/models.json` + `settings.json` | `~/.cline/data/settings/providers.json` |
| Config relocatable by env | `OPENCODE_CONFIG_CONTENT` | `PI_CODING_AGENT_DIR` | `CLINE_DIR` / `CLINE_DATA_DIR` |
| Provider id for OpenAI-compatible | your own key + `npm: @ai-sdk/openai-compatible` | `api: "openai-completions"` | `openai-compatible` |
| Non-interactive command | `opencode run --pure --format json` | `pi --mode json` | `cline --json` |
| Approval bypass | `--auto` (1.18.x) / `--dangerously-skip-permissions` (1.17.x) | none needed — no approval gate exists | `--auto-approve true` (**not** `--yolo`) |
| Prompt passing | positional or stdin (concatenated if both) | positional, `@file`, or stdin | positional (must contain whitespace) or stdin |
| Working directory | `--dir` (`chdir`) | process cwd only | `-c/--cwd`, but workspace root escapes to git toplevel |
| Path confinement | `permission` block, in-process only | none; `--tools` allowlist only | none |
| Exit codes | 0/1 only | 0/1 in text mode; **always 0 in JSON mode** | 0 ⇔ `finishReason === "completed"` |
| Built-in timeout | none (provider `timeout`/`chunkTimeout` only) | `retry.provider.timeoutMs`, `httpIdleTimeoutMs`, bounded 3-retry backoff | `-t <seconds>` |
| External timeout required | **Yes — verified hang** | Yes (prudence; no hang observed) | **Yes — unbounded loop issue** |
| Machine-readable output | JSONL, 6 event types | JSONL, 15 event types + per-message usage | NDJSON, `run_result` is the key event |
| Headless reliability | **Poor** — large open hang cluster, reproduced here | **Good** — everything terminated correctly | **Unknown/poor on paper** — unbounded loop, silent exits in the pinned version |

## Which to drive first for the end-to-end spike

**pi.**

It is the only harness where every path I exercised terminated correctly, and it needed no approval-bypass flag because it has no approval gate to bypass.
Its config is a single small JSON file in a directory that `PI_CODING_AGENT_DIR` relocates wholesale, which makes per-run isolation trivial.
Its JSON stream is the richest of the three — per-message token usage and an explicit `stopReason` — so the runner's outcome classifier can be written against it first and then adapted.
The one gotcha is known and cheap to handle: in `--mode json` the exit code is always 0, so classify from `stopReason` and `agent_end.willRetry`.

Two things to settle before pi becomes the reference: whether it is in nixpkgs (not checked), and whether it has any internal turn cap (not established).

**Do not start with OpenCode.**
It hung for over nine minutes with zero output against an unreachable endpoint and had to be killed, which is the exact failure the runner must survive, and it matches a well-populated cluster of open hang issues.
It is worth benchmarking, but only behind `timeout --kill-after`, with `--pure`, with every permission pinned to `allow`/`deny`, and running strictly serially.

**Cline is the substitution risk.**
Nothing in the research says headless Cline is unsupported — the flags are real, config is writable non-interactively, and there is a built-in `-t` timeout, which is more than the others offer.
But three things are unresolved and any one of them could force a substitution:

1. The binary is a prebuilt Bun standalone ELF and **may not execute at all on NixOS** without `nix-ld`. Test `cline --version` on the experiment machine before anything else — this is a five-minute check that gates everything.
2. The agent loop has no upper bound on non-interactive runs (#11542, fix PR unmerged), so a small model that loops will burn the machine until an external kill.
3. The pinned version 3.0.51 has an open silent-exit bug (#13036) filed the same day as this research.

If step 1 fails, Cline is out unless someone is willing to package it in Nix, and the wayfinder should plan a substitute.
