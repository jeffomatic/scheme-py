from procedures import ArityError, TypeError
from values import NumberValue, Value


class UnknownPrimitiveError(Exception):
    pass


def eval_primitive(id: str, args: list[Value]) -> Value:
    match id:
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
            raise TypeError()


def eval_add(args: list[Value]) -> Value:
    accum = 0
    for v in args:
        accum += unwrap_number(v)

    return NumberValue(accum)


def eval_sub(args: list[Value]) -> Value:
    if len(args) < 1:
        raise ArityError()

    if len(args) == 1:
        # special case: negation
        return NumberValue(-1 * unwrap_number(args[0]))

    accum = unwrap_number(args[0])
    for n in args[1:]:
        accum -= unwrap_number(n)

    return NumberValue(accum)


def eval_mul(args: list[Value]) -> Value:
    accum = 1
    for v in args:
        accum *= unwrap_number(v)

    return NumberValue(accum)


def eval_div(args: list[Value]) -> Value:
    if len(args) < 1:
        raise ArityError()

    if len(args) == 1:
        # special case: reciprocal
        return NumberValue(1 / unwrap_number(args[0]))

    accum = unwrap_number(args[0])
    for n in args[1:]:
        accum /= unwrap_number(n)

    return NumberValue(accum)
