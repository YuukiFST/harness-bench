"""Render the Layer 1 tables from the raw records, with no manual step.

    hb-report --out data --report data/report.md

Four tables, in the order the argument needs them: what each arm sends on the
first request, what the machine's ambient state adds to that, how the request
grows over the scripted steps, and the pi vs oh-my-pi ratio that is the flagship
instance of #9's question.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from .arms import AMBIENT, ISOLATED

FIRST_REQUEST_COLUMNS = [
    "arm",
    "arm_version",
    "tool_schema_count",
    "tools_bytes",
    "system_bytes",
    "conversation_bytes",
    "envelope_bytes",
    "total_bytes",
    "prompt_tokens",
]


def load(out_dir: Path, name: str) -> list[dict]:
    path = out_dir / name
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def latest_by_run(records: list[dict]) -> dict[tuple[str, str, str], dict[int, dict]]:
    """Keep the newest run per (task, arm, profile); n = 1, so a re-run replaces."""
    newest: dict[tuple[str, str, str], str] = {}
    for record in records:
        key = (record["task"], record["arm"], record["profile"])
        if key not in newest or record["run_id"] > newest[key]:
            newest[key] = record["run_id"]
    by_key: dict[tuple[str, str, str], dict[int, dict]] = {}
    for record in records:
        key = (record["task"], record["arm"], record["profile"])
        if record["run_id"] != newest[key] or record.get("error"):
            continue
        if record.get("step_index") is None:
            continue  # auxiliary calls are reported separately, not as steps
        by_key.setdefault(key, {})[record["step_index"]] = record
    return by_key


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    lines += ["| " + " | ".join(rows_) + " |" for rows_ in (map(str, row) for row in rows)]
    return "\n".join(lines)


def first_request_rows(by_key, task: str, profile: str) -> list[dict]:
    rows = []
    for (task_name, arm, prof), steps in sorted(by_key.items()):
        if task_name != task or prof != profile or 0 not in steps:
            continue
        rows.append({column: steps[0].get(column) for column in FIRST_REQUEST_COLUMNS})
    return rows


def ambient_rows(by_key, task: str) -> list[dict]:
    rows = []
    arms = sorted({arm for (task_name, arm, _), _ in by_key.items() if task_name == task})
    for arm in arms:
        isolated = by_key.get((task, arm, ISOLATED), {}).get(0)
        ambient = by_key.get((task, arm, AMBIENT), {}).get(0)
        if not isolated or not ambient:
            continue
        delta = ambient["total_bytes"] - isolated["total_bytes"]
        rows.append(
            {
                "arm": arm,
                "isolated_total_bytes": isolated["total_bytes"],
                "ambient_total_bytes": ambient["total_bytes"],
                "delta_bytes": delta,
                "ratio": round(ambient["total_bytes"] / isolated["total_bytes"], 3),
                "isolated_prompt_tokens": isolated["prompt_tokens"],
                "ambient_prompt_tokens": ambient["prompt_tokens"],
            }
        )
    return rows


def growth_rows(by_key, task: str, profile: str) -> list[dict]:
    rows = []
    for (task_name, arm, prof), steps in sorted(by_key.items()):
        if task_name != task or prof != profile:
            continue
        row = {"arm": arm}
        for index in sorted(steps):
            row[f"step_{index}_total_bytes"] = steps[index]["total_bytes"]
        rows.append(row)
    return rows


def ratio_rows(by_key, task: str, profile: str, left: str, right: str) -> list[dict]:
    a = by_key.get((task, left, profile), {}).get(0)
    b = by_key.get((task, right, profile), {}).get(0)
    if not a or not b:
        return []
    fields = ["total_bytes", "tools_bytes", "system_bytes", "tool_schema_count", "prompt_tokens"]
    return [
        {
            "metric": field,
            left: a[field],
            right: b[field],
            "ratio": round(b[field] / a[field], 3) if a[field] else None,
        }
        for field in fields
    ]


def auxiliary_rows(records: list[dict]) -> list[dict]:
    """Model calls a harness makes outside the agent loop — OpenCode's session
    title call is the one #4 warned the arms' own reporting omits."""
    counts: dict[tuple[str, str], dict] = {}
    for record in records:
        if record.get("step_index") is not None or record.get("error"):
            continue
        key = (record["arm"], record["profile"])
        row = counts.setdefault(
            key,
            {"arm": record["arm"], "profile": record["profile"], "calls": 0, "total_bytes": 0},
        )
        row["calls"] += 1
        row["total_bytes"] += record.get("total_bytes", 0)
    return [counts[key] for key in sorted(counts)]


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def section(title: str, rows: list[dict], empty: str) -> str:
    if not rows:
        return f"### {title}\n\n_{empty}_\n"
    headers = list(rows[0])
    body = markdown_table(headers, [[row.get(h, "") for h in headers] for row in rows])
    return f"### {title}\n\n{body}\n"


def build_report(out_dir: Path, task: str, left: str, right: str) -> str:
    records = load(out_dir, "records.jsonl")
    runs = load(out_dir, "runs.jsonl")
    by_key = latest_by_run(records)
    tokenizers = sorted({record.get("tokenizer", "?") for record in records})

    parts = [
        "# Layer 1 — request shape",
        "",
        f"Task `{task}`, n = 1 (the mock is deterministic). "
        f"Token counts use the proxy tokenizer `{', '.join(tokenizers) or 'n/a'}` and are "
        "comparable between arms only, never against a gateway's own `prompt_tokens`.",
        "",
        section(
            "First request, isolated environment",
            first_request_rows(by_key, task, ISOLATED),
            "no isolated-profile records",
        ),
        section(
            "Ambient-state delta (real HOME minus fresh HOME)",
            ambient_rows(by_key, task),
            "no arm has both profiles recorded",
        ),
        section(
            "Per-step growth, isolated environment",
            growth_rows(by_key, task, ISOLATED),
            "no isolated-profile records",
        ),
        section(
            f"{left} vs {right}, first request, isolated",
            ratio_rows(by_key, task, ISOLATED, left, right),
            f"{left} and {right} are not both recorded for this task",
        ),
        section(
            "Auxiliary (tool-less) model calls per run",
            auxiliary_rows(records),
            "no arm made a tool-less model call",
        ),
        section(
            "Runs",
            [
                {
                    "run_id": run["run_id"],
                    "status": run["status"],
                    "exit_code": run.get("exit_code"),
                    "requests": run.get("requests"),
                    "wall_seconds": run.get("wall_seconds"),
                }
                for run in runs
            ],
            "no runs recorded",
        ),
    ]
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render Layer 1 tables from raw records")
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[2] / "data")
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--task", default="probe")
    parser.add_argument("--left", default="pi")
    parser.add_argument("--right", default="omp")
    args = parser.parse_args(argv)

    out_dir = args.out
    records = load(out_dir, "records.jsonl")
    by_key = latest_by_run(records)
    write_csv(out_dir / "first_request.csv", first_request_rows(by_key, args.task, ISOLATED))
    write_csv(out_dir / "ambient_delta.csv", ambient_rows(by_key, args.task))
    write_csv(out_dir / "step_growth.csv", growth_rows(by_key, args.task, ISOLATED))

    report = build_report(out_dir, args.task, args.left, args.right)
    report_path = args.report or (out_dir / "report.md")
    report_path.write_text(report + "\n", encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
