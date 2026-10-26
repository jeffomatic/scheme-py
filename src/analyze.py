from errors import InvalidDatumError, InvalidSyntaxError
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
from values import BoolValue, EmptyListValue, NumberValue, PairValue, SymbolValue, Value


class InvalidCallExpression(Exception):
    pass


def analyze(expr_val: Value) -> Expr:
    match expr_val:
        case EmptyListValue() | NumberValue() | BoolValue():
            return ConstExpr(expr_val)
        case SymbolValue(text):
            return VarRefExpr(text)
        case PairValue(car, cdr):
            rest = flatten_list(cdr)
            match car:
                case SymbolValue("and"):
                    return AndExpr([analyze(v) for v in rest])
                case SymbolValue("or"):
                    return OrExpr([analyze(v) for v in rest])
                case SymbolValue("define"):
                    return analyze_define(rest)
                case SymbolValue("lambda"):
                    return analyze_lambda(rest)
                case SymbolValue("if"):
                    return analyze_if(rest)
                case SymbolValue("let"):
                    return analyze_let(rest)
                case _:
                    return CallExpr(analyze(car), [analyze(v) for v in rest])
        case _:
            raise InvalidDatumError()


def analyze_define(datums: list[Value]) -> DefineExpr:
    match datums:
        case SymbolValue(name), body_val:
            return DefineExpr(name, analyze(body_val))
        case _:
            raise InvalidSyntaxError("invalid define syntax")


def analyze_lambda(datums: list[Value]) -> LambdaExpr:
    match datums:
        case params_val, *body_vals:
            params: list[str] = [must_symbol(v) for v in flatten_list(params_val)]
            body = parse_body(body_vals)
            return LambdaExpr(params, body)
        case _:
            raise InvalidSyntaxError("invalid lambda syntax")


def analyze_if(datums: list[Value]) -> IfExpr:
    match datums:
        case [pred_val, then_val, else_val]:
            return IfExpr(analyze(pred_val), analyze(then_val), analyze(else_val))
        case [pred_val, then_val]:
            return IfExpr(analyze(pred_val), analyze(then_val), None)
        case _:
            raise InvalidSyntaxError("invalid if syntax")


def analyze_let(datums: list[Value]) -> CallExpr:
    match datums:
        case [decls_val, *body_vals]:
            bindings = [parse_let_binding(d) for d in flatten_list(decls_val)]
            decl_names = [name for name, _ in bindings]
            decl_bodies = [expr for _, expr in bindings]
            body = parse_body(body_vals)
            return CallExpr(LambdaExpr(decl_names, body), decl_bodies)
        case _:
            raise InvalidSyntaxError("invalid let syntax")


def parse_let_binding(datum: Value) -> tuple[str, Expr]:
    match flatten_list(datum):
        case [SymbolValue(name), body_val]:
            return (name, analyze(body_val))
        case _:
            raise InvalidSyntaxError("invalid let syntax")


def parse_body(datums: list[Value]) -> list[Expr]:
    body = [analyze(v) for v in datums]
    if not body:
        raise InvalidSyntaxError("empty body")
    return body


def must_symbol(v: Value) -> str:
    match v:
        case SymbolValue(s):
            return s
        case _:
            raise InvalidSyntaxError("expected symbol")


def flatten_list(datum: Value) -> list[Value]:
    """
    Assuming datum represents a properly-structured Scheme list, flatten the
    linked list structure into a Python list of value objects.
    """
    ret: list[Value] = []
    cur = datum
    while True:
        match cur:
            case EmptyListValue():
                return ret
            case PairValue(car, cdr):
                ret.append(car)
                cur = cdr
            case _:
                raise InvalidDatumError("malformed list")
