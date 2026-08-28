"""Byte-exact spans over a JSON document.

The Layer 1 split (system prompt / tool schemas / conversation) has to add up to
the bytes the harness actually put on the wire. Re-serialising a parsed body
with `json.dumps` changes whitespace, key order and escaping, which silently
moves bytes between buckets — so the decomposition slices the *raw* body, and
that needs the span of every value, not just its Python equivalent.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

_WHITESPACE = b" \t\n\r"
_DIGITS = b"-0123456789"


class JsonSpanError(ValueError):
    """The body is not a JSON document this scanner can span."""


@dataclass(frozen=True)
class Node:
    """A JSON value plus the half-open byte range `[start, end)` it occupies."""

    value: Any
    start: int
    end: int
    members: dict[str, "Node"] = field(default_factory=dict)
    items: tuple["Node", ...] = ()

    @property
    def nbytes(self) -> int:
        return self.end - self.start


class _Scanner:
    def __init__(self, body: bytes) -> None:
        self.body = body
        self.pos = 0

    def parse(self) -> Node:
        self._skip_whitespace()
        node = self._value()
        self._skip_whitespace()
        if self.pos != len(self.body):
            raise JsonSpanError(f"trailing bytes at offset {self.pos}")
        return node

    def _skip_whitespace(self) -> None:
        while self.pos < len(self.body) and self.body[self.pos] in _WHITESPACE:
            self.pos += 1

    def _expect(self, char: int) -> None:
        if self.pos >= len(self.body) or self.body[self.pos] != char:
            raise JsonSpanError(
                f"expected {chr(char)!r} at offset {self.pos}, "
                f"found {self.body[self.pos : self.pos + 1]!r}"
            )
        self.pos += 1

    def _value(self) -> Node:
        if self.pos >= len(self.body):
            raise JsonSpanError("unexpected end of document")
        char = self.body[self.pos]
        if char == ord("{"):
            return self._object()
        if char == ord("["):
            return self._array()
        if char == ord('"'):
            return self._string()
        if char in _DIGITS:
            return self._number()
        return self._literal()

    def _object(self) -> Node:
        start = self.pos
        self._expect(ord("{"))
        members: dict[str, Node] = {}
        value: dict[str, Any] = {}
        self._skip_whitespace()
        if self.pos < len(self.body) and self.body[self.pos] == ord("}"):
            self.pos += 1
            return Node(value, start, self.pos, members)
        while True:
            self._skip_whitespace()
            key_node = self._string()
            self._skip_whitespace()
            self._expect(ord(":"))
            self._skip_whitespace()
            member = self._value()
            members[key_node.value] = member
            value[key_node.value] = member.value
            self._skip_whitespace()
            if self.pos < len(self.body) and self.body[self.pos] == ord(","):
                self.pos += 1
                continue
            self._expect(ord("}"))
            return Node(value, start, self.pos, members)

    def _array(self) -> Node:
        start = self.pos
        self._expect(ord("["))
        items: list[Node] = []
        self._skip_whitespace()
        if self.pos < len(self.body) and self.body[self.pos] == ord("]"):
            self.pos += 1
            return Node([], start, self.pos, items=())
        while True:
            self._skip_whitespace()
            items.append(self._value())
            self._skip_whitespace()
            if self.pos < len(self.body) and self.body[self.pos] == ord(","):
                self.pos += 1
                continue
            self._expect(ord("]"))
            return Node([item.value for item in items], start, self.pos, items=tuple(items))

    def _string(self) -> Node:
        start = self.pos
        self._expect(ord('"'))
        while True:
            if self.pos >= len(self.body):
                raise JsonSpanError(f"unterminated string from offset {start}")
            char = self.body[self.pos]
            if char == ord("\\"):
                self.pos += 2
                continue
            self.pos += 1
            if char == ord('"'):
                break
        raw = self.body[start : self.pos]
        return Node(json.loads(raw), start, self.pos)

    def _number(self) -> Node:
        start = self.pos
        while self.pos < len(self.body) and self.body[self.pos] in b"-+.eE0123456789":
            self.pos += 1
        raw = self.body[start : self.pos]
        return Node(json.loads(raw), start, self.pos)

    def _literal(self) -> Node:
        for word, value in ((b"true", True), (b"false", False), (b"null", None)):
            if self.body.startswith(word, self.pos):
                start = self.pos
                self.pos += len(word)
                return Node(value, start, self.pos)
        raise JsonSpanError(f"unrecognised token at offset {self.pos}")


def parse_with_spans(body: bytes) -> Node:
    """Parse `body` and return its root node with byte spans attached."""
    return _Scanner(body).parse()
