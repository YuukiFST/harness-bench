# 08 — A free hosted OpenAI-compatible tier: OpenCode Zen and DeepSeek V4 Flash Free

Research ticket #8.
Question: can a free hosted OpenAI-compatible endpoint — specifically OpenCode Zen's free tier and its DeepSeek V4 Flash model — serve as a second model tier alongside the local LFM2.5-2.6B / Ollama arm, without breaking the proxy measurement design of ticket #4?

Retrieval date for every claim below: **2026-08-07**.

Sources read:
- `https://opencode.ai/docs/zen/`, and its source at `packages/web/src/content/docs/zen.mdx` on the `dev` branch of `github.com/anomalyco/opencode`.
- `https://opencode.ai/docs/models/` and `https://opencode.ai/docs/go/`.
- `https://opencode.ai/legal/terms-of-service`.
- `https://models.dev/api.json`, provider record `opencode`.
- `https://api-docs.deepseek.com/quick_start/pricing`.
- GitHub issues `anomalyco/opencode#16844`, `#28055`.

**A large share of this document is first-party measurement rather than documentation.**
Roughly fifty live requests were issued against `https://opencode.ai/zen/v1/chat/completions` on 2026-08-07 to settle questions the documentation does not answer.
Those observations are labelled as such, with the request shape given, so they can be re-run.
They describe the endpoint's behaviour on one day from one IP, which is a weaker guarantee than a source file, and that weakness is itself part of the finding.

Where a fact could not be established against the source that owns it, it is marked **UNVERIFIED** rather than filled in by inference.

---

## Headline

The proposal does **not** collapse to a single arm.
The endpoint is a plain, generic, OpenAI-compatible HTTPS API at `https://opencode.ai/zen/v1`, and the free DeepSeek model answered a `curl` request with **no API key, no account and no OpenCode process anywhere in the picture**.
Any harness that accepts a base URL can reach it, which includes all three of OpenCode, PI and Cline.

The problem is elsewhere, and it is worse than a reachability problem.
The endpoint is undocumented in exactly the places a benchmark depends on: there is a real, enforced, numerically unpublished free-usage cap; sampling parameters are not honoured, so `temperature: 0, seed: 42` produced two different answers in three attempts; the served context window and reasoning configuration differ between the free and paid variants of the *same* model; and the free tier is described by its own vendor as available "for a limited time".
Token counting, which was the hard problem against Ollama, is the one thing that gets *easier*.

---

## Section 1 — What OpenCode Zen is, and what is actually free

### 1.1 What it is

`zen.mdx` opens with: "OpenCode Zen is a list of tested and verified models provided by the OpenCode team."
It is a hosted AI gateway, not a model: "OpenCode Zen is an AI gateway that gives you access to these models."
It is explicitly optional to OpenCode itself — "It's **completely optional** and you don't need to use it to use OpenCode."

The stated goals section is directly load-bearing for this ticket.
Goal 4 reads verbatim: "**No lock-in** by allowing you to use it with any other coding agent. And always let you use any other provider with OpenCode as well."
That is the vendor stating in its own documentation that the gateway is meant to be driven from non-OpenCode clients.

### 1.2 The free models

The pricing table in `zen.mdx` lists eight models at `Free` for input, output and cached read:

```
Big Pickle, DeepSeek V4 Flash Free, MiMo-V2.5 Free, Laguna S 2.1 Free,
Ling-3.0-tiny Free, LongCat-2.0 Free, North Mini Code Free, Nemotron 3 Ultra Free
```

**DeepSeek V4 Flash Free is confirmed present.**
Its exact gateway identifier is `deepseek-v4-flash-free`, its endpoint is `https://opencode.ai/zen/v1/chat/completions`, and its documented AI SDK adapter is `@ai-sdk/openai-compatible`.
In an OpenCode config the same model is addressed as `opencode/deepseek-v4-flash-free`, per the note that "The model id in your OpenCode config uses the format `opencode/<model-id>`".

Note that a separate **paid** `deepseek-v4-flash` also exists at `$0.14` input / `$0.28` output per 1M tokens.
The two are different identifiers with different serving configurations (Section 6.2), and confusing them would silently change the experiment.

### 1.3 "Free" means: no charge, no published quota, and no guarantee of continuation

The docs state the terms in one sentence, repeated per model: "DeepSeek V4 Flash Free is available on OpenCode for a limited time. The team is using this time to collect feedback and improve the model."

There is **no unlimited claim, no trial-credit figure, and no published rate limit anywhere on the page.**
"Free" here means zero price per token, not zero restriction — see Section 5.

The privacy section adds the cost that is actually being paid: "During its free period, collected data may be used to improve the model."
For a benchmark this is tolerable, since the task prompts are synthetic and public, but it must be stated in the writeup, and it means the free tier cannot be used on any task containing real repository content the reader cares about.

### 1.4 Free access can be withdrawn, and the terms say so

Two independent statements cover this.

`zen.mdx` says the free models are available "for a limited time" with no end date given.

The Terms of Service, under "Will OpenCode ever change the Services?", says: "We're always trying to improve our Services, so they may change over time. We may suspend or discontinue any part of the Services, or we may introduce new features or impose limits on certain features or restrict access to parts or all of the Services."

There is also a live demonstration that the model roster churns.
`zen.mdx` lists eight free models; `GET https://opencode.ai/zen/v1/models` returned nine, the extra one being `ling-3.0-flash-free`, which appears in the live endpoint and in `models.dev` but not in the published table.
The docs and the live gateway disagreed on the same day.

**This is the single largest reproducibility objection to the whole proposal** and it is dealt with in Section 9.4, not here.

---

## Section 2 — The decisive question: reachability from a non-OpenCode harness

**Settled affirmatively, empirically, in the strongest possible way.**

### 2.1 There is a documented generic base URL

`models.dev/api.json` carries a provider record for the gateway, reproduced verbatim from the fetched JSON:

