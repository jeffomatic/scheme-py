from errors import InvalidDatumError
from exprs import (
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
            args = flatten_list(cdr)
            match car:
                case SymbolValue("and"):
                    return AndExpr([analyze(v) for v in args])
                case SymbolValue("or"):
                    return OrExpr([analyze(v) for v in args])
                case SymbolValue("define"):
                    return analyze_define(args)
                case SymbolValue("lambda"):
                    return analyze_lambda(args)
                case SymbolValue("if"):
                    return analyze_if(args)
                case SymbolValue("let"):
                    return analyze_let(args)
                case _:
                    return CallExpr(analyze(car), [analyze(v) for v in args])
        case _:
            raise InvalidDatumError()


def analyze_define(args: list[Value]) -> DefineExpr:
    match args:
        case SymbolValue(name), body_val:
            return DefineExpr(name, analyze(body_val))
        case _:
            raise SyntaxError("invalid define syntax")


def analyze_lambda(args: list[Value]) -> LambdaExpr:
    match args:
        case PairValue() as params_val, *body_vals:
            params: list[str] = []
            for pv in flatten_list(params_val):
                match pv:
                    case SymbolValue(text):
                        params.append(text)
                    case _:
                        raise SyntaxError("invalid lambda syntax")

            return LambdaExpr(params, [analyze(v) for v in body_vals])
        case _:
            raise SyntaxError("invalid lambda syntax")


def analyze_if(args: list[Value]) -> IfExpr:
    match args:
        case [pred_val, then_val, else_val]:
            return IfExpr(analyze(pred_val), analyze(then_val), analyze(else_val))
        case _:
            raise SyntaxError("invalid if syntax")


def analyze_let(args: list[Value]) -> LetExpr:
    match args:
        case [decls_val, *body_vals]:
            decls: list[tuple[str, Expr]] = []
            for decl_val in flatten_list(decls_val):
                match flatten_list(decl_val):
                    case [SymbolValue(name), decl_body_val]:
                        decls.append((name, analyze(decl_body_val)))
                    case _:
                        raise SyntaxError("invalid let syntax")

            body = [analyze(v) for v in body_vals]
            return LetExpr(decls, body)
        case _:
            raise SyntaxError("invalid let syntax")


def flatten_list(list_val: Value) -> list[Value]:
    """
    Assuming list_val represents a properly-structured Scheme list, flatten
    the linked list structure into a Python list of value objects.
    """
    match list_val:
        case EmptyListValue():
            return []
        case PairValue():
            cur = list_val
            items: list[Value] = []

            while True:
                items.append(cur.car)
                match cur.cdr:
                    case PairValue():
                        cur = cur.cdr
                        continue
                    case EmptyListValue():
                        break
                    case _:
                        raise InvalidDatumError()

            return items
        case _:
            raise InvalidDatumError()
