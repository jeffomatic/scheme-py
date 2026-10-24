# ruff: noqa: F401

import pytest

from lexer import (
    CloseParenToken,
    IdentifierToken,
    Lexer,
    NumberToken,
    OpenParenToken,
    QuoteStringToken,
    Token,
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
        ('""', [QuoteStringToken("")]),
    ],
)
def test_lexer(src: str, want: list[Token]):
    got = Lexer(src).lex()
    assert got == want
