from typing import assert_never

from analyze import CallExpr, ConstExpr, Expr, VarRefExpr
from env import Env
from primitives import eval_primitive
from values import (
    PrimitiveProcedureValue,
    Value,
)


class UnknownValueTypeError(Exception):
    pass


class InvalidOperatorError(Exception):
    pass


class MalformedProcedureCallError(Exception):
    pass


def evaluate(env: Env, expr: Expr) -> Value:
    match expr:
        case ConstExpr(val):
            return val
        case VarRefExpr(name):
            return env.resolve(name)
        case CallExpr(items):
            vals = [evaluate(env, i) for i in items]
            func = vals[0]
            args = vals[1:]
            match func:
                case PrimitiveProcedureValue(primitive):
                    return eval_primitive(primitive, args)
                case _:
                    raise InvalidOperatorError()
        case _:
            assert_never(expr)