```json
{
  "id": "opencode",
  "env": ["OPENCODE_API_KEY"],
  "npm": "@ai-sdk/openai-compatible",
  "api": "https://opencode.ai/zen/v1",
  "name": "OpenCode Zen",
  "doc": "https://opencode.ai/docs/zen"
}
```

That is a complete provider definition for any OpenAI-compatible client: base URL `https://opencode.ai/zen/v1`, bearer key from `OPENCODE_API_KEY`, adapter `@ai-sdk/openai-compatible`.
`zen.mdx` independently documents the per-model endpoint `https://opencode.ai/zen/v1/chat/completions` for the whole DeepSeek/MiniMax/GLM/Kimi family.

Nothing about it is OpenCode-specific.
There is no custom header, no signing, no client attestation and no proprietary transport.

### 2.2 The free model needs no API key at all

This is the finding that closes the question, and it was not expected.

```
$ curl -s -X POST https://opencode.ai/zen/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model":"deepseek-v4-flash-free","messages":[{"role":"user","content":"hi"}]}'
```

returned `HTTP/1.1 200 OK` and a well-formed `chat.completion` body, with **no `Authorization` header present**.

The auth behaviour is precisely three-valued and was probed for each case:

| Request | Result |
|---|---|
| Free model, no `Authorization` header | `200`, full completion |
| Paid model (`deepseek-v4-flash`), no header | `401`, `{"type":"error","error":{"type":"AuthError","message":"Missing API key."}}` |
| Free model, `Authorization: Bearer sk-bogus-000` | `401` |

The third row matters more than it looks.
Sending *no* key succeeds where sending a *wrong* key fails, so a harness that unconditionally emits an `Authorization` header — which most do, since most treat the API key as mandatory — must be given a real Zen key or be configured to omit the header entirely.
An empty-string key is untested.
**UNVERIFIED: whether an empty `Authorization: Bearer ` header is treated as absent or as invalid.**
This is a five-minute check and should be run before wiring any harness, because "harness A sends a placeholder key and gets 401 while harness B omits it and gets 200" is exactly the kind of asymmetry that would be misread as a harness difference.

### 2.3 Pointing the three harnesses at it

All three are already known from ticket #6 to accept a custom OpenAI-compatible base URL, and the required adapter is the same one they use for Ollama.

**OpenCode** — the provider block documented at `06-headless-invocation.md:76-79` takes `"npm": "@ai-sdk/openai-compatible"` and `"baseURL"`, which is exactly the adapter `zen.mdx` names for this model family.
Alternatively Zen is a first-class provider, so `opencode/deepseek-v4-flash-free` works with no custom provider block at all.

**PI** — `06-headless-invocation.md:295-298` records `"baseUrl"` plus `"api": "openai-completions"`, and `:312` confirms `openai-completions` is the correct value for Chat Completions endpoints.
The compat flags recommended there for Ollama (`supportsDeveloperRole: false`, `supportsReasoningEffort: false`, `:311`) were aimed at local servers and should be **re-evaluated rather than copied** for Zen, since this gateway does accept `reasoning_effort` (Section 9.2).

**Cline** — `06-headless-invocation.md:521,528-534` establishes `cline auth --provider openai-compatible --baseurl <url>`, with `--baseurl` gated to the `openai-compatible` and `openai-native` providers only.
`openai-compatible` is the right target here, and the `-P ollama` native route from `04-measuring-tokens-steps-time.md:371-374` is irrelevant and must not be used, since it rewrites the URL to `/api`.

**oh-my-pi** — **UNVERIFIED.** It does not appear anywhere in `docs/research/`, so its provider configuration surface has never been established in this project. It is not a Zen-specific gap; it is an open gap for the local Ollama arm too.

### 2.4 Transport: HTTPS, Cloudflare-fronted, and proxyable

The endpoint is HTTPS and Cloudflare-fronted; every response carried `Server: cloudflare` and a `CF-RAY` header.

Nothing in the auth scheme obstructs the ticket #4 proxy design.

- **No mTLS.** Every request above completed with a stock `curl` and no client certificate.
- **No host-header pinning problem.** Auth is a bearer token in a header, or nothing at all for the free model, so a forwarding proxy needs only to set `Host: opencode.ai` — which every HTTP client does by default when the upstream URL is `https://opencode.ai/...`.
- **Plain HTTP is accepted on the front door.** `curl --max-redirs 0 http://opencode.ai/zen/v1/models` connected on port 80 and returned `200 OK` rather than a redirect. This is incidental — the proxy should still speak HTTPS upstream — but it removes any doubt that a plaintext-HTTP local listener terminating and re-originating over TLS is viable.

The ticket #4 topology therefore survives intact: harnesses talk plaintext HTTP to `http://localhost:11435/v1`, and the proxy forwards to `https://opencode.ai/zen/v1` over TLS.
The only new proxy requirement is upstream TLS, which is one line in any HTTP client.

---

## Section 3 — Measurement fidelity at the wire

This is the section where the hosted endpoint is *better* than local Ollama, and it is worth saying so plainly before the rest of the document takes it apart.

### 3.1 Usage is returned unconditionally, including on streams

`04-measuring-tokens-steps-time.md:465-485` establishes that Ollama emits no usage on a stream unless the client sends `stream_options: {"include_usage": true}`, and that this single fact forced the proxy to rewrite requests.

**Zen does not have this problem.**
Two streaming requests were issued, identical except for the flag:

- With `"stream_options":{"include_usage":true}` — final content chunk carried a populated `usage` object.
- With the flag entirely absent — final content chunk carried a **populated `usage` object anyway**.

Every intermediate chunk carries `"usage":null`, and the terminal chunk carries the real numbers, so the OpenAI convention of "null except on the last chunk" is respected but the opt-in is not required.

Consequence: against this endpoint the proxy's mandatory request rewrite from `04:574` becomes **unnecessary**.
Sending the flag anyway is harmless and keeps one code path, but the fallback position is stronger here — a purely passive proxy would still see every token count, which it cannot do against Ollama.

### 3.2 The usage object is richer than Ollama's

Observed verbatim on a non-streaming response:

