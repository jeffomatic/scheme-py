from typing import assert_never

from analyze import (
    AndExpr,
    CallExpr,
    ConstExpr,
    DefineExpr,
    Expr,
    IfExpr,
    LambdaExpr,
    LetExpr,
    OrExpr,
    VarRefExpr,
)
from env import Env
from primitives import eval_primitive
from values import (
    ArityError,
    BoolValue,
    ClosureProcValue,
    PrimitiveProcValue,
    UnspecifiedValue,
    Value,
    truthy,
)


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
        case DefineExpr(name, body):
            env.bind(name, evaluate(env, body))
            return UnspecifiedValue()
        case LambdaExpr(params, body):
            return ClosureProcValue(env, params, body)
        case CallExpr(items):
            vals = [evaluate(env, i) for i in items]
            func = vals[0]
            args = vals[1:]
            match func:
                case PrimitiveProcValue(primitive):
                    return eval_primitive(primitive, args)
                case ClosureProcValue() as closure:
                    return eval_closure(closure, args)
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
        case IfExpr(pred, then_body, else_body):
            if truthy(evaluate(env, pred)):
                return evaluate(env, then_body)

            return evaluate(env, else_body)
        case LetExpr(decls, body):
            inner_env = Env(env)
            for name, decl_expr in decls:
                inner_env.bind(name, evaluate(env, decl_expr))
            ret = UnspecifiedValue()
            for body_expr in body:
                ret = evaluate(inner_env, body_expr)
            return ret
        case _:
            assert_never(expr)


def eval_closure(closure: ClosureProcValue, args: list[Value]) -> Value:
    if len(closure.params) != len(args):
        raise ArityError()

    env = Env(closure.env)
    for name, argval in zip(closure.params, args):
        env.bind(name, argval)

    ret: Value = UnspecifiedValue()
    for expr in closure.body:
        ret = evaluate(env, expr)

    return ret
