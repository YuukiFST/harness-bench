# 04 — Measuring tokens, steps and wall time across harnesses

Research ticket #4.
Question: for OpenCode, PI and Cline, how does a benchmark runner obtain per-run token usage (input/output), number of agent steps, and wall time — reliably and *identically* across all three?

Target endpoint: Ollama at `http://localhost:11434/v1` (OpenAI-compatible), model LFM2.5-2.6B (Q4_K_M), on NixOS.
Hard constraint: zero monetary cost.

Retrieval date for every claim below: **2026-08-07**.

Commits read:
- Ollama `github.com/ollama/ollama` @ `144893850fa778c8c81ff931f26614d62e6689c1`, committed 2026-08-05.
- Cline `github.com/cline/cline` @ `7348ba18478d34f3369116dba64b0659d912ac4d`, committed 2026-08-06.
- OpenCode v1.17.9, from the local install plus the repo at tag `v1.17.9`.

Where a fact could not be established against the source that owns it, it is marked **UNVERIFIED** rather than filled in by inference.

---

## Working hypothesis under test

The hypothesis to confirm or refute was: *the proxy is the only route that yields genuinely comparable numbers, because each harness accounts for tokens differently.*

**Verdict: confirmed in substance, but for a sharper reason than the one proposed.**
The problem is not mainly that harnesses exclude system prompts or retries from their arithmetic.
It is that each harness performs a *different number and kind of LLM calls* for the same task, and each one hides a different subset of those calls from its own reporting.
Cline's agentic compaction issues a summarizer call whose tokens are discarded before they reach any usage surface.
OpenCode issues a title-generation call on the first step of every session that bypasses its processor entirely and is recorded nowhere.
The two harnesses even leak in opposite directions: OpenCode counts compaction tokens where Cline does not, and Cline preserves retry tokens where OpenCode appears to lose them.
PI's reporting surface is entirely unverified.
A proxy counts every HTTP request that actually reached the model, which is the only definition all three harnesses cannot argue with.

---

## Section 1 — OpenCode

Status: **established**, against v1.17.9 from the local install plus the repo at that tag.

### 1.1 Headless invocation

The non-interactive entry point is `opencode run` with `--format json`.

The working invocation is:

```
opencode run --format json --dangerously-skip-permissions -m <provider>/<model> -s <session-id> "<task>"
```

The flag definitions are at `packages/opencode/src/cli/cmd/run.ts:170-174`.
Note that `-m` takes a combined `provider/model` identifier, not a bare model name.

In v1.17.9 the permission bypass flag is `--dangerously-skip-permissions`, confirmed against the local `--help` output and against the repo's own help snapshot test at `test/cli/help/__snapshots__/help-snapshots.test.ts.snap:106-115`.
The live documentation at https://opencode.ai/docs/cli/ currently documents `--auto` instead, because that page tracks the `dev` branch rather than the released tag.
Do not trust the published CLI page for this version.

Also present in v1.17.9 but undocumented: `--replay` / `--no-replay`, `--replay-limit`, `-i` / `--interactive`, `--demo`.

`opencode session list --format json` exists and is documented at `packages/web/src/content/docs/cli.mdx:427-432`; it is a cleaner way to recover a session id than scraping stdout.

### 1.2 The `--format json` event stream

The stream is newline-delimited JSON events, written by the `emit` writer at `packages/opencode/src/cli/cmd/run.ts:622`.

Each record has the shape `{type, timestamp, sessionID, ...data}`, and there are exactly six `type` values: `tool_use`, `step_start`, `step_finish`, `text`, `reasoning` and `error`.

Token counts arrive on `step_finish`, at the path `.part.tokens.{input, output, reasoning, cache.read, cache.write, total}`, defined at `packages/core/src/v1/session.ts:234-251`.

The delimiter is `os.EOL`, imported at `run.ts:21`, so on Windows the separator is `\r\n` and a naive `split("\n")` parser leaves a trailing `\r` on every line.
On the NixOS experiment machine this is moot, but it matters for any development done on the Windows box.

`reasoning` *text* events are suppressed unless `--thinking` is passed, which defaults to `false` in non-interactive mode (`run.ts:251`, gate at `run.ts:696-697`).
Reasoning *tokens* still arrive in `step_finish` regardless, so token accounting does not require `--thinking`.

**There is no terminal or summary event.** The loop simply `break`s when `session.status` becomes `idle`, at `run.ts:723-729`.
A runner must therefore aggregate `step_finish` events itself, or query the database or HTTP API after the process exits.

The `--format json` event schema is nowhere documented; the only published text is a one-line "raw JSON events".
Treat it as an unstable interface and pin the OpenCode version in the benchmark.

### 1.3 On-disk storage

OpenCode persists to SQLite, not to a tree of JSON files.

The storage root on Windows is `%USERPROFILE%\.local\share\opencode`, stated verbatim in the project's own troubleshooting docs at `packages/web/src/content/docs/troubleshooting.mdx:25-28`.
This is the same `.local/share` layout on every platform, because `xdg-basedir` is pinned at `5.1.0` (`packages/core/package.json:122`), is not in the root `patchedDependencies`, and contains no Windows branch.
On NixOS the path is therefore `~/.local/share/opencode`.

The database file is `opencode.db`, and the `OPENCODE_DB` environment variable overrides its location.

**WAL mode is on**, configured at `packages/core/src/database/database.ts:27-32` alongside `synchronous=NORMAL` and `busy_timeout=5000`.
Confirmed on disk by the presence of `opencode.db-wal` and `opencode.db-shm` next to `opencode.db`.
Copying only `opencode.db` after a run will silently lose the most recent writes.
Copy all three files, or read through `opencode db` or the HTTP API, or checkpoint first.