```json
"usage": {
  "prompt_tokens": 84,
  "completion_tokens": 18,
  "total_tokens": 102,
  "prompt_cache_hit_tokens": 0,
  "prompt_cache_miss_tokens": 84,
  "prompt_tokens_details": {"cached_tokens": 0},
  "completion_tokens_details": {"reasoning_tokens": 8}
}
```

Compare `04:455-460`, where Ollama's `Usage` struct has exactly three fields and no cache or reasoning detail at all.

Three fields are new and all three are useful:

- **`prompt_cache_hit_tokens` / `prompt_cache_miss_tokens`**, plus the OpenAI-standard `prompt_tokens_details.cached_tokens`. `04:508-509` records the per-request prompt-cache hit count as *unobtainable* from any Ollama HTTP surface. Here it is handed over directly, which makes cache behaviour a measurable harness property rather than a blind spot.
- **`completion_tokens_details.reasoning_tokens`**, which matters because this model thinks by default and reasoning is a real and large share of output (Section 9.2).

There is also a **non-standard `cost` sibling of `usage`** on the response body, observed as `"cost":"0"` — a string, not a number. It is free money on the free tier and therefore always `"0"`, but it is presumably the real billed figure on paid models, which would make the gateway self-reporting for the paid arms.
**UNVERIFIED: whether `cost` is populated with a real figure on a paid model**, since no API key was available to test one.

### 3.3 Two SSE quirks that will break a naive parser

Both were reproduced on every streaming request.

**Quirk 1 — the terminal usage chunk has `choices` populated, not empty.**
Ollama forces `finishChunk.Choices = []` when emitting usage (`04:576`), and `04:576-577` warns that a harness doing `chunk.choices[0].delta` without a length check will throw, which is why the proxy was designed to swallow the frame.
Zen instead attaches `usage` to a normal-looking final chunk that still carries `choices[0].finish_reason` and an empty `delta`.
**That hazard does not exist here, and the swallow logic from `04:574` must not be applied blindly** — swallowing Zen's usage chunk would also swallow the terminal `finish_reason`, which is the proxy's own definition of a completed step (`04:588`).

**Quirk 2 — there is a frame *after* `data: [DONE]`.**
Observed frame ordering, verbatim, on every stream:

```
data: {... "choices":[{"finish_reason":"stop", ...}], "usage":{...}}

data: [DONE]

data: {"choices":[],"cost":"0"}
```

The OpenAI SSE contract treats `[DONE]` as terminal.
A client that stops reading at `[DONE]` never sees the cost frame, which is fine; a client that keeps reading gets a frame with `choices: []`, which is the `choices[0]` hazard arriving one frame later than expected.
A proxy that forwards bytes verbatim is unaffected, but a proxy that *parses* must not assume `[DONE]` ends the stream, and must not assume every non-`[DONE]` frame has a choice.

### 3.4 A constant, unexplained ~83-token prompt overhead

Measured with `max_tokens: 1` and increasing user-message sizes of `"word "` repeated, which tokenizes at one token per repetition:

| User content | `prompt_tokens` |
|---|---|
| `"x"` (1 token) | 84 |
| 100 × `"word "` | 184 |
| 200 × `"word "` | 284 |
| 300 × `"word "` | 384 |

The overhead is a flat **83 tokens**, perfectly constant, and adding a 4-token system message moved the total from 84 to 89 rather than replacing anything.

Asked to repeat any prior instruction verbatim, the model answered `NONE`, which is weak evidence against an injected system prompt but is a model self-report and not proof.

**UNVERIFIED: what the 83 tokens are.**
Checked: response-body echo (nothing added), scaling behaviour (constant, so not proportional rewriting), system-message interaction (additive, so not a replaced system slot), and model self-report (`NONE`).
Candidate explanations not distinguished: DeepSeek's own chat-template and thinking-mode prefix, or a gateway-injected preamble.

For the benchmark this is a constant per-request offset applied identically to all arms, so it does not bias the *comparison*.
It does mean `prompt_tokens` is not attributable to harness prompt content alone, and any absolute simulated-cost figure inherits an 83-token-per-request floor that should be stated rather than hidden.

---

## Section 4 — Tool calling

**Established: native OpenAI-format tool calling works, including parallel calls, in both streaming and non-streaming modes.**

`models.dev` records `"tool_call": true` and `"structured_output": true` for `deepseek-v4-flash-free`.
DeepSeek's own model table marks **Tool Calls ✓** and **Json Output ✓** for `deepseek-v4-flash`.

Confirmed live with a single `get_weather` tool and the prompt "What is the weather in Paris and in Tokyo? Use the tool.":

```json
"finish_reason": "tool_calls",
"tool_calls": [
  {"index":0,"id":"call_00_xboyx78B4oSJWjTULDEq0019","type":"function",
   "function":{"name":"get_weather","arguments":"{\"city\": \"Paris\"}"}},
  {"index":1,"id":"call_01_ql4b84FFaIMjJ8lk6yhZ7541","type":"function",
   "function":{"name":"get_weather","arguments":"{\"city\": \"Tokyo\"}"}}
]
```

Two parallel calls in one response, correct `finish_reason`, valid JSON arguments, and an `index` field on each entry.

Streaming tool calls behave conventionally: the first delta carries `id`, `type` and `function.name` with `"arguments":""`, and subsequent deltas append `arguments` fragments keyed by `index`.
The fragments are very fine-grained — `{`, `"`, `city`, `"`, `: `, `"`, `Paris` were seven separate frames — so a parser that assumes one delta per argument, or that tries to `JSON.parse` each fragment, will fail.
That is standard OpenAI behaviour rather than a gateway defect, but it is worth noting because the local Ollama arm streams tool calls differently and ticket #6 already recorded open OpenCode issues on truncated streaming tool calls (`06-headless-invocation.md:248`, issue #40888).

Two formatting observations worth carrying forward:

