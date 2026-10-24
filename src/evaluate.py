from typing import assert_never

from analyze import AndExpr, CallExpr, ConstExpr, Expr, OrExpr, VarRefExpr
from env import Env
from primitives import eval_primitive
from values import BoolValue, PrimitiveProcedureValue, Value, truthy


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
        case AndExpr(operands):
            for o in operands:
                if not truthy(evaluate(env, o)):
                    return BoolValue(False)
            return BoolValue(True)
        case OrExpr(operands):
            for o in operands:
                if truthy(evaluate(env, o)):
                    return BoolValue(True)
            return BoolValue(False)
        case _:
            assert_never(expr)
