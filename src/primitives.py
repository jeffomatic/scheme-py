import math

from values import ArityError, NumberValue, Value, ValueTypeError


class UnknownPrimitiveError(Exception):
    pass


def eval_primitive(name: str, args: list[Value]) -> Value:
    match name:
        case "+":
            return eval_add(args)
        case "-":
            return eval_sub(args)
        case "*":
            return eval_mul(args)
        case "/":
            return eval_div(args)
        case _:
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
