"""The recording mock endpoint: an OpenAI-compatible server that never forwards.

This is the Layer 1 instrument itself. It answers `POST /v1/chat/completions`
from a fixed script (`script.py`), decomposes every inbound body
(`decompose.py`), and hands the result to a sink. It spends no gateway quota and
is deterministic, which is why n = 1 is enough (#37).

It is deliberately *not* the measuring proxy of `docs/spec/25-measuring-proxy.md`
— that one forwards upstream and lives on 443 behind Pier's squid sidecar (#38).
This one has no upstream at all.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable

from .decompose import RequestShape, decompose
from .script import DEFAULT_SCRIPT, ScriptError, Step, TextStep, choose_tool, fill_arguments
from .tokenizer import Tokenizer

RequestSink = Callable[[int, int | None, bytes, dict[str, str], RequestShape | None, str | None], None]


@dataclass
class MockConfig:
    tokenizer: Tokenizer
    probe_path: str
    model_id: str = "MOCK-2.6B"
    script: tuple[Step, ...] = DEFAULT_SCRIPT
    sink: RequestSink | None = None
    # What an auxiliary (tool-less) request is answered with; short and fixed so
    # it adds the same constant to every arm that makes one.
    auxiliary_reply: str = "Layer 1 probe"
    errors: list[str] = field(default_factory=list)


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    @property
    def config(self) -> MockConfig:
        return self.server.config  # type: ignore[attr-defined]

    def log_message(self, *args) -> None:  # noqa: D102 - silence stderr access log
        return

    def do_GET(self) -> None:  # noqa: N802
        # OMP probes /v1/models once per session (#27); pi never does (#26).
        if self.path.rstrip("/").endswith("/models"):
            self._send_json(
                200,
                {
                    "object": "list",
                    "data": [
                        {
                            "id": self.config.model_id,
                            "object": "model",
                            "created": 0,
                            "owned_by": "harness-bench-layer1",
                        }
                    ],
                },
            )
            return
        self._send_json(404, {"type": "error", "error": {"message": f"no route {self.path}"}})

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("content-length") or 0)
        body = self.rfile.read(length)
        if not self.path.rstrip("/").endswith("/chat/completions"):
            self._record(body, None, f"unsupported route {self.path}")  # noqa: F841
            self._send_json(
                404, {"type": "error", "error": {"message": f"no route {self.path}"}}
            )
            return

        try:
            shape = decompose(body, self.config.tokenizer)
        except Exception as exc:  # a body we cannot span is a recorded fault, not a crash
            self._record(body, None, f"undecodable body: {exc}")
            self._send_json(400, {"type": "error", "error": {"message": str(exc)}})
            return

        request_index, step_index = self._record(body, shape, None)
        try:
            reply = self._build_reply(step_index, body, shape)
        except ScriptError as exc:
            self.config.errors.append(f"request {request_index}: {exc}")
            self._send_json(400, {"type": "error", "error": {"message": str(exc)}})
            return

        if shape.stream:
            self._send_stream(reply, shape)
        else:
            self._send_json(200, self._completion(reply, shape))

    # --- recording -------------------------------------------------------

    def _record(
        self, body: bytes, shape: RequestShape | None, error: str | None
    ) -> tuple[int, int | None]:
        """Record one request and return `(request_index, step_index)`.

        A request carrying no tool schemas is *auxiliary*, not a step of the
        agent loop: OpenCode opens every session with a title-generation call
        (#4), and counting it as step 0 would compare one arm's titling prompt
        against another arm's system prompt. Auxiliary requests are recorded —
        they are a real cost of that harness design — but they do not advance
        the script and they carry `step_index: null`.
        """
        server = self.server  # type: ignore[assignment]
        is_agent_step = shape is not None and shape.tool_schema_count > 0
        with server.lock:  # type: ignore[attr-defined]
            request_index = server.request_count  # type: ignore[attr-defined]
            server.request_count += 1  # type: ignore[attr-defined]
            step_index: int | None = None
            if is_agent_step:
                step_index = server.step_count  # type: ignore[attr-defined]
                server.step_count += 1  # type: ignore[attr-defined]
        headers = {key.lower(): value for key, value in self.headers.items()}
        if self.config.sink is not None:
            self.config.sink(request_index, step_index, body, headers, shape, error)
        return request_index, step_index

    # --- reply construction ----------------------------------------------

    def _build_reply(self, step_index: int | None, body: bytes, shape: RequestShape) -> dict:
        script = self.config.script
        if step_index is None:
            return {"kind": "text", "text": self.config.auxiliary_reply}
        # A request past the end of the script gets the terminal text reply, so a
        # harness that keeps looping stops instead of running forever; the record
        # already carries the step index, so the overrun stays visible.
        step: Step = script[step_index] if step_index < len(script) else TextStep()
        if isinstance(step, TextStep):
            return {"kind": "text", "text": step.text}
        parsed = json.loads(body)
        name, parameters = choose_tool(parsed.get("tools") or [], step.prefer)
        arguments = fill_arguments(parameters, self.config.probe_path)
        return {
            "kind": "tool",
            "name": name,
            "arguments": json.dumps(arguments, separators=(",", ":")),
        }

    def _usage(self, reply: dict, shape: RequestShape) -> dict:
        payload = reply.get("text") or reply.get("arguments") or ""
        completion_tokens = self.config.tokenizer.count(payload)
        return {
            "prompt_tokens": shape.prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": shape.prompt_tokens + completion_tokens,
        }

    def _message(self, reply: dict) -> dict:
        if reply["kind"] == "text":
            return {"role": "assistant", "content": reply["text"]}
        return {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call_layer1",
                    "type": "function",
                    "function": {"name": reply["name"], "arguments": reply["arguments"]},
                }
            ],
        }

    def _completion(self, reply: dict, shape: RequestShape) -> dict:
        finish = "stop" if reply["kind"] == "text" else "tool_calls"
        return {
            "id": "chatcmpl-layer1",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": self.config.model_id,
            "choices": [{"index": 0, "message": self._message(reply), "finish_reason": finish}],
            "usage": self._usage(reply, shape),
        }

    # --- transport --------------------------------------------------------

    def _send_json(self, status: int, payload: dict) -> None:
        raw = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _send_stream(self, reply: dict, shape: RequestShape) -> None:
        self.send_response(200)
        self.send_header("content-type", "text/event-stream")
        self.send_header("cache-control", "no-cache")
        self.send_header("connection", "close")
        self.end_headers()
        for chunk in self._stream_chunks(reply, shape):
            self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode())
            self.wfile.flush()
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()
        self.close_connection = True

    def _stream_chunks(self, reply: dict, shape: RequestShape):
        base = {
            "id": "chatcmpl-layer1",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": self.config.model_id,
        }
        if reply["kind"] == "text":
            delta = {"role": "assistant", "content": reply["text"]}
            finish = "stop"
        else:
            delta = {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "index": 0,
                        "id": "call_layer1",
                        "type": "function",
                        "function": {"name": reply["name"], "arguments": reply["arguments"]},
                    }
                ],
            }
            finish = "tool_calls"
        yield {**base, "choices": [{"index": 0, "delta": delta, "finish_reason": None}]}
        # #25 measured a missing finish_reason costing 4 retried requests for one
        # turn, so it is always sent, in its own frame, before usage.
        yield {**base, "choices": [{"index": 0, "delta": {}, "finish_reason": finish}]}
        yield {**base, "choices": [], "usage": self._usage(reply, shape)}


class RecordingMock:
    """A mock OpenAI-compatible endpoint on an ephemeral localhost port."""

    def __init__(self, config: MockConfig, host: str = "127.0.0.1", port: int = 0) -> None:
        self.config = config
        self._server = ThreadingHTTPServer((host, port), _Handler)
        self._server.config = config  # type: ignore[attr-defined]
        self._server.request_count = 0  # type: ignore[attr-defined]
        self._server.step_count = 0  # type: ignore[attr-defined]
        self._server.lock = threading.Lock()  # type: ignore[attr-defined]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        host, port = self._server.server_address[:2]
        return f"http://{host}:{port}/v1"

    @property
    def request_count(self) -> int:
        return self._server.request_count  # type: ignore[attr-defined]

    @property
    def step_count(self) -> int:
        """Agent-loop steps, excluding auxiliary tool-less calls."""
        return self._server.step_count  # type: ignore[attr-defined]

    def __enter__(self) -> "RecordingMock":
        self._thread.start()
        return self

    def __exit__(self, *exc) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)