- Tool-call ids use the non-OpenAI shape `call_00_<random>` with a zero-padded sequence prefix. Any harness that validates the `call_` id format loosely will be fine; one that pattern-matches OpenAI's exact shape might not be.
- Every assistant message carries a non-standard **`reasoning_content`** field alongside `content`, and every streaming delta carries `"reasoning_content": null` or a fragment. `models.dev` documents this explicitly as `"interleaved": {"field": "reasoning_content"}`. A harness that rejects unknown message fields, or that concatenates all string fields of a delta, will produce garbage.

**UNVERIFIED: whether any of the three harnesses mishandles `reasoning_content` or the post-`[DONE]` frame in practice.** Nothing was executed through a harness; only raw HTTP was tested.

---

## Section 5 — Rate limits, and the undocumented free cap

**This is the most serious measurement objection after reachability, and the documentation does not answer it.**

### 5.1 Nothing is published

`zen.mdx` contains no requests-per-minute, tokens-per-minute or concurrency figure.
Its only quantitative limits are the **auto-reload** ("If your balance goes below $5, Zen will automatically reload $20") and **monthly limits** sections, both of which are billing controls for paid usage and say nothing about the free tier.

`https://opencode.ai/docs/go/` publishes dollar-denominated limits — "5 hour limit: $12 of usage", "Weekly limit: $30", "Monthly limit: $60" — but those govern the **Go subscription**, not Zen's free models. That page's only statement about free models is the opposite: "If you reach the usage limit, you can continue using the free models."

No response header advertised a limit either.
A full header dump of a successful completion returned only `Date`, `Content-Type`, `Content-Length`, `Connection`, `Cf-Placement`, `Server` and `CF-RAY`.
**There are no `x-ratelimit-*` headers, and no `retry-after`.**
A client therefore has no way to see how close it is to a limit until it trips one.

### 5.2 The cap is real, and users hit it

`anomalyco/opencode#16844`, opened 2026-03-10 and titled "What are the specific use terms of OpenCode Zen & its models per IP address, please?", reports this error appearing mid-session with no prior warning:

> `Free usage exceeded, add credits https://opencode.ai/zen [retrying in 20h 44m attempt #1]`

The reporter asked, among other things, what the daily allowance is, whether it is counted in tokens or requests, and whether the backend model or its parameters can change.
**The issue was closed as not planned with no maintainer answer to any of those questions.**
`#28055` ("FREE MODELS usage limits") asks the same thing and is likewise unanswered.

The `retrying in 20h 44m` fragment is the informative part: the client's own backoff resolves to a roughly 24-hour window, so the cap is a daily one, and once tripped it does not clear in minutes.

**UNVERIFIED: the numeric size of the free cap, its unit (requests or tokens), its reset window, and whether it is scoped per account, per API key or per IP.**
Checked: the Zen docs page, the Go docs page, the Terms of Service, live response headers, and the two GitHub issues that ask precisely this. All silent; the issues are unanswered and one is closed as not planned.
This was deliberately not established by exhausting the cap, since doing so would have burned the free tier for the rest of the day and produced a number valid only for one IP on one date.

### 5.3 What was observed under load

Roughly **fifty requests** were issued from a single IP with no API key over about fifteen minutes on 2026-08-07, totalling about **260,000 prompt tokens** (dominated by one deliberate 250k-token request).
Every one returned `200`. No `429` was seen, and no cap was hit.

A deliberate burst of **12 concurrent** completions all returned `200`, with individual `time_total` between 1.475 s and 1.814 s and a total wall time of 1.943 s.
Twelve requests in parallel therefore cost barely more than one, which means there is **no visible concurrency serialization at that scale** — a genuine advantage over the local arm, where `04:555` requires `OLLAMA_NUM_PARALLEL=1` and forbids running two harnesses at once.

This is encouraging and it is also not a guarantee.
Fifty requests is a small fraction of a real benchmark matrix, an unenforced limit today can be enforced tomorrow under the "impose limits on certain features" clause of Section 1.4, and the observed behaviour of an unauthenticated IP may differ from that of an authenticated key.

### 5.4 Why this matters for the numbers

A `429` mid-run does not merely slow a benchmark, it corrupts it in a specific and misleading way.
Each harness has its own retry policy — `04:133` records that OpenCode's retry loop has *no upper bound on attempts* and that its retry tokens are never recorded, while Cline's empty-response middleware defaults to three attempts and does aggregate their usage (`04:347-350`).
So the same rate-limit event produces a different token count, a different step count and a different wall time depending on which harness absorbed it.
**A 429 storm would present as a harness difference.** That is the failure mode this project exists to avoid.

Mandatory mitigation if this tier is used: the proxy must log HTTP status per request, and any run containing a non-2xx upstream response must be **discarded, not repaired**.

**Necessary but not sufficient, per `11-second-free-model.md`.** An upstream `ResourceExhausted 32/32` error from NVIDIA was observed arriving with **`HTTP 200`**, so a status-code check alone lets a failed request through as a successful one. The body must also be inspected for an upstream error payload, and the run discarded on that basis too.

---

## Section 6 — Model identity, routing and version pinning

### 6.1 No evidence of silent routing or fallback

**Corrected by `11-second-free-model.md`: this holds for the primary model and is false of the gateway as a whole.**
Four requests for `ling-3.0-flash-free` came back echoing `"model":"ling-3.0-tiny-free"`, and the token accounting matched the smaller model too, so it is a real substitution rather than an echo bug.
The mitigation is mandatory on every request, not merely advisable: **assert `response.model == requested_model` and discard the run otherwise.**
The three probes below stand as written for `deepseek-v4-flash-free` specifically.

Three probes, all clean:

- A request for `deepseek-v4-flash-free` echoed `"model":"deepseek-v4-flash-free"` in the response on every one of ~50 calls. No substitution was ever observed.
- A request for a non-existent id returned a clean error rather than a fallback: `{"type":"error","error":{"type":"ModelError","message":"Model deepseek-v4-flash-freeXX is not supported"}}`.
- A request larded with `logit_bias`, `frequency_penalty`, `top_p`, `stop` and a junk `nonsense_param` was accepted with `200` and no error. Unknown parameters are silently dropped rather than rejected.

