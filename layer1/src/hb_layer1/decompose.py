"""Split one chat-completions request body into the Layer 1 buckets.

The four buckets partition the raw body exactly: system + conversation + tools +
envelope == total. `envelope` is everything the harness spends on structure —
the enclosing object's punctuation, the `model`, `stream`, `temperature` and
`stream_options` fields — and it is reported rather than discarded so the split
can be audited by addition.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .json_spans import Node, parse_with_spans
from .tokenizer import Tokenizer

# `developer` is OpenAI's reasoning-model spelling of the system role. pi sends
# it unless `compat.supportsDeveloperRole` is false (#26), so both count as the
# system prompt or the split would move bytes between buckets per arm config.
SYSTEM_ROLES = frozenset({"system", "developer"})


@dataclass(frozen=True)
class RequestShape:
    total_bytes: int
    system_bytes: int
    conversation_bytes: int
    tools_bytes: int
    envelope_bytes: int
    message_count: int
    system_message_count: int
    tool_schema_count: int
    tool_names: tuple[str, ...]
    model: str | None
    stream: bool | None
    stream_options: dict | None
    system_tokens: int
    conversation_tokens: int
    tools_tokens: int
    prompt_tokens: int
    tokenizer: str

    def as_dict(self) -> dict:
        return asdict(self)


def _slice_tokens(body: bytes, nodes: list[Node], tokenizer: Tokenizer) -> int:
    return sum(tokenizer.count(body[node.start : node.end]) for node in nodes)


def decompose(body: bytes, tokenizer: Tokenizer) -> RequestShape:
    """Decompose a raw `POST /v1/chat/completions` body into Layer 1 buckets."""
    root = parse_with_spans(body)
    if not isinstance(root.value, dict):
        raise ValueError("chat-completions body must be a JSON object")

    messages = root.members.get("messages")
    message_nodes = list(messages.items) if messages is not None else []
    system_nodes = [node for node in message_nodes if _is_system(node)]
    conversation_nodes = [node for node in message_nodes if not _is_system(node)]

    tools = root.members.get("tools")
    tool_nodes = list(tools.items) if tools is not None else []
    tool_names = tuple(_tool_name(node.value) for node in tool_nodes)

    system_bytes = sum(node.nbytes for node in system_nodes)
    conversation_bytes = sum(node.nbytes for node in conversation_nodes)
    tools_bytes = tools.nbytes if tools is not None else 0
    total_bytes = len(body)

    system_tokens = _slice_tokens(body, system_nodes, tokenizer)
    conversation_tokens = _slice_tokens(body, conversation_nodes, tokenizer)
    tools_tokens = tokenizer.count(body[tools.start : tools.end]) if tools is not None else 0

    return RequestShape(
        total_bytes=total_bytes,
        system_bytes=system_bytes,
        conversation_bytes=conversation_bytes,
        tools_bytes=tools_bytes,
        envelope_bytes=total_bytes - system_bytes - conversation_bytes - tools_bytes,
        message_count=len(message_nodes),
        system_message_count=len(system_nodes),
        tool_schema_count=len(tool_nodes),
        tool_names=tool_names,
        model=root.value.get("model"),
        stream=root.value.get("stream"),
        stream_options=root.value.get("stream_options"),
        system_tokens=system_tokens,
        conversation_tokens=conversation_tokens,
        tools_tokens=tools_tokens,
        prompt_tokens=system_tokens + conversation_tokens + tools_tokens,
        tokenizer=tokenizer.name,
    )


def _is_system(node: Node) -> bool:
    return isinstance(node.value, dict) and node.value.get("role") in SYSTEM_ROLES


def _tool_name(tool: object) -> str:
    if isinstance(tool, dict):
        function = tool.get("function")
        if isinstance(function, dict) and isinstance(function.get("name"), str):
            return function["name"]
        if isinstance(tool.get("name"), str):
            return tool["name"]
    return "<unnamed>"
