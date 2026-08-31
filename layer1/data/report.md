# Layer 1 — request shape

Task `probe`, n = 1 (the mock is deterministic). Token counts use the proxy tokenizer `cl100k_base` and are comparable between arms only, never against a gateway's own `prompt_tokens`.

### First request, isolated environment

| arm | arm_version | tool_schema_count | tools_bytes | system_bytes | conversation_bytes | envelope_bytes | total_bytes | prompt_tokens |
|---|---|---|---|---|---|---|---|---|
| omp | omp/17.2.10 | 11 | 39273 | 25395 | 135 | 142 | 64945 | 16714 |
| opencode | 1.17.9 | 9 | 20007 | 9738 | 114 | 138 | 29997 | 6659 |
| pi | 0.80.10 | 4 | 2900 | 2499 | 135 | 142 | 5676 | 1228 |

### Ambient-state delta (real HOME minus fresh HOME)

| arm | isolated_total_bytes | ambient_total_bytes | delta_bytes | ratio | isolated_prompt_tokens | ambient_prompt_tokens |
|---|---|---|---|---|---|---|
| pi | 5676 | 5676 | 0 | 1.0 | 1228 | 1228 |

### Per-step growth, isolated environment

| arm | step_0_total_bytes | step_1_total_bytes | step_2_total_bytes | step_3_total_bytes | step_4_total_bytes |
|---|---|---|---|---|---|
| omp | 64945 | 65273 | 65898 | 66523 | 67148 |
| opencode | 29997 | 30695 | 31393 | 32091 | 32789 |
| pi | 5676 | 6231 | 6786 | 7341 | 7896 |

### pi vs omp, first request, isolated

| metric | pi | omp | ratio |
|---|---|---|---|
| total_bytes | 5676 | 64945 | 11.442 |
| tools_bytes | 2900 | 39273 | 13.542 |
| system_bytes | 2499 | 25395 | 10.162 |
| tool_schema_count | 4 | 11 | 2.75 |
| prompt_tokens | 1228 | 16714 | 13.611 |

### Auxiliary (tool-less) model calls per run

| arm | profile | calls | total_bytes |
|---|---|---|---|
| opencode | isolated | 1 | 2526 |

### Runs

| run_id | status | exit_code | requests | wall_seconds |
|---|---|---|---|---|
| probe-omp-isolated-20260828T105612Z | ok | 0 | 5 | 4.296 |
| probe-omp-ambient-20260828T105618Z | no_requests | 1 | 0 | 17.334 |
| probe-opencode-isolated-20260828T105636Z | ok | 0 | 6 | 4.396 |
| probe-opencode-ambient-20260828T105641Z | no_requests | 1 | 0 | 3.065 |
| probe-pi-isolated-20260828T105645Z | ok | 0 | 5 | 2.149 |
| probe-pi-ambient-20260828T105649Z | ok | 0 | 5 | 2.163 |

