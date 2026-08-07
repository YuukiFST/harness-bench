# 11 — The second free OpenCode Zen model: which one carries the robustness tier

Research ticket #11.
Question: which second free model on `https://opencode.ai/zen/v1` should run alongside the primary `deepseek-v4-flash-free`, so that a harness effect measured on one model can be shown to be a harness effect rather than a property of one checkpoint?

Companion document to `08-free-hosted-model-tier.md`, which established the gateway itself and picked the primary.
Facts already settled there — no-key access, unconditional streaming usage, the two SSE parser quirks, unhonoured `temperature`/`seed`, the 83-token prompt overhead, the undocumented daily cap — are cited rather than re-derived, except where this ticket depends on them, in which case they were re-run.

Retrieval date for every claim below: **2026-08-07**.

Sources read:
- `GET https://opencode.ai/zen/v1/models` (live gateway).
- `https://opencode.ai/docs/zen/` (published pricing and free-model table).
- `https://models.dev/api.json`, provider record `opencode`.
- `https://openrouter.ai/api/v1/models`, for published prices of the paid equivalents.
- `docs/research/08-free-hosted-model-tier.md` in this repository.

**Most of this document is first-party measurement.**
About forty live requests were issued against `https://opencode.ai/zen/v1/chat/completions` on 2026-08-07, with no API key, to settle questions no documentation answers.
Every such observation is labelled **PROBE** with the request shape given, so it can be re-run.
They describe the endpoint's behaviour on one day from one IP, which is weaker than a source file, and that weakness is part of the finding.

Where a fact could not be established against the source that owns it, it is marked **UNVERIFIED** with a note on what was checked.

---

## Headline

The pick is **`mimo-v2.5-free`** (Xiaomi MiMo-V2.5), with **`nemotron-3-ultra-free`** (NVIDIA Nemotron 3 Ultra) as the named fallback.

Three things came out of the probing that were not expected and that matter more than the choice itself.

**The gateway silently substitutes one model for another.**
Four requests for `ling-3.0-flash-free` returned bodies echoing `"model":"ling-3.0-tiny-free"` — a different, smaller model, with no error and no warning.
`08:359-360` recorded that no substitution was ever observed for the primary and concluded there was "no evidence of silent routing or fallback"; that conclusion was true of `deepseek-v4-flash-free` and is **false of the gateway as a whole**.

**The gateway is not one upstream, it is at least three, with three different response shapes.**
Usage field names, reasoning field names, tool-call id formats and error-message languages cluster into three distinct profiles across the free roster.
"Per-upstream parsing profile" was always the right idea and the wrong granularity: it has to be keyed by model, though it collapses to three families rather than nine.

**An upstream error can arrive with HTTP 200.**
`08:349` mandates discarding any run containing a non-2xx response; one observed failure carried a `200` status line with an `{"error":...}` body, so that rule is necessary and not sufficient.

On the narrow question: `mimo-v2.5-free` preserves both of the primary's SSE parser quirks exactly, calls tools correctly in single and parallel form, produced the best code of any candidate, and — once a system message is present, as it is in every real harness — carries a **smaller** fixed prompt overhead than the primary does.

---

## Section 1 — The live free roster on 2026-08-07

### 1.1 What the gateway returned

**PROBE.**

```
$ curl -s https://opencode.ai/zen/v1/models
```

returned `200` and 61 model ids, of which **nine** are free-tier:

```
big-pickle              deepseek-v4-flash-free   mimo-v2.5-free
ling-3.0-flash-free     ling-3.0-tiny-free       nemotron-3-ultra-free
north-mini-code-free    laguna-s-2.1-free        longcat-2.0-free
```

Records are bare, exactly as `08:399` describes: `{"id":"mimo-v2.5-free","object":"model","created":1786110301,"owned_by":"opencode"}`, with no version, no `limit` and no `cost`.
Two fetches minutes apart returned `created` values of `1786110293` and `1786110301`, confirming `08:400` — the timestamp is generated per response and is not a pin.

### 1.2 The docs still disagree with the gateway, on the same day, in the same way

`https://opencode.ai/docs/zen/` lists **eight** free models: the nine above minus `ling-3.0-flash-free`.

This is the identical discrepancy `08:84-85` recorded, unchanged after however long.
It is not a transient publishing lag; it is a standing gap between the published table and the served roster.
`08:85`'s instruction to trust the live endpoint stands, and Section 3.1 shows why trusting it is also not enough.

### 1.3 There is no paid sibling for any candidate

**PROBE.** Filtering the 61 live ids for each candidate's stem returns only the `-free` form:

| Stem | Live Zen ids |
|---|---|
| `mimo` | `mimo-v2.5-free` |
| `laguna` | `laguna-s-2.1-free` |
| `nemotron` | `nemotron-3-ultra-free` |
| `longcat` | `longcat-2.0-free` |
| `north` | `north-mini-code-free` |
| `deepseek` | `deepseek-v4-pro`, `deepseek-v4-flash`, `deepseek-v4-flash-free` |

The primary is the exception, not the rule.
`08:62` could compare the free and paid variants of the same model on the same gateway; for every candidate here, the paid equivalent has to come from a third party (Section 7).
The practical consequence is that `08:371-386`'s finding — that the free variant is a *different serving configuration* from the paid one — cannot be checked for any candidate, because there is nothing on Zen to check it against.

---

## Section 2 — Method

Each candidate got at most five small requests, all with no `Authorization` header, all through plain `curl`.

1. **Canary** — `{"messages":[{"role":"user","content":"x"}],"max_tokens":1}`, the same shape `08:246` used for the primary, to record the fixed prompt overhead and the usage-object field set.
2. **Parallel tools** — the `get_weather` tool from `08:272` with "What is the weather in Paris and in Tokyo? Use the tool."
3. **Single tool** — the same tool with one city, to check tool selection rather than just tool emission.
4. **Streaming** — `{"content":"Say OK"},"max_tokens":24,"stream":true` with **no `stream_options`**, to test unconditional usage and both SSE quirks.
5. **Coding** — write `parse_semver(s)` handling `1.2.3-beta.1+build5`, raising `ValueError` on invalid input, `max_tokens:1400`.

Two extra probes were run where a result demanded it: a `max_tokens:9000000` overflow to make the upstream leak its real context ceiling, and a scaling probe (100 × `"word "`) to separate flat overhead from proportional rewriting.

Deliberately **not** run: throughput benchmarking, cap-exhaustion, large prompts, or repetition loops.
The undocumented daily cap of `08:315-329` is a resource this project depends on.
No `429` was seen at any point.

---

## Section 3 — Two candidates are eliminated before capability is even reached

### 3.1 `ling-3.0-flash-free` is served by a different model — say this one loudly

**PROBE.** Four canary requests naming `ling-3.0-flash-free`:

