from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from analyze import Expr
    from env import Env


@dataclass
class SymbolValue:
    text: str


@dataclass
class NumberValue:
    val: float


@dataclass
class BoolValue:
    val: bool


@dataclass
class EmptyListValue:
    pass


# we need to be careful about equivalent of pair values
# - interpreter tests will probably do structural equivalence in some cases
# - other cases will require reference equality
@dataclass
class PairValue:
    car: Value
    cdr: Value


@dataclass
class PrimitiveProcValue:
    name: str


class ClosureProcValue:
    env: Env
    params: list[str]
    body: list[Expr]

    def __init__(self, env: Env, params: list[str], body: list[Expr]):
        self.env = env
        self.params = params
        self.body = body


# the unusable return value for statements like `define`
@dataclass
class UnspecifiedValue:
    pass


Value = (
    SymbolValue
    | NumberValue
    | EmptyListValue
    | PairValue
    | PrimitiveProcValue
    | ClosureProcValue
    | BoolValue
    | UnspecifiedValue
)


class ArityError(Exception):
    pass


class ValueTypeError(Exception):
    pass


def truthy(val: Value) -> bool:
    match val:
        case BoolValue(False):
            return False
        case _:
            return True
