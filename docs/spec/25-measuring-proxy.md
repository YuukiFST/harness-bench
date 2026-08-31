# 25 — Specification of the measuring proxy

Ticket #25.
Question: how is the measuring proxy specified, built and validated?

This is a **specification**, not an implementation: `harness-bench` itself is built under #17 and first exercised under #16.
The proxy is the project's measurement instrument, and #4 states the stake plainly — *"this proxy is the measurement instrument, and if it is wrong every number is wrong"* (`docs/research/04-measuring-tokens-steps-time.md:618`).

Retrieval date for every claim below: **2026-08-07**.

Two kinds of evidence appear here and they are labelled differently.
Claims marked **[R]** are inherited from a closed research ticket and cite its document by `file:line`.
Claims marked **[V]** were measured on 2026-08-07 on the validation rig described in §10.1, which drove a real client (pi 0.80.10, which consumes SSE through the `openai` SDK 6.26.0 per `docs/research/10-pi-measurement-surface.md:320-335`) through a throwaway reference proxy into a throwaway fault-injecting mock upstream.
Where a fact could not be established, it is marked **UNVERIFIED** rather than filled in by inference.

The specification exists because #4, #28, #26, #30 and #31 each appended a constraint to this ticket, and three of those constraints contradict each other by design.
The rewrite is required against Ollama and unnecessary against Zen (#28), the usage frame must be swallowed on one profile and must not be on the other (#28), and the parsing profile turned out to key on the *model* rather than on the gateway (#31).
§2 and §3 reconcile them into one parameterised contract; §10 shows the reconciliation surviving contact with a real client.

---

## 1. What the instrument is, and what it is not

The proxy is a reverse proxy that sits between every harness and the model endpoint, forwards bytes verbatim, and writes one JSON line per HTTP request to a JSONL file.
It is the **only** source of comparable token and step numbers, because it applies one definition to every arm while each harness applies its own (`docs/research/04-measuring-tokens-steps-time.md:664-674`). [R]

The proxy is **not** the source of wall time.
It cannot see harness startup, config parsing, tool-server initialisation, file indexing or shutdown, and the sum of request latencies understates true duration *differently per harness* — which is precisely the bias that would invalidate the comparison (`docs/research/04-measuring-tokens-steps-time.md:639-643`). [R]
End-to-end wall time comes from the runner, around spawn and exit, on a monotonic clock.

The proxy is also **not** a repair layer.
Its only responses to a defect are to record it and to mark the run discardable; it never retries, never rewrites a broken response into a working one, and never fills a missing field.
This is the single most important behavioural rule in the specification, because the failure mode that matters is not a crash but plausible-looking data (§6).

## 2. The upstream profile is a parameter, keyed on the model id

#28 established that the Ollama contract and the Zen contract invert, and #31 established that three distinct response profiles sit behind the *single* Zen base URL — DeepSeek-native, OpenRouter-normalised and Meituan-native — differing in usage field names, reasoning field names, tool-call id shapes and even error language (`docs/research/11-second-free-model.md:322-352`). [R]

Therefore the profile is keyed on the **requested model id**, never on the base URL.
Keying on the base URL would silently mis-parse any model that is not the one the parser was written against, and "silently mis-parse" is indistinguishable from "the harness used fewer tokens".

```
Profile = {
  force_include_usage: bool,   # add stream_options.include_usage if the client omitted it
  swallow_usage_frame: bool,   # remove the usage frame from the forwarded byte stream
  parse_past_done:     bool,   # keep parsing after `data: [DONE]`
  usage_carries_finish_reason: bool,  # the usage frame is also the terminal chunk
}
```

| Profile | Models | `force_include_usage` | `swallow_usage_frame` | `parse_past_done` | `usage_carries_finish_reason` |
|---|---|---|---|---|---|
| `ollama` | LFM2.5-2.6B on local Ollama (unmeasured reserve, #24) | true | true (but see §3) | false | false |
| `zen-deepseek` | `deepseek-v4-flash-free` | false | false | true | true |
| `zen-openrouter` | `mimo-v2.5-free` | false | false | true | true |

Only three profiles are specified because only three upstreams are in play: the two selected tiers (#31) plus the unmeasured Ollama reserve (#24).
`longcat-2.0-free` is deliberately absent — it splits `finish_reason` and `usage` across two frames and sends usage with `choices: []`, which is the *Ollama* shape arriving on the Zen gateway (`docs/research/11-second-free-model.md:307-319`), and it is one of the three reasons it was rejected. [R]
A fourth profile is a schema change, not a code change: adding a row to the table above is the whole cost.

**The profile is asserted at start-up, never trusted from configuration.**
§9 specifies the canary that does it.

## 3. The rewrite contract, corrected

The naive contract inherited from #4 is: force `stream_options.include_usage`, then swallow the resulting usage frame so the harness sees an unmodified byte stream (`docs/research/04-measuring-tokens-steps-time.md:574-577`). [R]

**Swallowing must be conditional on the proxy having caused the frame.**
This is a correction, not a restatement, and it was found by measurement.

When the proxy swallows a usage frame that the *client itself* asked for, pi's native usage reporting drops to `input: 0, output: 0` while the proxy still records `prompt_tokens: 137, completion_tokens: 11`. [V]
That is not a cosmetic loss.
#30 makes the native-vs-proxy cross-check mandatory on every run, with a hard failure on divergence beyond a stated tolerance, because a native count that silently undercounts reads exactly like a correct one when it is the only witness, and the totals stay plausible while being wrong by an order of magnitude.
Unconditional swallowing zeroes one side of that cross-check, so the instrument would destroy its own only witness.

The rule, in full:

```
if profile.force_include_usage and request.stream and not request.stream_options.include_usage:
    request.stream_options.include_usage = true
    record.rewrote_include_usage = true

swallow = profile.swallow_usage_frame and record.rewrote_include_usage
```

`record.rewrote_include_usage` is itself a finding worth reporting per arm, as #4 asked (`docs/research/04-measuring-tokens-steps-time.md:579`). [R]

In practice the rewrite is expected to be a no-op on every measured arm.
pi sets `stream_options: {include_usage: true}` itself on **every** request — 11 of 11 requests across 5 distinct model ids in the rig carried the field with no proxy rewrite [V] — which confirms `docs/research/10-pi-measurement-surface.md:320-335` against the wire, and #26 records the same for OpenCode, Cline's `openai-compatible` route and oh-my-pi. [R]
Both Zen profiles return usage unconditionally with no opt-in at all (`docs/research/11-second-free-model.md:247-251`). [R]
So on the measured configuration the force never fires and the swallow never fires; the branches exist for the Ollama reserve and as a guard against an arm that stops setting the flag.

Do **not** delete the branches on that basis.
An arm silently dropping `include_usage` is exactly the change that would produce zero tokens with no error, and the rewrite is what makes that unobservable case observable.

## 4. What one step is

**One step is one `POST /v1/chat/completions` that receives a 2xx and reaches a terminal `finish_reason`** (`docs/research/04-measuring-tokens-steps-time.md:588`). [R]
The definition is harness-agnostic and mechanically checkable, and no harness gets a vote on it.

Three distinct numbers are reported and never collapsed into one: `proxy_requests`, `proxy_steps` and `tool_invocations` (`docs/research/04-measuring-tokens-steps-time.md:598`). [R]
`proxy_requests` counts every POST to the completions path; `proxy_steps` counts those that reached a terminal `finish_reason` with a 2xx and no fault; `tool_invocations` sums `len(tool_calls)` because one response carrying three tool calls is one request and three executions.

Startup probing of `/v1/models` is excluded by path, not by heuristic.
pi issues no such probe (`docs/research/10-pi-measurement-surface.md:176-181`), but other arms do, and the path exclusion costs nothing. [R]

The input-token double-counting caveat from `docs/research/04-measuring-tokens-steps-time.md:601-612` is a reporting obligation of this instrument, not of the writeup alone: the proxy emits `total_prefill_tokens`, `final_context_tokens` and `output_tokens` as three separately labelled figures, because a harness taking twelve small steps can report far more summed input tokens than one taking five large steps with an identical final transcript. [R]

## 5. The record schema

One JSON object per line, one line per HTTP request, appended as the response completes.
Written for a run directory, never appended across runs.

| Field | Type | Notes |
|---|---|---|
| `run_id` | string | opaque; the runner supplies it |
| `seq` | int | monotonic within the run, assigned when the request arrives |
| `method` | string | |
| `path` | string | verbatim, before any routing |
| `status` | int \| null | null when no response line was ever received |
| `model_requested` | string \| null | from the request body |
| `model_echoed` | string \| null | from the first response frame carrying `model` |
| `profile` | string | the profile key resolved in §2 |
| `t_request_sent` | float | monotonic seconds |
| `t_first_byte` | float \| null | |
| `t_first_content_delta` | float \| null | first frame with a non-empty `delta.content`; separates model queue time from generation |
| `t_last_byte` | float \| null | |
| `prompt_tokens` | int \| null | |
| `completion_tokens` | int \| null | |
| `cached_tokens` | int \| null | from the portable `prompt_tokens_details.cached_tokens`, per §5.1 |
| `reasoning_tokens` | int \| null | from `completion_tokens_details.reasoning_tokens` |
| `has_tools` | bool | whether the request carried a `tools` array |
| `tool_schema_bytes` | int | length of the serialised `tools` array; this is the project's headline quantity (#27 measured 13.4x between pi and oh-my-pi) |
| `message_count` | int | `len(messages)` |
| `messages_hash` | string | sha256 of the canonicalised `messages` array, truncated to 16 hex chars |
| `request_body_bytes` | int | as sent upstream, after any rewrite |
| `tool_calls` | int | `len(tool_calls)` summed across frames |
| `finish_reason` | string \| null | |
| `rewrote_include_usage` | bool | §3 |
| `swallowed_usage_frame` | bool | §3 |
| `faults` | string[] | §6; empty on a clean request |
| `run_discardable` | bool | `len(faults) > 0` |

### 5.1 Field names to read, and one to stop reading

Read cache accounting from **`prompt_tokens_details.cached_tokens`**, which every free model on the gateway carries including the primary, rather than from DeepSeek's private `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens` pair, which appears on no other candidate (`docs/research/11-second-free-model.md:266-271`). [R]
Accept `reasoning` and `reasoning_details` alongside `reasoning_content`, because the field name differs by profile (`docs/research/11-second-free-model.md:326-330`). [R]

## 6. Faults, and the discard rule

Every fault below marks the request, and any run containing a marked request is **discarded, never repaired** (#28's discipline, extended by #31).
Discarding is affordable and repairing is not: a repaired run produces a number, and a number is what gets published.

| Fault | Detection | Why it is fatal |
|---|---|---|
| `non_2xx` | status line | #28: the only defence against the undocumented free cap (#29), which surfaces as a mid-run 429 with no advance header |
| `upstream_error_payload` | `error` key in a 2xx body or frame | #31: an upstream `ResourceExhausted 32/32` arrived with **HTTP 200**, so the status line alone is necessary and not sufficient |
| `model_substituted` | `model_echoed != model_requested` | #31: four requests for `ling-3.0-flash-free` returned bodies echoing `ling-3.0-tiny-free` with token accounting matching the smaller model (`docs/research/11-second-free-model.md:116-138`); this is the one defect that breaks *"the model held fixed"* without leaving a trace in any other field |
| `missing_finish_reason` | terminal frame carried none | §6.1 |
| `usage_after_done` | a frame carrying `usage` arrived after `data: [DONE]` | §6.2 |
| `stream_truncated` | no `[DONE]` and no terminal `finish_reason` | §6.3 |
| `upstream_disconnect` | transport exception while reading upstream | §6.3 |
| `no_usage_captured` | 2xx on the completions path with `prompt_tokens` still null | catches a profile misresolution directly |

### 6.1 The missing `finish_reason` is the most dangerous state the instrument can produce

#26 warned that pi throws on an absent `finish_reason` and that the resulting error **matches a retry pattern**, so a proxy bug would masquerade as a model failure and be silently retried instead of reported. [R]

Measured, and worse than the warning. [V]
Driving pi through the proxy against an upstream that omits `finish_reason` produced **four** requests for one turn, four identical `messages_hash` values, `stopReason: "error"` with `willRetry: true` on the first three, and **process exit code 0**.
Each retry carried a full, plausible usage object (`input: 137, output: 11`), so the run inflates token totals by 4x and reports success.

Two consequences for the instrument.
The proxy must flag `missing_finish_reason` on the request itself, because nothing downstream will: not the exit code, not the harness's own event stream, not the token totals.
And retry detection by identical `messages_hash` in a short window is not a nice-to-have — it is the only signal that separates four requests from four steps, and it worked exactly as #4 predicted (`docs/research/04-measuring-tokens-steps-time.md:595`). [R][V]

### 6.2 A usage frame after `[DONE]` is silently swallowed by the client, not thrown on

#26 ruled that the proxy must never place the usage frame after `data: [DONE]`, on the grounds that parsing past `[DONE]` and *emitting* past it are different things and only the first is safe. [R]
The rule stands; the predicted symptom does not.

Measured: with the usage frame moved after `[DONE]`, pi reported `usage: {input: 0, output: 0}` with `stopReason: "stop"`, no error, no retry and exit code 0, while the proxy recorded `137 / 11` correctly because `parse_past_done` was set. [V]

So the failure is not a crash but a silent zero on the harness side, which means the native-vs-proxy cross-check (§12) is what catches it.
This raises the value of that cross-check from "good practice" to "the only detector of an entire fault class", and it is a second, independent instance of the silent-undercount mode #30 documented.

Note the asymmetry that makes both rules coexist: on the Zen profiles the proxy **must** parse past `[DONE]`, because a `{"choices":[],"cost":"0"}` frame arrives there on every stream and is gateway-level rather than model-level (`docs/research/11-second-free-model.md:277-291`), while it must never **emit** a usage frame past `[DONE]`. [R]
Forwarding order is preserved byte-exactly, so a compliant proxy never has to choose.

### 6.3 A truncated stream must not be tidied up

Measured: when the upstream disconnected mid-stream and the reference proxy caught the exception and then wrote a well-formed terminal chunk, the client saw a **cleanly terminated, short** stream. [V]
Driven through pi the same injection produced four retried requests and exit code 0, with no usage captured on any of them. [V]

The proxy must therefore not close the client connection cleanly after an upstream disconnect: it aborts the downstream connection so the harness errors rather than accepting a truncated turn as a complete one.
Independently, an exception while reading upstream must never prevent the record from being written — an unrecorded request is strictly worse than a flagged one, because the run silently looks shorter.
The first version of the reference proxy lost the record entirely for this reason, which is how the requirement was found. [V]

## 7. Post-hoc segmentation: what is classified, what is flagged

The ticket asked which of these are automatic and which are held for review.
The split is by whether the signal is definitional or heuristic, and heuristics never silently drop data.

**Classified automatically**, because the rule is exact:

- `/v1/models`, `/api/tags` and `/api/show` are excluded from the step count by path.
- A request with a fault is excluded from `proxy_steps` and marks the run discardable.
- `tool_invocations` comes from `len(tool_calls)`, which is counted, not inferred.

**Classified automatically but reported as its own line**, because the rule is heuristic and the error direction matters:

- **Side-calls** — title generation, summarisation, classifiers — are marked by the conjunction of `has_tools == false`, a small `message_count` and a `max_tokens` below the run's configured value (`docs/research/04-measuring-tokens-steps-time.md:593`). [R] They are counted in `proxy_requests`, excluded from `proxy_steps`, and reported as `side_call_requests` so the exclusion is auditable rather than invisible. Both known instances are suppressible at the source — OpenCode with a fixed `--title`, pi has no title generation at all (`docs/research/10-pi-measurement-surface.md`) — so a non-zero count on a run configured to suppress them is itself a defect signal. [R]
- **Retries** are marked by identical `messages_hash` within a short window, verified in §6.1. [V] They are counted in `proxy_requests`, excluded from `proxy_steps`, and reported as `retry_requests`. The window is a stated parameter, not a magic number; **UNVERIFIED: what window length separates a retry from a legitimate identical request**, since no run long enough to produce a natural collision has been observed. Set it to the harness's own retry ceiling and record the value in the run manifest.

**Flagged for human review, never auto-classified:**

- **Compaction**, detected as a sudden drop in `prompt_tokens` between consecutive requests (`docs/research/04-measuring-tokens-steps-time.md:596`). [R] It is left to review because harnesses differ enormously in when they compact, that difference is a *result* rather than noise, and pi discards its compaction tokens from its own totals (`docs/research/10-pi-measurement-surface.md:579-607`) so the proxy's view is the only one there is. [R]
- Any request whose `faults` array is non-empty, since the run is discarded and the reason belongs in the log of what was thrown away.

## 8. Forwarding rules

These are correctness requirements, all non-negotiable, and most of them are one line each.

1. Forward **all paths and methods**, not only `/v1/chat/completions`; harnesses hit `/v1/models`, `/api/tags` and `/api/show` at startup and fail confusingly if those are missing (`docs/research/04-measuring-tokens-steps-time.md:617`). [R]
2. Write each upstream chunk to the client **before** parsing a copy of it.
3. Disable gzip and any buffering middleware; request `Accept-Encoding: identity` upstream so the body is parseable without decompression.
4. Buffer only a line remainder for SSE parsing, and forward raw bytes verbatim.
5. Preserve frame order byte-exactly; never reorder, never synthesise a frame, never omit `finish_reason` (#26). [R]
6. Timestamp request-sent, first-byte, first-content-delta and last-byte.
7. Append exactly one JSONL record per request, including for requests that failed.

## 9. Start-up canary

Before the first measured request of a run, the runner issues one canary completion per `(base_url, model)` pair in use and asserts the resolved profile against the observed response, rather than trusting the configuration file.
#31 requires this because configuration cannot see a gateway that substitutes models, and #28 requires it because the two contracts invert.

The canary asserts, in order:

1. HTTP 2xx **and** no `error` key in the body.
2. `response.model == requested_model`.
3. Usage is present without `stream_options` (Zen profiles) or absent without it (Ollama profile) — which is the discriminating observation between the two families.
4. The usage frame does or does not carry `choices[0].finish_reason`, matching `profile.usage_carries_finish_reason`.
5. A frame arrives after `data: [DONE]` on the Zen profiles.

A canary mismatch aborts the run before any measured request is issued.
The canary is cheap: a one-token completion, and on the free tiers it costs nothing but one request against the undocumented cap (#29).

## 10. Validation

### 10.1 The rig

The proxy is validated against a **mock OpenAI-compatible upstream that logs every byte and returns canned responses**, which #24 established as better than the `OLLAMA_DEBUG_LOG_REQUESTS` cross-check it replaced rather than as a workaround for its loss: with a mock upstream the request count, byte counts, token fields and frame ordering are all known in advance, so the proxy is asserted against exact ground truth instead of against a second imperfect observer.

The rig used on 2026-08-07 to validate *this specification* had three parts, and the same shape is what #16 must stand up:

- a mock upstream on `127.0.0.1:11436` logging every request line, header and body to `upstream.jsonl`, selecting a response profile or a fault injection from the requested model id;
- a reference proxy on `127.0.0.1:11435` implementing §2, §3, §5, §6 and §8, writing `records.jsonl`;
- **a real client**, pi 0.80.10 in `--mode json --print --no-session`, pointed at the proxy through an isolated `PI_CODING_AGENT_DIR` with the `models.json` recipe verified in `docs/research/10-pi-measurement-surface.md:109-136`. [R]

The reference proxy and mock are throwaway artefacts of this ticket and are deliberately not committed: #17 owns the real implementation, and a second copy of the instrument in the repo would be a second thing to keep correct.
What is committed is this specification, the assertion list in §10.2, and the measured results in §10.3.

Using a real client rather than a synthetic one is load-bearing.
Three of the findings below (§6.1, §6.2, §6.3) are about how a harness *reacts* to a malformed stream, and a synthetic client would have reported the malformation instead of hiding it.

### 10.2 Assertions the spike (#16) must pass before the proxy is trusted

Each is a mechanical check against the mock's own log, and each maps to a fault in §6.

1. `len(proxy_records) == len(mock_request_log)` — exact, not approximate.
2. Per request, `prompt_tokens` and `completion_tokens` equal the values the mock was configured to emit.
3. `proxy_steps` equals the number of injected terminal `finish_reason` frames.
4. On a Zen profile the usage frame is captured and **not** swallowed, and the terminal `finish_reason` survives it.
5. Parsing continues past `data: [DONE]` and captures the trailing `{"choices":[],"cost":"0"}` frame on the Zen profiles.
6. On the Ollama profile with a client that omits `include_usage`, the flag is forced, the usage frame is captured, and the client's byte stream contains no usage frame.
7. On the Ollama profile with a client that **sends** `include_usage`, the frame is captured and **forwarded** — the client's native usage must be non-zero (§3).
8. An injected non-2xx marks the run discardable and is not retried by the proxy.
9. An injected `error` payload arriving with HTTP 200 marks the run discardable.
10. An injected `model` echo mismatch marks the run discardable.
11. An injected missing `finish_reason` is flagged by the proxy's own check, and the resulting harness retries are visible as identical `messages_hash` values.
12. An injected usage frame after `[DONE]` is flagged, and the proxy's token figures remain correct while the harness's go to zero.
13. An injected mid-stream disconnect is classified as a failure, a record is still written, and the client connection is aborted rather than cleanly terminated.
14. `tool_schema_bytes` and `request_body_bytes` reproduce the #27 pi-vs-oh-my-pi baseline within the tolerance stated in §12 — 2,900 tool bytes exactly for pi, already reproduced independently twice (#26). [R]

### 10.3 What was measured on 2026-08-07

All rows below are **[V]**, from the rig in §10.1, with pi 0.80.10 as the client.

| Injection | Proxy record | Harness (pi) behaviour | Exit code |
|---|---|---|---|
| none, Zen shape | `prompt_tokens: 137`, `completion_tokens: 11`, `finish_reason: stop`, no faults | native usage `input 137 / output 11` — agrees exactly with the proxy | 0 |
| Ollama shape, client omits `include_usage` | flag forced, usage frame swallowed, `137 / 11` recorded | client stream contains no usage frame | 0 |
| Ollama shape, client sends `include_usage`, swallow applied unconditionally | `137 / 11` recorded | native usage **`0 / 0`** — the cross-check witness is destroyed | 0 |
| missing `finish_reason` | 4 records, `missing_finish_reason` on each, 4 identical `messages_hash` | 3x `stopReason: error, willRetry: true`, then give up | **0** |
| usage frame after `[DONE]` | `137 / 11` recorded, `usage_after_done` flagged | native usage **`0 / 0`**, `stopReason: stop`, no error | 0 |
| mid-stream disconnect | record written with `upstream_disconnect`, `stream_truncated`, `missing_finish_reason`, `no_usage_captured` | 4 attempts, no usage on any | **0** |
| HTTP 500 | `non_2xx` + `upstream_error_payload` | — (driven synthetically) | — |
| error payload with HTTP 200 | `upstream_error_payload` + `no_usage_captured` | — (driven synthetically) | — |
| `model` echo mismatch | `model_substituted` | client entirely oblivious | — |
| baseline, all runs | 11 proxy records vs 11 mock requests — exact match | — | — |

Two things in that table are worth stating separately because they change how results must be read.

**Exit code 0 appears on every failure row.**
This confirms `docs/research/06-headless-invocation.md`'s conclusion, folded into the map, that outcome classification must never use exit codes — and extends it: exit code 0 accompanies not merely a failed task but a *corrupted measurement*. [R][V]

**pi never rewrote its request.**
All 11 upstream requests carried `stream_options: {"include_usage": true}` as sent by pi, across 5 distinct model ids, so the force is idempotent on this arm exactly as #26 reported. [R][V]

## 11. Language and dependencies

~100-200 lines of async Python or Node, one HTTP client, no dependency of consequence, in one file that fits on a screen.
The size limit is a correctness argument rather than an aesthetic one: this instrument is audited by reading it, and #30's finding is that an aggregation bug producing plausible numbers survives exactly as long as nobody re-reads the code.

mitmproxy is **rejected** on the strength of its own documentation — buffered mode destroys time-to-first-token and streaming mode hides the body, which is a fork with no good branch (`docs/research/04-measuring-tokens-steps-time.md:620-624`). [R]
LiteLLM remains a fallback with two unresolved risks: SSE pass-through buffering is undocumented, and whether usage tracking requires Postgres was not established (`docs/research/04-measuring-tokens-steps-time.md:626-631`). [R]
Beyond those, LiteLLM performs its own request translation, and "silently alters the request" is the precise failure mode that would invalidate a harness comparison.

The reference implementation written for §10 used only the Python standard library (`http.server`, `http.client`, `json`, `hashlib`) and came to roughly 200 lines including the fault taxonomy, which puts the estimate on the record rather than leaving it as an assertion. [V]

## 12. The native cross-check is mandatory on every run

Both the harness's own aggregation and the proxy's count are recorded on **every** run and compared automatically, with a hard failure on divergence beyond a stated tolerance — not sampled, not eyeballed (#30). [R]

Tolerance: **zero** on request and step counts, which are integers the two sides either agree on or do not.
On token totals the tolerance is non-zero and per-arm, because the arms legitimately exclude different calls from their own arithmetic — pi discards compaction tokens (`docs/research/10-pi-measurement-surface.md:579-607`), Cline discards its summariser's, OpenCode loses title-generation entirely (`docs/research/04-measuring-tokens-steps-time.md:668-673`). [R]
The tolerance is therefore stated as a *direction and a mechanism*, not a percentage: the proxy total must be **greater than or equal to** the native total, and every unit of the gap must be attributable to a named excluded call.
An unexplained gap, or a native total exceeding the proxy total, fails the run.

§6.2 shows why the check cannot be dropped once things look stable: a native total of exactly zero, with the process exiting 0 and reporting `stopReason: stop`, is a state this instrument can produce.

## 13. Assumptions handed to #16 and #17

These are the open items; none blocks the spike from starting, and each has a defined place to be resolved.

1. **UNVERIFIED: the retry-detection window length** (§7). Resolve by setting it to each harness's own retry ceiling and recording the value in the run manifest.
2. **UNVERIFIED: how the proxy behaves under a real HTTPS upstream.** Zen is HTTPS and Cloudflare-fronted (`docs/research/08-free-hosted-model-tier.md:157-171`), while every measurement in §10.3 was against plaintext HTTP on loopback. [R] The proxy terminates nothing and originates a normal HTTPS client connection upstream, so no certificate machinery is expected — but "expected" is not "measured", and #16 measures it on its first real request.
3. **UNVERIFIED: whether the two selected models differ in any way the profile table does not already capture**, since §10 exercised synthetic profiles rather than the live gateway. The §9 canary is the mechanism that turns this from a risk into an abort.
4. **UNVERIFIED: the per-arm token tolerance values** (§12), which cannot be derived and must be measured once per arm on the calibration run.
5. The `t_first_content_delta` timestamp assumes the first non-empty `delta.content` is a meaningful boundary, which is false for a model that emits reasoning before content; on a reasoning-capable model the field measures time-to-first-*visible*-token, and the reasoning-first case is recorded rather than corrected.

---

## Summary

The measuring proxy is a single-file reverse proxy that forwards bytes verbatim, resolves a four-field behaviour profile from the **model id** rather than the base URL, forces `include_usage` only where the upstream requires it, swallows a usage frame only when it caused that frame, writes one JSONL record per request with the schema in §5, and marks a run discardable on any of eight faults without ever repairing one.
It is validated against a fault-injecting mock upstream driven by a real harness, against the fourteen assertions in §10.2.
Ten of those assertions were already exercised against pi 0.80.10 while writing this specification, and three of them changed it: swallowing must be conditional, a truncated stream must not be tidied up, and a misplaced usage frame produces a silent zero rather than a crash.
