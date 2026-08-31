"""The Layer 1 dataset: one JSONL record per request, plus the raw body.

Every reported figure is derived from these records with no manual step, and
every record points at the exact bytes it was derived from, so a number in the
document can be re-checked against the wire capture that produced it.
"""

from __future__ import annotations

import hashlib
import json
import threading
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from .decompose import RequestShape

# Headers worth keeping: they identify the client and the wire format. The
# credential itself is never stored, only whether one was sent.
KEPT_HEADERS = ("user-agent", "content-type", "accept", "x-stainless-package-version")


@dataclass(frozen=True)
class RunContext:
    run_id: str
    arm: str
    arm_version: str
    profile: str
    task: str
    model_id: str
    tokenizer: str
    script_steps: int


class RunRecorder:
    """Sink for `MockConfig.sink`, writing records and bodies under `out_dir`."""

    def __init__(self, out_dir: Path, context: RunContext) -> None:
        self.out_dir = out_dir
        self.context = context
        self.bodies_dir = out_dir / "bodies" / context.run_id
        self.bodies_dir.mkdir(parents=True, exist_ok=True)
        self.records_path = out_dir / "records.jsonl"
        self._lock = threading.Lock()
        self.count = 0

    def sink(
        self,
        request_index: int,
        step_index: int | None,
        body: bytes,
        headers: dict[str, str],
        shape: RequestShape | None,
        error: str | None,
    ) -> None:
        body_path = self.bodies_dir / f"request-{request_index:02d}.json"
        body_path.write_bytes(body)
        record = {
            **asdict(self.context),
            "request_index": request_index,
            "step_index": step_index,
            "request_role": "agent" if step_index is not None else "auxiliary",
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "body_path": str(body_path.relative_to(self.out_dir)).replace("\\", "/"),
            "body_sha256": hashlib.sha256(body).hexdigest(),
            "error": error,
            "headers": {key: headers[key] for key in KEPT_HEADERS if key in headers},
            "authorization_sent": "authorization" in headers,
        }
        if shape is not None:
            record.update(shape.as_dict())
            record["tool_names"] = list(shape.tool_names)
        with self._lock:
            with self.records_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            self.count += 1


def scrub_home(value: str) -> str:
    """Rewrite the dev's home directory as `~` so the committed dataset does not
    carry a username; the repo is published in #22."""
    home = str(Path.home())
    return value.replace(home, "~").replace(home.replace("\\", "/"), "~")


def write_manifest(out_dir: Path, manifest: dict) -> None:
    """Append one run manifest — the outcome of the arm process itself."""
    manifest = {
        key: (
            scrub_home(value)
            if isinstance(value, str)
            else [scrub_home(item) for item in value]
            if isinstance(value, list) and all(isinstance(item, str) for item in value)
            else value
        )
        for key, value in manifest.items()
    }
    path = out_dir / "runs.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(manifest, ensure_ascii=False) + "\n")


def load_records(out_dir: Path) -> list[dict]:
    path = out_dir / "records.jsonl"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]