The gateway's stated position supports this. `zen.mdx` Goal 2 is to "Have access to the **highest quality** options and not downgrade performance or route to cheaper providers."
Goal 3 is to "Pass along any **price drops** by selling at cost."

**UNVERIFIED: whether the gateway multiplexes across several upstream providers for the same identifier.**
Checked: the response `model` echo (stable), and the error text from a `/zen/v1/responses` probe, which leaked an upstream name — `"Error from provider (Console): Upstream request failed: [invalid_request_error] Empty input messages"`.
That confirms there *is* a distinct upstream behind the gateway but does not establish whether more than one serves this model.
The silent-parameter-drop behaviour is the more practical worry: it means a harness sending a sampling parameter the upstream ignores gets no signal that it was ignored (Section 9.2).

### 6.2 The free variant is a different serving configuration from the paid one

This is the finding in this section that actually bites.

`models.dev` describes `deepseek-v4-flash-free` and `deepseek-v4-flash` as the same model — identical `family`, `description`, `knowledge` cutoff (`2025-05`) and `release_date` (`2026-07-31`) — but with different serving limits:

| Field | `deepseek-v4-flash-free` | `deepseek-v4-flash` (paid) |
|---|---|---|
| `limit.context` | 200000 | 1000000 |
| `limit.output` | 128000 | 384000 |
| `reasoning_options` | `effort` only | `toggle` **and** `effort` |
| `cost` | 0 / 0 / 0 | 0.14 / 0.28 / 0.028 |

The `reasoning_options` row is the important one: the paid variant exposes a `toggle` to turn thinking off, and **the free variant does not**.
Consequence: on the free tier the model always thinks, and reasoning tokens are always billed against the output count (Section 9.2).

The context row, however, does not survive contact with the endpoint.
A deliberate ~250,000-token prompt was accepted with `200` and reported `"prompt_tokens": 250084` — well past the 200k that `models.dev` claims for the free variant.
**`models.dev` is community-maintained metadata and is not authoritative for this endpoint.**
Treat its `limit` fields as a hint, and measure the real ceiling if it ever matters.

DeepSeek's own documentation states 1M context and 384K maximum output for `deepseek-v4-flash`, which is consistent with the 250k request succeeding.

### 6.3 The served model is not version-pinned at the identifier

DeepSeek publishes a version string: **`DeepSeek-V4-Flash-0731`** is listed as the MODEL VERSION for `deepseek-v4-flash`.

Zen exposes nothing equivalent.
`GET /zen/v1/models` returns bare records of the form `{"id":"deepseek-v4-flash-free","object":"model","created":1786107604,"owned_by":"opencode"}`, with **no version, no `limit` and no `cost` field**.
The `created` timestamp is not a pin either: two fetches minutes apart returned `1786107516` and `1786107604`, so it is generated per response rather than describing the model.

Therefore the identifier `deepseek-v4-flash-free` can begin serving a different build, a different quantization or a different context configuration at any time, with no observable change at the API surface.
Ticket #16844 asked exactly this — "When backend model quality may be changed", "When backend parameters may be changed" — and got no answer.

The only defence available to a benchmark is to record, per run: the full `/v1/models` response, the `models.dev` record, the measured 83-token prompt overhead (which would move if the chat template changed), and a fixed canary prompt's `prompt_tokens`.
None of that *prevents* drift; it only makes drift visible after the fact.

---

## Section 7 — Terms of service

### 7.1 Publishing benchmark results

**Not found.**
The Terms of Service at `https://opencode.ai/legal/terms-of-service` contains no clause about benchmarking, performance testing, or publishing results, in either direction.
It neither grants nor forbids it.

There is a weak inference *for* permissibility — the gateway's own reason for existing is benchmarking ("we benchmarked the combination of the model/provider and came up with a list that we feel good recommending") and Goal 1 is to "**Benchmark** the best models/providers for coding agents" — but that describes what OpenCode does, not what it licenses users to do, and it is not a permission clause.
Recorded as an inference, not a finding.

### 7.2 Automated use — the clause that does create risk

The restrictions list under "Are there restrictions in how I can use the Services?" includes, verbatim:

> "automatically or programmatically extracts data or Output"

and separately:

> "crawls," "scrapes," or "spiders" any page, data, or portion of or relating to the Services"

and:

> "uses Output to develop artificial intelligence models that compete with the Services"

The first of these is the problem.
A benchmark runner that drives the API on a schedule and captures every response body to a JSONL file is, read literally, programmatically extracting Output.
Read narrowly — as an anti-scraping and anti-distillation clause aimed at bulk data harvesting — a coding-agent benchmark is plainly not the target, and the adjacent clauses about spiders and training competing models support that narrower reading.

**This is a genuine ambiguity and it should be resolved by asking rather than by interpreting.**
`zen.mdx` provides a contact address for exactly this ("Contact us if you have any questions").
The honest position for the writeup is: no clause forbids publishing results; one clause could be read to restrict the automated collection that produces them; the vendor was not asked.

The third clause is worth a separate note: the benchmark must not use the free tier's Output as training data for anything, which it does not, but the constraint should be stated because "we collected 50k agent trajectories from a free endpoint" is a natural next step for a project like this and it would not be permitted.

### 7.3 The reciprocal data term

Section 1.3's "During its free period, collected data may be used to improve the model" is the mirror image and applies to every prompt sent.
Nothing confidential goes through this tier.

---

## Section 8 — Published pricing for the same model

Per `04:706-709`, the project multiplies measured token counts by public price tables to state a simulated cost.
A free-tier run can be priced honestly against DeepSeek's own list price for the same model.

**Retrieved 2026-08-07 from `https://api-docs.deepseek.com/quick_start/pricing`.**
All figures USD per 1M tokens.