| Attempt | HTTP | `model` echoed in the response |
|---|---|---|
| 1 | 200 | `ling-3.0-tiny-free` |
| 2 | 200 | `ling-3.0-tiny-free` |
| 3 | 200 | `ling-3.0-tiny-free` |
| 4 | 503 | `{"error":{"type":"server_error","message":"Error from provider (Console): Upstream request failed: Endpoint is unavailable."}}` |

A direct request for `ling-3.0-tiny-free` returned `prompt_tokens: 21` and the same `reasoning`/`reasoning_details` shape; so did every `ling-3.0-flash-free` request.
The substitution is not a display bug in the echo — the token accounting matches the smaller model too.

Three independent signals agree that this id is being retired underneath callers.
`models.dev` records `ling-3.0-flash-free` with `"status": "deprecated"` while `ling-3.0-tiny-free` has no such status.
`models.dev` also gives `ling-3.0-flash-free` a `release_date` of `2026-07-23` — **fifteen days** before this probe.
And the docs page never listed it at all (Section 1.2).

This is the concrete form of `08:402`'s warning that "the identifier `deepseek-v4-flash-free` can begin serving a different build … with no observable change at the API surface."
Here the surface *does* change — the `model` echo is honest — but only for a client that reads it.
**Mandatory consequence for the proxy: assert `response.model == requested_model` on every request, and fail the run on mismatch.**
That check costs nothing and is the only defence that exists.

### 3.2 `north-mini-code-free` is not serving

**PROBE.** Three canary requests across roughly twenty minutes, all identical:

```
HTTP 401
{"error":{"type":"server_error","message":"Error from provider (Console):
  Upstream request failed: [401] Provider returned error"}}
```

Note the shape: this is not the gateway's own `{"type":"error","error":{"type":"AuthError","message":"Missing API key."}}` from `08:133`.
The gateway accepted the unauthenticated request, forwarded it, and the **upstream** rejected it — Zen's own credential for Cohere is failing, or the free slot has been quietly withdrawn without leaving the roster.

`north-mini-code-free` was the strongest candidate on paper: `models.dev` describes it as a "Cohere coding model for practical software engineering and agentic edits", with `tool_call: true`, `structured_output: true`, 256k context and 64k output, and the ticket named it a plausible pick.
It cannot be evaluated, because it does not answer.

**UNVERIFIED: whether `north-mini-code-free` works with a real Zen API key.**
Checked: three unauthenticated attempts, all `401` from the upstream rather than from the gateway; the docs page still lists it as Free; `models.dev` does not mark it deprecated; and every other free model answered unauthenticated in the same session, so this is not a general auth change.
No Zen API key was available to distinguish "broken for everyone" from "broken for anonymous callers".
This is worth ten minutes with a real key before the fallback is invoked, because on documented capability it would otherwise be the best fit in the roster.

### 3.3 `big-pickle` is almost certainly the primary wearing a different name

**PROBE.** Side by side on identical requests:

| Signal | `deepseek-v4-flash-free` | `big-pickle` |
|---|---|---|
| Canary `prompt_tokens` | 84 | 84 |
| First reasoning token on `"x"` | `"We"` | `"We"` |
| Usage fields | `prompt_cache_hit_tokens`, `prompt_cache_miss_tokens`, `prompt_tokens_details.cached_tokens`, `completion_tokens_details.reasoning_tokens` | identical set |
| Reasoning field | `reasoning_content` | `reasoning_content` |
| Tool-call id shape | `call_00_<rand>` (`08:292`) | `call_00_ikL4wH20UrE45YDlvX7m7174`, `call_01_txp7LjlsDHxiR3euFADb7776` |
| Response `id` shape | UUID | UUID |

The zero-padded `call_00_` / `call_01_` sequence prefix is the distinctive shape `08:292` flagged as "non-OpenAI"; `big-pickle` reproduces it exactly, including the two-digit counter.
The 84-token canary matches to the token, and the `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens` pair appears on **no other free model** in the roster (Section 5.2).

`models.dev` describes `big-pickle` as an anonymous "Reasoning model for deliberate analysis, multi-step problem solving, and tool use", `open_weights: false`, `release_date: 2025-10-17`, 200k context, 32k output.
Anonymous stealth-model slots are conventionally a vendor evaluating an unreleased checkpoint.

**UNVERIFIED: whether `big-pickle` is literally `deepseek-v4-flash-free`.**
Checked: canary token count, first reasoning token, complete usage field set, reasoning field name, tool-call id format and response id format — all six match, and all six differ from every other candidate.
Not checked: nothing distinguishes "same model" from "same DeepSeek-family upstream at a different checkpoint", and `models.dev` gives them different context limits (200k/32k versus 200k/128k).
Either way it fails selection criterion 1 on the evidence available: the point is to vary the model family, and every observable says this is the same family behind the same serving stack.

`ling-3.0-tiny-free` is also set aside — `models.dev` gives it a `release_date` of `2026-08-06`, one day before this probe, and it is the substitution target of a model already being retired.
Its 32k output limit and "compact MoE" description put it below the capability floor of criterion 2 in any case.

---

## Section 4 — Tool calling at the wire

**All four surviving candidates call tools natively in OpenAI `tools` format, in both single and parallel form.**
This was verified, not inferred from `models.dev`'s `tool_call: true` flag, which is set for every free model including the two that cannot be reached.

### 4.1 Parallel call — "weather in Paris and in Tokyo"

**PROBE.** All four returned `finish_reason: "tool_calls"` with exactly two well-formed calls and valid JSON arguments.

| Model | Tool-call id shape | `index` | `content` alongside the calls | Latency |
|---|---|---|---|---|
| `mimo-v2.5-free` | `call_acefc93b6925417cb69ab8ae` (24 hex) | `0`, `1` | `null` | 14.8 s |
| `nemotron-3-ultra-free` | `call-6346183b-5116-...` (UUID) | `0`, `1` | `null` | 5.1 s |
| `laguna-s-2.1-free` | `chatcmpl-tool-1747640ecccd...` (vLLM style) | `0`, `1` | `null` | 3.9 s |
| `longcat-2.0-free` | `call_ed919246db9c4d8198880661` | **`null`, `null`** | `"I'll get the current weather for both Paris and Tokyo for you."` | 6.5 s |

Verbatim from `mimo-v2.5-free`:

```json
"finish_reason": "tool_calls",
"tool_calls": [
  {"index":0,"id":"call_18ded008ba94455285e27574","type":"function",
   "function":{"name":"get_weather","arguments":"{\"city\": \"Paris\"}"}},
  {"index":1,"id":"call_79daf621d6ed4f32b2a036a2","type":"function",
   "function":{"name":"get_weather","arguments":"{\"city\": \"Tokyo\"}"}}
]
```

