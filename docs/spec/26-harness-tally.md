# 26 — Consuming harness-tally v0.1.0

Ticket [#85](https://github.com/YuukiFST/harness-bench/issues/85).
Question: which harness-tally does the runner install, how does it drive it, and how does one build stay one measured session?

The measuring proxy is no longer specified here.
It lives in [harness-tally](https://github.com/YuukiFST/harness-tally), charted on [its map](https://github.com/YuukiFST/harness-tally/issues/1).
On 2026-09-28 the author re-scoped the measurement ([harness-tally #43](https://github.com/YuukiFST/harness-tally/issues/43)): each build is **one long session per harness**, resumed after a refusal and after the daily free cap, and the arms are **pi and oh-my-pi**.
The full spec 25 instrument (profile table, `max_tokens` rewrite, canary, fault-injecting mock, the 14 assertions of §10.2, discard on fault) was cut in the same decision.
This document is the contract #16 and #17 build against; where spec 11 or spec 25 disagree with it, this document wins.

## 1. Pin

```
harness-tally @ git+https://github.com/YuukiFST/harness-tally@a0d5cefdaf0ea9b0d0f2f5283b88abb09141389a
```

- The pin is the full commit SHA that tag `v0.1.0` points at ([harness-tally #13](https://github.com/YuukiFST/harness-tally/issues/13)): never the tag name, a branch, or PyPI.
- Python ≥ 3.11, no runtime dependencies.
- On Windows the pin installs only once harness-tally's `main` carries v0.1.0: pip checks out the default branch before the pinned commit, and `main` before the merge holds capture paths too long for MAX_PATH (fixed at the pinned commit, guarded by `tests/test_repo_paths.py`).
- The runner records `importlib.metadata.version("harness-tally")` and the pinned SHA in every result record.

## 2. Contract the runner uses

Upstream is OpenRouter's free tier, `https://openrouter.ai/api/v1`, one account with training switched off (harness-tally [#38](https://github.com/YuukiFST/harness-tally/issues/38), [#40](https://github.com/YuukiFST/harness-tally/issues/40)).
Tiers: primary `google/gemma-4-31b-it:free`, robustness `qwen/qwen3.8-27b:free`, both context 262144.

1. Start `python -m harness_tally serve --upstream https://openrouter.ai/api/v1 --run-id <build id> --out <run dir> --upstream-key-env OPENROUTER_API_KEY` with stdin held as a pipe.
2. Read one JSON line from its stdout: `{"event":"ready","port":…,"base_url":…}`.
   Nothing else is ever written to stdout.
3. Point the arm's OpenAI-compatible provider at `base_url` (no `/v1`) with the literal key `harness-tally`.
   Strip every `*_API_KEY` from the arm's environment: the proxy injects the real key, so an arm with a shell tool cannot echo it into a tool result.
4. Run the arm with its stdout captured.
5. Close the proxy's stdin; it drains in-flight requests and exits.
6. Run `python -m harness_tally summarize <run dir>` and read only `<run dir>/summary.json` (`harness-tally/summary/1`).

Records (`records.jsonl`, `harness-tally/record/1`) carry the gateway's `usage` on every answered request, `model_echoed` checked against the requested id (`model_substituted` flag), and one line per refused request.
The proxy never retries, repairs, or measures wall time.

## 3. One session per build

- A build is one harness session, one `--run-id`, one `--out`.
- **Refusals are normal.** OpenRouter's shared free pools refused about 10 requests in 11 on 2026-09-28, for both models, and a pool refusal (429, `limit_source: upstream_provider_shared_pool`) costs no daily quota ([pool measurement](https://github.com/YuukiFST/harness-tally/blob/a0d5cefdaf0ea9b0d0f2f5283b88abb09141389a/docs/research/pool-availability.md)).
- **Resume from the records, not from the exit code.** pi 0.80.10 exits 0 after a refused request ([live smoke](https://github.com/YuukiFST/harness-tally/blob/a0d5cefdaf0ea9b0d0f2f5283b88abb09141389a/docs/research/live-smoke.md)). After the arm exits, if `summary.json` `requests.refused` grew, the build is unfinished: restart the proxy with the same `--run-id` and `--out` (the log continues; another run id in the log exits 1) and resume the same harness session.
- **The daily cap pauses, it does not end.** 50 accepted free requests a day per account. Before each resume, read `GET /api/v1/key` `free_model_daily_requests.remaining`; at 0, wait for the 00:00 UTC reset.
- The build's token count is `summary.json` `tokens`, a plain sum over answered requests.

## 4. What is still open here

- Resuming a session is harness-specific (pi and oh-my-pi session files); #16 settles it.
- spec 11 still describes per-unit fresh processes, opencode, and Zen tiers, and `AGENTS.md` still rules oh-my-pi out; both predate harness-tally #43 and are the author's to rewrite.
