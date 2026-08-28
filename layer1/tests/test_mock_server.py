import json
import urllib.error
import urllib.request

from fake_arm import run_fake_arm

from hb_layer1.mock_server import MockConfig, RecordingMock
from hb_layer1.records import RunContext, RunRecorder, load_records
from hb_layer1.script import DEFAULT_SCRIPT


def _recorder(tmp_path, tokenizer):
    context = RunContext(
        run_id="probe-fake-isolated-test",
        arm="fake",
        arm_version="0",
        profile="isolated",
        task="probe",
        model_id="MOCK-2.6B",
        tokenizer=tokenizer.name,
        script_steps=len(DEFAULT_SCRIPT),
    )
    return RunRecorder(tmp_path, context)


def test_the_script_drives_exactly_its_own_number_of_steps(tokenizer, tmp_path):
    recorder = _recorder(tmp_path, tokenizer)
    config = MockConfig(tokenizer=tokenizer, probe_path="/w/PROBE.md", sink=recorder.sink)
    with RecordingMock(config) as mock:
        sent = run_fake_arm(mock.base_url)
    assert len(sent) == len(DEFAULT_SCRIPT)
    assert mock.request_count == len(DEFAULT_SCRIPT)
    assert config.errors == []


def test_records_carry_the_shape_and_the_raw_body(tokenizer, tmp_path):
    recorder = _recorder(tmp_path, tokenizer)
    config = MockConfig(tokenizer=tokenizer, probe_path="/w/PROBE.md", sink=recorder.sink)
    with RecordingMock(config) as mock:
        run_fake_arm(mock.base_url)

    records = load_records(tmp_path)
    assert [record["step_index"] for record in records] == list(range(len(DEFAULT_SCRIPT)))
    first = records[0]
    assert first["tool_names"] == ["read"]
    assert first["arm"] == "fake"
    assert first["authorization_sent"] is True
    body = (tmp_path / first["body_path"]).read_bytes()
    assert len(body) == first["total_bytes"]


def test_request_grows_monotonically_because_the_fake_arm_resends_history(tokenizer, tmp_path):
    recorder = _recorder(tmp_path, tokenizer)
    config = MockConfig(tokenizer=tokenizer, probe_path="/w/PROBE.md", sink=recorder.sink)
    with RecordingMock(config) as mock:
        run_fake_arm(mock.base_url)
    totals = [record["total_bytes"] for record in load_records(tmp_path)]
    assert totals == sorted(totals)
    assert totals[-1] > totals[0]


def test_streaming_carries_finish_reason_and_a_usage_frame(tokenizer, tmp_path):
    recorder = _recorder(tmp_path, tokenizer)
    config = MockConfig(tokenizer=tokenizer, probe_path="/w/PROBE.md", sink=recorder.sink)
    with RecordingMock(config) as mock:
        request = urllib.request.Request(
            f"{mock.base_url}/chat/completions",
            data=json.dumps(
                {
                    "model": "MOCK-2.6B",
                    "stream": True,
                    "messages": [{"role": "user", "content": "hi"}],
                    "tools": [{"type": "function", "function": {"name": "read", "parameters": {}}}],
                }
            ).encode(),
            headers={"content-type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            raw = response.read().decode()
    chunks = [
        json.loads(line[len("data: ") :])
        for line in raw.splitlines()
        if line.startswith("data: ") and line != "data: [DONE]"
    ]
    assert raw.rstrip().endswith("data: [DONE]")
    assert any(
        choice.get("finish_reason") == "tool_calls"
        for chunk in chunks
        for choice in chunk.get("choices", [])
    )
    usage = [chunk["usage"] for chunk in chunks if "usage" in chunk]
    assert usage and usage[0]["prompt_tokens"] > 0


def test_streaming_arm_completes_the_same_script(tokenizer, tmp_path):
    recorder = _recorder(tmp_path, tokenizer)
    config = MockConfig(tokenizer=tokenizer, probe_path="/w/PROBE.md", sink=recorder.sink)
    with RecordingMock(config) as mock:
        sent = run_fake_arm(mock.base_url, stream=True)
    assert len(sent) == len(DEFAULT_SCRIPT)


def test_an_arm_offering_no_usable_tool_is_recorded_as_a_script_error(tokenizer, tmp_path):
    recorder = _recorder(tmp_path, tokenizer)
    config = MockConfig(tokenizer=tokenizer, probe_path="/w/PROBE.md", sink=recorder.sink)
    with RecordingMock(config) as mock:
        request = urllib.request.Request(
            f"{mock.base_url}/chat/completions",
            data=json.dumps(
                {
                    "model": "MOCK-2.6B",
                    "messages": [{"role": "user", "content": "hi"}],
                    "tools": [{"type": "function", "function": {"name": "teleport", "parameters": {}}}],
                }
            ).encode(),
            headers={"content-type": "application/json"},
        )
        try:
            urllib.request.urlopen(request, timeout=10)
            raised = False
        except urllib.error.HTTPError as exc:
            raised = True
            payload = json.loads(exc.read().decode())
    assert raised
    assert payload["type"] == "error"
    assert config.errors and "teleport" in config.errors[0]


def test_models_endpoint_answers_for_the_arms_that_probe_it(tokenizer):
    config = MockConfig(tokenizer=tokenizer, probe_path="/w/PROBE.md")
    with RecordingMock(config) as mock:
        with urllib.request.urlopen(f"{mock.base_url}/models", timeout=10) as response:
            payload = json.loads(response.read().decode())
    assert payload["data"][0]["id"] == "MOCK-2.6B"


def test_a_tool_less_request_is_auxiliary_and_does_not_consume_a_script_step(tokenizer, tmp_path):
    """OpenCode opens a session with a title-generation call carrying no tools."""
    recorder = _recorder(tmp_path, tokenizer)
    config = MockConfig(tokenizer=tokenizer, probe_path="/w/PROBE.md", sink=recorder.sink)
    with RecordingMock(config) as mock:
        run_fake_arm(mock.base_url, tools=[], max_steps=1)
        assert mock.step_count == 0
        sent = run_fake_arm(mock.base_url)
    assert len(sent) == len(DEFAULT_SCRIPT)
    assert mock.step_count == len(DEFAULT_SCRIPT)
    records = load_records(tmp_path)
    assert records[0]["request_role"] == "auxiliary"
    assert records[0]["step_index"] is None
    assert [record["step_index"] for record in records[1:]] == list(range(len(DEFAULT_SCRIPT)))
