from dataclasses import dataclass


class Value:
    pass


@dataclass
class SymbolValue(Value):
    text: str


@dataclass
class NumberValue(Value):
    val: float


@dataclass
class EmptyListValue(Value):
    pass


# we need to be careful about equivalent of pair values
# - interpreter tests will probably do structural equivalence in some cases
# - other cases will require reference equality
@dataclass
class PairValue(Value):
    car: Value
    cdr: Value
