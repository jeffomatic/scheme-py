from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from env import Env


@dataclass
class SymbolValue:
    text: str


@dataclass
class NumberValue:
    val: float


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
class PrimitiveProcedureValue:
    name: str


class ClosureProcedureValue:
    env: Env
    params: list[str]
    body: list[Value]


class ArityError(Exception):
    pass


class ValueTypeError(Exception):
    pass


Value = (
    SymbolValue
    | NumberValue
    | EmptyListValue
    | PairValue
    | PrimitiveProcedureValue
    | ClosureProcedureValue
)
