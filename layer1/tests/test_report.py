import json

from hb_layer1.report import ambient_rows, build_report, first_request_rows, latest_by_run, ratio_rows


def record(arm, profile, step, total, run="r1", **extra):
    base = {
        "run_id": f"{arm}-{profile}-{run}",
        "arm": arm,
        "arm_version": "1.0",
        "profile": profile,
        "task": "probe",
        "step_index": step,
        "total_bytes": total,
        "system_bytes": total // 2,
        "conversation_bytes": total // 4,
        "tools_bytes": total // 4,
        "envelope_bytes": 0,
        "tool_schema_count": 4,
        "prompt_tokens": total // 4,
        "tokenizer": "fake-words",
        "error": None,
    }
    base.update(extra)
    return base


RECORDS = [
    record("pi", "isolated", 0, 5739),
    record("pi", "isolated", 1, 6100),
    record("pi", "ambient", 0, 14233),
    record("omp", "isolated", 0, 62111, tool_schema_count=11),
    record("omp", "ambient", 0, 62111, tool_schema_count=11),
]


def write(tmp_path, records):
    with (tmp_path / "records.jsonl").open("w", encoding="utf-8") as handle:
        for item in records:
            handle.write(json.dumps(item) + "\n")


def test_first_request_table_has_one_row_per_arm(tmp_path):
    write(tmp_path, RECORDS)
    by_key = latest_by_run(RECORDS)
    rows = first_request_rows(by_key, "probe", "isolated")
    assert sorted(row["arm"] for row in rows) == ["omp", "pi"]


def test_ambient_delta_is_ambient_minus_isolated(tmp_path):
    by_key = latest_by_run(RECORDS)
    rows = {row["arm"]: row for row in ambient_rows(by_key, "probe")}
    assert rows["pi"]["delta_bytes"] == 14233 - 5739
    assert rows["pi"]["ratio"] == round(14233 / 5739, 3)
    assert rows["omp"]["delta_bytes"] == 0


def test_the_flagship_ratio_is_computed_from_the_records(tmp_path):
    by_key = latest_by_run(RECORDS)
    rows = {row["metric"]: row for row in ratio_rows(by_key, "probe", "isolated", "pi", "omp")}
    assert rows["total_bytes"]["ratio"] == round(62111 / 5739, 3)


def test_a_rerun_replaces_the_earlier_run_because_n_is_one():
    older = record("pi", "isolated", 0, 1, run="20260101T000000Z")
    newer = record("pi", "isolated", 0, 2, run="20260102T000000Z")
    by_key = latest_by_run([older, newer])
    assert by_key[("probe", "pi", "isolated")][0]["total_bytes"] == 2


def test_records_marked_with_an_error_are_excluded():
    by_key = latest_by_run([record("pi", "isolated", 0, 10, error="undecodable body")])
    assert by_key == {}


def test_report_renders_every_section(tmp_path):
    write(tmp_path, RECORDS)
    report = build_report(tmp_path, "probe", "pi", "omp")
    assert "First request, isolated environment" in report
    assert "Ambient-state delta" in report
    assert "Per-step growth" in report
    assert "pi vs omp" in report
    assert "fake-words" in report
