"""The tokenizer the mock counts with.

Layer 1 reports a token count, not only a byte count, so a difference between
arms can be read in the unit the gateway bills in. The gateway's own tokenizer
is not published for `mimo-v2.5-free` or `hy3-free`, so this is an explicitly
disclosed *proxy* tokenizer: the encoding name travels in every record, and
Layer 1 token counts are only ever compared between arms, never against a
`prompt_tokens` value returned by the real gateway (which #34 showed carries a
gateway-injected offset anyway).
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_ENCODING = "cl100k_base"


class TokenizerUnavailable(RuntimeError):
    """The proxy tokenizer could not be loaded, so no token count is honest."""


@dataclass(frozen=True)
class Tokenizer:
    name: str
    _encoding: object

    def count(self, raw: bytes | str) -> int:
        text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw
        return len(self._encoding.encode(text, disallowed_special=()))  # type: ignore[attr-defined]


def load_tokenizer(name: str = DEFAULT_ENCODING) -> Tokenizer:
    """Load the proxy tokenizer, or fail loudly.

    Failing loudly is the point: a silently degraded token count would be a
    fabricated measurement, which is the one thing this instrument must not
    produce.

        >>> load_tokenizer().count("hello world")
        2
    """
    try:
        import tiktoken
    except ImportError as exc:  # pragma: no cover - environment failure
        raise TokenizerUnavailable(
            "tiktoken is not installed; install the layer1 dependencies"
        ) from exc
    try:
        encoding = tiktoken.get_encoding(name)
    except Exception as exc:  # pragma: no cover - environment failure
        raise TokenizerUnavailable(
            f"could not load encoding {name!r}; the BPE file is fetched once and "
            "then cached, so the first run needs network access"
        ) from exc
    return Tokenizer(name=name, _encoding=encoding)
