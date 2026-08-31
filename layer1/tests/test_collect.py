import os
from pathlib import Path

from hb_layer1.arms import ARMS_DIR_ENV, resolve_binary
from hb_layer1.collect import default_ws_root, stage_workspace

TASK = Path(__file__).resolve().parents[1] / "tasks" / "probe"


def test_every_run_gets_the_byte_identical_workspace_path(tmp_path):
    """Path length *and* spelling are measurement inputs: the arms put the cwd
    into their system prompt, so a per-run name would move both bytes and
    tokens between arms."""
    first = stage_workspace(TASK, tmp_path)
    second = stage_workspace(TASK, tmp_path)
    assert first == second
    assert (second / "PROBE.md").exists()


def test_restaging_clears_what_the_previous_arm_wrote(tmp_path):
    workspace = stage_workspace(TASK, tmp_path)
    (workspace / "written-by-the-agent.txt").write_text("x", encoding="utf-8")
    workspace = stage_workspace(TASK, tmp_path)
    assert not (workspace / "written-by-the-agent.txt").exists()


def test_the_prompt_never_lands_in_the_workspace(tmp_path):
    workspace = stage_workspace(TASK, tmp_path)
    assert not (workspace / "prompt.txt").exists()


def test_the_manifest_does_not_carry_the_devs_home_path(tmp_path):
    from pathlib import Path as _Path

    from hb_layer1.records import write_manifest

    write_manifest(tmp_path, {"run_dir": str(_Path.home() / "x"), "command": [str(_Path.home())]})
    written = (tmp_path / "runs.jsonl").read_text(encoding="utf-8")
    assert str(_Path.home()) not in written
    assert "~" in written


def test_the_default_workspace_root_is_outside_the_repo_and_outside_home():
    """OpenCode walks up to the git root and injects the context files it finds,
    and every arm puts the working directory into its system prompt. A default
    under this repo measured harness-bench's own CONTEXT.md; a default under
    `~` would publish the machine's username."""
    root = default_ws_root()
    repo = Path(__file__).resolve().parents[2]
    assert repo not in root.parents and root != repo
    assert Path.home() not in root.parents and root != Path.home()


def test_an_arm_installed_in_the_arms_dir_wins_over_path(tmp_path, monkeypatch):
    """pi writes its own package directory into its system prompt, so a global
    install under the dev's home would leak the username into every capture and
    make the byte count machine-specific."""
    bin_dir = tmp_path / "node_modules" / ".bin"
    bin_dir.mkdir(parents=True)
    suffix = ".cmd" if os.name == "nt" else ""
    pinned = bin_dir / f"pi{suffix}"
    pinned.write_text("", encoding="utf-8")
    monkeypatch.setenv(ARMS_DIR_ENV, str(tmp_path))
    assert resolve_binary("pi") == str(pinned)
