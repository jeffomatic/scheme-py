import math
from collections.abc import Callable

from values import (
    FALSE,
    TRUE,
    ArityError,
    NumberValue,
    Value,
    ValueTypeError,
    truthy,
)


class UnknownPrimitiveError(Exception):
    pass


def eval_primitive(name: str, args: list[Value]) -> Value:
    if (f := PRIMITIVES.get(name)) is not None:
        return f(args)
    raise UnknownPrimitiveError()


def unwrap_number(v: Value) -> float:
    match v:
        case NumberValue(n):
            return n
        case _:
            raise ValueTypeError()


def eval_add(args: list[Value]) -> Value:
    return NumberValue(sum(unwrap_number(v) for v in args))


def eval_sub(args: list[Value]) -> Value:
    if len(args) < 1:
        raise ArityError()

    if len(args) == 1:
        # special case: negation
        return NumberValue(-unwrap_number(args[0]))

    accum = unwrap_number(args[0])
    for v in args[1:]:
        accum -= unwrap_number(v)

    return NumberValue(accum)


def eval_mul(args: list[Value]) -> Value:
    return NumberValue(math.prod(unwrap_number(v) for v in args))


def eval_div(args: list[Value]) -> Value:
    if len(args) < 1:
        raise ArityError()

    if len(args) == 1:
        # special case: reciprocal
        return NumberValue(1 / unwrap_number(args[0]))

    accum = unwrap_number(args[0])
    for v in args[1:]:
        accum /= unwrap_number(v)

    return NumberValue(accum)


def eval_gt(args: list[Value]) -> Value:
    match args:
        case [NumberValue(a), NumberValue(b)]:
            return TRUE if a > b else FALSE
        case [a, b]:
            raise ValueTypeError()
        case _:
            raise ArityError()


def eval_gte(args: list[Value]) -> Value:
    match args:
        case [NumberValue(a), NumberValue(b)]:
            return TRUE if a >= b else FALSE
        case [a, b]:
            raise ValueTypeError()
        case _:
            raise ArityError()


def eval_lt(args: list[Value]) -> Value:
    match args:
        case [NumberValue(a), NumberValue(b)]:
            return TRUE if a < b else FALSE
        case [a, b]:
            raise ValueTypeError()
        case _:
            raise ArityError()


def eval_lte(args: list[Value]) -> Value:
    match args:
        case [NumberValue(a), NumberValue(b)]:
            return TRUE if a <= b else FALSE
        case [a, b]:
            raise ValueTypeError()
        case _:
            raise ArityError()


def eval_num_eq(args: list[Value]) -> Value:
    match args:
        case [NumberValue(a), NumberValue(b)]:
            return TRUE if a == b else FALSE
        case [a, b]:
            raise ValueTypeError()
        case _:
            raise ArityError()


def eval_not(args: list[Value]) -> Value:
    match args:
        case [v]:
            return TRUE if not truthy(v) else FALSE
        case _:
            raise ArityError()


PRIMITIVES: dict[str, Callable[[list[Value]], Value]] = {
    "+": eval_add,
    "-": eval_sub,
    "*": eval_mul,
    "/": eval_div,
    ">": eval_gt,
    ">=": eval_gte,
    "<": eval_lt,
    "<=": eval_lte,
    "=": eval_num_eq,
    "not": eval_not,
}
