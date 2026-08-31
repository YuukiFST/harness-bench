"""How each arm is pointed at the mock, headlessly, in two environment profiles.

Every invocation here is the one verified end to end in `docs/research/`:
pi in doc 10, oh-my-pi in doc 07, OpenCode in doc 06.

Two profiles, and the difference between them *is* the ambient-state
measurement of #37:

- `isolated` — a fresh `HOME` and fresh XDG dirs, so nothing on the machine
  reaches the request. This is the profile the cross-arm table is built from.
- `ambient` — the machine's real `HOME`, which is how #26 found pi injecting
  `$HOME/.agents/skills` into its system prompt for a 2.48x inflation.

Both profiles keep `PI_CODING_AGENT_DIR` pointed at a run-local directory: the
mock provider has to be registered somewhere, and writing it into the dev's real
`~/.pi` would pollute the machine being measured.

The discovery-disabling flags the docs recommend for a benchmark run
(`--no-skills`, `--no-extensions`, `--no-context-files`, `--no-rules`) are
deliberately *not* passed. They would erase the exact effect the ambient profile
exists to measure, and the isolated profile already achieves the same result by
construction.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

PROVIDER_ID = "mockollama"
MODEL_ID = "MOCK-2.6B"
CONTEXT_WINDOW = 32768
MAX_TOKENS = 4096

ISOLATED = "isolated"
AMBIENT = "ambient"

# Where the arms are looked for before PATH. An arm installed here wins over a
# global install, because pi writes its own package directory into its system
# prompt: a global install under the dev's home would put the machine's username
# into every committed capture (#22) and make the byte count machine-specific.
# HB_ARMS_DIR overrides it so the install root can be short and neutral.
DEFAULT_ARMS_DIR = Path(__file__).resolve().parents[2] / ".arms"
ARMS_DIR_ENV = "HB_ARMS_DIR"


def arms_bin_dir() -> Path:
    root = os.environ.get(ARMS_DIR_ENV)
    return (Path(root) if root else DEFAULT_ARMS_DIR) / "node_modules" / ".bin"


class ArmUnavailable(RuntimeError):
    """The arm's binary is not installed on this machine."""


@dataclass(frozen=True)
class Invocation:
    command: list[str]
    env: dict[str, str]
    cwd: Path


def resolve_binary(name: str) -> str:
    # npm writes both a POSIX shell script and a .cmd shim into node_modules/.bin;
    # on Windows CreateProcess rejects the extensionless one with WinError 193.
    suffixes = (".cmd", ".exe", "") if os.name == "nt" else ("", ".sh")
    bin_dir = arms_bin_dir()
    for suffix in suffixes:
        candidate = bin_dir / f"{name}{suffix}"
        if candidate.exists():
            return str(candidate)
    found = shutil.which(name)
    if found:
        return found
    raise ArmUnavailable(
        f"{name!r} is not in {bin_dir} and not on PATH; "
        "see layer1/README.md for how to install the arms"
    )


def arm_version(name: str) -> str:
    binary = resolve_binary(name)
    result = subprocess.run(
        [binary, "--version"], capture_output=True, text=True, timeout=120
    )
    return (result.stdout or result.stderr).strip().splitlines()[0] if result.stdout or result.stderr else "unknown"


def _env_for(profile: str, home: Path) -> dict[str, str]:
    env = dict(os.environ)
    if profile == AMBIENT:
        return env
    home.mkdir(parents=True, exist_ok=True)
    env["HOME"] = str(home)
    env["USERPROFILE"] = str(home)  # Node's os.homedir() reads this on Windows
    for key, sub in (
        ("XDG_CONFIG_HOME", ".config"),
        ("XDG_DATA_HOME", ".local/share"),
        ("XDG_STATE_HOME", ".local/state"),
        ("XDG_CACHE_HOME", ".cache"),
    ):
        path = home / sub
        path.mkdir(parents=True, exist_ok=True)
        env[key] = str(path)
    # OpenCode puts the OS temp directory into its system prompt verbatim, so
    # the default machine temp path would be both a username leak in the
    # committed captures and a per-machine addend to the byte count.
    temp = home / "tmp"
    temp.mkdir(parents=True, exist_ok=True)
    for key in ("TEMP", "TMP", "TMPDIR"):
        env[key] = str(temp)
    return env


class Arm:
    name = ""
    binary = ""

    def version(self) -> str:
        return arm_version(self.binary)

    def prepare(
        self, sandbox: Path, workspace: Path, base_url: str, profile: str, prompt: str
    ) -> Invocation:
        """`sandbox` holds the run's HOME and agent dir; its path length is held
        constant across runs because the arms put paths into their prompts."""
        raise NotImplementedError


