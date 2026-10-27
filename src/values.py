from dataclasses import dataclass
from enum import Enum
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


class BoolValue(Enum):
    TRUE = True
    FALSE = False


TRUE = BoolValue.TRUE
FALSE = BoolValue.FALSE


class EmptyListValue(Enum):
    EMPTY_LIST = "()"


EMPTY_LIST = EmptyListValue.EMPTY_LIST


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
class UnspecifiedValue(Enum):
    UNSPECIFIED = "<unspecified>"


UNSPECIFIED = UnspecifiedValue.UNSPECIFIED

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
    return val != FALSE