**`longcat-2.0-free` emits `"index": null` on every tool call.**
`08:286` establishes that streaming argument fragments are keyed by `index`; a client that accumulates deltas into a map keyed by `index` gets one bucket for two calls, or a `null` key, depending on the language.
This is not a style difference, it is a protocol violation, and it is the first of three reasons longcat is unusable here.

### 4.2 Single call — tool selection, not just tool emission

**PROBE.** Same tool, "What is the weather in Paris? Use the tool.".
`mimo-v2.5-free`, `nemotron-3-ultra-free` and `laguna-s-2.1-free` each returned exactly one call with `{"city": "Paris"}` and `finish_reason: "tool_calls"`.
No spurious second call, no hallucinated tool name, no prose-instead-of-call.

### 4.3 The reasoning field name is not the same as the primary's

`08:293` records that the primary carries `reasoning_content` alongside `content`, and that `models.dev` documents this as `"interleaved": {"field": "reasoning_content"}`.

**PROBE.** On the wire, the free roster splits:

| Field carrying the reasoning trace | Models |
|---|---|
| `reasoning_content` | `deepseek-v4-flash-free`, `big-pickle`, `longcat-2.0-free` |
| `reasoning` **plus** `reasoning_details: [{"type":"reasoning.text","text":...,"format":"unknown","index":0}]` | `mimo-v2.5-free`, `nemotron-3-ultra-free`, `laguna-s-2.1-free`, `ling-3.0-*` |

**`models.dev` is wrong about this for `mimo-v2.5-free`**, which it annotates `"interleaved": {"field": "reasoning_content"}` while the endpoint sends `reasoning`.
That matters because harnesses read `models.dev` — a harness configured from that record will look for a field that never arrives and silently drop the reasoning trace.
It is one more instance of `08:389`'s conclusion that `models.dev` is community metadata and is not authoritative for this endpoint.

---

## Section 5 — Streaming, usage, and whether the two parser quirks hold

### 5.1 Usage arrives unconditionally on every candidate

**PROBE.** Streaming requests with **no `stream_options` field at all**.
All four candidates returned a populated `usage` object on the terminal chunk.
`08:180-186`'s finding generalises across the roster: the `include_usage` opt-in that `04:465-485` forces for Ollama is not needed anywhere on this gateway.

### 5.2 The usage object differs by model, and the primary's cache fields are the outlier

**PROBE.** Canary responses, verbatim field sets:

| Model | Usage fields beyond the standard three |
|---|---|
| `deepseek-v4-flash-free` | `prompt_cache_hit_tokens`, `prompt_cache_miss_tokens`, `prompt_tokens_details.cached_tokens`, `completion_tokens_details.reasoning_tokens` |
| `big-pickle` | identical to the above |
| `mimo-v2.5-free` | `prompt_tokens_details.{audio_tokens, cached_tokens, cache_write_tokens}`, `completion_tokens_details.{audio_tokens, reasoning_tokens}` |
| `nemotron-3-ultra-free` | identical to `mimo` |
| `laguna-s-2.1-free` | identical to `mimo` |
| `longcat-2.0-free` | `prompt_tokens_details.{audio_tokens, cached_tokens}` — **and no `completion_tokens_details` at all** |

Two consequences.

`08:211` treats `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens` as the gateway's gift.
It is not the gateway's, it is DeepSeek's, and it appears on no candidate.
The portable field is the OpenAI-standard `prompt_tokens_details.cached_tokens`, which **every** free model carries, including the primary.
The proxy should read that one and treat DeepSeek's pair as a bonus, not as the primary key.

**`longcat-2.0-free` reports no `completion_tokens_details`, so its reasoning tokens are unmeasurable.**
`08:667` lists `reasoning_tokens` among the metrics the hosted arm must report.
That is the second reason longcat is unusable.

### 5.3 Quirk 2 holds everywhere — the post-`[DONE]` frame is gateway-level

**PROBE.** Every streaming response from all four candidates ended:

```
data: {... "usage":{...}}

data: [DONE]

data: {"choices":[],"cost":"0"}
```

`08:226-239`'s quirk 2 is a property of the Zen gateway, not of any model.
The `cost` frame, the `"0"` string and the empty `choices` array are byte-identical across DeepSeek, Xiaomi, NVIDIA, Poolside and Meituan upstreams.
Nothing in the proxy needs to change for this.

### 5.4 Quirk 1 holds for three candidates and breaks for `longcat-2.0-free` — say this one loudly too

`08:221-224` established that Zen attaches usage to a normal-looking final chunk that **still carries `choices[0].finish_reason`**, the opposite of Ollama's empty-`choices` frame, and warned that swallowing it would destroy the proxy's own definition of a completed step (`04:588`).

**PROBE.** `mimo-v2.5-free`, verbatim, penultimate frame:

```
data: {"id":"gen-...","object":"chat.completion.chunk","model":"mimo-v2.5-free",
 "choices":[{"index":0,"finish_reason":"length","delta":{"role":"assistant","content":""}}],
 "usage":{"prompt_tokens":249,"completion_tokens":24,...}}
```

`nemotron-3-ultra-free` and `laguna-s-2.1-free` produce the same shape — `finish_reason` present, `choices[0]` present, `usage` attached.

**`longcat-2.0-free` does not.**
Verbatim, its last two content-bearing frames:

```
data: {..."choices":[{"index":0,"finish_reason":"length","logprobs":null,"delta":{}}]}

data: {..."choices":[],"usage":{"prompt_tokens":9,"completion_tokens":24,"total_tokens":33,...}}
```

LongCat splits `finish_reason` and `usage` across **two** frames and sends the usage frame with `choices: []` — that is the *Ollama* shape from `04:576`, arriving on a gateway whose documented behaviour is the opposite.

A proxy written against `08:642`'s rule ("do not swallow the usage frame, it carries `finish_reason`") would, on longcat, count the step boundary and the usage as one event when they are two, and would hit the `choices[0]` hazard `04:576-577` describes.
This is the third reason longcat is out, and it is the expensive one: **had longcat been the pick, the proxy's parsing profile would have had to become genuinely per-model rather than per-gateway.**
It is not the pick, and Section 9 shows the chosen model costs nothing structurally.

### 5.5 Three upstream profiles behind one gateway

The clustering in Sections 4.1, 4.3 and 5.2 is not coincidental.

| Profile | Models | Response `id` | Reasoning field | Cache fields | Error language |
|---|---|---|---|---|---|
| A — DeepSeek-native | `deepseek-v4-flash-free`, `big-pickle` | UUID | `reasoning_content` | `prompt_cache_hit/miss_tokens` | English, `invalid_request_error` |
| B — OpenRouter-normalised | `mimo-v2.5-free`, `nemotron-3-ultra-free`, `laguna-s-2.1-free`, `ling-3.0-*` | `gen-<unixtime>-<21 alnum>` | `reasoning` + `reasoning_details[]` | `cached_tokens`, `cache_write_tokens` | English, "use the context-compression plugin" |
| C — Meituan-native | `longcat-2.0-free` | 32-hex | `reasoning_content` | `cached_tokens` only | **Chinese**, `参数校验失败` |