class PiArm(Arm):
    name = "pi"
    binary = "pi"

    def prepare(self, sandbox, workspace, base_url, profile, prompt) -> Invocation:
        agent_dir = sandbox / "agent"
        agent_dir.mkdir(parents=True, exist_ok=True)
        # pi treats a model as unusable without a credential even for a keyless
        # endpoint (doc 10), hence the placeholder apiKey.
        (agent_dir / "models.json").write_text(
            json.dumps(
                {
                    "providers": {
                        PROVIDER_ID: {
                            "baseUrl": base_url,
                            "api": "openai-completions",
                            "apiKey": "layer1",
                            "compat": {
                                "supportsDeveloperRole": False,
                                "supportsReasoningEffort": False,
                            },
                            "models": [
                                {
                                    "id": MODEL_ID,
                                    "name": "Layer 1 mock",
                                    "reasoning": False,
                                    "input": ["text"],
                                    "contextWindow": CONTEXT_WINDOW,
                                    "maxTokens": MAX_TOKENS,
                                    "cost": {
                                        "input": 0,
                                        "output": 0,
                                        "cacheRead": 0,
                                        "cacheWrite": 0,
                                    },
                                }
                            ],
                        }
                    }
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        env = _env_for(profile, sandbox / "home")
        env["PI_CODING_AGENT_DIR"] = str(agent_dir)
        env["PI_OFFLINE"] = "1"
        return Invocation(
            command=[
                resolve_binary(self.binary),
                "--mode",
                "json",
                "--no-session",
                "--model",
                f"{PROVIDER_ID}/{MODEL_ID}",
                prompt,
            ],
            env=env,
            cwd=workspace,  # pi has no --cwd flag (doc 10)
        )


class OmpArm(Arm):
    name = "omp"
    binary = "omp"

    def prepare(self, sandbox, workspace, base_url, profile, prompt) -> Invocation:
        agent_dir = sandbox / "agent"
        agent_dir.mkdir(parents=True, exist_ok=True)
        # OMP reads models.yml, not pi's models.json, and accepts `auth: none`
        # (doc 07). Written literally rather than via a YAML library so the
        # instrument keeps a stdlib-only dependency set.
        (agent_dir / "models.yml").write_text(
            "\n".join(
                [
                    "providers:",
                    f"  {PROVIDER_ID}:",
                    f"    baseUrl: {base_url}",
                    "    api: openai-completions",
                    "    auth: none",
                    "    models:",
                    f"      - id: {MODEL_ID}",
                    "        name: Layer 1 mock",
                    "        api: openai-completions",
                    "        reasoning: false",
                    "        input: [text]",
                    "        cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }",
                    f"        contextWindow: {CONTEXT_WINDOW}",
                    f"        maxTokens: {MAX_TOKENS}",
                    "        compat:",
                    "          supportsDeveloperRole: false",
                    "          supportsReasoningEffort: false",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        env = _env_for(profile, sandbox / "home")
        env["PI_CODING_AGENT_DIR"] = str(agent_dir)
        return Invocation(
            command=[
                resolve_binary(self.binary),
                "--mode",
                "json",
                "--no-session",
                "--auto-approve",
                "--max-time",
                "180",
                "--cwd",
                str(workspace),
                "--model",
                f"{PROVIDER_ID}/{MODEL_ID}",
                prompt,
            ],
            env=env,
            cwd=workspace,
        )


class OpenCodeArm(Arm):
    name = "opencode"
    binary = "opencode"

    def prepare(self, sandbox, workspace, base_url, profile, prompt) -> Invocation:
        env = _env_for(profile, sandbox / "home")
        # OPENCODE_CONFIG_CONTENT beats every config file, including one a task
        # workspace might ship (doc 06).
        env["OPENCODE_CONFIG_CONTENT"] = json.dumps(
            {
                "$schema": "https://opencode.ai/config.json",
                "provider": {
                    PROVIDER_ID: {
                        "npm": "@ai-sdk/openai-compatible",
                        "name": "Layer 1 mock",
                        "options": {
                            "baseURL": base_url,
                            "apiKey": "layer1",
                            "timeout": 120000,
                            "chunkTimeout": 60000,
                        },
                        "models": {
                            MODEL_ID: {
                                "limit": {"context": CONTEXT_WINDOW, "output": MAX_TOKENS}
                            }
                        },
                    }
                },
                "model": f"{PROVIDER_ID}/{MODEL_ID}",
                "small_model": f"{PROVIDER_ID}/{MODEL_ID}",
                # In headless mode "ask" is a hang, not a refusal (doc 06), so
                # every permission class is pinned.
                "permission": {
                    "*": "allow",
                    "external_directory": "deny",
                    "question": "deny",
                    "webfetch": "deny",
                    "websearch": "deny",
                    "doom_loop": "deny",
                },
            }
        )
        command = [resolve_binary(self.binary), "run", "--format", "json", "--dir", str(workspace)]
        if profile == ISOLATED:
            # --pure drops the machine's global plugins. Keeping it out of the
            # ambient profile is the point: ambient means ambient.
            command.append("--pure")
        command += [
            "-m",
            f"{PROVIDER_ID}/{MODEL_ID}",
            "--dangerously-skip-permissions",  # the 1.17.9 spelling of --auto
            prompt,
        ]
        return Invocation(command=command, env=env, cwd=workspace)


ARMS: dict[str, Arm] = {arm.name: arm for arm in (PiArm(), OmpArm(), OpenCodeArm())}
