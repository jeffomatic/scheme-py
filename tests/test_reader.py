# ruff: noqa: F401

import pytest

from lexer import Lexer
from reader import Reader
from values import EMPTY_LIST, FALSE, TRUE, NumberValue, PairValue, SymbolValue, Value


@pytest.mark.parametrize(
    "src, want",
    [
        ("", []),
        ("()", [EMPTY_LIST]),
        (
            "(())",
            [PairValue(EMPTY_LIST, EMPTY_LIST)],
        ),
        ("(1234.5678)", [PairValue(NumberValue(1234.5678), EMPTY_LIST)]),
        ("(foo)", [PairValue(SymbolValue("foo"), EMPTY_LIST)]),
        ("#t", [TRUE]),
        ("#true", [TRUE]),
        ("#f", [FALSE]),
        ("#false", [FALSE]),
        (
            "((foo))",
            [PairValue(PairValue(SymbolValue("foo"), EMPTY_LIST), EMPTY_LIST)],
        ),
        (
            "((foo bar) baz)",
            [
                PairValue(
                    PairValue(
                        SymbolValue("foo"),
                        PairValue(SymbolValue("bar"), EMPTY_LIST),
                    ),
                    PairValue(SymbolValue("baz"), EMPTY_LIST),
                )
            ],
        ),
        (
            "((foo bar) (baz (quux)))",
            [
                PairValue(
                    PairValue(
                        SymbolValue("foo"),
                        PairValue(SymbolValue("bar"), EMPTY_LIST),
                    ),
                    PairValue(
                        PairValue(
                            SymbolValue("baz"),
                            PairValue(
                                PairValue(SymbolValue("quux"), EMPTY_LIST),
                                EMPTY_LIST,
                            ),
                        ),
                        EMPTY_LIST,
                    ),
                )
            ],
        ),
    ],
)
def test_reader(src: str, want: list[Value]):
    got = Reader(Lexer(src).lex()).read()
    assert got == want
