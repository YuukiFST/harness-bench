import json

import pytest

from hb_layer1.json_spans import JsonSpanError, parse_with_spans


def test_spans_slice_back_to_the_original_bytes():
    body = b'{"a": [1, {"b": "x"}], "c": null}'
    root = parse_with_spans(body)
    assert body[root.start : root.end] == body
    assert body[root.members["a"].start : root.members["a"].end] == b'[1, {"b": "x"}]'
    assert body[root.members["c"].start : root.members["c"].end] == b"null"


def test_escaped_quotes_do_not_end_the_string_span():
    body = json.dumps({"s": 'a "quoted" \\ tail', "n": 1}).encode()
    root = parse_with_spans(body)
    node = root.members["s"]
    assert json.loads(body[node.start : node.end]) == 'a "quoted" \\ tail'


def test_non_ascii_spans_are_measured_in_bytes():
    body = json.dumps({"s": "café"}, ensure_ascii=False).encode("utf-8")
    node = parse_with_spans(body).members["s"]
    assert node.nbytes == len(b'"caf\xc3\xa9"')


def test_array_items_keep_their_own_spans():
    body = b'[{"i": 0}, {"i": 1}]'
    items = parse_with_spans(body).items
    assert [body[item.start : item.end] for item in items] == [b'{"i": 0}', b'{"i": 1}']


def test_trailing_bytes_are_rejected():
    with pytest.raises(JsonSpanError):
        parse_with_spans(b'{"a": 1} trailing')
