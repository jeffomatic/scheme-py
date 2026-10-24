# ruff: noqa: F401

import pytest

from source import evaluate_source
from values import EmptyListValue, NumberValue, Value


@pytest.mark.parametrize(
    "src, want",
    [
        ("", EmptyListValue()),
        ("(+)", NumberValue(0)),
        ("(+ 3)", NumberValue(3)),
        ("(+ 3 0.1415)", NumberValue(3.1415)),
        ("(- 0)", NumberValue(0)),
        ("(- 1)", NumberValue(-1)),
        ("(- -1)", NumberValue(1)),
        ("(- 1 3)", NumberValue(-2)),
        ("(- 1 3 5)", NumberValue(-7)),
        ("(*)", NumberValue(1)),
        ("(* 2)", NumberValue(2)),
        ("(* 2 3)", NumberValue(6)),
        ("(* 2 3 5)", NumberValue(30)),
        ("(/ 30)", NumberValue(1 / 30)),
        ("(/ 30 5)", NumberValue(6)),
        ("(/ 30 5 3)", NumberValue(2)),
        ("(+ (/ 4 2) (* 5 (- 2)))", NumberValue(-8)),
    ],
)
def test_eval(src: str, want: Value):
    got = evaluate_source(src)
    assert got == want