**PROBE**, the evidence for profile B being OpenRouter specifically.
A `max_tokens: 9000000` overflow against `mimo-v2.5-free` returned:

> `Error from provider (Console): Upstream request failed: [400] This endpoint's maximum context length is 1048576 tokens. However, you requested about 9000001 tokens (1 of text input, 9000000 in the output). Please reduce the length of either one, or use the context-compression plugin to compress your prompt automatically.`

The `gen-<timestamp>-<id>` response-id format, the `reasoning_details[{type:"reasoning.text", format, index}]` schema, the `cache_write_tokens` field and the phrase "context-compression plugin" are all OpenRouter's normalisation layer.
Corroborating, `https://openrouter.ai/api/v1/models` carries exact context-length matches for the profile-B models:

| Zen id | Zen-leaked ceiling | OpenRouter counterpart | OpenRouter `context_length` |
|---|---|---|---|
| `nemotron-3-ultra-free` | 1,000,000 | `nvidia/nemotron-3-ultra-550b-a55b:free` | 1,000,000 |
| `laguna-s-2.1-free` | 262,144 | `poolside/laguna-s-2.1:free` | 262,144 |
| `ling-3.0-tiny-free` | not probed | `inclusionai/ling-3.0-tiny:free` | 262,144 |
| `north-mini-code-free` | unreachable | `cohere/north-mini-code:free` | 256,000 |

Note that OpenRouter's *paid* `nvidia/nemotron-3-ultra-550b-a55b` is listed at 512,288 context, not 1,000,000 — so Zen's ceiling matches the **free** OpenRouter endpoint specifically, which is a stronger fingerprint than a generic model-capability match.

**UNVERIFIED: that Zen routes profile-B models through OpenRouter.**
Checked: four independent format fingerprints (id shape, reasoning schema, cache field names, error copy) and four exact context-ceiling matches against OpenRouter's free endpoints.
Not checked: nothing in Zen's documentation, terms or headers names any sub-provider, and the error string says only "provider (Console)", which is the same opaque label `08:367` saw.
The inference is strong but it is an inference; what is *measured* and what actually matters is that three response profiles exist behind one base URL.

---

## Section 6 — Context windows, measured

`08:387-390` established that `models.dev`'s `limit` fields do not survive contact with the endpoint.
They do not survive here either, but there is a cheap way to make the upstream state its own limit.

**PROBE.** `{"messages":[{"role":"user","content":"hi"}],"max_tokens":9000000}` — one request per model, one token of input, no large prompt sent.

| Model | Upstream's own words | `models.dev` claim | Verdict |
|---|---|---|---|
| `mimo-v2.5-free` | "maximum context length is **1048576** tokens" | `context: 200000` | models.dev understates by 5x |
| `nemotron-3-ultra-free` | "maximum context length is **1000000** tokens" | `context: 1000000` | agrees |
| `laguna-s-2.1-free` | "maximum context length is **262144** tokens" | `context: 256000` | close, models.dev rounds |
| `longcat-2.0-free` | `/max_tokens: 9000000 is not less or equal to **131072**` | `output: 131072` | agrees on output; context not leaked |
| `deepseek-v4-flash-free` | "valid range of max_tokens is **[1, 393216]**" | `output: 128000` | models.dev understates by 3x |

Two things follow.

The primary's real output ceiling is **393,216**, not the 128,000 `models.dev` claims, and it matches DeepSeek's published 384K (`08:392`).
`08:381`'s table row is therefore wrong in the same direction as its context row, and the whole `limit` block should be treated as decorative.

Every candidate's context window is **far** beyond what an agentic loop with tool schemas needs.
The largest prompt any harness in this project will assemble is a system prompt, a handful of tool schemas and a growing transcript — tens of thousands of tokens at the extreme.
`08:504`'s conclusion holds unchanged: context control is lost and it does not matter, because the ceiling is unreachable.

---

## Section 7 — Fixed prompt overhead, and a 247-token surprise

### 7.1 The canary numbers

**PROBE.** `{"messages":[{"role":"user","content":"x"}],"max_tokens":1}` — one token of user content, no system message.

| Model | `prompt_tokens` | `prompt_tokens_details.cached_tokens` |
|---|---|---|
| `longcat-2.0-free` | 8 | 0 |
| `nemotron-3-ultra-free` | 17 | 0 |
| `ling-3.0-tiny-free` | 21 | 0 |
| `laguna-s-2.1-free` | 44 | 32 |
| `deepseek-v4-flash-free` | **84** | 0 |
| `big-pickle` | 84 | 0 |
| `mimo-v2.5-free` | **248** | **192** |

`08:246`'s 84 for the primary reproduced exactly, so the 83-token overhead is stable across at least the interval between the two documents.

The spread is the point: **there is no single "gateway overhead" figure.**
It runs from 7 tokens to 247 depending on the model, so `08:405`'s per-run canary must be recorded per *model*, not once per gateway.

### 7.2 The overhead is flat everywhere

**PROBE.** Same request with 100 × `"word "` as user content, which tokenises at one token per repetition (`08:243`):

| Model | canary (1 token) | 100 tokens | Delta | Flat overhead |
|---|---|---|---|---|
| `mimo-v2.5-free` | 248 | 348 | +100 | 247 |
| `nemotron-3-ultra-free` | 17 | 117 | +100 | 16 |
| `laguna-s-2.1-free` | 44 | 144 | +100 | 43 |

Perfectly additive in all three cases, so no candidate rewrites the prompt proportionally.

### 7.3 MiMo's 247 tokens are a vendor system prompt — and a client system message replaces it entirely

The 192 cached tokens on a one-token prompt were the tell: a fixed prefix long enough to be cached.

**PROBE.** Asked `mimo-v2.5-free` to repeat verbatim everything preceding the user message.
It returned, beginning verbatim:

```
**Identity**

- Your name is **MiMo-v2.5**.
- You were developed by the **Xiaomi LLM Core Team**.
- You have a **1M-token context window.**
...
# Response Style

Be warm, conversational, and respectful. ...
Use examples, metaphors, or thought experiments when they help explain an idea.
...
## Safety and Compliance

You are a **Chinese AI model** and must strictly comply with all applicable laws and
regulations of the **People's Rep[ublic of China]
```

This is a model self-report, which `08:254` correctly treats as weak evidence on its own.
Here it is corroborated by two independent measurements: the 192-token cached prefix, and the "1M-token context window" claim matching the 1,048,576 ceiling the upstream leaked in Section 6 — a number the model was not told in the prompt.

`08:257` ruled out a replaced system slot for the primary because adding a system message was additive (84 → 89).
**MiMo behaves the opposite way.**

**PROBE.** Adding `{"role":"system","content":"You are a terse coding agent."}` to the canary:

