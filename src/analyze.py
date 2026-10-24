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


@dataclass
class DefineExpr:
    name: str
    body: Expr


@dataclass
class LambdaExpr:
    params: list[str]
    body: list[Expr]


Expr = ConstExpr | VarRefExpr | CallExpr | AndExpr | OrExpr | DefineExpr | LambdaExpr


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
            return AndExpr([analyze(item) for item in flatten_list(pair.cdr)])
        case SymbolValue("or"):
            return OrExpr([analyze(item) for item in flatten_list(pair.cdr)])
        case SymbolValue("define"):
            match flatten_list(pair.cdr):
                case SymbolValue(name), body_val:
                    return DefineExpr(name, analyze(body_val))
                case _:
                    raise InvalidAnalyzeValueError()
        case SymbolValue("lambda"):
            match flatten_list(pair.cdr):
                case PairValue() as params_val, *body_vals:
                    params: list[str] = []
                    for pv in flatten_list(params_val):
                        match pv:
                            case SymbolValue(text):
                                params.append(text)
                            case _:
                                raise InvalidAnalyzeValueError()

                    return LambdaExpr(params, [analyze(v) for v in body_vals])
                case _:
                    raise InvalidAnalyzeValueError()
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


def flatten_list(list_val: Value) -> list[Value]:
    if not isinstance(list_val, PairValue):
        raise InvalidAnalyzeValueError()

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
                raise InvalidAnalyzeValueError()

    return items


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
