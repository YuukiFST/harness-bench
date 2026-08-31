import json

from hb_layer1.decompose import decompose

BODY = {
    "model": "MOCK-2.6B",
    "stream": True,
    "stream_options": {"include_usage": True},
    "messages": [
        {"role": "system", "content": "you are a coding agent"},
        {"role": "user", "content": "read PROBE.md"},
    ],
    "tools": [
        {"type": "function", "function": {"name": "read", "parameters": {"required": ["path"]}}},
        {"type": "function", "function": {"name": "bash", "parameters": {"required": ["command"]}}},
    ],
}


def test_buckets_partition_the_raw_body(tokenizer):
    body = json.dumps(BODY).encode()
    shape = decompose(body, tokenizer)
    assert shape.total_bytes == len(body)
    assert (
        shape.system_bytes + shape.conversation_bytes + shape.tools_bytes + shape.envelope_bytes
        == shape.total_bytes
    )
    assert shape.envelope_bytes > 0


def test_developer_role_counts_as_system(tokenizer):
    with_developer = dict(BODY, messages=[{"role": "developer", "content": "x"}])
    shape = decompose(json.dumps(with_developer).encode(), tokenizer)
    assert shape.system_message_count == 1
    assert shape.conversation_bytes == 0


def test_tool_names_and_count_are_read_from_the_wire(tokenizer):
    shape = decompose(json.dumps(BODY).encode(), tokenizer)
    assert shape.tool_schema_count == 2
    assert shape.tool_names == ("read", "bash")


def test_prompt_tokens_is_the_sum_of_its_parts(tokenizer):
    shape = decompose(json.dumps(BODY).encode(), tokenizer)
    assert shape.prompt_tokens == shape.system_tokens + shape.conversation_tokens + shape.tools_tokens
    assert shape.tokenizer == "fake-words"


def test_a_body_without_tools_reports_zero_tool_bytes(tokenizer):
    without_tools = {key: value for key, value in BODY.items() if key != "tools"}
    shape = decompose(json.dumps(without_tools).encode(), tokenizer)
    assert shape.tools_bytes == 0
    assert shape.tool_schema_count == 0
    assert (
        shape.system_bytes + shape.conversation_bytes + shape.envelope_bytes == shape.total_bytes
    )
