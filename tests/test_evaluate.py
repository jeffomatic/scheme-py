# ruff: noqa: F401

import pytest

from source import evaluate_source
from values import BoolValue, EmptyListValue, NumberValue, UnspecifiedValue, Value


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
        ("(= 1 1)", BoolValue(True)),
        ("(= 1 2)", BoolValue(False)),
        ("(> 1 0)", BoolValue(True)),
        ("(> 1 1)", BoolValue(False)),
        ("(> 1 2)", BoolValue(False)),
        ("(and)", BoolValue(True)),
        ("(and 1)", NumberValue(1)),
        ("(and #f)", BoolValue(False)),
        ("(and (> 1 0))", BoolValue(True)),
        ("(and (> 1 0) (> 1 -1))", BoolValue(True)),
        ("(and (> 1 0) (> 1 2))", BoolValue(False)),
        ("(and (> 1 2) (> 1 0))", BoolValue(False)),
        ("(or)", BoolValue(False)),
        ("(or 1)", NumberValue(1)),
        ("(or #f)", BoolValue(False)),
        ("(or (> 1 0))", BoolValue(True)),
        ("(or (> 0 1))", BoolValue(False)),
        ("(or (> 1 0) (> 1 -1))", BoolValue(True)),
        ("(or (> 1 0) (> 1 2))", BoolValue(True)),
        ("(or (> 1 2) (> 1 0))", BoolValue(True)),
        ("(or (> 1 2) (> 1 3))", BoolValue(False)),
        ("(not #f)", BoolValue(True)),
        ("(not #t)", BoolValue(False)),
        ("(not 1)", BoolValue(False)),
        ("(define foo 1) foo", NumberValue(1)),
        ("(define foo 1) (define bar (> foo 0)) bar", BoolValue(True)),
        ("(define foo 1) (define bar (> foo 2)) bar", BoolValue(False)),
        ("((lambda () 5))", NumberValue(5)),
        ("(if #t 1 2)", NumberValue(1)),
        ("(if #f 1 2)", NumberValue(2)),
        ("(if #t 1)", NumberValue(1)),
        ("(if #f 1)", UnspecifiedValue()),
        # builtins
        ("(>= 1 0)", BoolValue(True)),
        ("(>= 1 1)", BoolValue(True)),
        ("(>= 1 2)", BoolValue(False)),
        ("(< 1 0)", BoolValue(False)),
        ("(< 1 1)", BoolValue(False)),
        ("(< 1 2)", BoolValue(True)),
        ("(<= 1 0)", BoolValue(False)),
        ("(<= 1 1)", BoolValue(True)),
        ("(<= 1 2)", BoolValue(True)),
        # Fibonacci with define
        (
            """
(define fib (lambda (n)
    (if (= n 0)
        0
        (if (= n 1)
            1
            (+ (fib (- n 1))
                (fib (- n 2)))))))
(fib 10)
""",
            NumberValue(55),
        ),
        # Fibonacci with y combinator
        (
            """
(let (
    (y (lambda (f)
        ((lambda (proc)
            (f (lambda (arg) ((proc proc) arg))))
        (lambda (proc)
            (f (lambda (arg) ((proc proc) arg)))))))
    (fib-pre (lambda (f)
        (lambda (n)
            (if (= n 0)
                0
                (if (= n 1)
                    1
                    (+ (f (- n 1)) (f (- n 2)))))))))
    (let ((fib (y fib-pre)))
        (fib 10)))
""",
            NumberValue(55),
        ),
    ],
)
def test_eval(src: str, want: Value):
    got = evaluate_source(src)
    assert got == want
