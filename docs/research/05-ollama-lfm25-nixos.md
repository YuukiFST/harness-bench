# 05 — LFM2.5-2.6B on Ollama / NixOS: tool calling, setup, and viability

Research ticket #5.
Question: does LFM2.5-2.6B actually do reliable tool calling through Ollama, and can agentic CLIs drive it?

Researched 2026-08-07.
All version numbers, option names, and template contents below were read from primary sources on that date and are cited inline.
Where a fact could not be established it is marked **UNVERIFIED** rather than guessed.

---

## 0. Executive summary

The plumbing works, but only if you wire it manually, and the experiment has a validity problem that matters more than the plumbing.

1. Ollama **does** ship a purpose-built Go parser for LFM2's Pythonic tool-call format (`model/parsers/lfm2.go`), and it emits real OpenAI-style `tool_calls`.
2. That parser is **not attached** when you `ollama pull hf.co/LiquidAI/LFM2.5-2.6B-GGUF:Q4_K_M` — the Hugging-Face-served manifest carries no `parser` and no `renderer`, and its template has no tool support at all, so the model reports no `tools` capability and a request with `tools` is rejected with HTTP 400.
3. The fix is a three-line Modelfile (`RENDERER lfm2` / `PARSER lfm2-thinking`), not a template hack — a `TEMPLATE` override alone provably cannot parse a Pythonic call.
4. There is an **open, unfixed upstream bug filed 2026-08-06 that names this exact GGUF repo** and describes tool calls being mangled by quote/escape handling — the single largest risk to a coding benchmark, where arguments are full of quotes and backslashes.
5. **Liquid AI states the model was RL-trained inside PI**, one of the four harnesses under test.
   This is a benchmark-validity confound that no amount of setup care can remove.

Verdict is in §8.

---

## 1. The model: ground truth

