import pytest

from lex import (
    CloseParenToken,
    IdentifierToken,
    OpenParenToken,
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
    ],
)
def test_lex(src: str, want: list[Token]):
    got = lex(src)
    assert got == want