The database stores paths posix-normalized, at `packages/core/src/database/path.ts:5-25`, which returns the input unchanged on non-Windows and replaces `\` with `/` on Windows.
A runner filtering sessions by directory via direct SQL must therefore use forward slashes, while the HTTP API and `opencode export` hand back backslashes.

The `session` table carries `tokens_*` rollup columns, so per-run totals can be read with a single query rather than by aggregating the event stream.

`opencode export` emits a single pretty-printed JSON blob, not JSONL, at `packages/opencode/src/cli/cmd/export.ts:283-291`.

### 1.4 HTTP API

`opencode serve` exposes a session API defined in `packages/opencode/src/server/routes/instance/httpapi/groups/session.ts`, with `SessionPaths` at lines 78-105 (`const root = "/session"` at line 29) and endpoint registrations at lines 111-444.

The route that carries assistant token counts is `GET /session/:sessionID/message`, registered at line 179, returning `Schema.Array(SessionV1.WithParts)`.
`GET /session/:sessionID/message/:messageID` is at line 191.
`POST /session/:sessionID/message` is at line 316 and `POST /session/:sessionID/prompt_async` at line 329 (returns 204).

Pagination on the messages route is defined at `groups/session.ts:43-47` with the handler at `handlers/session.ts:104-143`: `?limit=` and `?before=`, where `before` without `limit` returns 400, and omitting `limit` returns the full history.
Paginated responses carry `Link: <…>; rel="next"` and `X-Next-Cursor` headers.

`/doc` is the only spec endpoint, built lazily via `OpenApi.fromApi(PublicApi)` and cached, at `packages/opencode/src/server/routes/instance/httpapi/server.ts:174-183`.
There is no `/openapi` or `/spec`.
The SSE event stream is `GET /event`, at `groups/event.ts:7-16`.

### 1.5 Step semantics

**One assistant row equals one `step_finish` equals one LLM round trip.**
A turn containing five tool calls is **one** step carrying five `tool` parts, not five steps.
This was verified empirically across an entire 16.6 MB production database, where the maximum number of `step-start` parts per message is 1.

This is the cleanest step definition of the three harnesses, and it happens to align exactly with the proxy's definition in Section 6.3, which makes OpenCode the natural calibration arm for validating the proxy.

### 1.6 Side-calls — three behaviours, two of them leaks

**Compaction tokens ARE counted.**
Verified against real database rows and cross-checked against the `tokens_*` rollup.
This is the opposite of Cline's behaviour and worth noting: the same category of side-call is accounted by one harness and discarded by another.

**Retry tokens are LOST.**
Source-derived from `packages/opencode/src/session/processor.ts:717-718` and `:976-1024`, and explicitly **not reproduced empirically**, so treat this as a strong indication rather than a settled fact.
A second agent independently re-fetched `processor.ts:716-718` and confirmed it, and additionally established that `retry.ts:26-29` with `policy()` at `:176-198` imposes **no upper bound on attempts**.
The two findings compound: an unbounded retry loop whose tokens are never recorded means OpenCode's under-reporting has no ceiling.
The proxy is the only place this becomes visible, as identical `messages`-array hashes in a short window (Section 6.3).

**Title-generation tokens are NEVER recorded. This is a real, silent leak.**
On the first step of every new session, `packages/opencode/src/session/prompt.ts:1186-1192` forks a `title(...)` call.
That function, at `prompt.ts:177-237`, calls `llm.stream(...)` **directly, bypassing the processor**: it consumes only `textDelta` events and terminates at `sessions.setTitle(...)`.
It never calls `sessions.updateMessage`, so it produces no assistant message row, no `step_finish` part, and **no tokens anywhere in the database or the JSON event stream**.

Worse for this benchmark, it resolves its model via `getSmallModel(providerID)` with a fallback to the same model, so against a custom Ollama provider it burns the benchmark model itself.

Mitigation: pass `--title <x>`, since the call is guarded by `if (!Session.isDefaultTitle(...)) return`.
Do this on every run, or every OpenCode run silently under-reports by one full LLM call.

**UNVERIFIED: whether a parent session's token rollup includes child-session tokens.**
The mitigation is to sum across `WHERE id = ? OR parent_id = ?` and confirm empirically before trusting single-session numbers on any task that spawns subagents.

### 1.7 Provider configuration against Ollama

OpenCode **force-enables** `includeUsage` at `packages/opencode/src/provider/provider.ts:1643-1645`, so `stream_options: {include_usage: true}` is sent on every streaming request.
Confirmed empirically by existing rows with `providerID: "ollama"` carrying real token counts.

Per Section 5.3 this is exactly what Ollama requires, so OpenCode's native token counts against a local Ollama endpoint are real rather than zero.

### 1.8 Reliability blocker

A parallel agent working ticket #6 reproduced **OpenCode headless hangs**: zero bytes of output, no exit, killed after roughly nine minutes.
It also found open bugs that turn failed runs into **exit 0 with plausible-looking transcripts**.

This is a correctness problem for the benchmark before it is a measurement problem.
A run that hangs produces no numbers at all, and a run that fails while reporting success produces numbers that are worse than missing.
Outcome classification for OpenCode must not rely on exit codes, and every run needs an external timeout.

### 1.9 Repository location

`github.com/sst/opencode` now redirects to `github.com/anomalyco/opencode`.
Raw URLs at tag `v1.17.9` still resolve.

### 1.10 Second-pass verification — the v2 `/api` surface and a `--title` caveat

A second agent re-fetched every load-bearing file at tag `v1.17.9` (commit `5c23e88419c4743b9be42cea132f2fb1e6cb63ff`) rather than trusting the first pass, and confirmed §1.2 through §1.7 as written, including the `includeUsage` force-enable at `provider.ts:1643-1645` and the six `type` values.
It also closed the "exact `step_finish.part.tokens` field list" gap: the schema is `StepFinishPart` at `packages/core/src/v1/session.ts:234-251`, with `reason`, optional `snapshot`, `cost`, and `tokens` = `{ total?, input, output, reasoning, cache: { read, write } }`; the SDK mirror is `packages/sdk/js/src/v2/gen/types.gen.ts:553-571`.
Note that `total` is **optional** while the rest are required, so a runner must sum rather than read `total`.

**An undocumented v2 `/api` surface exists, and it is the better runner contract.**
It lives in a package the first pass did not cover, `packages/server/src/groups/*.ts`, wired in via `import { Api } from "@opencode-ai/server/api"` at `httpapi/api.ts:24` and `.addHttpApi(Api)` at `:73`.
Routes at the tag: `GET`/`POST /api/session` (`:92`, `:112`), `GET /api/session/:sessionID` (`:129`), `POST /api/session/:sessionID/prompt` (`:144`), `/compact` (`:165`), `GET /api/session/:sessionID/context` (`:195`), `GET /api/session/:sessionID/message` (`message.ts:27`), and `GET /api/event` (`event.ts:18`).

The one that matters is **`POST /api/session/:sessionID/wait` → 204, "Wait for a session agent loop to become idle"** (`:180-192`).
Prompt-then-wait is a *declared* contract that appears in `/doc`, which beats §1.2's remedy of aggregating an undocumented JSONL stream that has no terminal event.
For the runner this is the recommended control channel; the JSONL stream stays useful as a per-step record.

**Shape trap: v2 `/api` messages are not the v1 shape, and mixing them will silently produce zeros.**
The v2 route returns `SessionMessage.Message` from `packages/core/src/session/message.ts:142-168`, where `tokens` is `Schema.optional` — the whole object can be absent — there is **no `tokens.total`**, `cost` is optional, and parts are inlined as `content: AssistantContent[]` with no step-finish part at all.
The `.part.tokens.total` path from §1.2 is **v1-only**.
Pick one surface per concern and do not cross them: v2 `/api` for lifecycle control, v1 `/session` or the JSONL stream for token accounting.

**The `--title` mitigation in §1.6 has a third gate.**
`prompt.ts:200-201` reads `const ag = yield* agents.get("title"); if (!ag) return`, so the title call is also skipped when no `title` agent is configured.
Consequence for verification: observing that no title side-call happened does **not** prove `--title` did its job.
Confirm the mitigation at the proxy — count `POST /v1/chat/completions` requests with a tiny `messages` array and no `tools` field — rather than by absence in the transcript.

**UNVERIFIED: whether `--print-logs` writes only to stderr.** The logger sink was not traced. A runner that captures stdout for JSONL should not assume the log stream stays out of it; verify on the first run.

---

## Section 2 — PI

Status: **not established.** The agent assigned to PI never reported, and the deadline for this ticket arrived first.

What is known with certainty:

The CLI shim is installed at `C:\Users\tisao\AppData\Local\pi-node\current\pi`.
A user data directory exists at `C:\Users\tisao\.pi\`, containing at least `agent/` and `skills/`.

One fact is available second-hand, from the parallel agent that resolved ticket #6, and is recorded here for cross-checking rather than as independently verified work:

PI's `--mode json` **returns exit code 0 even on total failure**, because `dist/modes/print-mode.js` guards its `stopReason` check with `if (mode === "text")`.
Outcome classification for PI therefore cannot use exit codes, exactly as for OpenCode.

Everything else is unverified and must be established before PI can be included as an arm:

- **UNVERIFIED: the canonical package name, version, and upstream repository URL.**
- **UNVERIFIED: whether `--mode json` emits per-run token usage at all**, and if so under which field names.
- **UNVERIFIED: whether PI writes session transcripts to disk**, in what format, and whether records carry token counts and timestamps.
- **UNVERIFIED: PI's agent loop and step semantics**, including whether any max-iterations setting exists.
- **UNVERIFIED: how PI is pointed at a custom OpenAI-compatible base URL**, and whether it sets `stream_options: {include_usage: true}`.
- **UNVERIFIED: whether PI emits any telemetry** that could be scraped locally.

Given Section 5.3, the `include_usage` question is decisive: if PI streams without setting that flag, Ollama returns no usage to it whatsoever, and PI's own numbers would be structurally unavailable rather than merely inconsistent.
This must be checked at the wire before any effort is spent on PI's native reporting.

---

## Section 3 — Cline

Status: **fully established**, against `github.com/cline/cline` @ `7348ba18` (2026-08-06).

### 3.1 The repository layout has changed

`apps/cli` does exist, and is `@cline/cli` version `3.0.51` (`apps/cli/package.json:1-4`).

However, the older world of `src/api/providers/`, `src/core/storage/disk.ts`, `api_conversation_history.json`, `ui_messages.json` and `task_metadata.json` is **gone from the CLI path**.
Those names survive only under `apps/vscode` — in `apps/vscode/src/core/storage/disk.ts:19-35` and in `apps/vscode/src/sdk/legacy-state-reader.ts:57-74`, a reader for pre-migration tasks.

`api_req_started` likewise exists nowhere in the CLI or SDK.
It survives only in `apps/vscode/src/sdk/message-translator.ts` (for example at `:1768-1773`, `:1835`, `:2215`), which synthesizes legacy `ClineMessage` records from new SDK agent events for the webview.

**A CLI-driven benchmark must not target any of those files.**
Guidance written against Cline's VS Code extension does not transfer.

There is also **no gRPC or protobuf hop for the CLI**.
The CLI imports `@cline/core` and `@cline/shared` directly; the protos under `apps/vscode/proto/` are the extension-to-webview channel only.
The real engine lives in `sdk/packages/{core,agents,llms,shared,sdk,ui}`.

### 3.2 Headless invocation

Flags are defined at `apps/cli/src/commands/program.ts:23-104`.

Headless mode is decided at `apps/cli/src/main.ts:985-990`, where the run is headless if yolo mode, zen mode, `--json`, or a non-TTY stdin without `--interactive`.

`--json` requires a prompt argument or piped stdin and rejects interactive use, at `main.ts:807-813`.

Tool auto-approval already defaults to `true` at `program.ts:141`.

The recommended invocation is:

```
cline --json -P <provider> -m <model> -c <workdir> -t <timeout-seconds> "<task prompt>"
```

Two configuration decisions matter for run isolation.

`-y` / `--yolo` sets `forceLocalBackend: true` at `apps/cli/src/runtime/run-agent.ts:173`, avoiding the background hub daemon, but it also disables spawn-agent and agent-teams at `main.ts:1084-1085`, which changes the agent's capabilities and would bias the comparison.
`--data-dir <path>` also forces the local backend, via `sandbox: !!opts.dataDir` at `program.ts:137`, without touching the toolset.
**Prefer `--data-dir` over `-y`.**

Plain `--json` otherwise uses backend mode `auto`, meaning a persistent daemon shared across runs, which is exactly what a benchmark must avoid.

Note that `--retries <n>` is **not** an HTTP retry count.
It maps to `execution.maxConsecutiveMistakes` at `main.ts:1067`.
Its real default is **3**, not the 6 claimed by both the published docs and `program.ts:57`; the source at `main.ts:1067` is authoritative.

### 3.3 Machine-readable output — the primary metrics channel

Every JSON line is written by `emitJsonLine` at `apps/cli/src/utils/output.ts:129-139`, as NDJSON, with an injected `ts` that is an **ISO-8601 string** (`nowIso()`, `apps/cli/src/utils/helpers.ts:35-37`).

The record types are `run_start` (only with `--verbose`, `run-agent.ts:52-60`), `agent_event` (`apps/cli/src/utils/events.ts:97-101`), `team_event` (`events.ts:229-231`), `run_result` (`run-agent.ts:362-373`), `run_aborted` and `run_abort_requested` (`run-agent.ts:380-384`, `:73`), `team_restored` (`run-agent.ts:82`), `error` on stderr (`output.ts:189`), and hook payloads (`apps/cli/src/utils/hooks.ts:29`).

The single record a runner needs is `run_result`, emitted at `apps/cli/src/runtime/run-agent.ts:350-373`.
It carries `finishReason`, `iterations`, `usage`, optionally `aggregateUsage`, `durationMs`, `text` and `model`.

`usage` and `aggregateUsage` are of type `SessionAccumulatedUsage`, whose five fields are **all non-optional**, defined at `sdk/packages/core/src/runtime/host/runtime-host.ts:260-266`: `inputTokens`, `outputTokens`, `cacheReadTokens`, `cacheWriteTokens`, `totalCost`.
`usage` is the root agent; `aggregateUsage` includes teammates and subagents, per `sdk/packages/core/src/ClineCore.ts:341-351`.

Prefer `run_result.usage` over `AgentResult.usage`: the latter is `LegacyAgentUsage` (`sdk/packages/shared/src/agents/types.ts:567-578`), where the cache and cost fields are optional.

`durationMs` is `endedAt - startedAt` of the agent run, at `sdk/packages/core/src/runtime/orchestration/session-runtime-orchestrator.ts:1333-1340`.
**This is agent run time, not process wall time**, and must not be used as the benchmark's wall-time figure.

Per-step events arrive as `{"type":"agent_event","event":{…}}`, with the union defined at `sdk/packages/shared/src/agents/types.ts:63-72`.
The ones that matter are `iteration_start` (`:134-138`), `iteration_end` with `hadToolCalls` and `toolCallCount` (`:140-148`), and `usage` (`:150-169`), which carries both the per-turn delta and running totals, built at `sdk/packages/core/src/runtime/orchestration/runtime-event-adapter.ts:334-370`.

A parsing trap: zero-valued deltas and totals are emitted as `undefined`, so **absent means zero, not unreported**.

There is also a `notice` event whose `reason` includes `auto_compaction`, `manual_compaction` and `mistake_limit` (`types.ts:171-186`), which Section 3.6 relies on.

**Documentation drift:** both https://docs.cline.bot/usage/cli-overview and https://docs.cline.bot/cli/cli-reference document the `--json` schema as `{"type":"say","text":"…","ts":1760501486669,"say":"text"}` with a numeric millisecond `ts`.
That does not match the source at HEAD, which emits `agent_event` and `run_result` with an ISO-string `ts`.
Pin the installed version and verify the first run's actual NDJSON before trusting any parser.

### 3.4 On-disk artifacts

Path resolution lives in `sdk/packages/shared/src/storage/paths.ts`: `resolveClineDir()` at `:130-139` returns `$CLINE_DIR` or `<home>/.cline`; `resolveClineDataDir()` at `:158-164` returns `$CLINE_DATA_DIR` or `<clineDir>/data`; `resolveSessionDataDir()` at `:166-172` returns `$CLINE_SESSION_DATA_DIR` or `<dataDir>/sessions`; `resolveDbDataDir()` at `:219-225` returns `$CLINE_DB_DATA_DIR` or `<dataDir>/db`.

Home resolution at `:63-82` is `$HOME`, then `$USERPROFILE`, then `$HOMEDRIVE$HOMEPATH`, then `os.homedir()`.
The layout is identical on all three operating systems, with no `AppData` or `Library` split; on NixOS it is `~/.cline/data/…`.

Per-session files are created at `sdk/packages/core/src/services/session-artifacts.ts:63-94`:

```
<sessionsDir>/<sessionId>/<sessionId>.messages.json      # transcript   (:75-80)
<sessionsDir>/<sessionId>/<sessionId>.json               # manifest     (:89-94)
<sessionsDir>/<sessionId>/<sessionId>.compaction.json    # compaction   (:82-87)
<sessionsDir>/<sessionId>/<agentId>.messages.json        # subagents    (:132-144)
```

**Each assistant message in `<sessionId>.messages.json` carries its own per-turn `metrics`**, stamped at `sdk/packages/agents/src/agent-runtime.ts:1231-1234` and persisted via `withLatestAssistantTurnMetadata` at `sdk/packages/core/src/services/session-data.ts:122-170`.
The fields are `inputTokens`, `outputTokens`, `cacheReadTokens`, `cacheWriteTokens` and `cost` (`sdk/packages/shared/src/agent.ts:79-113`).

Two live contract tests lock this behaviour: `apps/cli/src/tests/headless/messages-contract.live.test.ts:97-119` asserts all five fields are numbers plus `modelInfo.{id,provider}`, and `apps/cli/src/tests/headless/per-turn-metrics.live.test.ts:116-141` asserts turn 1 is 1000/25 and turn 2 is 1500/40 — that is, **per-turn and not cumulative**.
This file is the authoritative per-step token record.

There is also SQLite at `<dataDir>/db/sessions.db` (`sdk/packages/core/src/services/storage/sqlite-session-store.ts:44-46`).
The `sessions` table columns at `:86-91` carry no token columns; usage lives inside `metadata_json`, whose schema is at `sdk/packages/core/src/types/sessions.ts:4-45` and includes `usage` and `aggregateUsage` of type `SessionUsageMetadata` (`inputTokens`, `outputTokens`, `cacheReadTokens`, `cacheWriteTokens`, `totalCost`).
It is written after every turn at `sdk/packages/core/src/runtime/host/local-runtime-host.ts:1742-1748`.

Note that the published docs describe `~/.cline/data/sessions/` as the SQLite database, which is wrong: the database is at `~/.cline/data/db/sessions.db` and `sessions/` holds the JSON artifacts.

### 3.5 Step semantics

The agent loop is at `sdk/packages/agents/src/agent-runtime.ts:686-798`.
`this.state.iteration += 1` happens once per model turn at `:692`, and each turn is one `generateAssistantMessageWithOverflowRecovery()` call at `:700`.

Three equivalent ways to count LLM round trips, in decreasing order of reliability: `run_result.iterations`; counting `agent_event` records with `event.type === "iteration_start"`; counting assistant messages that carry a `metrics` object in `<sessionId>.messages.json`.

Tool calls are separately countable from `iteration_end.toolCallCount`, or from `content_start` / `content_end` events with `contentType: "tool"`, which also give per-tool `durationMs`.

`maxIterations` exists in `AgentConfig` and is honoured at `agent-runtime.ts:686-688` and `:800-802`, but **the CLI never sets it**; it appears only in the scheduled-agent wizard at `apps/cli/src/wizards/schedule/index.ts:157-224`.
A headless `cline` run is therefore unbounded in iterations, and must be bounded with `-t` / `--timeout` (`run-agent.ts:313-324`).

### 3.6 Accounting caveats — where Cline's own numbers diverge from reality

**Empty-response retries: tokens counted, step not counted.**
`sdk/packages/llms/src/providers/middleware/retry-empty-response.ts` is applied to every AI SDK vendor (`ai-sdk.ts:1248-1263`, `:1323-1327`), defaulting to 3 total attempts at `:67`.
Its own header comment at `:30-33` is explicit that empty attempts still bill real tokens and that their usage is aggregated into the final finish part, so a turn that took three requests reports three requests' worth of usage.
The middleware is called out at `:5-8` as targeting **Ollama especially**, which makes this directly relevant here.
Consequence: token totals are right, but **HTTP request count exceeds iteration count**, and no event exposes the retry count.

**Context-overflow recovery: one extra model call, tokens counted, step not counted.**
At `agent-runtime.ts:891-932`, a provider context-window rejection forces a compaction and re-calls `generateAssistantMessage({overflowRecovery:true})` within the same iteration, at most once per run (`overflowRecoveryAttempted`, `:664`, `:941`).

**Agentic compaction: an LLM call whose tokens are invisible. This is a real gap.**
The CLI's default compaction mode is `agentic`, that is, an LLM summarizer (`apps/cli/src/utils/compaction-mode.ts:5-8`, `:16-20`).
`generateSummary` at `sdk/packages/core/src/extensions/context/agentic-compaction.ts:62-87` builds its own handler via `createHandlerAsync` and consumes only `chunk.type === "text"` and `"done"` — it **discards the `usage` chunk**, and there is no usage or metrics reference anywhere in that file.

Every auto-compaction therefore fires an LLM request whose tokens are invisible to `run_result.usage`, to the `usage` events, to `messages.json` metrics, and to `sessions.metadata_json`.
For an honest token benchmark, run with `--compaction basic` (truncation, no summarizer model, `basic-compaction.ts:444`) or `--compaction off`.
If the default is kept, compactions are at least *detectable* as `notice` events with `reason: "auto_compaction"`, so contaminated runs can be rejected — but the missing tokens can never be recovered.

**This single finding is the clearest refutation of relying on native reporting.**

### 3.7 Ollama plumbing — it works, but pick the right route

Two distinct routes exist and they are not interchangeable.

Route A, `-P openai-compatible` against `http://localhost:11434/v1`, is configured at `sdk/packages/llms/src/providers/vendors/openai-compatible.ts:154-162`, which passes **`includeUsage: true`** at line 160 — the `@ai-sdk/openai-compatible` flag that emits `stream_options: {include_usage: true}`.

Route B, `-P ollama`, is the default and uses the **native** API, not `/v1`.
Per `builtins.ts:911-927` the default base URL is `http://localhost:11434` and models are discovered from `http://localhost:11434/api/tags`.
`normalizeOllamaBaseUrl` at `vendors/ollama.ts:39-47` *strips* a trailing `/v1` or `/api` and appends `/api`, deliberately, because `/v1` ignores `options.num_ctx` and would leave every model at the server's default context.
Passing `http://localhost:11434/v1` under `-P ollama` therefore silently becomes `http://localhost:11434/api`.
No API key is needed for a local server (`:126-129`).

Usage flows correctly on the native route: `ollama-ai-provider-v2@4.0.1`, pinned at `sdk/packages/llms/package.json:73` with a local patch, maps `prompt_eval_count` to `usage.inputTokens.total` and `eval_count` to `usage.outputTokens.total`, with `cacheRead` and `cacheWrite` explicitly `undefined`.
Cline's `normalizeUsage` at `sdk/packages/llms/src/providers/ai-sdk.ts:714-855` reads exactly that nested shape at `:774` and `:778`, and falls back to `prompt_tokens` / `completion_tokens` and `prompt_tokens_details.cached_tokens` for the OpenAI-compatible route.
The usage chunk is yielded at `ai-sdk.ts:1141-1146`.

Expected values against local Ollama: `inputTokens` and `outputTokens` real; `cacheReadTokens` and `cacheWriteTokens` **always 0**, because the provider never reports them; `totalCost` 0 or absent, because locally-discovered Ollama models carry no pricing (`normalizeUsage:846-852`).
A zero cost is a signal, not a bug.

A configuration gotcha: `cline auth` quick-setup requires `--apikey` and `--modelid` (`apps/cli/src/commands/auth.ts:144-149`) and **rejects `--baseurl` for any provider other than `openai-compatible` or `openai-native`** (`:150-156`).
So either use `-P openai-compatible` with `--baseurl`, or write `<dataDir>/settings/providers.json` directly, or use `-P ollama` with the builtin default base URL.

### 3.8 Auth and telemetry — no blockers

There is no account gate for BYO-local operation.
OAuth is never attempted in headless mode, per the guard at `main.ts:992-1003`.
`ollama` is not an OAuth provider and needs no key locally.

Telemetry is opted out by setting `telemetryOptOut: true` in `<dataDir>/settings/global-settings.json` (`sdk/packages/core/src/services/global-settings.ts:49`, consumed at `.../telemetry/OpenTelemetryProvider.ts:384-388`).
**`CLINE_TELEMETRY_DISABLED` is not read by any source file** — it appears only in test helpers at `apps/cli/src/tests/helpers/env.ts:93` — so do not rely on it.

Set `CLINE_NO_AUTO_UPDATE=1` and `NO_UPDATE_NOTIFIER=1` so the CLI does not self-update mid-benchmark.

For per-run isolation, mirror Cline's own e2e harness at `apps/cli/src/tests/helpers/env.ts:87-131` by pointing `CLINE_DIR`, `CLINE_DATA_DIR`, `CLINE_DB_DATA_DIR`, `CLINE_SESSION_DATA_DIR`, `CLINE_GLOBAL_SETTINGS_PATH`, `CLINE_PROVIDER_SETTINGS_PATH`, `CLINE_TEAM_DATA_DIR`, `CLINE_HUB_PORT` and `CLINE_HUB_DISCOVERY_PATH` at a fresh temporary directory.

### 3.9 Cline gaps

- **UNVERIFIED: whether `--json` with the hub backend (no `-y`, no `--data-dir`) reliably yields `run_result`.** Both hub and local hosts implement `getAccumulatedUsage`, but this was not executed. Forcing the local backend sidesteps the question.
- **UNVERIFIED: whether the docs' `{"type":"say",…}` JSON format exists on any published npm version.**
- **UNVERIFIED: the exact field list of the session manifest `<sessionId>.json`.** Not needed, since `run_result`, `messages.json` and `sessions.db` already cover every requested metric.

---

## Section 4 — Route A: native reporting

**Verdict: necessary, useful, and insufficient as the comparison basis. Collect it, but do not compare on it.**

Native reporting is in wildly different states across the three arms.

Cline is excellent: a single `run_result` NDJSON record with five non-optional token fields, an explicit `iterations` count, per-turn `metrics` on every assistant message, and a SQLite mirror.
If the benchmark had only one arm, this would be enough.

OpenCode is good on step semantics — one `step_finish` is exactly one LLM round trip, verified empirically across a whole production database — and its token paths are well defined, but there is **no run-total event at all**, the event schema is undocumented and unstable, and the database needs WAL-aware copying.

PI is entirely unverified and may report nothing.

The disqualifying problem is not the unevenness, though.
It is that **each harness's totals omit a different set of real LLM calls**, and each omission is invisible in the output.

The clearest demonstration is that the two harnesses that were fully researched leak in *opposite* places.
Cline records nothing for its agentic compaction summarizer, which discards its usage chunk outright (Section 3.6), whereas OpenCode does count compaction tokens.
OpenCode loses title-generation tokens entirely — a full LLM call on the first step of every session that produces no row and no event (Section 1.6) — whereas Cline has no equivalent leak.
Cline's empty-response retries, from a middleware written specifically with Ollama in mind, make its HTTP request count exceed its reported iteration count with no field exposing the difference; OpenCode's retry tokens appear to be lost outright.

Two harnesses, four different accounting behaviours, none of them documented, and every one of them invisible in the harness's own output.
PI is a blank on all four questions.

This is not a gap that post-processing can close, because a runner cannot add back a number that was never recorded anywhere.

There is also a definitional problem that no amount of harness fidelity fixes: `iterations` in Cline, `step_finish` in OpenCode, and whatever PI reports are three different concepts, defined by three different codebases, and they cannot be made to mean the same thing by post-processing.

Native reporting should still be captured on every run, for two reasons.
It is the only source of *per-turn* attribution and of harness-internal semantics such as `toolCallCount` and compaction notices.
And the delta between native totals and proxy totals is itself a finding — it quantifies exactly how much each harness hides from its own users.

## Section 5 — Route C: Ollama's own surface

Presented before the proxy because the proxy's design depends entirely on these facts.

### 5.1 Native `/api/*` metrics

Both `/api/generate` and `/api/chat` embed a single `Metrics` struct, at `api/types.go:557-564`: `total_duration`, `load_duration`, `prompt_eval_count`, `prompt_eval_duration`, `eval_count`, `eval_duration`.

All durations are in **nanoseconds**, stated verbatim in `docs/api.md`.

Every field carries `omitempty`, so **a zero value is omitted from the JSON entirely**.
A parser must treat absence as zero rather than as an error.

### 5.2 `/v1/chat/completions` usage

The OpenAI-compat `Usage` struct at `openai/openai.go:76-80` has exactly three fields: `prompt_tokens`, `completion_tokens`, `total_tokens`.
It is populated at `openai/openai.go:240-247` as a direct relabel of `prompt_eval_count` and `eval_count`.

There is **no `prompt_tokens_details`, no `cached_tokens`, and no `completion_tokens_details`**.
Any harness expecting OpenAI's cache-token fields will read zeros.

**Non-streaming responses always include usage**, because `ChatCompletion.Usage` is a value type rather than a pointer (`openai/openai.go:134`) and is set unconditionally at `openai/openai.go:297`.

### 5.3 Streaming usage — the crux, and it is decisive

**Ollama emits a final `usage` frame when streaming if and only if the client sends `stream_options: {"include_usage": true}`.**

The gate is at `middleware/openai.go:141`:

```go
if w.streamOptions != nil && w.streamOptions.IncludeUsage {
    u := openai.ToUsage(chatResponse)
    finishChunk.Usage = &u
    finishChunk.Choices = []openai.ChunkChoice{}
    // … written as one extra SSE frame, immediately before data: [DONE]
}
```

`StreamOptions` is defined at `openai/openai.go:98-100` and plumbed from the request at `middleware/openai.go:384` and `:476`.
`ChatCompletionChunk.Usage` is `*Usage` with `json:"usage,omitempty"` at `openai/openai.go:145`, so without the flag a nil pointer is omitted from **every** chunk, including the finish chunk.
Support is also documented at `docs/api/openai-compatibility.mdx:205-206`.

This conforms to OpenAI's own contract, which states that `usage` "will only be present when you set `stream_options: {"include_usage": true}`", contains null "except for the last chunk", and that "if the stream is interrupted or cancelled, you may not receive the final usage chunk" (https://developers.openai.com/api/reference/resources/chat/subresources/completions/streaming-events).

**Consequence: a purely passive proxy sees zero token counts from any harness that streams without opting in.**
This single fact dictates the proxy design in Section 6.

A minor wart: the `/v1/completions` path at `middleware/openai.go:192-194` stamps an *empty* `Usage{}` onto every intermediate chunk when the flag is set, which the chat path does not do.
On that endpoint, ignore all-zero usage objects and take only the final one.

### 5.4 What `prompt_eval_count` actually counts

This matters more than it first appears.
At `llm/llama_server.go:1470-1480`:

```go
func (t llamaServerTimings) promptEvalCount() int {
	return t.CacheN + t.PromptN
}
```

So `prompt_eval_count` is the **full prompt length in tokens, including the KV-cache-hit prefix**, not just the freshly evaluated suffix.
That is exactly what a benchmark wants: a stable, comparable input-token measure that does not fluctuate with cache state.

But the paired duration does *not* match: `prompt_eval_duration` is `PromptMS`, covering only freshly evaluated tokens.
**Do not compute a prefill throughput from these two fields** — dividing a full prompt by the time to process only its tail gives a wildly inflated number.
`docs/api.md` only ever gives the formula for the generation rate, which is unaffected.

Because `cache_n` is summed away before reaching any HTTP surface, **UNVERIFIED and in fact unobtainable: the per-request prompt-cache hit count.**
It is absent from `Metrics`, from `Usage`, and even from `/v1/responses`, where `cached_tokens` is hardcoded to literal `0` (`openai/responses.go:863`, `:1369`).

### 5.5 Logs and metrics endpoint

**There is no metrics endpoint.** This was refuted by enumerating the full route table in `server/routes.go` (`GenerateRoutes`, lines 1823-1910), not assumed.
A case-insensitive search for `prometheus` and `/metrics` across the tree returns only two cosmetic TUI strings in `cmd/tui/chat/render.go:577,584`.

The HTTP engine is `gin.Default()` at `server/routes.go:1851`, which installs gin's standard access logger.
That yields one line per request with status, latency, client IP, method and path — **useful for counting requests and per-request latency, but carrying no token counts.**

`OLLAMA_DEBUG=1` raises the log level to DEBUG and `=2` to TRACE (`envconfig/config.go:200-212`), but **no per-request line emits `prompt_eval_count` or `eval_count` at any level.**
Do not plan on scraping tokens from logs.

One genuinely useful discovery: **`OLLAMA_DEBUG_LOG_REQUESTS=1`** (`envconfig/config.go:219-220`, implemented in `server/inference_request_log.go`) makes Ollama write **every inference request body verbatim to disk**, plus a runnable replay `curl` script, into a temp directory announced at startup (`:44`).
The middleware is wired onto `/api/generate`, `/api/chat`, `/v1/chat/completions`, `/v1/completions`, `/v1/responses` and `/v1/messages` at `server/routes.go:1890-1908`.
Files are timestamped with a monotonic counter at `:106`, giving exact ordering.

This is a free, built-in, harness-independent **request** recorder.
Its limit is fatal on its own: `log()` at `:87-125` writes only the request body, so there are **no responses and no token counts**.
Use it as a cross-check on the proxy's request count, not as a replacement.

**Verdict on Route C: an indispensable source of truth for token *definitions*, but not a complete measurement route by itself.**
Ollama knows the real numbers, and its `prompt_eval_count` is the cleanest definition of input tokens available anywhere in this system.
But it exposes them only in HTTP responses, one request at a time, with no aggregation, no run boundary, no persistence, and no metrics endpoint.
Something must sit in the path and collect them.

### 5.6 Fairness knobs that must be pinned

`FromChatRequest` at `openai/openai.go:617-660` maps `max_tokens` to `num_predict`, plus `temperature`, `seed`, `frequency_penalty`, `presence_penalty`, `top_p` and `stop`.

**Trap 1 — silent defaults.** If a harness omits `temperature`, Ollama does not fall back to the model's Modelfile default; it hardcodes `1.0`. The same applies to `top_p`.
Two harnesses can therefore differ purely because one is silent.
Log the effective sampling parameters per request and verify all three arms send identical values.

**Trap 2 — `num_ctx` cannot be set over `/v1`.**
`ChatCompletionRequest` has no such field, and `docs/api/openai-compatibility.mdx:341-350` states plainly that the OpenAI API has no way to set the context size and that a Modelfile is required.
The default is VRAM-tiered, at `server/routes.go:2031-2039`: 256k above 47 GiB, 32k above 23 GiB, and **4096 otherwise**.
`docs/context-length.mdx` adds that agent and coding tools "should be set to at least 64000 tokens".

This is the single largest silent-corruption risk in the whole experiment.
On a typical consumer GPU the run lands in the 4096 tier, a coding agent's system prompt plus tool schemas plus a couple of file reads exceeds that almost immediately, and Ollama **truncates the input rather than erroring** (`server/routes.go:873-900`).
Harnesses have different prompt sizes, so they would hit the wall at different steps, and the comparison would be measuring prompt bloat against a context limit rather than harness quality.

Mitigation, applied identically to all arms: set `OLLAMA_CONTEXT_LENGTH=65536` on the `ollama serve` process (on NixOS, in `systemd.services.ollama.environment`), which reliably overrides the VRAM tiering because `usesAutomaticNumCtx` (`server/routes.go:176-186`) returns false as soon as the variable is non-zero.
Then verify with `ollama ps` that the `CONTEXT` column matches, and assert that no run's `prompt_eval_count` approaches the limit.

Also set `OLLAMA_NUM_PARALLEL=1` (already the default, `envconfig/config.go:275`) and **never run two harnesses concurrently against the same Ollama instance**, or the second one's wall time includes queueing behind the first.

Warm the model before each run with `keep_alive` set generously, poll `/api/ps` until it is resident and shows `100% GPU`, and assert `load_duration` is zero or absent on measured requests.
The `docs/api.md` example shows a cold request spending 6.34 s of 10.7 s on loading — 59% of wall time — so an unwarmed benchmark measures disk I/O.

## Section 6 — Route B: the measuring proxy

**Verdict: adopt it as the primary and comparable measurement, with one mandatory design decision.**

### 6.1 What it can see

Because the traffic is local plaintext HTTP with no TLS, a proxy sees the entire exchange with no certificate machinery: full request bodies including the system prompt and tool schemas, full response bodies or every SSE frame, per-request wall clock, time to first token, and request count and ordering.

The system prompt and tool schemas are the largest and most harness-differentiating part of the payload, and they are exactly what this project exists to compare.

### 6.2 The mandatory design decision

Section 5.3 makes a *passive* proxy unviable: without `include_usage`, there are no token counts on the wire at all, and whether a harness sets that flag is its own decision — Cline's OpenAI-compatible route does (`openai-compatible.ts:160`), OpenCode apparently does, PI is unknown.

The proxy must therefore **rewrite the request to force `stream_options: {"include_usage": true}`**, and — to avoid perturbing the harness — **swallow the resulting usage frame before forwarding the stream onward**.

The risk of rewriting is real and specific: the usage frame has `choices: []` (forced at `middleware/openai.go:144`), and a harness whose SSE parser does `chunk.choices[0].delta` without a length check will throw.
Swallowing the frame removes that risk entirely, at a cost of roughly five lines, because the harness then sees a byte-stream indistinguishable from an unmodified one while the proxy captures Ollama's own authoritative counts.

If a harness already sets the flag, leave its request untouched and simply read the frame; record which harnesses needed the rewrite, since that is itself a finding.

Two alternatives were assessed and rejected as primary methods.
Tokenizing locally is unreliable for a *comparison* because it requires reproducing the model's chat template byte-exactly — Ollama exposes no tokenizer endpoint, so the template must be replicated out of band — and because Ollama truncates server-side against `num_ctx` while a local tokenizer would count the untruncated prompt.
Use it only as a sanity check on a handful of requests.
Replaying conversations against the native API runs inference a second time, doubling GPU cost and perturbing the prompt cache for the real run that follows; **UNVERIFIED: whether `/api/generate` with `num_predict: 0` returns `prompt_eval_count` without generating**, and it is not worth establishing.

### 6.3 What "one step" means at the proxy

Define it precisely: **one step is one `POST /v1/chat/completions` that receives a 2xx and reaches a terminal `finish_reason`.**
That definition is unambiguous, harness-agnostic and mechanically checkable, which is the entire point.

It will diverge from every harness's internal counter, in known ways.
Parallel tool calls collapse: one response containing three tool calls is one request but three tool executions, so record `len(tool_calls)` separately.
Side-calls inflate: title generation, summarization and classifier calls are each one extra POST that no harness shows as an agent step, and they are detectable heuristically by a tiny `messages` array, an absent `tools` field, and a small `max_tokens` — so record `has_tools` and `message_count` per request and segment afterwards.
Startup probing of `/v1/models` should be excluded by path.
Retries inflate the count with no semantic step, and are only heuristically detectable by hashing the `messages` array and watching for identical hashes in a short window — log a content hash per request so they are at least visible post hoc.
Compaction shows up as a sudden drop in `prompt_tokens` between consecutive requests, which is a useful signal precisely because harnesses differ enormously in when they compact.

Report `proxy_requests`, `proxy_steps` and `tool_invocations` as three distinct numbers.
Do not attempt to reverse-engineer each harness's own definition; state one definition, apply it uniformly, and treat the divergence as part of the result.

### 6.4 The input-token double-counting caveat

This must be stated in the writeup, not buried in a footnote.

The Chat Completions API is stateless, so every tool result comes back as a new POST carrying the entire prior conversation plus the tool output.
Across N steps the input sizes are `P₁ ⊂ P₂ ⊂ … ⊂ Pₙ`, and `Σ input_tokens` grows roughly quadratically in step count.

This is **not** an artifact: it is real work the model performs, and it is exactly what `prompt_eval_count` measures, since Section 5.4 established that cache hits are included in the count.
But it is emphatically not "unique tokens the conversation contained".
A harness taking twelve small steps can report far more summed input tokens than one taking five large steps with an identical final transcript.

Report three numbers with unambiguous labels: `total_prefill_tokens` (the sum, honest cumulative model work and the right basis for simulated cost), `final_context_tokens` (the last request's `prompt_tokens`, the conversation's actual size), and `output_tokens` (the sum, which is clean and additive with no double counting).

### 6.5 Implementation

A **~100-line async reverse proxy in Python or Node is the recommendation.**
The correctness requirements are short: forward all paths and methods (harnesses also hit `/v1/models`, sometimes `/api/tags` and `/api/show`, and will fail at startup in confusing ways if those are not proxied); iterate the upstream body chunk-by-chunk and write each chunk to the client *before* parsing a copy of it; disable any gzip or buffering middleware; buffer only a line remainder for SSE parsing while forwarding raw bytes verbatim; timestamp request-sent, first-byte, first-content-delta and last-byte; and append one JSON line per request to a JSONL file.
Cost is zero, the dependency is one HTTP client, and the whole thing fits on a screen — which matters, because this proxy *is* the measurement instrument, and if it is wrong every number is wrong.

**mitmproxy was assessed and is rejected**, on the strength of its own documentation.
https://docs.mitmproxy.org/stable/overview/features/ states that by default it "will read an entire request/response, perform any indicated manipulations on it, and then send the message on to the other party", and that when streaming is enabled "the message body will not be accessible within mitmproxy, and body modifications will have no effect".
That is a hard fork with no good branch: buffered mode destroys time-to-first-token and may change harness behaviour, while streaming mode hides the body that is the entire point.
Community workarounds exist (mitmproxy discussion #6996) but were not verified against SSE on current versions.
mitmproxy's strength is TLS interception of traffic you do not control, which is worth nothing against local plaintext HTTP.

**LiteLLM was assessed as a capable fallback, with two unresolved risks.**
Verified: its `StandardLoggingPayload` (https://docs.litellm.ai/docs/proxy/logging_spec) carries `prompt_tokens`, `completion_tokens`, `total_tokens`, `startTime`, `endTime`, `completionStartTime` (time to first token), `response_time`, `messages`, `response` and `model_parameters` — a near-perfect schema match.
Verified: local-only logging with no cloud account works via a `CustomLogger` subclass wired through `litellm_settings: callbacks` (https://docs.litellm.ai/docs/observability/custom_callback), reading `kwargs["standard_logging_object"]`.
**UNVERIFIED: whether LiteLLM passes SSE through without introducing buffering that distorts time-to-first-token** — no documentation asserts it, and `docs.litellm.ai/docs/proxy/streaming_logging` returns 404.
**UNVERIFIED: whether its usage tracking requires Postgres** on the callback path.
Beyond those, LiteLLM is a large dependency with its own request translation, and "silently alters the request" is precisely the failure mode that would invalidate a harness comparison.

### 6.6 Wall time — the proxy deliberately measures the wrong thing

The proxy can measure per-request latency, time to first token (only if it never buffers), inter-request gaps, and the sum of request latencies.

The inter-request gap is worth highlighting as a metric in its own right: it isolates harness overhead and tool-execution time from model time, which is arguably the most interesting number this project can produce.

But the proxy **cannot** measure total run wall time.
It sees nothing of harness startup, config parsing, tool-server initialization, file indexing or shutdown.
The sum of request latencies systematically understates true duration, and understates it *differently per harness* — precisely the bias that would invalidate the comparison.

**End-to-end wall time must come from the runner that wraps the harness process**, using a monotonic clock around spawn and exit, never a wall clock subject to NTP steps.

The decomposition to publish is:

```
runner_wall_time                  ← runner only, authoritative
  ├─ Σ request_latency            ← proxy: model busy time
  ├─ Σ inter_request_gap          ← proxy: harness overhead + tool execution
  └─ startup + shutdown residual  ← runner minus the two above
```

If the residual differs by an order of magnitude across harnesses, that is a finding, and it is invisible to any proxy-only measurement.

---

## Section 7 — Recommendation

**Measure with the proxy. Record native reporting alongside it. Take wall time from the runner. Never compare on native numbers.**

The rationale, in order of weight:

**1. Only the proxy produces one definition applied three times.**
`iterations` (Cline), `step_finish` (OpenCode) and PI's unknown equivalent are three different concepts from three codebases.
"One POST to `/v1/chat/completions` that reached a terminal `finish_reason`" is one concept, applied identically, and no harness gets a vote on it.

**2. Native totals provably omit real LLM calls, and they omit different ones per harness.**
Cline's agentic compaction summarizer discards its usage chunk outright (`agentic-compaction.ts:62-87`), so those tokens exist in no Cline surface at all.
OpenCode's title generation bypasses the processor entirely (`prompt.ts:177-237`), producing no row and no event, and on a custom Ollama provider it burns the benchmark model itself.
Cline's empty-response retry middleware, written with Ollama specifically in mind, makes request count exceed iteration count with no field exposing the gap.
OpenCode counts compaction tokens where Cline does not, and appears to lose retry tokens where Cline preserves them.
PI is unknown end to end.
A proxy counts what actually reached the model, so none of these can hide.

**3. Ollama's `prompt_eval_count` is the best available definition of input tokens**, and the proxy is what harvests it per request.
It includes the KV-cache-hit prefix (`llm/llama_server.go:1478-1480`), so it is stable against cache state, and it is the model's own count rather than a client's reconstruction.

**4. The cost of the proxy is genuinely small** — roughly 100 lines, zero dependencies of consequence, zero money — and it is auditable in full, which the alternatives are not.

The one thing the proxy must not do is stay passive.
Section 5.3 is decisive: without forcing `stream_options.include_usage`, a streaming harness yields no token counts whatsoever.
Force it, and swallow the resulting frame so the harness sees an unmodified stream.

### Concrete setup

1. **Ollama server** (NixOS, `systemd.services.ollama.environment`): `OLLAMA_CONTEXT_LENGTH=65536`, `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_KEEP_ALIVE=30m`, `OLLAMA_DEBUG_LOG_REQUESTS=1`.
2. **Proxy** on `:11435`, forwarding all paths to `:11434`, true chunk-by-chunk SSE passthrough, forcing `include_usage` and swallowing the usage frame, one JSONL line per request.
3. **Harnesses** all pointed at `http://localhost:11435/v1`. Verify each sends identical `temperature`, `seed` and `max_tokens`, since silence means `temperature=1.0`. For Cline specifically, use `-P openai-compatible --baseurl` rather than `-P ollama`, so that it traverses the proxy at all — the native `-P ollama` route rewrites the URL to `/api` and would bypass an OpenAI-compat proxy.
4. **Cline** additionally: `--compaction basic` (to avoid the invisible summarizer tokens), `--data-dir` per run, `-t <timeout>`, telemetry opted out.
5. **OpenCode** additionally: `--title <fixed-string>` on every run, to suppress the unaccounted title-generation LLM call (Section 1.6), plus an external timeout because headless hangs have been reproduced.
6. **Runner**: wraps each harness process, warms the model and polls `/api/ps` asserting `100% GPU` and the expected `CONTEXT`, records monotonic wall time, asserts `load_duration` is zero on measured requests, and enforces an external timeout.
7. **Outcome classification must not use exit codes** for OpenCode or PI, both of which return 0 on failure. Classify from task-specific artifacts (did the code change, do the tests pass), never from the process exit status.
8. **Report**: `total_prefill_tokens`, `final_context_tokens`, `output_tokens`, `proxy_steps`, `tool_invocations`, `runner_wall_time`, `Σ request_latency`, `Σ inter_request_gap`, plus the native-vs-proxy delta per harness.

### Cross-check, not redundancy

`OLLAMA_DEBUG_LOG_REQUESTS=1` gives an independent, zero-code record of every request body and its ordering.
If the proxy's request count disagrees with the file count, the proxy is wrong.
This is worth having precisely because the proxy is a bespoke instrument.

---

## Section 8 — Frontier model price table

Purpose: the benchmark runs a small local model for free, counts real input and output tokens, then multiplies by these prices to state what the same run would have cost on a frontier model.
Input and output prices must therefore be separately correct.

All prices in USD per 1M tokens.
**Retrieved 2026-08-07.** Every row was read from the vendor's own live pricing page on that date; nothing here is recalled from training data.

| Family | Model (vendor's id) | Input $/1M | Output $/1M | Cached input $/1M | Source URL |
|---|---|---|---|---|---|
| Claude | Claude Opus 5 | 5.00 | 25.00 | 0.50 (cache hit) | https://platform.claude.com/docs/en/about-claude/pricing |
| Claude | Claude Sonnet 5 | 2.00 | 10.00 | 0.20 (cache hit) | https://platform.claude.com/docs/en/about-claude/pricing |
| Claude | Claude Haiku 4.5 | 1.00 | 5.00 | 0.10 (cache hit) | https://platform.claude.com/docs/en/about-claude/pricing |
| GPT | gpt-5.6-sol | 5.00 | 30.00 | 0.50 | https://developers.openai.com/api/docs/pricing |
| GPT | gpt-5.6-terra | 2.00 | 12.00 | 0.20 | https://developers.openai.com/api/docs/pricing |
| GPT | gpt-5.6-luna | 0.20 | 1.20 | 0.02 | https://developers.openai.com/api/docs/pricing |
| Gemini | gemini-3.1-pro-preview | 2.00 (≤200k) / 4.00 (>200k) | 12.00 (≤200k) / 18.00 (>200k) | 0.20 / 0.40 | https://ai.google.dev/gemini-api/docs/pricing |
| Gemini | gemini-3.6-flash | 1.50 | 7.50 | 0.15 | https://ai.google.dev/gemini-api/docs/pricing |
| Gemini | gemini-3.1-flash-lite | 0.25 (text/image/video) | 1.50 | 0.025 | https://ai.google.dev/gemini-api/docs/pricing |

### Caveats that materially affect the computed figure

**Claude Sonnet 5's $2 / $10 is introductory pricing, in effect only through 2026-08-31.**
From 2026-09-01 the standard rate is **$3 / $15**.
Any cost figure computed with the $2/$10 row must state the date it was computed, or it will be wrong within a month of this writing.

**Claude's newer models use a different tokenizer.**
The pricing page states that Claude 4.7 and later "use a newer tokenizer… This tokenizer produces approximately 30% more tokens for the same text."
Since the simulated-cost figure multiplies *Ollama's* token counts by Claude's prices, this is a genuine source of error: the same text would be billed as roughly 30% more tokens on Opus 5 than a naive substitution assumes.
State this as a known bias rather than silently ignoring it.
The same concern applies in principle to every vendor — token counts are not portable across tokenizers — and is the strongest argument for presenting simulated cost as an order-of-magnitude comparison rather than a precise dollar figure.

**Claude lists separate cache-write prices**, at 1.25x base input for a 5-minute TTL and 2x for a 1-hour TTL, with cache reads at 0.1x.
The table above shows only the cache-read (hit) price.

**Gemini output prices include thinking tokens**, stated explicitly on the pricing page.

**Gemini's Pro tier and 2.5-series models are context-tiered**, changing price above 200k input tokens; Claude 4.6 and later include the full 1M context at standard pricing.

**Batch pricing is a flat 50% discount** on both input and output for Claude and for most OpenAI models.
It is not applicable to an interactive agent workload and should not be used for this figure.

**Anthropic's canonical API price list is the docs page cited above**; `claude.com/pricing` is the marketing page and was not used.
`platform.openai.com/docs/pricing` now redirects to `developers.openai.com/api/docs/pricing`, which is what was read.

### Flagship selection note

The choice of "flagship" is not clean in every family and is a judgement call worth revisiting.

For Claude, the pricing table lists Claude Fable 5 and Claude Mythos 5 above Opus 5, both at $10 / $50, with Mythos marked limited-availability.
Opus 5 was chosen as the comparison flagship because it is the general-availability top coding model; if the writeup wants the most expensive plausible comparison, Fable 5 at $10 / $50 is the row to use.

For Gemini, there is currently **no GA Pro-tier model in the 3.x line** — `gemini-3.1-pro-preview` is a preview, and `gemini-3.6-flash` is the GA workhorse.
Using a preview model's price in a published comparison is defensible but should be labelled as such.

---

## Summary of what could not be established

- **PI is essentially unresearched.** Its reporting surface, session artifacts, step semantics, provider configuration and `include_usage` behaviour are all unverified. The assigned agent did not report before this document was due. The only PI facts recorded here are its install path, its data directory, and the second-hand ticket-#6 finding about exit codes.
- **OpenCode's step-to-round-trip mapping** is unverified, as is its subagent token attribution and its session-table `tokens_*` column names. The `step_finish.part.tokens` field list was closed by the second pass (§1.10). Retry token handling remains source-derived rather than reproduced, but is now known to sit behind an *unbounded* retry policy, which raises its severity.
- **Ollama's per-request prompt-cache hit count** is not merely unverified but unobtainable from any HTTP surface.
- **LiteLLM's SSE buffering behaviour and Postgres requirement** were not confirmed, which is why it is a fallback rather than the recommendation.
- **Cline's hub-backend `run_result` reliability** was not executed, though forcing the local backend makes the question moot.

Every one of these is recorded as a gap rather than filled by inference.
The two that block the experiment are PI's entire measurement surface and OpenCode's step semantics; both need a follow-up before the arms can be considered comparable on native numbers — though the recommendation in Section 7 is specifically designed so that the comparison does not depend on them.