| Model (DeepSeek's id) | Input, cache hit | Input, cache miss | Output |
|---|---|---|---|
| `deepseek-v4-flash` | $0.0028 | $0.14 | $0.28 |
| `deepseek-v4-pro` | $0.003625 | $0.435 | $0.87 |

Model version: `DeepSeek-V4-Flash-0731`. Context 1M, maximum output 384K. Both models "Supports both non-thinking and thinking (default) modes".

Four caveats that materially affect the computed figure:

**The price is about to rise, by DeepSeek's own statement.**
The pricing page carries the notice: "We plan to raise the overall pricing for DeepSeek API services in the near future, with a significant increase expected."
Any simulated-cost figure computed from this table must carry the retrieval date, exactly as `04:728` requires for Claude's introductory pricing.

**The cache-hit price is a 50x discount and the endpoint reports the split.**
`$0.0028` versus `$0.14` is a 50-fold difference, and Section 3.2 established that the response hands over `prompt_cache_hit_tokens` and `prompt_cache_miss_tokens` directly.
Simulated cost should therefore be computed as `hit × 0.0028 + miss × 0.14 + output × 0.28` rather than by applying the cache-miss rate to all input tokens.
This is a **capability the local Ollama arm does not have at all** — `04:508-509` records the cache-hit count as unobtainable there — so the hosted tier can produce a more honest cost figure than the local one.

In practice the cache almost never hit during probing: ten identical back-to-back requests each reported `prompt_cache_hit_tokens: 0`, and the 250k-token request reported only 256 cached tokens.
**UNVERIFIED: whether prompt caching is disabled on the free tier, or simply did not engage for these prompt shapes.** Checked only by observation across ~50 requests; no documentation addresses free-tier caching.

**Zen's own price for the paid `deepseek-v4-flash` matches DeepSeek exactly** at $0.14 / $0.28 (`zen.mdx` pricing table), which is consistent with Goal 3's "selling at cost".
**Zen's price for `deepseek-v4-pro` does not**: `zen.mdx` lists $1.74 / $3.48 against DeepSeek's own $0.435 / $0.87, exactly 4x on both columns.
**UNVERIFIED: why.** Checked both pricing pages on the same date; neither explains the gap. Note also that `models.dev` records the Zen `deepseek-v4-pro` output price as `3.84` where `zen.mdx` prints `$3.48`, one of which is a digit transposition. Use `zen.mdx` if a Zen price is ever needed, and DeepSeek's page for the simulated-cost table.

**The tokenizer-portability caveat from `04:730-734` applies unchanged**, and here it applies with less force in one direction: the token counts being priced were produced by DeepSeek's own tokenizer against DeepSeek's own price list, so for this one model the simulated cost is a *real* cost rather than a cross-tokenizer estimate.
That is a genuine advantage of the hosted tier for the cost-reporting goal specifically.

---

## Section 9 — What controlled variables are lost

The local arm's control surface is enumerated at `04:536-559`.
This section prices each item against the hosted arm.

### 9.1 Context window control — lost, but the loss is benign here

Locally, `num_ctx` cannot be set over `/v1` at all, the VRAM-tiered default lands at 4096 on a typical consumer GPU, and Ollama **truncates the input silently rather than erroring** (`04:543-551`).
`04:548` calls this "the single largest silent-corruption risk in the whole experiment", mitigated only by `OLLAMA_CONTEXT_LENGTH=65536` on the server process.

Hosted, there is no knob whatsoever — no `num_ctx`, no server flag, no Modelfile.
But the ceiling is enormous: a 250k-token prompt was accepted without complaint, against DeepSeek's documented 1M.
A coding-agent benchmark will not approach that.

**Net: control is lost, and it does not matter.** The hosted arm removes the largest silent-corruption risk of the local arm by making the limit unreachable rather than by making it controllable.
What is lost is the *guarantee*: a silent reduction of the free tier's context window would be invisible until a run started truncating.

### 9.2 Sampling parameter control — lost, and this one is serious

`04:539-542` warns that Ollama hardcodes `temperature: 1.0` when a harness omits it, so two harnesses can differ purely because one is silent, and requires logging the effective parameters per request to verify all arms send the same values.

Hosted, the equivalent verification is not available and the parameters may not be honoured at all.

Three requests were sent with **identical bodies**, `"temperature": 0` and `"seed": 42`, asking for one random fruit in one word:

| Run | Content | `completion_tokens` |
|---|---|---|
| 1 | `Mango` | 29 |
| 2 | `Apple` | 18 |
| 3 | `Mango` | 29 |

**Greedy decoding with a fixed seed produced two different answers and two different token counts.**
Either `temperature` and `seed` are dropped by the gateway or ignored by the upstream; Section 6.1 established that unknown and unwanted parameters are silently accepted with `200`, so there is no error to observe either way.

`reasoning_effort` behaves the same way — accepted without error, but `"low"` produced 33 reasoning tokens and `"max"` produced 24, which is the wrong direction and is consistent with the parameter being ignored.
Recall from Section 6.2 that the free variant has no `toggle` option at all, so thinking cannot be turned off: every response measured carried non-zero `reasoning_tokens`, up to 33 tokens for answering "2+2?".

**UNVERIFIED: whether `temperature`, `seed` and `reasoning_effort` are dropped at the gateway or ignored upstream.** Checked by output variance across identical requests and by parameter-echo (there is none). The distinction does not change the consequence.

**This is the single largest measurement loss.**
The local arm can be made deterministic; the hosted free arm cannot. Output token counts and step counts become random variables rather than fixed quantities, which forces repeated runs and statistics where the local arm needs one run.

### 9.3 Concurrency, queueing and warm state

**Concurrency: gained, not lost.**
`04:555` requires `OLLAMA_NUM_PARALLEL=1` and forbids running two harnesses at once, because the second one's wall time would include queueing behind the first.
The hosted endpoint absorbed 12 concurrent requests in 1.943 s total, so arms could in principle run in parallel — with the caveat that shared-fleet contention is then invisible rather than absent.

**Warm-vs-cold state: gained in one sense, lost in another.**
`04:557-559` requires warming the model before each run, polling `/api/ps` until it is resident at 100% GPU, and asserting `load_duration` is zero, because a cold request can spend 59% of its wall time loading.
There is no cold start on a hosted fleet and no warm-up procedure needed.
There is also **no `load_duration` field and no `/api/ps`**, so the assertion that a request was served warm cannot be made — it must be assumed.

**Queueing: lost entirely as an observable.**
The endpoint is shared with every other user of the free tier. Nothing distinguishes model compute time from queue time, and no header reports either.

### 9.4 Long-term reproducibility — the worst loss

The local arm is reproducible in the strongest sense: a reader with the same GGUF file, the same Ollama version and the same environment variables reproduces the setup exactly, indefinitely.

The hosted free arm is reproducible **only while the vendor chooses to offer it**, and every fact points the same direction:

- "available on OpenCode for a limited time", with no end date (Section 1.3).
- "We may suspend or discontinue any part of the Services … or impose limits on certain features or restrict access to parts or all of the Services" (Section 1.4).
- The published free-model list and the live `/v1/models` list already disagree (Section 1.4).
- `zen.mdx` maintains a **Deprecated models** table with 18 entries and hard dates, nine of them falling in the two months before this writing — the roster demonstrably churns.
- The identifier carries no version, so the served build can change silently (Section 6.3).
- The free cap is real, undocumented, and unanswered when asked (Section 5.2).

A reader attempting to reproduce this arm in six months may find the model gone, renamed, capped differently, or serving a different build under the same name — and would have no way to detect the last of these.

### 9.5 Does wall time survive?

**Partially, and the surviving part is the part this project cares most about.**

`04:645-654` decomposes wall time into three components. Take them one at a time.

**`Σ request_latency` — badly degraded.**
Ten sequential, byte-identical requests that each produced *exactly* the same token counts (`prompt_tokens: 88`, `completion_tokens: 8`, `reasoning_tokens: 8`) took between 1.563 s and 2.470 s, a spread of 58% on a workload with zero variability in the work performed.
That spread is shared-fleet contention plus wide-area network round trip, and it is irreducible.
Against local Ollama the same experiment would be near-deterministic.
So request latency stops being a property of the harness's prompt and becomes a property of DeepSeek's fleet and the runner's internet connection on that day.
It should still be recorded, but it must not be compared across arms without many repetitions, and the writeup must not present it as a model-speed figure.

**`Σ inter_request_gap` — survives essentially intact.**
This is harness overhead plus tool-execution time, all of it local, and `04:637` calls it "arguably the most interesting number this project can produce".
It is unaffected by where the model lives.

**`runner_wall_time` — survives as a measurement but is contaminated as a comparison.**
It remains the authoritative end-to-end figure per `04:643`, but it now contains a large, variable, non-local component. With enough repetitions the contention noise averages out; with one run per cell it does not.

**Time to first token — lost as a model metric.**
It now measures TLS handshake plus network RTT plus queue position, none of which is a harness property.

**Net verdict on wall time: the local arm remains the only one where the model-time component is trustworthy.**
This is the strongest argument for keeping local Ollama rather than replacing it.

### 9.6 Summary table

| Controlled variable | Local Ollama | Zen free tier |
|---|---|---|
| Context window | Settable server-side (`OLLAMA_CONTEXT_LENGTH`), silent truncation risk | No control; ceiling so high it is unreachable |
| Sampling parameters | Settable and verifiable per request | **Not honoured**; identical requests give different outputs |
| Determinism | Achievable | **Not achievable** |
| Concurrency | Must be serialized (`OLLAMA_NUM_PARALLEL=1`) | 12-way concurrency absorbed with no penalty |
| Warm state | Controllable and assertable (`load_duration`, `/api/ps`) | No cold start; also no way to assert one |
| Queueing | Absent by construction | Present, invisible, unbounded |
| Request latency variance | Near-deterministic | 58% spread on identical work |
| Prompt-cache visibility | **Unobtainable** | `prompt_cache_hit_tokens` reported directly |
| Streaming usage | Requires forced `include_usage` | Returned unconditionally |
| Reasoning tokens | Not reported | `completion_tokens_details.reasoning_tokens` |
| Long-term reproducibility | Indefinite | "for a limited time", unversioned, capped |
| Cost of a run | Zero, unconditionally | Zero until an undocumented daily cap trips |

---

## Section 10 — Verdict

### 10.1 Can a non-OpenCode harness reach this endpoint?

**Yes.**

The deciding fact: `curl -X POST https://opencode.ai/zen/v1/chat/completions -d '{"model":"deepseek-v4-flash-free","messages":[...]}'` returned a `200` and a well-formed OpenAI `chat.completion` body **with no `Authorization` header, no account, and no OpenCode process involved**, on 2026-08-07.

Supporting facts: `models.dev` publishes the provider as `{"api": "https://opencode.ai/zen/v1", "npm": "@ai-sdk/openai-compatible", "env": ["OPENCODE_API_KEY"]}`; `zen.mdx` documents the same base path per model; and the vendor's own Goal 4 is "**No lock-in** by allowing you to use it with any other coding agent."

PI and Cline both accept a custom OpenAI-compatible base URL through the same configuration path already established for Ollama (`06-headless-invocation.md:295-298`, `:528-534`).
oh-my-pi is unverified, but that is an open gap for the local arm too.

One operational caveat: sending a *wrong* key returns `401` where sending *no* key returns `200`, so any harness that unconditionally emits an `Authorization` header needs a real Zen API key.

### 10.2 Can the proxy measure it as faithfully as it measures local Ollama?

**For tokens, more faithfully. For time and for control, meaningfully less.**

Gained:
- Streaming usage arrives unconditionally, so the mandatory request rewrite of `04:574` is no longer load-bearing.
- `prompt_cache_hit_tokens` and `prompt_cache_miss_tokens` are reported, closing the gap that `04:508-509` records as *unobtainable* against Ollama.
- `completion_tokens_details.reasoning_tokens` is reported, which Ollama does not expose.
- Simulated cost becomes a real cost, priced by the same vendor's tokenizer that produced the counts.
- Concurrency is available, so arms could run in parallel.

Lost, precisely:
- **Determinism.** `temperature: 0` and `seed: 42` do not produce identical output. Output token counts, step counts and text all become random variables. Every cell needs repetition; the local arm needs one run.
- **Sampling-parameter verification.** `04:541` requires asserting that all arms send identical parameters; here the parameters are accepted with `200` and apparently ignored, so the assertion is unfalsifiable.
- **Trustworthy request latency.** 58% spread across ten byte-identical requests. Time to first token stops being a model metric entirely.
- **Warm-state assertion.** No `load_duration`, no `/api/ps`; a request cannot be proven to have been served warm.
- **Queue visibility.** Contention is present, unbounded and unreported.
- **The `OLLAMA_DEBUG_LOG_REQUESTS` cross-check** from `04:522-528`, which is what validates the bespoke proxy against an independent request record. There is no hosted equivalent, so the proxy becomes the sole instrument with nothing to check it against.
- **Run integrity under rate limiting.** With no `x-ratelimit-*` headers and an undocumented daily cap, a run can be silently corrupted by retries whose accounting differs per harness (Section 5.4).

Two proxy changes are required and are not optional:
1. **Do not swallow the usage frame.** Zen attaches usage to a chunk that still carries `finish_reason`, so swallowing it would destroy the proxy's own step definition (`04:588`). This is the opposite of the Ollama requirement.
2. **Do not treat `data: [DONE]` as end-of-stream when parsing**, because a `{"choices":[],"cost":"0"}` frame follows it.

Plus one new discipline: log HTTP status per request, and discard — never repair — any run containing a non-2xx response.

### 10.3 Replacement, second tier, or neither?

**A viable second tier alongside local Ollama. Not a viable replacement.**

It is not a replacement for four reasons, in order of weight.
Determinism is unavailable, so the arm cannot produce a single clean number per cell.
Wall time's model component is contaminated by shared-fleet contention and wide-area RTT, and wall time is one of the project's three headline metrics.
Long-term reproducibility is explicitly disclaimed by the vendor — "for a limited time", unversioned, with a documented right to "restrict access to parts or all of the Services".
And an undocumented daily cap can terminate a run mid-matrix with no advance signal.

It is a strong *second* tier for three reasons that the local arm cannot supply at any price.
LFM2.5-2.6B is a 2.6B model that ticket #6 already flags as likely to hit its output cap constantly (`06-headless-invocation.md:240`) and to emit malformed tool calls; DeepSeek V4 Flash is a frontier-class agentic model with confirmed parallel tool calling, so a second tier tests whether harness differences observed at 2.6B are artifacts of model incapacity or real.
It costs nothing, so the project's hard zero-cost constraint holds.
And its richer usage object makes cost and cache behaviour measurable in ways the local arm cannot match.

Recommended shape if adopted:

1. Keep local Ollama as the **primary, controlled arm**. Every headline comparison is computed there.
2. Add Zen `deepseek-v4-flash-free` as a **secondary, capability arm**, reported separately and never averaged with the local arm.
3. Run **n ≥ 5 repetitions per cell** on the hosted arm and report median with spread, because §9.2 makes single runs uninformative.
4. Report `total_prefill_tokens`, `final_context_tokens`, `output_tokens`, `reasoning_tokens`, `proxy_steps`, `tool_invocations` and `Σ inter_request_gap` from the hosted arm. Report `Σ request_latency` with an explicit contention caveat. Do **not** report time to first token.
5. Pin and archive per run: the full `GET /v1/models` response, the `models.dev` record, and a fixed canary prompt's `prompt_tokens` (expected 83 + content) so a template or model change is detectable after the fact.
6. Discard any run containing a non-2xx response rather than retrying it.
7. Before wiring anything, settle the empty-`Authorization` question from §2.2 and re-check PI's `supportsReasoningEffort: false` compat flag, which was set for Ollama and may not be right here.
8. Ask OpenCode directly about §7.2's "automatically or programmatically extracts data or Output" clause before publishing results collected this way.

---

## Summary of what could not be established

- **The numeric free-usage cap, its unit, its reset window, and its scope (account, key or IP).** Checked the Zen docs, the Go docs, the Terms of Service, live response headers, and issues `#16844` and `#28055`. All silent; `#16844` was closed as not planned with the questions unanswered. The only hard evidence is a user-reported error string with a ~24-hour backoff.
- **Whether `temperature`, `seed` and `reasoning_effort` are dropped at the gateway or ignored upstream.** Established that they are not honoured; not established where they are lost.
- **What the constant 83-token prompt overhead consists of.** Ruled out proportional rewriting and a replaced system slot; could not distinguish DeepSeek's own chat template from a gateway preamble.
- **Whether prompt caching is functional on the free tier.** Ten identical consecutive requests all reported zero cache hits.
- **Whether the `cost` field carries a real figure on paid models.** No API key was available.
- **Whether an empty `Authorization: Bearer ` header is treated as absent or invalid.** Not tested; decisive for harnesses that always send the header.
- **Whether the gateway multiplexes several upstreams behind one identifier.** An error message leaked one upstream name ("Console"); whether there are others is unknown.
- **Whether any of the three harnesses actually tolerates `reasoning_content` and the post-`[DONE]` frame.** Only raw HTTP was tested; nothing was executed through a harness.
- **oh-my-pi's provider configuration surface.** Absent from `docs/research/` entirely, for the local arm as much as this one.
- **Why Zen prices `deepseek-v4-pro` at exactly 4x DeepSeek's own list price**, and which of `zen.mdx`'s `$3.48` or `models.dev`'s `3.84` is the typo.
- **Whether the Terms of Service's "automatically or programmatically extracts data or Output" clause is intended to cover a benchmark runner.** The vendor was not asked. No clause about publishing benchmark results exists in either direction — **not found**, not inferred.

The one that would block adoption is the **free-usage cap**, because a run terminated mid-matrix by an invisible quota produces exactly the kind of corrupted comparison this project exists to avoid.
It cannot be closed by reading; it can only be characterised by deliberately exhausting the cap once and measuring where it falls, which is a cheap follow-up experiment and should precede any real use of this tier.
