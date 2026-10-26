from dataclasses import dataclass

from values import Value


@dataclass
class ConstExpr:
    val: Value


@dataclass
class VarRefExpr:
    name: str


@dataclass
class CallExpr:
    func: Expr
    args: list[Expr]


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


@dataclass
class IfExpr:
    pred: Expr
    then_body: Expr
    else_body: Expr


@dataclass
class LetExpr:
    decls: list[tuple[str, Expr]]
    body: list[Expr]


Expr = (
    ConstExpr
    | VarRefExpr
    | CallExpr
    | AndExpr
    | OrExpr
    | DefineExpr
    | LambdaExpr
    | IfExpr
    | LetExpr
)
