"""The fixed reply sequence the mock plays back.

Per-step growth is a Layer 1 quantity (#37): how a harness's request grows over
the first *k* steps exposes its context-management strategy — full-history
resend, truncation or compaction — without running a real task. That needs the
model side to be a script, not a model, and the script has to be identical for
every arm or the growth curves are not comparable.

The arms do not agree on tool argument names (`path` vs `filePath` vs
`file_path`), so the tool call is built from the schema the arm itself sent,
filling required properties from one shared table. An unknown required property
raises instead of guessing: a guessed argument produces a tool error, which
changes the conversation bytes of the next step and therefore the measurement.
"""

from __future__ import annotations

from dataclasses import dataclass


class ScriptError(RuntimeError):
    """The script cannot be played against the tools this arm offered."""


@dataclass(frozen=True)
class ToolStep:
    """Reply with a tool call, choosing the first offered tool in `prefer`."""

    prefer: tuple[str, ...] = ("read",)


@dataclass(frozen=True)
class TextStep:
    """Reply with plain text, which ends the arm's loop."""

    text: str = "Layer 1 probe complete."


Step = ToolStep | TextStep

# Four tool round trips then a final answer: five recorded requests per run,
# which is the k of "per-step growth over the first k steps".
DEFAULT_SCRIPT: tuple[Step, ...] = (
    ToolStep(),
    ToolStep(),
    ToolStep(),
    ToolStep(),
    TextStep(),
)


def normalise_tool(tool: dict) -> tuple[str, dict]:
    """Return `(name, parameters)` for either tool-schema shape arms send."""
    function = tool.get("function") if isinstance(tool.get("function"), dict) else tool
    name = function.get("name", "")
    parameters = function.get("parameters") or function.get("input_schema") or {}
    return name, parameters if isinstance(parameters, dict) else {}


def choose_tool(tools: list[dict], prefer: tuple[str, ...]) -> tuple[str, dict]:
    """Pick the first preferred tool the arm actually offered."""
    if not tools:
        raise ScriptError("the arm offered no tool schemas, so no tool call can be scripted")
    by_name = {}
    for tool in tools:
        name, parameters = normalise_tool(tool)
        by_name[name] = parameters
    for wanted in prefer:
        if wanted in by_name:
            return wanted, by_name[wanted]
    raise ScriptError(
        f"none of {prefer} is offered; the arm sent {sorted(by_name)}"
    )


def argument_table(probe_path: str) -> dict[str, object]:
    """Values keyed by the property names the arms use for the same argument."""
    return {
        "path": probe_path,
        "file_path": probe_path,
        "filepath": probe_path,
        "file": probe_path,
        "filename": probe_path,
        "abs_path": probe_path,
        "absolute_path": probe_path,
        "target_file": probe_path,
        "command": "echo harness-bench-layer1",
        "cmd": "echo harness-bench-layer1",
        "description": "Layer 1 probe step",
        # OMP requires a "concise intent" string alongside every tool call.
        "i": "Layer 1 probe step",
        "explanation": "Layer 1 probe step",
        "timeout": 30,
        "offset": 0,
        "limit": 50,
    }


def fill_arguments(parameters: dict, probe_path: str) -> dict:
    """Build arguments for one scripted tool call from the arm's own schema."""
    required = parameters.get("required") or []
    properties = parameters.get("properties") or {}
    table = argument_table(probe_path)
    arguments: dict[str, object] = {}
    unknown: list[str] = []
    for name in required:
        key = str(name).lower()
        if key in table:
            arguments[str(name)] = table[key]
            continue
        unknown.append(str(name))
    if unknown:
        raise ScriptError(
            f"required tool arguments {unknown} are not in the shared argument table; "
            f"offered properties were {sorted(properties)}"
        )
    return arguments