| Model | canary, no system message | canary + 7-token system message | Behaviour |
|---|---|---|---|
| `deepseek-v4-flash-free` | 84 | **92** | additive — no replaceable default |
| `mimo-v2.5-free` | 248 | **19** | **replacing** — the vendor prompt is a default |

Confirmed flat with the system message present: 19 for one token of user content, 119 for a hundred.

This inverts the finding completely.
Every real coding harness sends a system prompt — that is what a harness *is* — so the 247-token vendor preamble never appears in a benchmark run.
With a system message present, `mimo-v2.5-free` carries **73 fewer fixed tokens per request than the primary** (19 versus 92 on the same canary).

The operational requirement is that the archived canary must include a system message, or the recorded baseline swings by 229 tokens depending on a field the run may or may not set.

**Recommended canary for both tiers**, to be archived per run per `08:668`:

```json
{"messages":[{"role":"system","content":"You are a terse coding agent."},
             {"role":"user","content":"x"}],
 "max_tokens":1}
```

Expected `prompt_tokens`: **92** for `deepseek-v4-flash-free`, **19** for `mimo-v2.5-free`.
Any movement in either number means the chat template, the vendor prompt or the served build has changed.

---

## Section 8 — Capability, judged from a short real coding prompt

**PROBE.** "In Python, write a function `parse_semver(s)` that parses a semantic version string like `1.2.3-beta.1+build5` into a tuple `(major, minor, patch, prerelease, build)` with ints for the numbers and None for missing parts. Raise ValueError on invalid input. Code only." — `max_tokens: 1400`.

| Model | `finish_reason` | completion / reasoning tokens | Latency | Outcome |
|---|---|---|---|---|
| `mimo-v2.5-free` | `stop` | 1355 / 1100 | 40.2 s | **Correct.** Full SemVer 2.0.0 regex with leading-zero rules, named groups, `ValueError` on no-match |
| `laguna-s-2.1-free` | `stop` | 271 / 0 | 17.3 s | Functional. `rsplit` parsing, catches non-integer parts, but accepts leading zeros and does not validate prerelease grammar |
| `nemotron-3-ultra-free` | `length` | 1400 / **1441** | 47.2 s | **Failed.** Burned the entire budget reasoning; produced no code |
| `longcat-2.0-free` | `length` | 1400 / not reported | 34.7 s | **Failed.** Entire budget in `reasoning_content`; `content` absent |

MiMo's answer, verbatim and complete:

```python
import re

def parse_semver(s):
    pattern = r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:\-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    match = re.match(pattern, s)
    if not match:
        raise ValueError(f'Invalid semantic version: {s}')
    major = int(match.group('major'))
    minor = int(match.group('minor'))
    patch = int(match.group('patch'))
    prerelease = match.group('prerelease')
    build = match.group('build')
    return (major, minor, patch, prerelease or None, build or None)
```

**This is one prompt, and one prompt does not rank models.**
What it does establish, which is what criterion 2 actually asks, is that `mimo-v2.5-free` and `laguna-s-2.1-free` will not floor on a numbered-goal suite with partial credit, and that both reasoning-heavy candidates can consume a four-figure output budget on a fifteen-line function without emitting any.
That last point is a scheduling fact the suite has to absorb regardless of which model is chosen: **per-turn `max_tokens` must be generous on this tier, or reasoning models never reach the answer.**

**UNVERIFIED: relative coding capability of these models on anything resembling the real suite.**
Checked: one function-writing prompt per model, one attempt each, with `temperature` and `seed` known to be unhonoured (`08:513-521`) so even a repeat would not be a controlled comparison.
Published benchmark scores were not consulted, because the identifiers are Zen-specific and no vendor publishes scores for "the checkpoint Zen serves for free under this name".

---

## Section 9 — The defect that decides it: Nemotron duplicates its reasoning into `content`

This is the single fact that separates the recommendation from the fallback, so it was probed twice on two unrelated prompts.

**PROBE 1.** `nemotron-3-ultra-free`, the `parse_semver` prompt, `max_tokens: 1400`, `finish_reason: "length"`:

```
message keys : ['role', 'content', 'refusal', 'reasoning', 'reasoning_details']
len(content) : 5679
len(reasoning): 5679
content == reasoning : True
content[:120] : 'The user wants a Python function parse_semver(s) that parses a semantic
                 version string according to SemVer specification'
```

**PROBE 2.** Same model, "Prove carefully that sqrt(2) is irrational.", `max_tokens: 40`, `finish_reason: "length"`:

```
len(content) = 166   len(reasoning) = 166   identical = True
content = 'The user wants a careful proof that $\\sqrt{2}$ is irrational.\nI should provide
           the standard proof by contradiction.\nKey steps:\n1. Assume $\\sqrt{2}$ is'
```

**PROBE 3, the control.** Same model, "What is 2+2? Answer with the number only.", `max_tokens: 60`, `finish_reason: "stop"`:

```
content   = '4'
reasoning = 'The user is asking for the result of 2+2 and wants the answer to be just the number.'
identical = False
```

**PROBE 4, the counter-control.** `max_tokens: 40` on the sqrt(2) prompt for the other three candidates, all `finish_reason: "length"`:

| Model | `len(content)` | `len(reasoning)` | identical |
|---|---|---|---|
| `mimo-v2.5-free` | 0 | 185 | no |
| `laguna-s-2.1-free` | 0 | 176 | no |
| `longcat-2.0-free` | 0 | 143 | no |

So: **whenever `max_tokens` truncates `nemotron-3-ultra-free` mid-thought, its entire chain of thought is copied byte-for-byte into `content`.**
When the response completes normally the fields separate cleanly.
No other candidate does this.

The likely mechanism — stated as an inference, not a finding — is that Nemotron emits its reasoning inside `<think>` tags in the raw content stream, and the profile-B normalisation layer only moves that text out of `content` once the closing tag arrives.
Truncation means the closing tag never arrives.

**Why this is disqualifying rather than a curiosity.**
`06-headless-invocation.md:240` already flags that a model hitting its output cap constantly is the expected failure mode on the weak tier, and Section 8 measured Nemotron spending 1,441 reasoning tokens without finishing a fifteen-line function.
A truncated turn on this model therefore does not merely lose the answer — it hands the harness several kilobytes of chain-of-thought *as the assistant's message*.
The harness appends it to the transcript, `total_prefill_tokens` inflates on every subsequent step, and the trajectory diverges.
And it does so **by a different amount for each harness**, because each harness sets its own per-turn `max_tokens`.

That is precisely the artifact class this project exists to isolate: a model-level behaviour that presents as a harness difference, exactly as `08:347` describes for `429` storms.
Worse, unlike a `429`, it produces no error and no non-2xx status, so the run-discard rule of `08:349` never fires.

---

## Section 10 — Two operational findings that apply to both tiers

