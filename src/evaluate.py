from dataclasses import dataclass
from typing import assert_never

from env import Env
from exprs import (
    AndExpr,
    CallExpr,
    ConstExpr,
    DefineExpr,
    Expr,
    IfExpr,
    LambdaExpr,
    OrExpr,
    VarRefExpr,
)
from primitives import eval_primitive
from values import (
    FALSE,
    TRUE,
    UNSPECIFIED,
    ArityError,
    ClosureProcValue,
    PrimitiveProcValue,
    Value,
    truthy,
)


class InvalidOperatorError(Exception):
    pass


class MalformedProcedureCallError(Exception):
    pass


@dataclass
class TailCall:
    env: Env
    expr: Expr


def evaluate(env: Env, expr: Expr) -> Value:
    while True:
        match expr:
            case ConstExpr(val):
                return val
            case VarRefExpr(name):
                return env.resolve(name)
            case CallExpr(func, args):
                arg_vals = [evaluate(env, arg_expr) for arg_expr in args]
                match apply(evaluate(env, func), arg_vals):
                    case TailCall() as tc:
                        env = tc.env
                        expr = tc.expr
                    case _ as v:
                        return v
            case IfExpr(pred, then_body, else_body):
                if truthy(evaluate(env, pred)):
                    expr = then_body
                elif else_body:
                    expr = else_body
                else:
                    return UNSPECIFIED
            case AndExpr([]):
                return TRUE
            case AndExpr(operands):
                *leading, last = operands
                for o in leading:
                    if not truthy(v := evaluate(env, o)):
                        return v
                expr = last
            case OrExpr([]):
                return FALSE
            case OrExpr(operands):
                *leading, last = operands
                for o in leading:
                    if truthy(v := evaluate(env, o)):
                        return v
                expr = last
            case DefineExpr(name, body):
                env.bind(name, evaluate(env, body))
                return UNSPECIFIED
            case LambdaExpr(params, body):
                return ClosureProcValue(env, params, body)
            case _:
                assert_never(expr)


def apply(func: Value, args: list[Value]) -> Value | TailCall:
    match func:
        case PrimitiveProcValue(primitive):
            return eval_primitive(primitive, args)
        case ClosureProcValue() as closure:
            return eval_closure(closure, args)
        case _:
            raise InvalidOperatorError()


def eval_closure(closure: ClosureProcValue, args: list[Value]) -> Value | TailCall:
    if len(closure.params) != len(args):
        raise ArityError()

    env = Env(closure.env)
    for name, argval in zip(closure.params, args):
        env.bind(name, argval)

    *leading, last = closure.body
    for expr in leading:
        evaluate(env, expr)

    return TailCall(env, last)
