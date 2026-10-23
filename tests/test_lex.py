# ruff: noqa: F401

import pytest

from lex import (
    CloseParenToken,
    IdentifierToken,
    NumberToken,
    OpenParenToken,
    QuoteStringToken,
    Token,
    lex,
)


@pytest.mark.parametrize(
    "src, want",
    [
        ("", []),
        ("()", [OpenParenToken(), CloseParenToken()]),
        (
            "(())",
            [OpenParenToken(), OpenParenToken(), CloseParenToken(), CloseParenToken()],
        ),
        ("(foo)", [OpenParenToken(), IdentifierToken("foo"), CloseParenToken()]),
        ("(1)", [OpenParenToken(), NumberToken(1), CloseParenToken()]),
        ("(-1)", [OpenParenToken(), NumberToken(-1), CloseParenToken()]),
        ("(3.1415)", [OpenParenToken(), NumberToken(3.1415), CloseParenToken()]),
        ("(-3.1415)", [OpenParenToken(), NumberToken(-3.1415), CloseParenToken()]),
        ('("foo")', [OpenParenToken(), QuoteStringToken("foo"), CloseParenToken()]),
        ('("\\foo")', [OpenParenToken(), QuoteStringToken("foo"), CloseParenToken()]),
        ('("\\"foo")', [OpenParenToken(), QuoteStringToken('"foo'), CloseParenToken()]),
    ],
)
def test_lex(src: str, want: list[Token]):
    got = lex(src)
    assert got == want
