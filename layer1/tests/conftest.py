import pytest

from hb_layer1.tokenizer import Tokenizer


class WordTokenizer:
    """A named fake standing in for tiktoken: one token per whitespace-run.

    The instrument's tests must not depend on a BPE file being fetched, and the
    properties under test (additivity, determinism, ordering) hold for any
    tokenizer.
    """

    def encode(self, text: str, disallowed_special=()) -> list[str]:
        return text.split()


@pytest.fixture
def tokenizer() -> Tokenizer:
    return Tokenizer(name="fake-words", _encoding=WordTokenizer())
