# ruff: noqa: F401

import pytest

from source import evaluate_source
from values import (
    EMPTY_LIST,
    FALSE,
    TRUE,
    UNSPECIFIED,
    BoolValue,
    NumberValue,
    UnspecifiedValue,
    Value,
)


@pytest.mark.parametrize(
    "src, want",
    [
        ("", EMPTY_LIST),
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
        ("(= 1 1)", TRUE),
        ("(= 1 2)", FALSE),
        ("(> 1 0)", TRUE),
        ("(> 1 1)", FALSE),
        ("(> 1 2)", FALSE),
        ("(and)", TRUE),
        ("(and 1)", NumberValue(1)),
        ("(and #f)", FALSE),
        ("(and (> 1 0))", TRUE),
        ("(and (> 1 0) (> 1 -1))", TRUE),
        ("(and (> 1 0) (> 1 2))", FALSE),
        ("(and (> 1 2) (> 1 0))", FALSE),
        ("(or)", FALSE),
        ("(or 1)", NumberValue(1)),
        ("(or #f)", FALSE),
        ("(or (> 1 0))", TRUE),
        ("(or (> 0 1))", FALSE),
        ("(or (> 1 0) (> 1 -1))", TRUE),
        ("(or (> 1 0) (> 1 2))", TRUE),
        ("(or (> 1 2) (> 1 0))", TRUE),
        ("(or (> 1 2) (> 1 3))", FALSE),
        ("(not #f)", TRUE),
        ("(not #t)", FALSE),
        ("(not 1)", FALSE),
        ("(define foo 1) foo", NumberValue(1)),
        ("(define foo 1) (define bar (> foo 0)) bar", TRUE),
        ("(define foo 1) (define bar (> foo 2)) bar", FALSE),
        ("((lambda () 5))", NumberValue(5)),
        ("(if #t 1 2)", NumberValue(1)),
        ("(if #f 1 2)", NumberValue(2)),
        ("(if #t 1)", NumberValue(1)),
        ("(if #f 1)", UNSPECIFIED),
        # builtins
        ("(>= 1 0)", TRUE),
        ("(>= 1 1)", TRUE),
        ("(>= 1 2)", FALSE),
        ("(< 1 0)", FALSE),
        ("(< 1 1)", FALSE),
        ("(< 1 2)", TRUE),
        ("(<= 1 0)", FALSE),
        ("(<= 1 1)", TRUE),
        ("(<= 1 2)", TRUE),
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
        # proper tail calls (don't expand host language stack for tail recursion)
        (
            """
(define loop (lambda (end acc)
    (if (< acc end)
        (loop end (+ acc 1))
        acc)))
(loop 100000 0)
""",
            NumberValue(100000),
        ),
    ],
)
def test_eval(src: str, want: Value):
    got = evaluate_source(src)
    assert got == want
