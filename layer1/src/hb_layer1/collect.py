"""Drive each arm against the recording mock and write the Layer 1 dataset.

    hb-collect --arm pi --arm opencode --profile isolated --profile ambient

One run is one (arm, profile, task) triple. It gets a fresh mock on an ephemeral
port, a fresh copy of the task workspace, and a fresh run directory; nothing is
shared between runs, so a run that hangs or crashes cannot contaminate the next.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from .arms import AMBIENT, ARMS, ISOLATED, ArmUnavailable, MODEL_ID
from .mock_server import MockConfig, RecordingMock
from .records import RunContext, RunRecorder, write_manifest
from .script import DEFAULT_SCRIPT
from .tokenizer import DEFAULT_ENCODING, load_tokenizer

REPO_LAYER1 = Path(__file__).resolve().parents[2]
DEFAULT_TASKS_DIR = REPO_LAYER1 / "tasks"
DEFAULT_OUT_DIR = REPO_LAYER1 / "data"
PROMPT_FILE = "prompt.txt"
PROBE_FILE = "PROBE.md"


def default_ws_root() -> Path:
    """Stage outside every repository and outside the dev's home, on purpose.

    Two separate effects force this. OpenCode walks up from the working
    directory to the enclosing git root and injects the context files it finds
    there: staging under this repo put harness-bench's own `CONTEXT.md` into
    every OpenCode request for 4,918 extra bytes, measuring the instrument's
    repository instead of the harness. And the path itself lands verbatim in the
    arms' system prompts, so a path under `~` would put the machine's username
    into the published captures (#22).
    """
    return Path(Path.cwd().anchor) / "hb" if os.name == "nt" else Path("/tmp/hb")


def load_prompt(task_dir: Path) -> str:
    """The prompt is read as bytes and decoded once, so it is byte-identical
    across arms (#10) — the precondition for the whole measurement."""
    return (task_dir / PROMPT_FILE).read_bytes().decode("utf-8")


def stage_workspace(task_dir: Path, workspaces_root: Path, name: str = "run") -> Path:
    """Stage the task at a path that is byte-identical for every run.

    The arms put the working directory into their system prompt, so the path is
    part of the measurement twice over: a longer path is more bytes, and a
    differently-spelled path of the same length is a different *token* count.
    The first two passes of this instrument hit both — "ambient" being one
    character shorter than "isolated", then a per-run hex digest tokenising
    differently between runs. So the sandbox has one fixed name and is rebuilt
    per run, which also means two collections must not run concurrently against
    the same output directory.
    """
    sandbox = workspaces_root / name
    if sandbox.exists():
        shutil.rmtree(sandbox, ignore_errors=True)
    workspace = sandbox / "workspace"
    workspace.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(task_dir, workspace)
    (workspace / PROMPT_FILE).unlink(missing_ok=True)
    return workspace


def run_one(
    arm_name: str,
    profile: str,
    task_dir: Path,
    out_dir: Path,
    runs_root: Path,
    workspaces_root: Path,
    timeout: int,
    encoding: str,
) -> dict:
    arm = ARMS[arm_name]
    task = task_dir.name
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{task}-{arm_name}-{profile}-{stamp}"
    run_dir = runs_root / run_id
    run_dir.mkdir(parents=True)
    workspace = stage_workspace(task_dir, workspaces_root)
    prompt = load_prompt(task_dir)

    try:
        version = arm.version()
    except (ArmUnavailable, OSError, subprocess.SubprocessError) as exc:
        return {
            "run_id": run_id,
            "arm": arm_name,
            "profile": profile,
            "task": task,
            "status": "unavailable",
            "detail": str(exc),
        }

    tokenizer = load_tokenizer(encoding)
    context = RunContext(
        run_id=run_id,
        arm=arm_name,
        arm_version=version,
        profile=profile,
        task=task,
        model_id=MODEL_ID,
        tokenizer=tokenizer.name,
        script_steps=len(DEFAULT_SCRIPT),
    )
    recorder = RunRecorder(out_dir, context)
    config = MockConfig(tokenizer=tokenizer, probe_path=str(workspace / PROBE_FILE), sink=recorder.sink)

    started = time.monotonic()
    with RecordingMock(config) as mock:
        invocation = arm.prepare(workspace.parent, workspace, mock.base_url, profile, prompt)
        stdout_path = run_dir / "stdout.jsonl"
        stderr_path = run_dir / "stderr.txt"
        status = "ok"
        exit_code: int | None = None
        with stdout_path.open("wb") as out, stderr_path.open("wb") as err:
            try:
                completed = subprocess.run(
                    invocation.command,
                    cwd=invocation.cwd,
                    env=invocation.env,
                    stdin=subprocess.DEVNULL,
                    stdout=out,
                    stderr=err,
                    timeout=timeout,
                )
                exit_code = completed.returncode
            except subprocess.TimeoutExpired:
                status = "timeout"
            except OSError as exc:
                status = "spawn_failed"
                err.write(str(exc).encode())
        requests_seen = mock.request_count
        steps_seen = mock.step_count

    if status == "ok" and requests_seen == 0:
        status = "no_requests"
    if config.errors:
        status = "script_error"

    manifest = {
        "run_id": run_id,
        "arm": arm_name,
        "arm_version": version,
        "profile": profile,
        "task": task,
        "status": status,
        "exit_code": exit_code,
        "requests": requests_seen,
        "agent_steps": steps_seen,
        "records": recorder.count,
        "script_errors": config.errors,
        "wall_seconds": round(time.monotonic() - started, 3),
        "command": invocation.command,
        "run_dir": str(run_dir),
        "workspace": str(workspace),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    write_manifest(out_dir, manifest)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect Layer 1 request-shape records")
    parser.add_argument("--arm", action="append", choices=sorted(ARMS), default=None)
    parser.add_argument("--profile", action="append", choices=[ISOLATED, AMBIENT], default=None)
    parser.add_argument("--task", default="probe")
    parser.add_argument("--tasks-dir", type=Path, default=DEFAULT_TASKS_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--runs-dir", type=Path, default=None)
    parser.add_argument("--ws-root", type=Path, default=None, help=default_ws_root.__doc__)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--encoding", default=DEFAULT_ENCODING)
    args = parser.parse_args(argv)

    arms = args.arm or sorted(ARMS)
    profiles = args.profile or [ISOLATED, AMBIENT]
    task_dir = args.tasks_dir / args.task
    if not task_dir.is_dir():
        parser.error(f"no task workspace at {task_dir}")
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    runs_root = args.runs_dir or (out_dir / "runs")
    runs_root.mkdir(parents=True, exist_ok=True)
    workspaces_root = args.ws_root or default_ws_root()
    workspaces_root.mkdir(parents=True, exist_ok=True)

    failures = 0
    for arm_name in arms:
        for profile in profiles:
            manifest = run_one(
                arm_name,
                profile,
                task_dir,
                out_dir,
                runs_root,
                workspaces_root,
                args.timeout,
                args.encoding,
            )
            if manifest["status"] != "ok":
                failures += 1
            print(
                f"{manifest['arm']:<9} {manifest['profile']:<9} "
                f"{manifest['status']:<13} requests={manifest.get('requests', 0)} "
                f"exit={manifest.get('exit_code')}"
            )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