### 10.1 An upstream error can arrive with HTTP 200

**PROBE.** A canary against `nemotron-3-ultra-free` returned, with `curl -w "HTTP %{http_code}"` reporting **`HTTP 200`**:

```json
{"error":{"type":"server_error","message":"Error from provider (Console): Upstream request failed: [502] Upstream error from Nvidia: ResourceExhausted: Worker local total request limit reached (32/32)"}}
```

The same model answered normally on the next attempt seconds later, so this is a transient capacity condition, not an outage.
Errors were also seen with `HTTP 401` (`north-mini-code-free`), `HTTP 503` (`ling-3.0-flash-free`) and `HTTP 400` (the overflow probes), so the status line is *usually* right.

`08:349` requires discarding any run containing a non-2xx upstream response.
**That rule is necessary and not sufficient.**
The proxy must additionally treat any `200` body carrying a top-level `error` key as a failed request, and any SSE stream whose first frame is an error object likewise.

**UNVERIFIED: how often a `200`-with-error-body occurs, or which conditions produce it.**
Checked: one observed instance out of roughly forty probe requests, with the status code read from curl's own `%{http_code}` rather than from a header dump.
Not reproducible on demand, because it depends on upstream fleet saturation.
The mitigation is cheap and unconditional, so it should be implemented regardless of the frequency.

### 10.2 Free capacity is oversubscribed on at least one candidate

The `ResourceExhausted: Worker local total request limit reached (32/32)` message names a per-worker concurrency limit of 32 on NVIDIA's side, shared with every other free user.
`08:336` measured 12-way concurrency absorbed with no penalty against the primary and concluded arms could run in parallel.
That conclusion is model-specific; it was measured on profile A and does not transfer to profile B.

**UNVERIFIED: concurrency headroom for `mimo-v2.5-free`.**
Checked: nothing — no concurrency burst was run against any candidate, deliberately, to protect the daily cap.
This should be measured once, at low fan-out, before the tier is used in anger.

---

## Section 11 — Published price of the paid equivalent

Section 1.3 established that Zen carries no paid sibling for any candidate, so `08:481`'s method — read Zen's own price for the paid twin — is unavailable.
The nearest primary source is OpenRouter, which lists the same underlying models from their originating labs.

**Retrieved 2026-08-07 from `https://openrouter.ai/api/v1/models`.**
Prices in the API are USD per token; converted here to USD per 1M tokens.

| OpenRouter id | Input | Output | Context |
|---|---|---|---|
| `xiaomi/mimo-v2.5` | **$0.14** | **$0.28** | 1,050,000 |
| `xiaomi/mimo-v2.5-pro` | $0.435 | $0.87 | 1,050,000 |
| `nvidia/nemotron-3-ultra-550b-a55b` | $0.60 | $3.60 | 512,288 |
| `nvidia/nemotron-3-ultra-550b-a55b:batch` | $0.30 | $1.80 | 512,288 |
| `poolside/laguna-s-2.1` | $0.09 | $0.18 | 1,048,576 |
| `meituan/longcat-2.0` | $0.30 | $1.20 | 1,048,756 |
| `inclusionai/ling-3.0-flash` | $0.021 | $0.063 | 262,144 |

`xiaomi/mimo-v2.5` at **$0.14 / $0.28** is numerically identical to `deepseek-v4-flash`'s price (`08:462`), which is a convenient accident: a simulated-cost table for the two free tiers uses the same rate for both, and any cost difference between them is purely a token-count difference.

Three caveats, all material.

**This is a third-party price for a model Zen serves, not Zen's price.**
`08:482` already recorded Zen pricing `deepseek-v4-pro` at exactly 4x DeepSeek's own list price with no explanation, so Zen's markup is not predictable from the lab's price.
If Zen ever lists a paid `mimo-v2.5`, that figure supersedes this one.

**Xiaomi publishes two MiMo V2.5 tiers and Zen's id does not say which it serves.**
`mimo-v2.5-free`'s leaked ceiling of 1,048,576 matches both `xiaomi/mimo-v2.5` and `xiaomi/mimo-v2.5-pro`.
**UNVERIFIED: whether `mimo-v2.5-free` corresponds to MiMo-V2.5 or MiMo-V2.5-Pro.**
Checked: the leaked context ceiling (identical for both), the model's own self-report (which said "MiMo-v2.5", not "Pro", but is a self-report), and the Zen id string.
The base tier is the conservative assumption and is what the table above uses; if the Pro price is right, simulated cost triples.

**No cache-hit price applies.**
`08:475` computes simulated cost as `hit × cache_rate + miss × input_rate + output × output_rate` using DeepSeek's 50x cache discount.
Section 5.2 established that `mimo-v2.5-free` reports `prompt_tokens_details.cached_tokens` but OpenRouter publishes no separate cached-read rate for `xiaomi/mimo-v2.5`, so the second tier's cost must be computed flat: `prompt_tokens × 0.14 + completion_tokens × 0.28`.
Stating that asymmetry is required, because otherwise the two tiers' cost figures are computed by different formulas and are not comparable.

---

## Section 12 — Version pinning and withdrawal risk

### 12.1 No candidate is version-pinned at the identifier

`08:394-402` established this for the primary: DeepSeek publishes `DeepSeek-V4-Flash-0731` and Zen's id carries none of it.

Every candidate is the same or worse.

`nemotron-3-ultra-free` is the worst.
OpenRouter names the model `nvidia/nemotron-3-ultra-550b-a55b`, carrying the total and active parameter counts.
Zen's id drops both, so a swap from the 550B-A55B checkpoint to `nemotron-3-super-120b-a12b` would be invisible at the API surface — and `models.dev` records a `nemotron-3-super-free` that has already been deprecated, so the family demonstrably rotates within Zen.

`mimo-v2.5-free`, `laguna-s-2.1-free` and `longcat-2.0-free` at least carry a minor version in the identifier, so a jump to a new minor version would change the id and be caught by the `response.model` assertion of Section 3.1.
A silent rebuild *within* a minor version would not be caught by anything except the canary of Section 7.3.

### 12.2 Roster churn, measured by release date

`models.dev` `release_date` for each live free id, oldest first:

| Model | `release_date` | Age on 2026-08-07 | `models.dev` status |
|---|---|---|---|
| `big-pickle` | 2025-10-17 | ~10 months | live |
| **`mimo-v2.5-free`** | **2026-04-24** | **~3.5 months** | live |
| `nemotron-3-ultra-free` | 2026-06-04 | ~2 months | live |
| `north-mini-code-free` | 2026-06-09 | ~2 months | live (but 401 on the wire) |
| `longcat-2.0-free` | 2026-06-30 | ~5 weeks | live |
| `laguna-s-2.1-free` | 2026-07-21 | ~2.5 weeks | live |
| `ling-3.0-flash-free` | 2026-07-23 | ~2 weeks | **deprecated, and substituting** |
| `deepseek-v4-flash-free` | 2026-07-31 | ~1 week | live |
| `ling-3.0-tiny-free` | 2026-08-06 | 1 day | live |

