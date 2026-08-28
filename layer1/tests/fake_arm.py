"""A named fake harness: the smallest client that exercises the mock's loop.

It exists so the instrument can be tested headlessly, without pi, omp or
OpenCode installed — the real arms are driven by `collect.py`, which is what the
recorded dataset comes from.
"""

from __future__ import annotations

import json
import urllib.request


def run_fake_arm(
    base_url: str,
    *,
    system: str = "you are a fake arm",
    prompt: str = "read PROBE.md",
    tools: list[dict] | None = None,
    stream: bool = False,
    max_steps: int = 10,
) -> list[dict]:
    """Drive the mock until it stops asking for tools; return the sent bodies."""
    tools = tools if tools is not None else [
        {"type": "function", "function": {"name": "read", "parameters": {"required": ["path"]}}}
    ]
    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    sent: list[dict] = []
    for _ in range(max_steps):
        payload = {"model": "MOCK-2.6B", "messages": messages, "tools": tools, "stream": stream}
        sent.append(payload)
        body = json.dumps(payload).encode()
        request = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=body,
            headers={"content-type": "application/json", "authorization": "Bearer layer1"},
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            raw = response.read().decode()
        message = _stream_message(raw) if stream else json.loads(raw)["choices"][0]["message"]
        messages.append(message)
        calls = message.get("tool_calls") or []
        if not calls:
            return sent
        for call in calls:
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": "PROBE.md contents, as read by the fake arm",
                }
            )
    return sent


def _stream_message(raw: str) -> dict:
    message: dict = {"role": "assistant", "content": ""}
    for line in raw.splitlines():
        if not line.startswith("data: ") or line == "data: [DONE]":
            continue
        chunk = json.loads(line[len("data: ") :])
        for choice in chunk.get("choices", []):
            delta = choice.get("delta") or {}
            if delta.get("content"):
                message["content"] += delta["content"]
            if delta.get("tool_calls"):
                message.setdefault("tool_calls", []).extend(
                    {
                        "id": call["id"],
                        "type": "function",
                        "function": call["function"],
                    }
                    for call in delta["tool_calls"]
                )
    return message