| Fact | Value | Source |
|---|---|---|
| Total parameters | 2.69B | [model card](https://huggingface.co/LiquidAI/LFM2.5-2.6B) |
| Architecture | hybrid — 22 double-gated short-convolution blocks + 8 GQA attention layers | [model card](https://huggingface.co/LiquidAI/LFM2.5-2.6B) |
| Context window | **131,072 tokens** (`max_position_embeddings` in config.json) | [config.json](https://huggingface.co/LiquidAI/LFM2.5-2.6B/raw/main/config.json) |
| Vocabulary | 128,000 | [model card](https://huggingface.co/LiquidAI/LFM2.5-2.6B) |
| License | frontmatter `license: other` / `license_name: lfm1.0`; the LICENSE file is titled "LFM Open License v1.0" | [LICENSE](https://huggingface.co/LiquidAI/LFM2.5-2.6B/raw/main/LICENSE) |
| Tool use claimed officially | Yes — "function calling in four steps" | [model card](https://huggingface.co/LiquidAI/LFM2.5-2.6B) |
| Reasoning | "pure reasoning model that always thinks before it answers. It adds a `<think>` tag directly in the chat template" | [model card](https://huggingface.co/LiquidAI/LFM2.5-2.6B) |

Q4_K_M is published.
Exact size from the HTTP `content-length` on the resolve URL, not the rounded page display: `LFM2.5-2.6B-Q4_K_M.gguf` = **1,674,454,848 bytes ≈ 1.674 GB** ([file tree](https://huggingface.co/LiquidAI/LFM2.5-2.6B-GGUF/tree/main)).
Other quants in the repo: Q4_0 (1.594 GB), Q5_K_M (1.94 GB), Q6_K (2.22 GB), Q8_0 (2.87 GB), F16/BF16 (5.4 GB each).

The GGUF repo contains **no** `chat_template.jinja`, no `Modelfile`, and no `params` file — only the GGUFs, LICENSE, README, and a `leap/` directory.
The chat template exists only inside GGUF metadata.
This is the root of the problem described in §3.

### 1.1 What the chat template actually emits

Read verbatim from [`chat_template.jinja`](https://huggingface.co/LiquidAI/LFM2.5-2.6B/raw/main/chat_template.jinja) in the base repo.

Tool **definitions** go into the system block as plain text with no wrapper tokens:

```jinja
{%- set ns.system_prompt = ns.system_prompt + ("\n" if ns.system_prompt else "") + "List of tools: [" -%}
{%- for tool in tools -%}  ... tool | tojson ...  {%- endfor -%}
{%- set ns.system_prompt = ns.system_prompt + "]" -%}
```

Tool **calls** are Pythonic, not JSON:

```jinja
{{- "<|tool_call_start|>[" + (tool_calls_ns.tool_calls | join(", ")) + "]<|tool_call_end|>" -}}
```

Each call is built as `func_name + "(" + args | join(", ") + ")"`, with string arguments single-quoted by `format_arg_value`.
The model card's own example is `<|tool_call_start|>[get_candidate_status(candidate_id="12345")]<|tool_call_end|>`.
The template explicitly `raise_exception`s if you hand it JSON-encoded argument strings.

Tool **results** go back through the generic branch as `<|im_start|>tool\n{content}<|im_end|>\n`.
There is no `<|tool_response_start|>` token in the LFM2.5 template, though the older LFM2-1.2B template did have one.

Thinking is **forced on by the template**, not optional:

```jinja
{%- if add_generation_prompt -%}
    {{- "<|im_start|>assistant\n<think>" -}}
{%- endif -%}
```

The only related knob is `preserve_thinking` (default `false`), which controls whether *past* turns retain their `<think>` blocks — not whether the model thinks.
There is no `enable_thinking=False` switch in this template.

---

## 2. NixOS setup

### 2.1 Corrections to common assumptions

Four things that are widely repeated and are wrong against the current sources.

`services.ollama.acceleration` **no longer exists** on current stable or unstable.
It was removed and replaced by setting `.package`.
It still exists on `nixos-25.11`.

`services.ollama.models` is a **directory path (string), not a list of models**.
The list option is `.loadModels`.
On `nixos-unstable` the directory option was renamed to `.modelsDir`.

llama.cpp discussion #4167 is the **Apple Silicon** thread, not the CUDA one ([#4167](https://github.com/ggml-org/llama.cpp/discussions/4167)).
The CUDA scoreboard is [#15013](https://github.com/ggml-org/llama.cpp/discussions/15013), and it does contain RTX 3060 12GB rows.

NVIDIA does **not** publish a 360 GB/s bandwidth figure for the RTX 3060 12GB.
Its own spec page lists only "12 GB GDDR6" and "192-bit", with no bandwidth and no memory clock ([nvidia.com](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060-3060ti/)).

### 2.2 Branches and versions verified

Branches confirmed to exist via the GitHub API: `nixos-unstable`, `nixos-26.05`, `nixos-25.11`, `nixos-25.05`, `nixos-24.11`.
Current stable is **26.05** ([nixos.org/download](https://nixos.org/download/)).

Commits actually read for this note:

- `nixos-unstable` @ `b7c2ada94fe99c15b0dbcf4d11fd7850b957a436` (2026-08-05) — ollama **0.32.5**
- `nixos-26.05` @ `445d861c6d31b4af0c79d8d4be2331f762a361d7` (2026-08-06) — ollama **0.32.3**
- `nixos-25.11` @ `b6018f87da91d19d0ab4cf979885689b469cdd41` (2026-06-30) — ollama **0.21.1**

Hydra has since built `ollama-0.32.6` on unstable; the branch moves.
Latest upstream Ollama release is v0.32.6 (2026-08-04).

### 2.3 Package

Attribute is `ollama`, CUDA variant is `ollama-cuda` ([package.nix](https://github.com/NixOS/nixpkgs/blob/nixos-unstable/pkgs/by-name/ol/ollama/package.nix)).

```nix
shouldEnable = mode: fallback: (acceleration == mode) || (fallback && acceleration == null && validateFallback);
cudaRequested = shouldEnable "cuda" config.cudaSupport;
```

`passthru` exposes `ollama-rocm`, `ollama-cuda`, `ollama-vulkan`.
CUDA dependencies are `cudaPackages.cuda_cudart`, `libcublas`, and `cccl` (unstable) / `cuda_cccl` (26.05, 25.11), built with `buildGoModule.override { stdenv = cudaPackages.backendStdenv; }`.

### 2.4 Module options (read from source, not memory)

From [`nixos/modules/services/misc/ollama.nix`](https://github.com/NixOS/nixpkgs/blob/nixos-unstable/nixos/modules/services/misc/ollama.nix).

| Option | Type | Default | Notes |
|---|---|---|---|
| `enable` | bool | `false` | |
| `package` | package | `pkgs.ollama` | `mkPackageOption` |
| `user` | `nullOr str` | `null` | `null` → systemd `DynamicUser` |
| `group` | `nullOr str` | `cfg.user` | only used when `user` is set |
| `home` | str | `"/var/lib/ollama"` | |
| `modelsDir` (unstable) / `models` (26.05, 25.11) | str | `"${cfg.home}/models"` | **a directory, not a model list** |
| `host` | str | `"127.0.0.1"` | |
| `port` | port | `11434` | |
| `rocmOverrideGfx` | `nullOr str` | `null` | sets `HSA_OVERRIDE_GFX_VERSION` |
| `environmentVariables` | `attrsOf str` | `{ }` | server-only, see caveat |
| `loadModels` | `listOf str` | `[ ]` | `ollama pull` at boot |
| `syncModels` | bool | `false` | removes models not in `loadModels` |
| `openFirewall` | bool | `false` | |
| `acceleration` | `nullOr (enum [false "rocm" "cuda" "vulkan"])` | `null` | **25.11 only — removed in 26.05 and unstable** |

The removal is explicit in the `imports` block of 26.05 and unstable:

```nix
(lib.mkRemovedOptionModule [ "services" "ollama" "acceleration" ]
  "Set `services.ollama.package` to one of `pkgs.ollama[,-vulkan,-rocm,-cuda,-cpu]` instead.")
```

Two caveats from the module source that will bite a benchmark.
The `environmentVariables` description states: "Be aware that these are only seen by the ollama server (systemd service), not normal invocations like `ollama run`."
The generated unit hardcodes `OLLAMA_MODELS` and `OLLAMA_HOST` **after** merging your `environmentVariables`, so those two cannot be overridden through that option.

On the positive side the unit already sets `DeviceAllow` for `char-nvidiactl`, `char-nvidia-caps`, `char-nvidia-frontend`, and `char-nvidia-uvm`, so CUDA works under the systemd sandbox without extra work.

### 2.5 Copy-pasteable flake

Targeting **nixos-26.05**, where `acceleration` is unavailable and `.package` is the only route.

`flake.nix`:

```nix
{
  description = "Ollama + LFM2.5-2.6B (Q4_K_M) on NixOS, CUDA, RTX 3060 12GB";

  inputs.nixpkgs.url =
    "github:NixOS/nixpkgs/445d861c6d31b4af0c79d8d4be2331f762a361d7"; # nixos-26.05 @ 2026-08-06

  outputs = { self, nixpkgs }: {
    nixosConfigurations.bench = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [ ./hardware-configuration.nix ./ollama-cuda.nix ];
    };
  };
}
```

`ollama-cuda.nix`:

```nix
{ config, lib, pkgs, ... }:
{
  nixpkgs.config.allowUnfree = true;          # NVIDIA driver + CUDA are unfree

  # --- NVIDIA driver (see 2.6) ---
  hardware.graphics.enable = true;
  services.xserver.videoDrivers = [ "nvidia" ];   # load-bearing: gates all of hardware.nvidia
  hardware.nvidia = {
    modesetting.enable = true;
    open = true;                                  # GA106 is Ampere, i.e. Turing-or-later
    nvidiaSettings = false;
  };

  # --- Ollama ---
  services.ollama = {
    enable  = true;
    package = pkgs.ollama-cuda;                   # NOT `acceleration = "cuda"` on >= 26.05
    host    = "127.0.0.1";
    port    = 11434;
    environmentVariables = {
      OLLAMA_CONTEXT_LENGTH  = "65536";           # see 5.3 — the 4k default will ruin the run
      OLLAMA_FLASH_ATTENTION = "1";
      OLLAMA_KEEP_ALIVE      = "30m";
      OLLAMA_NUM_PARALLEL    = "1";               # single-stream benchmarking
    };
  };

  # --- CUDA binary cache: without this you compile CUDA from source ---
  nix.settings = {
    substituters       = [ "https://cache.nixos-cuda.org" ];
    trusted-public-keys = [
      "cache.nixos-cuda.org:74DUi4Ye579gUqzH4ziL9IyiJBlDpMRn9MBN8oNan9M="
    ];
  };
}
```

`services.xserver.videoDrivers = [ "nvidia" ]` is not optional.
`nvidia.nix:8` defines `nvidiaEnabled = lib.elem "nvidia" config.services.xserver.videoDrivers`, and the entire `hardware.nvidia` config block is gated on it.

Note that `loadModels` is deliberately absent — see §2.8 and §3.5 for why the model must be built from a Modelfile instead.

### 2.6 NVIDIA prerequisites for an RTX 3060 (Ampere GA106, CC 8.6)

From [`nixos/modules/hardware/video/nvidia.nix`](https://github.com/NixOS/nixpkgs/blob/nixos-unstable/nixos/modules/hardware/video/nvidia.nix).

`hardware.nvidia.open` must be set explicitly; there is a hard assertion:

```nix
assertion = cfg.open != null || cfg.datacenter.enable;
message = ''
  You must configure `hardware.nvidia.open` on NVIDIA driver versions >= 560.
  It is suggested to use the open source kernel modules on Turing or later GPUs (RTX series, GTX 16xx), and the closed source modules otherwise.
'';
```

The RTX 3060 is Ampere, i.e. later than Turing, so `open = true` is the module's own recommendation.
This is corroborated upstream: NVIDIA's own README states "The NVIDIA open kernel modules can be used on any Turing or later GPU" ([open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules)).

`hardware.nvidia.package` has type `package` and default `nvidiaPackages.${cfg.branch}`; its description says "Prefer using `hardware.nvidia.branch` when possible."
`branch` defaults to `"stable"`.
Leave both alone unless you have a specific reason.

`hardware.graphics.enable` is bool, default `false` ([graphics.nix](https://github.com/NixOS/nixpkgs/blob/nixos-unstable/nixos/modules/hardware/graphics.nix)).
`nixpkgs.config.allowUnfree = true` is required.

Ollama's GPU docs state "Ollama supports Nvidia GPUs with compute capability 5.0+ and driver version 550 and newer" and list the RTX 3060 explicitly under compute capability 8.6 ([docs.ollama.com/gpu](https://docs.ollama.com/gpu)).
The `stable` branch is well above 550.

### 2.7 The `cudaSupport` alternative, and why not to use it

```nix
nixpkgs.config = {
  allowUnfree = true;
  cudaSupport = true;
  cudaCapabilities = [ "8.6" ];   # RTX 3060 = Ampere GA106
};
services.ollama = { enable = true; package = pkgs.ollama; };  # now resolves to ollama-cuda
```

The nixpkgs manual says of `cudaSupport`: "Changing the default may cause a mass rebuild" ([nixpkgs manual](https://nixos.org/manual/nixpkgs/unstable/#sec-values-of-config)).
Prefer `package = pkgs.ollama-cuda`, which CUDA-ifies exactly one package instead of the whole closure.

**`ollama-cuda` is not in `cache.nixos.org` — this was verified, not assumed.**
The Hydra job `nixpkgs:unstable:ollama-cuda.x86_64-linux` returns `{"error":"There is no successful build to redirect to."}`, and its build-history page shows "Showing builds 1 - 0 out of 0" — zero builds, ever.
The same query for `ollama.x86_64-linux` returns a green build at `/nix/store/n85l5hkk80xfzx5mcmayrnnzm8wadrg7-ollama-0.32.6`.
The cause is stated in the nixpkgs manual: "Unfree software is not tested or built in Nixpkgs continuous integration, and therefore not cached."
The NixOS wiki says it directly: "NixOS Foundation does not build (and therefore cache.nixos.org does not cache) CUDA packages" ([wiki.nixos.org/wiki/CUDA](https://wiki.nixos.org/wiki/CUDA)).

`https://cache.nixos-cuda.org/nix-cache-info` returns HTTP 200 with `Priority: 50`; the older `cuda-maintainers.cachix.org` also still answers 200 with `Priority: 41`.
The wiki now documents `cache.nixos-cuda.org`, so use that one.

**UNVERIFIED:** whether `ollama-cuda` specifically is present in `cache.nixos-cuda.org`.
Confirming that requires a store path from a local `nix eval`, which could not be run here.
Budget for a from-source CUDA build on the first `nixos-rebuild`.

### 2.8 Pinning for reproducibility

Pin nixpkgs by rev in `inputs`, as in the flake above.
`flake.lock` records `rev` plus `narHash` regardless, but an explicit rev survives an accidental `nix flake update`.

There is no version option on the ollama module or package.
The recommended way to pin an Ollama version is to pick a nixpkgs rev that already carries it — read `version = "...";` in `pkgs/by-name/ol/ollama/package.nix` at candidate revs, which is exactly how the 0.32.5 / 0.32.3 / 0.21.1 figures above were obtained.
This keeps the vendored llama.cpp, the patches, and `vendorHash` mutually consistent.

**UNVERIFIED:** whether a naive `overrideAttrs { version; src; }` bump builds.
`ollama` is a `buildGoModule` derivation, so a new `src` also needs a matching `vendorHash`, and the package pulls llama.cpp as a submodule.
Treat an overlay-based version bump as real work, not a config tweak.

**Model pulls are not pinned by the flake.**
`loadModels = [ "hf.co/LiquidAI/LFM2.5-2.6B-GGUF:Q4_K_M" ]` resolves against Hugging Face `main` at service-start time, so an upstream repo update silently changes your benchmark subject.
The Hugging Face docs document only `hf.co/{user}/{repo}:{quantization}`; no revision or digest syntax is documented ([huggingface.co/docs/hub/en/ollama](https://huggingface.co/docs/hub/en/ollama)).
**UNVERIFIED:** whether Ollama's `hf.co/` route accepts a commit SHA.

The reproducible route is to fetch the GGUF by hash and build the model from a Modelfile.
Hugging Face `resolve/<sha>/` URLs are content-stable.
The repo revision as of this research is `b421ad1d549afeda6a0fb2ad3a697cb5a7879adc` (HF API `lastModified` 2026-08-06T17:10:07Z).
The combined snippet that does both the hash-pinning and the tool-call wiring is in §3.5.

### 2.9 Importing the GGUF

Route A, direct, syntax verified against the Hugging Face docs:

```sh
ollama run hf.co/{username}/{repository}:{quantization}
```

The docs state that "you can use both `hf.co` and `huggingface.co` as the domain name", that "the quantization name is case-insensitive", and that "By default, the `Q4_K_M` quantization scheme is used, when it's present inside the model repo" ([huggingface.co/docs/hub/en/ollama](https://huggingface.co/docs/hub/en/ollama)).
The GGUF model card gives the exact command: `ollama run hf.co/LiquidAI/LFM2.5-2.6B-GGUF:Q4_K_M`.

**Do not use route A for this experiment.**
It produces a model with no tool-call parser — see §3.

Route B is a local Modelfile with `FROM <path>.gguf`, which is both the reproducible route and the only one that yields working tool calls.

---

## 3. Tool calling: does Ollama translate the Pythonic format?

**Short answer: yes, via a dedicated Go parser — but that parser is not attached to the Hugging-Face-served model, so out of the box it does not work.**

### 3.1 Ollama has a real LFM2 parser

`model/parsers/lfm2.go` exists in the Ollama source.
It was added 2026-01-20 in commit `01cf7445`, "model: add lfm2 architecture and LFM2.5-1.2B-Thinking support (#13792)", and updated 2026-06-15 by [PR #16359](https://github.com/ollama/ollama/pull/16359), "model: update lfm2 parser/renderer for optional thinking".

It parses Pythonic calls explicitly.
Verbatim from the source comments:

```go
// parseToolCallsContent parses one or more Python-style tool calls.
// Example: [func1(arg='v'), func2(x=1)]
...
// parsePythonStyleToolCalls parses one or more Python-style tool calls
// Examples: [bash(command='ls'),bash(command='pwd')] or bash(command='ls')
```

It runs a state machine over `<think>`, `</think>`, `<|tool_call_start|>`, and `<|tool_call_end|>`, streams partial tags correctly, assigns `Function.Index` for parallel calls, validates call names against the declared tool set (`toolCallsAllowed`), and has a fallback for bare tool calls emitted without the wrapper tags.

Registration in `model/parsers/parsers.go`: `case "lfm2": &LFM2Parser{hasThinkingSupport: false}` and `case "lfm2-thinking": &LFM2Parser{hasThinkingSupport: true}`.
`HasToolSupport()` returns `true` unconditionally.
A matching renderer lives in `model/renderers/lfm2.go`, registered as `"lfm2"` and `"lfm2-thinking"`.

Architecture support is established: LFM2 MoE landed in v0.12.6 after the llama.cpp vendor sync ([#12549](https://github.com/ollama/ollama/issues/12549)), LFM2.5-8B-A1B needs v0.30.0 ([#16439](https://github.com/ollama/ollama/issues/16439)), and the official `lfm2.5-thinking` manifest declares `"requires":"0.14.3"`.

### 3.2 The breakage: the Hugging-Face-served manifest

The manifest Ollama consumes for `hf.co/LiquidAI/LFM2.5-2.6B-GGUF:Q4_K_M` was fetched directly from `https://huggingface.co/v2/LiquidAI/LFM2.5-2.6B-GGUF/manifests/Q4_K_M`.
Its config blob is:

```json
{"model_format":"gguf","model_family":"lfm2","model_families":["lfm2"],
 "model_type":"2.7B","file_type":"unknown",
 "config":{"format":"gguf","architecture":"lfm2","parameters":"2.7B","size":"1.67B"},
 "descriptor":{"created":"2026-08-01T22:42:15.000Z"}, ...}
```

There is **no `renderer` field and no `parser` field**.
The shipped template layer is 197 bytes, verbatim:

```
{{ if .System }}<|startoftext|><|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>
```

No `.Tools`, no `.ToolCalls`, no `.Messages`.
The params layer is just stop tokens.

Contrast the official ollama.com library models, fetched from `ollama.com/v2/library/.../blobs/...`:

- `lfm2.5-thinking:1.2b` → `"renderer":"lfm2-thinking","parser":"lfm2-thinking","requires":"0.14.3"`
- `lfm2.5:8b` → `"renderer":"lfm2","parser":"lfm2-thinking","requires":"0.30.0"`

Per `server/images.go`, capabilities are the union of `configCapabilities`, `ggufCapabilities`, `templateCapabilities`, and `parserCapabilities`, and `parserCapabilities` grants `tools` and `thinking` **only** when `m.Config.Parser` resolves to a registered parser.
With an empty parser and a `.Tools`-free template, `hf.co/LiquidAI/LFM2.5-2.6B-GGUF` gets neither capability, and a request carrying `tools` is rejected with HTTP 400.

There is **no official ollama.com library build of the 2.6B**.
`library/lfm2.5` has only `8b` and `8b-a1b-*` (MoE); `library/lfm2.5-thinking` has only `1.2b`.
Both show a `tools` badge.
Only third-party uploads exist for 2.6B (e.g. `oamazonasgabriel/lfm2.5-2.6b`), and that page shows no capability badges.

### 3.3 Issue-tracker history

The maintainer has answered this exact question, for a sibling model, and closed it the same day.

| Issue | Date | State | Substance |
|---|---|---|---|
| [ollama/ollama#15953](https://github.com/ollama/ollama/issues/15953) | 2026-05-04 | closed same day | "LiquidAI/lfm2.5-1.2b-instruct and lfm2.5-350m don't accept tool calling even though they support it", error `does not support tools`. Maintainer **rick-github**: "These are user uploaded models and the supplied Modelfile doesn't provide tool support. Fortunately the chat template for these models is the same as for lfm2, which ollama supports. So the Modelfile can be modified to use the RENDERER and PARSER from the official lfm2 models." He then demonstrates it working end to end, and closes with "Be aware that small models are generally not great tool users." |
| [ollama/ollama#14742](https://github.com/ollama/ollama/issues/14742) | 2026-03-09 | closed | `lfm2.5-thinking cannot run tools` via OpenCode. Root cause was context size plus model competence, not parsing. rick-github: "Logs show that the model is getting the tool list, it's just very bad at tool use. This is not uncommon with small models… I suggest looking at larger models for more accurate tool use." |
| [ollama/ollama#14928](https://github.com/ollama/ollama/issues/14928) | 2026-03-18 | closed | `lfm2:24b cannot call tools` — model emitted `<function=bash>` garbage in VS Code, OpenCode, and Claude Code. rick-github: "It can call tools, it's just not very good at it… using a coding assistant that loads up the context with instructions and tools often results in malformed tool calls… It seems that this model is not suitable for use with a coding assistant." |
| [ollama/ollama#12549](https://github.com/ollama/ollama/issues/12549) | 2025-10-09, closed 2026-07-03 | closed | HF-pulled LFM2-8B-A1B. rick-github: "The template is basic and doesn't support tool calling." User logxdx: "None of the LFM2 models are good at tool calling… THEY FAIL 100% OF THE TIME." (This was the 2025-era LFM2 with a hand-written Go TEMPLATE, before the Go parser existed.) |
| [ollama/ollama#13637](https://github.com/ollama/ollama/issues/13637) | 2026-01-07, closed 2026-07-03 | closed | LFM2.5 model request; loading bugs across 0.13.5 and 0.14.x. |
| [LFM2-1.2B-Tool-GGUF discussion #1](https://huggingface.co/LiquidAI/LFM2-1.2B-Tool-GGUF/discussions/1) | Sep 2025 | open, no vendor reply | "Missing Tool Support in Ollama". A user diagnoses the same root cause: "The embedded template in the gguf does support tool calling. The problem you're having with Ollama is that the modelfile doesn't have the correct template." |

**Status of the historical breakage: works-as-designed / won't-fix.**
Ollama's position is that user-uploaded HF models must supply their own `RENDERER`/`PARSER`, and `server/create.go` auto-detects renderer and parser from GGUF architecture for **only** `gemma4`, `laguna`, and `nemotron_h*` — `lfm2` is not in that switch, with a `TODO: abstract this into a registry/lookup table` next to it.

### 3.4 The open bug that names this exact repo

[ggml-org/llama.cpp#26658 — "LFM2.5-2.6B-GGUF struggles with tool calls because of some problem with quotes"](https://github.com/ggml-org/llama.cpp/issues/26658), opened **2026-08-06**, **still open** as of 2026-08-07.
Python code containing quotes gets mangled (`label=\\` instead of `label=''`) and the call never reaches the MCP server.
Maintainer **aldehir**, 2026-08-06: "This is partly true, the Python syntax parsing is an incomplete implementation. I'll follow up with a PR."

This is llama.cpp's parser, not Ollama's Go parser, so it is not literally the same code path.
It is the same *class* of bug — escaping inside Pythonic string arguments — and no Ollama-side test was found proving the Go parser handles backslash and quote escaping correctly.
**Treat quote-heavy arguments (source code, regexes, Windows paths, shell commands) as UNVERIFIED on Ollama.**
For a *coding* benchmark this is the highest-severity open risk, because essentially every `write_file` or `bash` argument is quote-heavy.

For context, llama.cpp's LFM2.5 support has a long repair tail: [#23856](https://github.com/ggml-org/llama.cpp/pull/23856) routed LFM2.5 through a specialized parser (merged 2026-05-29), then [#24178](https://github.com/ggml-org/llama.cpp/pull/24178) unified and fixed it, [#24071](https://github.com/ggml-org/llama.cpp/pull/24071) narrowed the tool-call start detection, [#24234](https://github.com/ggml-org/llama.cpp/pull/24234) fixed a reasoning round-trip and a `<think>` leak, [#24667](https://github.com/ggml-org/llama.cpp/pull/24667) fixed double-escaping in tool-call parsing, and [#24377](https://github.com/ggml-org/llama.cpp/pull/24377) fixed LFM2/LFM2.5 ignoring `json_schema`.
Six merged fixes in ten weeks, and one still open, is the signal here.

Independently, the [LFM2.5-2.6B-GGUF discussions tab](https://huggingface.co/LiquidAI/LFM2.5-2.6B-GGUF/discussions) has five open threads, all roughly two days old.
Discussion [#2, "how is it so bad at mcp usage?"](https://huggingface.co/LiquidAI/LFM2.5-2.6B-GGUF/discussions/2): a user running llama.cpp server with LiquidAI's own recommended config reports it "fails the most basic mcp calls and almost never follow the instructions" and goes "completely rogue" after one exchange; a second user reports the same on an LM Studio backend.
**No LiquidAI staff reply on any of them.**

### 3.5 The fix, and what a TEMPLATE override cannot do

**A `TEMPLATE` override alone cannot parse a Pythonic tool call.**
This was verified in source, not inferred.
Ollama's template-derived tool parser is `tools/tools.go`: `NewParser(tmpl, tools)` derives a tag from the template via `parseTag(tmpl)`, finds it in the stream, then calls `parseToolCall()` → `findArguments()`.
`findArguments` is a brace-balanced **JSON object** scanner (`braces`, `inString`, `escaped`, looking for `{`…`}`) that returns `map[string]any`.
Nothing in that file can parse `func(arg='v')`.
So a template override buys you the `tools` capability badge and correct prompt rendering, and then fails to parse the response — precisely the outcome logxdx reported in #12549: "it did show it supports tool calls, but the model NEVER calls the tools".

`PARSER` and `RENDERER` are real Modelfile instructions, even though [docs.ollama.com/modelfile](https://docs.ollama.com/modelfile) does not list them (a docs bug — the page lists only FROM, PARAMETER, TEMPLATE, SYSTEM, ADAPTER, LICENSE, MESSAGE, REQUIRES).
Verified in `parser/parser.go`:

```go
case "renderer":
    req.Renderer = c.Args
case "parser":
    req.Parser = c.Args
...
errInvalidCommand = errors.New("command must be one of \"from\", \"license\", \"template\", \"system\", \"adapter\", \"draft\", \"renderer\", \"parser\", \"parameter\", \"message\", or \"requires\"")
```

The working Modelfile:

```dockerfile
FROM ./LFM2.5-2.6B-Q4_K_M.gguf

RENDERER lfm2
PARSER   lfm2-thinking

PARAMETER num_ctx 65536
PARAMETER temperature 0.1
PARAMETER top_k 50
PARAMETER repeat_penalty 1.1
```

```bash
ollama create lfm2.5-2.6b-tools -f Modelfile
ollama show lfm2.5-2.6b-tools     # confirm: capabilities include tools + thinking
```

Every line justified from source:

- `PARSER lfm2-thinking` is what converts Pythonic output into `tool_calls` **and** separates `<think>` into `thinking`/`reasoning`.
  The non-thinking `lfm2` parser would be wrong here: `setInitialState` puts it straight into `LFM2CollectingContent`, so for an always-thinking model the `<think>` block lands in `content`.
- `RENDERER lfm2` (not `lfm2-thinking`) matches what Ollama's own `lfm2.5:8b` config uses; the `lfm2-thinking` renderer additionally replays past-turn `<think>` blocks.
- **Do not add a `TEMPLATE`.**
  `server/prompt.go` short-circuits when `m.Config.Renderer != ""` and uses the Go renderer instead, so a TEMPLATE would be dead weight and can interfere with capability detection via `shouldUseGoTemplate`.
- `num_ctx` is mandatory for the OpenAI-compat path — see §5.3.
- The sampler parameters match those LiquidAI publishes on the model card (`--temp 0.1 --top-k 50 --repeat-penalty 1.1`).
- Requires Ollama ≥ 0.14.3 for the parser; use ≥ 0.30.0, and in practice the 0.32.x in current nixpkgs.

The NixOS-native, hash-pinned version of the same thing:

```nix
let
  lfmRev = "b421ad1d549afeda6a0fb2ad3a697cb5a7879adc";   # HF repo rev, 2026-08-06
  lfmGguf = pkgs.fetchurl {
    url = "https://huggingface.co/LiquidAI/LFM2.5-2.6B-GGUF/resolve/${lfmRev}/LFM2.5-2.6B-Q4_K_M.gguf";
    hash = "sha256-AAAA...";   # nix-prefetch-url --type sha256 <url> | nix hash to-sri --type sha256
  };
  lfmModelfile = pkgs.writeText "Modelfile" ''
    FROM ${lfmGguf}
    RENDERER lfm2
    PARSER   lfm2-thinking
    PARAMETER num_ctx 65536
    PARAMETER temperature 0.1
    PARAMETER top_k 50
    PARAMETER repeat_penalty 1.1
  '';
in {
  systemd.services.ollama-create-lfm = {
    after = [ "ollama.service" ]; requires = [ "ollama.service" ];
    wantedBy = [ "multi-user.target" ];
    environment = config.systemd.services.ollama.environment;
    serviceConfig.Type = "oneshot";
    script = "${lib.getExe config.services.ollama.package} create lfm2.5-2.6b-tools -f ${lfmModelfile}";
  };
}
```

Weights are hash-pinned by Nix, sampler parameters and parser wiring are in the closure, and only the Ollama binary version comes from the nixpkgs rev.

**Caveat, stated plainly:** the combination of `fetchurl`-pinned GGUF plus `RENDERER`/`PARSER` in a NixOS oneshot unit is a synthesis of two separately-verified facts (the fetchurl pinning pattern, and rick-github's demonstrated `RENDERER`/`PARSER` fix).
It was not executed end to end on a NixOS box during this research.
**UNVERIFIED as a running system.**

### 3.6 One prompt-fidelity divergence worth knowing

Ollama's `lfm2` renderer wraps tool schemas as `List of tools: <|tool_list_start|>[…]<|tool_list_end|>`, while LFM2.5's own template emits plain `List of tools: […]` with no wrapper tokens.
This was established by diffing `LFM2-1.2B` (which does use `tool_list` tags) against `LFM2.5-1.2B-Thinking` and `LFM2.5-2.6B` (which do not).
Ollama also does not prefill `<think>` the way the official template does.
Ollama ships this same renderer for its own `lfm2.5-thinking` model and it demonstrably works, so the divergence is tolerated upstream, but it is a real mismatch that could cost some tool-call reliability.
**Impact UNVERIFIED.**

---

## 4. Reasoning tags and the `/v1` endpoint

LFM2.5 always emits `<think>`, so every single turn of this benchmark, in all four harnesses, exercises this code path.
That makes it worth getting exactly right.

### 4.1 What Ollama does

On the native `/api/chat` endpoint, thinking is split into its own field.
[docs.ollama.com/capabilities/thinking](https://docs.ollama.com/capabilities/thinking): "The `message.thinking` (chat endpoint) or `thinking` (generate endpoint) field contains the reasoning trace while `message.content` / `response` holds the final answer."
A `think` parameter accepts `true`/`false` or `low`/`medium`/`high`/`max`.

`server/routes.go` defaults thinking **on**: if the model has the `thinking` capability and the request omits `think`, `if req.Think == nil { req.Think = &api.ThinkValue{Value: true} }`.

On the OpenAI-compat `/v1/chat/completions` endpoint, `openai/openai.go` maps `r.Message.Thinking` to a field named **`reasoning`** — *not* the de-facto-standard `reasoning_content` — on both non-streaming responses (`Message{... Reasoning: r.Message.Thinking}`) and streaming deltas, splitting reasoning-only chunks from content and tool-call chunks.
`finish_reason` is set to `"tool_calls"` when calls are present, and `ToToolCalls()` converts to the OpenAI shape.
Thinking can be disabled on `/v1` with `reasoning_effort: "none"`, which maps to `think=false`.

[docs.ollama.com/openai](https://docs.ollama.com/openai) confirms `[x] Tools` and `[x] reasoning_effort`, and lists **`tool_choice` as unsupported**.
It does *not* document the response shape for reasoning at all.

### 4.2 The `reasoning` vs `reasoning_content` naming, and who it breaks

The naming is **closed as-is**; Ollama will not rename it.

- [ollama/ollama#12628](https://github.com/ollama/ollama/issues/12628), 2025-10-15, closed: "The thought processes of the OLLAMA /v1 endpoint are stored in key 'reasoning', while those from platforms like VLLM are stored in key 'reasoning_content'. … this situation may result in some Agent framework being unable to retrieve the corresponding thinking content."
- [ollama/ollama#8529](https://github.com/ollama/ollama/issues/8529), 2025-01-22, closed: "feat: OpenAI reasoning_content compatibility".
- [ollama/ollama#15288](https://github.com/ollama/ollama/issues/15288), 2026-04-03, closed: with Gemma 4, "all generated text appears only in the `reasoning` field", and "the OpenAI-compatible endpoint does not accept or pass through the `think` parameter", making the model "unusable with any tool that uses the OpenAI-compatible API."

Documented client breakage, including one that hits a harness in this benchmark directly:

| Issue | Date | Status | Substance |
|---|---|---|---|
| [anomalyco/opencode#21903](https://github.com/anomalyco/opencode/issues/21903) | 2026-04-10 | closed | **OpenCode + Ollama specifically.** Ollama ≥0.20.4 returns `reasoning`; OpenCode's Zod schema accepted only Copilot's `reasoning_text`/`reasoning_opaque`. Validation fails, the UI shows "Build -" and **spins indefinitely at high CPU**. Fix demonstrated: add `reasoning: z.string().nullish()` in two places in `openai-compatible-chat-language-model.ts`. |
| [lmstudio-ai/lmstudio-bug-tracker#1589](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1589) | 2026-03-02 | closed | Qwen3.5 reasoning tags interleaved with tool-call JSON made the JSON unparseable. Notable aside: "Ollama automatically strips reasoning tags for tool calls, allowing the same query to work there." |
| [ollama/ollama#15798](https://github.com/ollama/ollama/issues/15798) | 2026-04-24 | closed as not planned | Gemma 4 emits the tool call **as plain text inside the assistant message, often inside a thinking block**, with template markers leaked verbatim, and `finish_reason: stop` — so the client treats a tool call as a final answer. Claimed fixed in 0.20.6, still reproducible in 0.21.1. |
| [ollama/ollama#17248](https://github.com/ollama/ollama/issues/17248) | — | — | A literal `</think>` **inside user content** is parsed as a structural delimiter, corrupting the prompt before inference. Relevant if the benchmark feeds transcripts or code containing that string. |
| [BerriAI/litellm#26326](https://github.com/BerriAI/litellm/issues/26326) | — | — | The canonical leak shape on another provider: `<think>` tags leak into `content` instead of populating `reasoning_content`. |
| [QwenLM/Qwen-Agent#789](https://github.com/QwenLM/Qwen-Agent/issues/789) | — | — | Same root cause, third client: Ollama streaming chunks use `reasoning`, thinking content silently lost. |
| [NousResearch/hermes-agent#21811](https://github.com/NousResearch/hermes-agent/issues/21811) | — | — | Harness sees empty `content` while `reasoning_content` is populated, fires a "you produced nothing" nudge, wasting a turn. |

**Nothing here is systematically fixed.**
Ollama's field name is settled and non-standard; every client patches around it independently.
Each of the four harnesses must be verified individually against the `reasoning` field before any scoring run.

---

## 5. Context window: does it survive an agentic loop?

### 5.1 Advertised vs effective

Advertised is 131,072 tokens, verified in [config.json](https://huggingface.co/LiquidAI/LFM2.5-2.6B/raw/main/config.json), and Liquid describes a "dedicated 128K context-extension phase".

Advertised is not usable.
**RULER** ([arXiv:2404.06654](https://arxiv.org/abs/2404.06654), Hsieh et al., NVIDIA, COLM 2024; repo [github.com/NVIDIA/RULER](https://github.com/NVIDIA/RULER)) states in its abstract: "Despite achieving nearly perfect accuracy in the vanilla NIAH test, almost all models exhibit large performance drops as the context length increases."
Of models claiming 32K or more, "only half of them can maintain satisfactory performance at the length of 32K."
RULER defines "Effective Length" as the longest sequence at which a model stays above the threshold set by Llama-2-7B's 4K performance (85.6%), and finds models "fall below the threshold before reaching the claimed context lengths" — GPT-4-1106 claims 128K with an effective 64K; Command-R-plus claims 128K with an effective 32K.

Critically, the vanilla needle-in-a-haystack test is saturated and tells you nothing; the gap appears on multi-hop tracing and aggregation.
Agentic coding is multi-hop-and-aggregate, not retrieval.

For the size class that matters here, the [xGen-small Technical Report (arXiv:2505.06496)](https://arxiv.org/pdf/2505.06496) RULER evaluations show Llama-3.2-3B-Instruct going 92.5% at 4k → **77.8%** at extended length, and Gemma-3-4B-it going 90.9% → **62.3%**, a 29-point collapse.
Both fall below RULER's 85.6% effective-length threshold well before their advertised windows.
[LongFuncEval (arXiv:2505.10570)](https://arxiv.org/pdf/2505.10570) measures the same degradation specifically for function calling, which is the axis that actually matters here.

**UNVERIFIED:** there is no published RULER or equivalent effective-context measurement for LFM2.5-2.6B.
Given the 3–4B results above, planning on 128k of usable agentic context would be unjustified.

### 5.2 The arithmetic

Fixed per-turn overhead, measured from the repos at HEAD on 2026-08-07 (Cline `7348ba18`, OpenCode `284214c7`).
Token figures use 4 chars/token and are estimates, ±20%; character and byte counts are exact.

| Harness | Fixed overhead (system prompt + tool schemas) | Basis |
|---|---|---|
| Cline v3.89 full | **~14,800 tok** | 59,124-byte rendered Jest snapshot (`anthropic_claude_sonnet_4-basic.snap`) — measured, not estimated from source |
| Cline v3.89 compact prompt | **~1,500 tok** | 5,943 bytes (`compact-system-prompt.ts`) |
| Cline v4 (SDK, native tools) | **~2,500–3,500 tok** | 3,695 chars measured + tool-schema estimate |
| OpenCode (`default.txt` + 16 tool descriptions) | **~6,300 tok**, realistically ~7,000 with schema structure and environment block | 8,623 B + 16,598 B, measured |
| Minimal ReAct loop | ~300–800 tok | your design |
| PI | **UNVERIFIED** — no public repo located | — |

The compact-prompt ratio checks out at 5,943 / 59,124 = 10.05%, corroborating Cline's own claim that "The compact prompt is roughly 10% the size of Cline's full system prompt, making it much more efficient for local inference" ([cline.bot/blog/local-models](https://cline.bot/blog/local-models), 2025-08-28).
The stated tradeoff there: "you lose access to MCP tools, Focus Chain, and MTP features."

Note that Cline v4 is a different architecture from v3: the 50KB XML prompt is gone from the main path, replaced by a ~3,695-char `DEFAULT_CLINE_SYSTEM_PROMPT` plus native tool schemas for 9 tools.
**Which Cline major version you pin moves Cline's result more than the model does.**

A realistic five-turn agentic task, with LFM2.5's always-on `<think>` block priced in at ~400 tokens per assistant turn:

```
user task                                              100
turn 1  think 400 + call 60 + glob result 500          960
turn 2  think 400 + call 60 + read 300-line file 3000 3,460
turn 3  think 400 + call 60 + grep result 800        1,260
turn 4  think 400 + edit call 900 + result 100       1,400
turn 5  think 400 + bash/test output 1500            1,900
                                        history =    9,080
environment block                                      800
                                    variable total =  9,880
```

| Harness | Fixed | + variable | Turn-5 total | vs 32k | vs 128k |
|---|---|---|---|---|---|
| Cline v3.89 full | 14,800 | 9,880 | **24,680** | **77% used** | 19% |
| Cline v3.89 compact | 1,500 | 9,880 | 11,380 | 36% | 9% |
| Cline v4 (SDK) | ~3,000 | 9,880 | ~12,900 | 40% | 10% |
| OpenCode | 7,000 | 9,880 | 16,880 | **53% used** | 13% |
| Minimal ReAct | ~500 | 9,880 | ~10,380 | 32% | 8% |

Against a 32k window Cline v3-full is at 77% by turn five, so compaction fires almost immediately and each compaction round-trip is another full-context prefill.
Neither Cline v3-full nor OpenCode survives a ten-turn task at 32k.

Against the **4,096-token Ollama default** (§5.3), Cline v3's system prompt alone is 3.6× the entire window.

### 5.3 The Ollama default-context trap

Ollama's own docs give two answers that agree for this hardware.

- [docs.ollama.com/faq](https://docs.ollama.com/faq): "By default, Ollama uses a context window size of 4096 tokens."
- [docs.ollama.com/context-length](https://docs.ollama.com/context-length): "Ollama defaults to the following context lengths based on VRAM: < 24 GiB VRAM: 4k context; 24-48 GiB VRAM: 32k context; >= 48 GiB VRAM: 256k context"

**An RTX 3060 12GB lands in the 4k tier under both rules.**
**UNVERIFIED:** the exact release that introduced VRAM-tiered defaults; secondary sources place it around v0.32.x. Verify against your installed version's release notes.

Truncation is silent and drops from the **front** of the prompt, where the system prompt and tool schemas live.
Aider's docs state it flatly: Ollama "silently discards context that exceeds the window", and "This is especially dangerous because many users don't even realize that most of their data is being discarded by Ollama" ([aider.chat/docs/llms/ollama.html](https://aider.chat/docs/llms/ollama.html)).
[openclaw/openclaw#4028](https://github.com/openclaw/openclaw/issues/4028) (2026-01-29, closed) is a worked example: a 10,573-token prompt cut to 4,096, which "effectively removed bootstrap files (SOUL.md, USER.md, IDENTITY.md) from the system prompt", because `openai-completions.js` never forwarded `options.num_ctx`.

**The `/v1` path does not accept `num_ctx`.**
The OpenAI-compat request body has no `options` field, and [docs.ollama.com/openai](https://docs.ollama.com/openai) states that because "the OpenAI API does not have a way of setting the context size", you must build a Modelfile with `PARAMETER num_ctx <size>`.
All four harnesses in this benchmark use `/v1` — OpenCode's documented Ollama config uses `baseURL: http://localhost:11434/v1` ([opencode.ai/docs/providers](https://opencode.ai/docs/providers/)).
So the context length must be set via `OLLAMA_CONTEXT_LENGTH` on the server **and/or** baked into the Modelfile, and a per-request `num_ctx` will be silently ignored.

Ollama's own guidance already rules out the default for this workload: "Tasks which require large context like web search, agents, and coding tools should be set to at least 64000 tokens" ([context-length](https://docs.ollama.com/context-length)), and [docs.ollama.com/integrations/opencode](https://docs.ollama.com/integrations/opencode) is blunt: "OpenCode requires a context length of 64k or higher."

### 5.4 VRAM is not the constraint

Computed from the real config: LFM2.5-2.6B is hybrid, with `layer_types` showing **8 `full_attention` layers out of 30** (the other 22 are conv), `num_key_value_heads = 8`, `num_attention_heads = 32`, `hidden_size = 2048`, so `head_dim = 64`.
Only the 8 attention layers carry a KV cache; the 22 conv blocks carry a fixed `conv_L_cache = 3` state instead.

Using `2 × n_attn_layers × kv_heads × head_dim × ctx × bytes_per_elem`:

| Context | KV @ f16 | KV @ q8_0 |
|---|---|---|
| 4,096 | 0.06 GiB | 0.03 GiB |
| 32,768 | 0.50 GiB | 0.25 GiB |
| 131,072 | **2.00 GiB** | 1.00 GiB |

Weights at Q4_K_M are ~1.67 GB, so even the full 128k context totals roughly 4 GB on a 12 GB card.
**You can afford the full advertised context, so there is no memory reason to run a truncated window.**

KV cache quantization exists if you want it — [docs.ollama.com/faq](https://docs.ollama.com/faq): "The K/V context cache can be quantized to significantly reduce memory usage when Flash Attention is enabled", via `OLLAMA_KV_CACHE_TYPE` with `f16` (default), `q8_0`, or `q4_0`, and it only takes effect with Flash Attention on.
For this model on this card it is unnecessary.

Verify placement with `ollama ps` and confirm 100% GPU, avoiding CPU offload.

---

## 6. Throughput and the wall-clock budget

### 6.1 Measured RTX 3060 12GB numbers

From [llama.cpp Discussion #15013, "Performance of llama.cpp on Nvidia CUDA"](https://github.com/ggml-org/llama.cpp/discussions/15013), the official CUDA scoreboard.
Fixed benchmark: `llama-bench -m llama-2-7b.Q4_0.gguf -ngl 99 -fa 0,1`, single GPU, `pp512` = prefill, `tg128` = generation.

| GPU | Model / quant | Flash attn | pp512 (prefill) t/s | tg128 (generation) t/s |
|---|---|---|---|---|
| RTX 3060 12GB / GDDR6 / 192-bit | Llama 2 7B Q4_0 | no | **2137.50 ± 10.12** | **75.57 ± 0.07** |
| RTX 3060 12GB / GDDR6 / 192-bit | Llama 2 7B Q4_0 | yes | **2407.67 ± 3.73** | **76.92 ± 0.03** |

**Analogue, secondary source — treat as indicative only.**
RTX 3060 12GB with an i7-12700F on Debian 13, llama.cpp: Llama-3.2-3B-Instruct Q4_K_M at **128.3 tok/s**, Llama-3.2-1B-Instruct Q8_0 at 211.9 tok/s, Qwen3.5-4B Q4_K_M at 77.1 tok/s ([tyolab.com](https://www.tyolab.com/blog/2026/05/11-64gb-ram-12gb-vram-the-honest-local-llm-benchmark/)).
The post does not distinguish prefill from generation; from magnitude these are generation figures.

### 6.2 LiquidAI's own numbers do not cover this hardware

The [LFM2.5-2.6B model card](https://huggingface.co/LiquidAI/LFM2.5-2.6B) publishes "220 tok/s on an M5 Max and 113 tok/s on an AMD Ryzen CPU", ~30 tok/s on mobile, and "almost 15K output tokens per second at high concurrency" on H100.
None of these is an RTX 3060 measurement.

**UNVERIFIED: no published LFM2.5 tokens/sec figure on any NVIDIA consumer GPU could be found.**
Checked: llama.cpp #15013 (no LFM2 rows), #4167 (Apple Silicon only), both model cards, and web search.

### 6.3 Memory bandwidth

NVIDIA's product page lists "12 GB GDDR6" and "192-bit" with no bandwidth and no memory clock ([nvidia.com](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060-3060ti/)).
TechPowerUp's GPU database returned HTTP 403 to fetch attempts, so it could not serve as a secondary source either.
360 GB/s is the arithmetic result of 192-bit × 15 Gbps ÷ 8, and appears on board-partner and aggregator pages, but **the 15 Gbps memory clock could not be confirmed from an NVIDIA-owned page — UNVERIFIED at source.**

It is however consistent with the measured data, which is the stronger argument:

| Data point | Weight file | tok/s | Implied effective bandwidth | % of 360 GB/s |
|---|---|---|---|---|
| Llama-2-7B Q4_0, #15013, no FA | 3.826 GB | 75.57 | 289.1 GB/s | 80% |
| Llama-2-7B Q4_0, #15013, FA | 3.826 GB | 76.92 | 294.3 GB/s | 82% |
| Llama-3.2-3B Q4_K_M (blog) | ~2.02 GB | 128.3 | 259.2 GB/s | 72% |

All three land at 72–82% of the assumed peak, exactly the band expected from a memory-bound decode loop.
If peak were materially below 360, the 7B row would imply over 100% utilization.

### 6.4 Estimate for LFM2.5-2.6B Q4_K_M

Roofline: 1.674 GB read per token at 70–80% of 360 GB/s gives a **~151–172 tok/s generation ceiling**.

Realistically expect **~110–160 tok/s generation**.
Two reasons to sit below the roofline: at 2.6B the per-token kernel-launch and sampling overhead is a larger fraction of the budget (visible in the 3B analogue landing at 72% versus the 7B's 80%), and LFM2's short-convolution blocks are a different kernel mix than the dense-attention models every one of these benchmarks measures.
**This is a derived estimate, not a measurement of LFM2.5. Measure it before budgeting on it.**

Prefill is compute-bound and scales with model size rather than weight-file size, so LFM2.5-2.6B prefill should land in the high thousands of tok/s — roughly 7B/2.6B ≈ 2.7× the 7B figure, i.e. order **5,000–6,500 tok/s**.
**Estimate, unmeasured.**

### 6.5 What this means for the wall-clock budget

Take a mid-run Cline v3-full turn at ~25,000 prompt tokens producing ~500 output tokens.
Prefill: 25,000 / 5,750 ≈ **4.3 s**.
Generation: 500 / 135 ≈ **3.7 s**.
So roughly **8 s per turn**, split about evenly.

Take a minimal-ReAct turn at ~10,000 prompt tokens producing ~500 output tokens.
Prefill ≈ 1.7 s, generation ≈ 3.7 s, so **~5.4 s per turn**, generation-dominated.

Neither prefill nor generation dominates universally — the crossover sits around 20k prompt tokens for this model on this card.
The practical consequence is that **the harnesses with fat system prompts pay a real, measurable prefill tax**, and this is a legitimate thing for the benchmark to measure, provided prompt token counts are logged per turn.
Note also that `OLLAMA_KEEP_ALIVE` matters: a cold model reload costs a full 1.67 GB PCIe transfer before any of this.

Flash attention bought +12.6% prefill and only +1.8% generation on the 3060 (the two #15013 rows).
`OLLAMA_FLASH_ATTENTION=1` is worth setting but is not a generation-speed lever.

At ~8 s/turn and, say, 25 turns per task, a task costs ~3.3 minutes of pure inference.
Four harnesses × 20 tasks × 3 repetitions ≈ 240 runs ≈ **13 hours of inference**, before retries, timeouts, and loop-detection blowups.
That is a feasible overnight-scale budget, not a blocker.

---

## 7. Failure modes when driving small models from agentic CLIs

### 7.1 The causal chain

Almost every documented "small model loops forever" case resolves to a **format or plumbing mismatch between what the harness expects and what the model plus template actually emit** — not to raw model weakness.
The three failure modes in the ticket are one chain:

context overflow silently truncates the system prompt and tool schemas from the front → the model, never having seen the tool list, answers in prose → the harness reports "no tool was used" and re-prompts → the model repeats itself → infinite loop until context exhaustion.

**Every "the small model is too dumb" report produced under default Ollama settings is actually this.**

### 7.2 Infinite / repeating tool-call loops

| Issue | Date | Status | Substance |
|---|---|---|---|
| [cline/cline#10843](https://github.com/cline/cline/issues/10843) | 2026-05-18 | **open** | Local Ollama models emit valid JSON tool calls; Cline's streaming parser only recognises XML tags, treats the JSON as prose, tells the model "no tool was used", and the model repeats the identical payload **until context exhaustion**. Reporter proved it was the parser: forcing XML via custom rules made it work. |
| [cline/cline#11263](https://github.com/cline/cline/issues/11263) | 2026-06-04 | **open** | Two modes: models without native tool support get HTTP 400/500 because `tools` is sent unconditionally; models with native tools return JSON tool calls, the XML-expecting receiver raises `MODEL_NO_TOOLS_USED`, and loops forever. |
| [cline/cline#1418](https://github.com/cline/cline/issues/1418) | 2025-01-23 | closed | DeepSeek-R1 on local Ollama: "You did not use a tool in your previous response! Please retry with a tool use." → "Cline is having trouble…" → recommends Claude 3.5 Sonnet. |
| [bytedance/deer-flow#1055](https://github.com/bytedance/deer-flow/issues/1055) | 2026-03-10 | closed | **Directly relevant to the in-house ReAct loop.** "Calls `bash` … Gets the result … Calls `bash` with the exact same command again" until the recursion limit. Explicitly names "non-OpenAI models (DeepSeek, Qwen, Ollama) that are more prone to this behavior." Root cause framed as a **harness gap**: the ReAct loop "has no mechanism to track recent tool calls, detect identical calls being repeated, or warn the model when stuck in loops." |
| [google/adk-python#5650](https://github.com/google/adk-python/issues/5650) | 2026-05-09 | closed | Gemma **2B and 4B**. Tool results serialised as `role="tool"` (OpenAI default) but the chat template expects `role="tool_responses"`, so the model reads its own tool result as a new user turn and re-issues the call forever. Pure role-name mismatch, not model incapacity. |
| [BerriAI/litellm#28530](https://github.com/BerriAI/litellm/issues/28530) | — | — | Same class, LiteLLM side. |

### 7.3 Malformed or hallucinated tool calls, tool calls emitted as plain text

| Issue | Date | Status | Substance |
|---|---|---|---|
| [ollama/ollama#15798](https://github.com/ollama/ollama/issues/15798) | 2026-04-24 | closed as not planned | Template special tokens leak into OpenAI-compat output; the tool call arrives as plain text inside the assistant message with `finish_reason: stop`, so the client treats it as a final answer. Claimed fixed in 0.20.6, still reproducible in 0.21.1. |
| [ollama/ollama#15539](https://github.com/ollama/ollama/issues/15539) | — | — | Model produces correct tool-call JSON, the parser doesn't intercept it, raw JSON leaks into `content` with trailing template tokens. |
| [ollama/ollama#14601](https://github.com/ollama/ollama/issues/14601) | 2026-03-03 | **open** | Qwen3 tool definitions rendered into the prompt as **Go struct notation** (`{get_weather Get the current weather...}`) instead of JSON, because the template uses `{{ .Function }}`. Prior assistant tool calls also stripped from history. |
| [anomalyco/opencode#21181](https://github.com/anomalyco/opencode/issues/21181) | 2026-04-06 | closed as not planned | "Instead of executing the tool and continuing the loop, OpenCode returns the tool call itself as text or pseudo-tool output" — no filesystem side effects. |
| [anomalyco/opencode#20995](https://github.com/anomalyco/opencode/issues/20995) | — | — | Model returns valid `tool_calls`, OpenCode doesn't recognise them; the model then says "I do not have the capability to execute system commands." |
| [anomalyco/opencode#20719](https://github.com/anomalyco/opencode/issues/20719) | 2026-04-02 | closed as not planned | "The agent loop exits after exactly one LLM call per run — before any tool is called", because `@ai-sdk/openai-compatible` returns `finish_reason: "stop"` where the spec wants `"tool_calls"`. |
| [anomalyco/opencode#21354](https://github.com/anomalyco/opencode/issues/21354) | — | — | Model invents a tool name: looks for `read_file`, OpenCode exposes `read`. |
| [anomalyco/opencode#5694](https://github.com/anomalyco/opencode/issues/5694) | 2025-12-17 | closed | "Local Ollama models are not agentic" — "If I use opencode with BigPickle it works. If I use it with any Ollama model whether local or cloud, it is not able to see files." |

Note: `sst/opencode` now redirects to **`anomalyco/opencode`** (verified via `gh api repos/sst/opencode --jq .full_name`), which is why issue links use that path.

### 7.4 Does any harness officially support tiny local models?

**No. None of them. Two publish explicit minimums that this model cannot meet.**

**Cline.**
The docs are quiet — [docs.cline.bot/running-models-locally/ollama](https://docs.cline.bot/running-models-locally/ollama) gives a RAM table and advises "Keep tasks focused (smaller context = faster responses)" and "Enable **Use Compact Prompt**", with no explicit small-model warning.
Cline's own blog is not quiet.
[cline.bot/blog/local-models-amd](https://cline.bot/blog/local-models-amd) (2025-09-30), reporting AMD's test of 20+ models, states: **"models smaller than Qwen3 Coder 30B consistently fail with Cline, producing broken outputs or refusing to execute commands properly."**
Named failures include gpt-oss-20b, bytedance/seed-oss-36b, and deepseek-r1-0528-qwen3-8b.
The stated cause: "This isn't a limitation of the models themselves but rather a mismatch between model capabilities and Cline's requirements for tool use, code understanding, and autonomous operation."
Effective floor as published: **30B parameters, 32GB RAM, 32K context.**
Ollama's own Cline integration page recommends at least 32K context and suggests `qwen3-coder:480b` and `deepseek-v3.1:671b` ([docs.ollama.com/integrations/cline](https://docs.ollama.com/integrations/cline)).
Cline v3 also shipped an in-product warning, quoted verbatim as the title of [cline/cline#5915](https://github.com/cline/cline/issues/5915) (2025-08-31, open): "Cline uses complex prompts and iterative task execution that may be challenging for less capable models. For best results, it's recommended to use Claude 4 Sonnet for its advanced agentic coding capabilities."
That string was not found in HEAD and appears to have been removed or reworded in v4.

**OpenCode.**
[opencode.ai/docs/models](https://opencode.ai/docs/models/): "there are only a few of them that are good at both generating code and tool calling."
Recommended models are GPT 5.2, GPT 5.1 Codex, Claude Opus 4.5, Claude Sonnet 4.5, Minimax M2.1, and Gemini 3 Pro.
No local model is recommended and no parameter minimum is published.
[opencode.ai/docs/providers](https://opencode.ai/docs/providers/) does give a working Ollama config, with the tip: "If tool calls aren't working, try increasing `num_ctx` in Ollama. Start around 16k - 32k."
The hardest number available is Ollama's: "OpenCode requires a context length of 64k or higher" ([docs.ollama.com/integrations/opencode](https://docs.ollama.com/integrations/opencode)).

**PI — and this is the finding that most threatens the experiment.**
No public repository or docs site for the PI harness could be located, so no model-requirement statement could be checked (**UNVERIFIED**).
However, Liquid AI's own launch post for this exact model states that LFM2.5-2.6B "works out of the box with popular harnesses like Hermes Agent, OpenClaw, and **Pi**", and that the model was trained "**directly inside** Hermes Agent, OpenClaw, and other harnesses" ([liquid.ai/blog/lfm2-5-2-6b](https://www.liquid.ai/blog/lfm2-5-2-6b)).

If that is the same PI, then **PI is the only harness in the set that the model vendor claims compatibility with, and the only one the model was RL-trained inside.**
Cline and OpenCode are not named.
Expect a large, systematic advantage for PI that is a **training-set artifact, not a measure of harness quality**.
A benchmark that reports "PI wins" without stating this is measuring the wrong thing and will mislead its readers.

---

## 8. Fallback candidates

If tool calling proves unreliable, these are the zero-cost local options with **verified** `tools` capability that fit 12GB VRAM.

**First choice — `qwen3:4b`** ([ollama.com/library/qwen3](https://ollama.com/library/qwen3)).
Badges: `tools` and `thinking`.
Q4_K_M download **2.5 GB**, context **256K** on that tag.
Closest in size to LFM2.5-2.6B, so it preserves the "small local model" premise of the experiment while removing the tool-call plumbing risk.
Ollama has a first-class `qwen3` parser (`model/parsers/qwen3.go`, both `qwen3` and `qwen3-thinking` variants) — a maintained code path, not a template hack.

**Second choice — `qwen3:8b`** (same library page).
Badges `tools` and `thinking`, Q4_K_M **5.2 GB**, context **40K** on the 8b tag.
Comfortable on 12GB with a large KV cache.
Thinking is on by default and burns tokens before every tool call, so use `reasoning_effort: "none"` or `/no_think` for latency-sensitive loops.

Also verified with a `tools` badge, if variety is wanted:

- `llama3.1:8b` — 4.9 GB, 128K context ([library page](https://ollama.com/library/llama3.1)). Oldest of the set; JSON-only tool calling, solid but weaker at multi-step agentic work.
- `granite3.3:8b` — 4.9 GB, 128K context, Apache 2.0 ([library page](https://ollama.com/library/granite3.3)).
- `mistral-nemo:12b` — 7.1 GB, 128K context ([library page](https://ollama.com/library/mistral-nemo)). Last updated about a year ago.
- `qwen3-coder:30b` — `tools` badge, 256K context, but **19 GB at the default tag, exceeding 12GB VRAM**; only viable with partial CPU offload. Named because it is the strongest agentic-CLI performer in the family, with the size caveat stated plainly — and because it is the size class Cline's own blog says is the floor.

**Caveat on the ordering:** no primary-source benchmark ranking these against each other on agentic-CLI tool use was found.
The ordering above is reasoned from Ollama having dedicated Go parsers for the Qwen3 family versus template-derived JSON parsing elsewhere.
That is an inference, not a cited claim.

A zero-Modelfile-work LFM option also exists: `ollama pull lfm2.5-thinking:1.2b` is official, carries `tools` and `thinking` badges with `parser: lfm2-thinking` baked in, and is 731 MB.
But it is 1.2B, materially weaker, and only 32,768 context.

---

## 9. Verdict

### GO — conditional, with a hard pre-flight gate and one disclosure that must be made

**Go, because the mechanical objections all resolve.**

Ollama has a real, maintained, purpose-built Go parser for LFM2's Pythonic format that emits proper `tool_calls` (§3.1).
The out-of-the-box failure is a known, diagnosed, one-Modelfile fix that an Ollama maintainer demonstrated end to end for a sibling model (§3.3, #15953).
The NixOS setup is straightforward and reproducible, with the only real friction being an uncached CUDA build on first rebuild (§2).
Context is not a constraint: 131,072 advertised, and even the full window costs only ~2 GiB of KV on this hybrid architecture, totalling ~4 GB on a 12 GB card (§5.4).
Throughput is comfortable at an estimated 110–160 tok/s generation and thousands of tok/s prefill, putting the whole experiment in overnight-scale wall-clock (§6).

**Conditional, because two risks could still sink it, and both are cheap to test before committing.**

The first is escaping.
[llama.cpp#26658](https://github.com/ggml-org/llama.cpp/issues/26658) is **open as of 2026-08-07**, names this exact GGUF repo, and describes Pythonic tool-call arguments being mangled by quote handling, with the maintainer conceding "the Python syntax parsing is an incomplete implementation."
That is llama.cpp's parser rather than Ollama's Go one, but no Ollama-side test proving correct backslash and quote handling was found.
In a *coding* benchmark, nearly every tool argument is quote-heavy, so this is not an edge case — it is the main path.

The second is competence under load.
The Ollama maintainer's repeated verdict across #14742 and #14928 is that these models "can call tools, [they're] just not very good at it", and that "using a coding assistant that loads up the context with instructions and tools often results in malformed tool calls."
Cline's own blog puts the working floor at 30B (§7.4).
Meanwhile the model's own Hugging Face discussion #2 — "how is it so bad at mcp usage?" — has two independent users reporting near-total MCP failure and **no vendor reply**.

**The pre-flight gate — run this before committing to the full experiment:**

1. Build the model per §3.5 and confirm `ollama show` lists `tools` and `thinking`.
2. Issue 20 tool calls through `/v1/chat/completions` whose arguments contain single quotes, double quotes, backslashes, and newlines — i.e. real file writes and real shell commands.
   If the parsed `tool_calls` arguments do not round-trip byte-for-byte, **stop and switch to the fallback.**
3. Confirm each of the four harnesses tolerates Ollama's non-standard `reasoning` response field.
   OpenCode specifically hung at 100% CPU on this ([#21903](https://github.com/anomalyco/opencode/issues/21903)); verify the pinned version carries the fix.
4. Confirm `OLLAMA_CONTEXT_LENGTH` actually took effect, by logging `n_ctx` from the server and prompt token counts per turn.
   Without this instrumentation the benchmark cannot distinguish parser mismatch from silent truncation from effective-context decay — all three look identical from the outside, and all three look like "the small model is dumb" (§7.1).

If the gate fails, fall back to **`qwen3:4b`** (2.5 GB, 256K context, first-class Ollama parser), which preserves the small-local-model premise, or **`qwen3:8b`** if more headroom is wanted.

**The disclosure that must be made regardless of the gate.**

Liquid AI states the model was trained "directly inside Hermes Agent, OpenClaw, and other harnesses", and names **Pi** among the harnesses it works with out of the box ([liquid.ai/blog/lfm2-5-2-6b](https://www.liquid.ai/blog/lfm2-5-2-6b)).
PI is one of the four harnesses under test.
Any PI advantage this benchmark measures is confounded with the model's training distribution and **cannot be attributed to harness design**.
This must be stated in the results, not buried in methodology, or the benchmark's headline conclusion will be wrong.

If that confound is unacceptable, the cleanest correction is to run the full matrix against **both** LFM2.5-2.6B and a neutral model (`qwen3:4b`) that was not trained inside any of the four harnesses.
The delta between the two matrices isolates the training artifact, and doubling the run cost is affordable within the wall-clock budget in §6.5.

---

## 10. Consolidated list of things that could not be verified

- Whether Ollama's Go `LFM2Parser` handles backslash-and-quote-heavy Pythonic arguments correctly. The analogous llama.cpp bug is open ([#26658](https://github.com/ggml-org/llama.cpp/issues/26658)); no Ollama-side test or issue was found either way.
- Real-world tool-call success rate of LFM2.5-**2.6B** specifically on Ollama. Every maintainer datapoint found concerns 1.2B, 8B-A1B, or lfm2:24b. The GGUF is only about six days old (manifest `created: 2026-08-01`).
- Whether `ollama-cuda` is substitutable from `cache.nixos-cuda.org` (needs a local `nix eval` for the store path).
- Whether a simple `overrideAttrs` version bump of the `ollama` package builds (`vendorHash` plus llama.cpp submodule).
- Whether Ollama's `hf.co/` route accepts a commit SHA for pinning. Not documented by Hugging Face.
- NVIDIA-owned confirmation of the 15 Gbps memory clock / 360 GB/s bandwidth for the RTX 3060 12GB. NVIDIA omits it; TechPowerUp returned 403.
- Any published LFM2.5 tokens/sec figure on any NVIDIA consumer GPU.
- Any RULER or equivalent effective-context measurement for LFM2.5-2.6B.
- The exact Ollama release that introduced VRAM-tiered default context lengths.
- PI's system prompt size, model requirements, and repository location. No public repo or docs site was located.
- The end-to-end NixOS snippet in §3.5 (hash-pinned GGUF + `RENDERER`/`PARSER` in a oneshot unit) is a synthesis of two separately-verified facts and was not executed on a NixOS machine.
- The impact of Ollama's `lfm2` renderer emitting `<|tool_list_start|>` wrapper tokens that LFM2.5's own template does not use (§3.6).