Setting aside `big-pickle` (Section 3.3), **`mimo-v2.5-free` is the longest-lived free id in the roster by a factor of nearly two.**
It has survived while three complete cohorts arrived around it, and while `models.dev` accumulated deprecated Xiaomi predecessors — `mimo-v2-flash-free` (2025-12-16), `mimo-v2-omni-free` and `mimo-v2-pro-free` (both 2026-03-18).
So the Xiaomi *slot* on Zen has been continuously occupied across four generations while the *id* rotates roughly every two months, and the current occupant is already well past that median.

The counter-reading, stated honestly: 3.5 months is longer than the family's own rotation cadence, which could equally mean `mimo-v2.5-free` is *due* for replacement.
Either way the id has outlasted every alternative on offer.

`laguna-s-2.1-free` carries a specific warning.
It was released two days before `ling-3.0-flash-free`, which is in the same intake cohort and is already deprecated and silently substituting fifteen days later.
That cohort's demonstrated half-life is very short.

### 12.3 The docs' own language ranks the risk

`https://opencode.ai/docs/zen/`, retrieved 2026-08-07, attaches a different sentence to different free models:

| Model | Verbatim statement |
|---|---|
| `mimo-v2.5-free` | "During its free period, collected data may be used to improve the model." |
| `laguna-s-2.1-free` | "During its free period, collected data may be used to improve the model." |
| `longcat-2.0-free` | "During its free period, collected data may be used to improve the model." |
| `north-mini-code-free` | "Do not submit personal or confidential data." |
| **`nemotron-3-ultra-free`** | **"Trial use only — do not submit personal or confidential data."** |
| `big-pickle` | "Free on OpenCode for a limited time." |

`mimo-v2.5-free` gets the same sentence as the primary (`08:67`), which is the mildest of the set.
`nemotron-3-ultra-free` is the only model in the roster labelled **"Trial use only"**, which is a stronger disclaimer than "for a limited time" and points the same direction as the `ResourceExhausted` capacity error of Section 10.1.

`08:73`'s data caveat applies unchanged to whichever model is picked: nothing confidential goes through this tier, and the benchmark's synthetic public prompts are the only acceptable payload.

---

## Section 13 — Scorecard

| | `mimo-v2.5-free` | `nemotron-3-ultra-free` | `laguna-s-2.1-free` | `longcat-2.0-free` |
|---|---|---|---|---|
| Family vs DeepSeek | Xiaomi — different lab, different checkpoint | NVIDIA — maximally different | Poolside — different, coding-specialised | Meituan — different |
| Single tool call | pass | pass | pass | not probed |
| Parallel tool calls | pass | pass | pass | pass, but `index: null` |
| Streaming usage unconditional | yes | yes | yes | yes |
| Quirk 1 (usage on `finish_reason` chunk) | **holds** | **holds** | **holds** | **BREAKS** — `choices: []` |
| Quirk 2 (frame after `[DONE]`) | holds | holds | holds | holds |
| `reasoning_tokens` reported | yes | yes | yes | **no** |
| Reasoning field | `reasoning` + `reasoning_details` | same | same | `reasoning_content` |
| Measured context ceiling | 1,048,576 | 1,000,000 | 262,144 | ≥ output 131,072 |
| Canary `prompt_tokens` (no system msg) | 248 | 17 | 44 | 8 |
| Canary `prompt_tokens` (with system msg) | **19** | not measured | not measured | not measured |
| Coding probe | **correct** | failed (budget exhausted) | functional, loose | failed (budget exhausted) |
| Reasoning leaks into `content` on truncation | no | **YES** | no | no |
| Paid equivalent | $0.14 / $0.28 | $0.60 / $3.60 | $0.09 / $0.18 | $0.30 / $1.20 |
| Id age on 2026-08-07 | ~3.5 months | ~2 months | ~2.5 weeks | ~5 weeks |
| Docs disclaimer | standard | **"Trial use only"** | standard | standard |

---

## Recommendation

**Second tier: `mimo-v2.5-free`.**

**The single fact that decides it:** `nemotron-3-ultra-free` — the only candidate that beats MiMo on family distance from DeepSeek — copies its **entire chain of thought byte-for-byte into `content` whenever `max_tokens` truncates it mid-thought** (Section 9, reproduced on two unrelated prompts, with a clean control and a three-model counter-control).
Since each harness sets its own per-turn `max_tokens`, that defect injects a different amount of chain-of-thought into the transcript for each harness, inflating prefill on every subsequent step — a model-level behaviour that presents as a harness difference, produced silently, with a `200` status and no error to discard the run on.
`mimo-v2.5-free` leaves `content` empty under identical truncation.

Supporting facts, in the order of the stated criteria:

1. **Different enough.** Xiaomi MiMo-V2.5 is a different lab, a different pretraining corpus and a different serving profile from DeepSeek V4 Flash — profile B versus profile A in Section 5.5, with a different reasoning field, a different usage field set and a different tool-call id format. Honest caveat: Nemotron would have been a *more* distant second model, and that distance is what it lost.
2. **Capable enough not to floor.** It was the only candidate to produce a correct, spec-complete `parse_semver` (Section 8), and it did so within budget with `finish_reason: "stop"`. One prompt is not a ranking, but it clears the criterion as written.
3. **Least likely to be withdrawn.** At ~3.5 months its identifier is the longest-lived free id in the roster apart from the anonymous `big-pickle` (Section 12.2), and it carries the mildest of the docs' disclaimers — the same sentence as the primary, not Nemotron's "Trial use only" (Section 12.3).

Two facts that emerged as bonuses rather than criteria: with a system message present it carries **73 fewer fixed tokens per request than the primary** (19 versus 92, Section 7.3), and its paid equivalent prices at **$0.14 / $0.28 per 1M** — identical to `deepseek-v4-flash`, so both tiers share one rate in the simulated-cost table (Section 11).

**Named fallback: `nemotron-3-ultra-free`.**
It lost on the `content` duplication of Section 9 and nothing else; on family distance, prompt overhead (17 tokens) and context (1M) it is the stronger choice.
It becomes viable if either the duplication is fixed upstream, or the suite guarantees that no turn is ever truncated by `max_tokens` — which Section 8's 1,441-reasoning-token measurement suggests would need a very large per-turn budget and is not a guarantee worth making.
Its secondary marks against it are the `ResourceExhausted (32/32)` capacity error, the "Trial use only" disclaimer, and an identifier that hides the parameter count OpenRouter publishes.

