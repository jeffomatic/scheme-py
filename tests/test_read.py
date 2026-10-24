# ruff: noqa: F401

import pytest

from read import read
from values import EmptyListValue, NumberValue, PairValue, SymbolValue, Value


@pytest.mark.parametrize(
    "src, want",
    [
        ("", []),
        ("()", [EmptyListValue()]),
        (
            "(())",
            [PairValue(EmptyListValue(), EmptyListValue())],
        ),
        ("(1234.5678)", [PairValue(NumberValue(1234.5678), EmptyListValue())]),
        ("(foo)", [PairValue(SymbolValue("foo"), EmptyListValue())]),
        (
            "((foo))",
            [
                PairValue(
                    PairValue(SymbolValue("foo"), EmptyListValue()), EmptyListValue()
                )
            ],
        ),
        (
            "((foo bar) baz)",
            [
                PairValue(
                    PairValue(
                        SymbolValue("foo"),
                        PairValue(SymbolValue("bar"), EmptyListValue()),
                    ),
                    PairValue(SymbolValue("baz"), EmptyListValue()),
                )
            ],
        ),
        (
            "((foo bar) (baz (quux)))",
            [
                PairValue(
                    PairValue(
                        SymbolValue("foo"),
                        PairValue(SymbolValue("bar"), EmptyListValue()),
                    ),
                    PairValue(
                        PairValue(
                            SymbolValue("baz"),
                            PairValue(
                                PairValue(SymbolValue("quux"), EmptyListValue()),
                                EmptyListValue(),
                            ),
                        ),
                        EmptyListValue(),
                    ),
                )
            ],
        ),
    ],
)
def test_read(src: str, want: list[Value]):
    got = read(src)
    assert got == want
