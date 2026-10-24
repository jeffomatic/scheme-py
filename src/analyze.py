from dataclasses import dataclass

from values import EmptyListValue, NumberValue, PairValue, SymbolValue, Value


@dataclass
class ConstExpr:
    val: Value


@dataclass
class VarRefExpr:
    name: str


@dataclass
class CallExpr:
    items: list[Expr]


Expr = ConstExpr | VarRefExpr | CallExpr


class InvalidAnalyzeValueError(Exception):
    pass


class InvalidCallExpression(Exception):
    pass


def analyze(expr_val: Value) -> Expr:
    match expr_val:
        case EmptyListValue() | NumberValue():
            return ConstExpr(expr_val)
        case SymbolValue(text):
            return VarRefExpr(text)
        case PairValue():
            return analyze_pair(expr_val)
        case _:
            raise InvalidAnalyzeValueError()


def analyze_pair(pair: PairValue) -> Expr:
    match pair.car:
        case (
            SymbolValue("lambda")
            | SymbolValue("define")
            | SymbolValue("if")
            | SymbolValue("let")
            | SymbolValue("set!")
            | SymbolValue("quote")
            | SymbolValue("cond")
            | SymbolValue("and")
            | SymbolValue("or")
            | SymbolValue("begin")
        ):
            # special forms
            raise NotImplementedError()
        case _:
            return CallExpr(analyze_list(pair))


def analyze_list(list_val: PairValue) -> list[Expr]:
    """
    Assuming list_val represents a properly-structured Scheme list, performs
    separate analysis of each item in the list and returns a host-language list
    of the resulting expressions.
    """
    match list_val.cdr:
        case EmptyListValue():
            return [analyze(list_val.car)]
        case PairValue():
            return [analyze(list_val.car)] + analyze_list(list_val.cdr)
        case _:
            raise InvalidAnalyzeValueError()