**Third, and worth reconsidering only if MiMo is withdrawn: `laguna-s-2.1-free`.**
It is clean on every protocol test, by far the fastest (3.9 s for a parallel tool call, 17.3 s for the coding prompt) and the only purpose-built agentic coding model that actually answers.
It lost on two things: its `parse_semver` was the weakest of those that finished, accepting leading zeros and not validating prerelease grammar; and it belongs to the same two-day intake cohort as `ling-3.0-flash-free`, which was deprecated and silently substituted within fifteen days (Section 3.1).

**Excluded, with reasons:** `longcat-2.0-free` breaks quirk 1 and reports no `reasoning_tokens` (Sections 5.2, 5.4); `north-mini-code-free` returns `401` from its upstream on every attempt (Section 3.2); `ling-3.0-flash-free` serves a different model (Section 3.1); `ling-3.0-tiny-free` is one day old and is that substitution's target; `big-pickle` matches the primary on all six identity fingerprints (Section 3.3).

**One check before wiring anything:** re-probe `north-mini-code-free` with a real Zen API key.
On documented capability — a Cohere model built for "practical software engineering and agentic edits", 256k context, `structured_output: true` — it would beat every candidate here, and the only thing standing in its way is an upstream `401` that may be specific to anonymous callers.

---

## Cost of this choice to the proxy

**Structurally, nothing. Two field-name additions, both of which simplify the existing code.**

**No change to the SSE state machine.**
`mimo-v2.5-free` reproduces both of the primary's parser quirks exactly (Sections 5.3, 5.4): usage attached to a chunk that still carries `choices[0].finish_reason`, and a `{"choices":[],"cost":"0"}` frame after `data: [DONE]`.
`08:642-643`'s two mandatory proxy rules — do not swallow the usage frame, do not treat `[DONE]` as end-of-stream — apply unchanged to both tiers.
Streaming usage arrives without `stream_options`, so `08:626`'s conclusion that the `04:574` request rewrite is not load-bearing holds too.

**Change 1 — read the portable cache field.**
The primary's `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens` pair is DeepSeek's, not the gateway's, and appears on no other free model (Section 5.2).
The proxy should key cache accounting on `prompt_tokens_details.cached_tokens`, which both tiers carry, and treat DeepSeek's pair as an optional extra.
This is a simplification: one field instead of a per-model branch.
Note the consequence for `08:475`'s cost formula — the split-rate calculation applies only to the DeepSeek tier, because no separate cached-read rate is published for MiMo (Section 11).

**Change 2 — accept two reasoning field names.**
The primary sends `reasoning_content`; MiMo sends `reasoning` plus a `reasoning_details` array (Section 4.3).
If the proxy only counts tokens this is irrelevant, since `completion_tokens_details.reasoning_tokens` is present on both.
If it records assistant text — and `08:293` warns that a harness concatenating all string fields of a delta produces garbage — it must know both names, and must not trust `models.dev`, which annotates MiMo with the wrong one.

**Two new disciplines, neither MiMo-specific, both cheap and both mandatory:**

- **Assert `response.model == requested_model` on every request** and fail the run on mismatch. Section 3.1 caught the gateway serving `ling-3.0-tiny-free` for `ling-3.0-flash-free` three times out of four. Nothing else detects this.
- **Treat a `200` response whose body carries a top-level `error` key as a failed request.** Section 10.1 observed exactly that. `08:349`'s non-2xx discard rule does not fire on it.

**What was avoided.**
Had `longcat-2.0-free` been the pick, the proxy's parsing profile would have had to become genuinely per-model: its usage frame carries `choices: []` — the Ollama shape from `04:576` — so the step-boundary logic and the usage-extraction logic would need separate code paths per model within the same gateway, plus a `null`-safe tool-call `index` accumulator, plus a fallback for absent `completion_tokens_details`.
That cost is real and it is not being paid.

The one thing that must become per-model regardless of this choice is the **canary baseline**, since fixed prompt overhead ranges from 7 to 247 tokens across the roster (Section 7.1).
Archive `prompt_tokens` for the Section 7.3 canary — expected **92** for `deepseek-v4-flash-free` and **19** for `mimo-v2.5-free` — once per run per model, so a silent model or template swap is detectable after the fact, per `08:668`.

---

## Summary of what could not be established

- **Whether `north-mini-code-free` works with a real Zen API key.** Three unauthenticated attempts, all `401` from the upstream rather than from the gateway, while every other free model answered unauthenticated in the same session. No key was available. This is the highest-value open item, because on documented capability it would outrank the recommendation.
- **Whether `big-pickle` is literally `deepseek-v4-flash-free` or another checkpoint on the same DeepSeek stack.** Six identity fingerprints match exactly and all six differ from every other candidate; `models.dev` gives them different output limits. Either reading disqualifies it under criterion 1.
- **Whether `mimo-v2.5-free` serves MiMo-V2.5 or MiMo-V2.5-Pro.** The leaked 1,048,576 ceiling matches both. The model's self-report says "MiMo-v2.5" but is a self-report. The base-tier price is used in Section 11 as the conservative assumption; the Pro price would triple simulated cost.
- **That Zen routes profile-B models through OpenRouter.** Four format fingerprints and four exact free-endpoint context matches all agree, but no Zen documentation, header or error string names a sub-provider — only the opaque label "provider (Console)" that `08:367` also saw.
- **How often an upstream error arrives with `HTTP 200`, and under what conditions.** One instance in roughly forty probe requests, not reproducible on demand because it tracks upstream fleet saturation. The mitigation is unconditional, so the frequency does not change what the proxy must do.
- **Concurrency headroom on `mimo-v2.5-free`.** Deliberately not probed, to protect the daily cap. `08:336`'s 12-way result was measured on profile A and does not transfer; profile B produced a `ResourceExhausted: 32/32` error on a *single* request to a sibling model.
- **Relative coding capability on anything resembling the real suite.** One prompt per model, one attempt each, with `temperature` and `seed` known to be unhonoured so a repeat would not be controlled either. Enough to clear criterion 2's "will not floor"; not enough to rank.
- **Whether `mimo-v2.5-free` honours `temperature`, `seed` or `reasoning_effort`.** Not probed. `08:513-527` established the primary does not, and profile B is a different upstream, so the finding does not automatically transfer in either direction. `models.dev` records `reasoning_options: []` for MiMo, meaning no documented reasoning control at all — which if true is a *smaller* loss than the primary's, since there is nothing to silently ignore.
- **`longcat-2.0-free`'s context ceiling.** The overflow probe hit its `max_tokens ≤ 131072` guard before reaching a context check, so only the output limit was leaked. Moot, since it is excluded.
- **Whether any harness tolerates the `reasoning` / `reasoning_details` shape.** As in `08:295`, only raw HTTP was tested; nothing was executed through OpenCode, PI, oh-my-pi or Cline. MiMo's shape differs from the primary's, so this gap is now two-shaped rather than one.

The one that would change the recommendation is **`north-mini-code-free` with a real key**.
Everything else either confirms MiMo or bears on the fallback.
