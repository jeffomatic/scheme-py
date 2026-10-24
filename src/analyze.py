from dataclasses import dataclass

from values import BoolValue, EmptyListValue, NumberValue, PairValue, SymbolValue, Value


@dataclass
class ConstExpr:
    val: Value


@dataclass
class VarRefExpr:
    name: str


@dataclass
class CallExpr:
    items: list[Expr]


@dataclass
class AndExpr:
    operands: list[Expr]


@dataclass
class OrExpr:
    operands: list[Expr]


Expr = ConstExpr | VarRefExpr | CallExpr | AndExpr | OrExpr


class InvalidAnalyzeValueError(Exception):
    pass


class InvalidCallExpression(Exception):
    pass


def analyze(expr_val: Value) -> Expr:
    match expr_val:
        case EmptyListValue() | NumberValue() | BoolValue():
            return ConstExpr(expr_val)
        case SymbolValue(text):
            return VarRefExpr(text)
        case PairValue():
            return analyze_pair(expr_val)
        case _:
            raise InvalidAnalyzeValueError()


def analyze_pair(pair: PairValue) -> Expr:
    match pair.car:
        case SymbolValue("and"):
            return AndExpr(analyze_list(pair.cdr))
        case SymbolValue("or"):
            return OrExpr(analyze_list(pair.cdr))
        case (
            SymbolValue("lambda")
            | SymbolValue("define")
            | SymbolValue("if")
            | SymbolValue("let")
            | SymbolValue("set!")
            | SymbolValue("quote")
            | SymbolValue("cond")
            | SymbolValue("begin")
        ):
            # unimplemented special forms
            raise NotImplementedError()
        case _:
            return CallExpr(analyze_list(pair))


def analyze_list(list_val: Value) -> list[Expr]:
    """
    Assuming list_val represents a properly-structured Scheme list, performs
    separate analysis of each item in the list and returns a host-language list
    of the resulting expressions.
    """
    if not isinstance(list_val, PairValue):
        raise InvalidAnalyzeValueError()

    match list_val.cdr:
        case EmptyListValue():
            return [analyze(list_val.car)]
        case PairValue():
            return [analyze(list_val.car)] + analyze_list(list_val.cdr)
        case _:
            raise InvalidAnalyzeValueError()
