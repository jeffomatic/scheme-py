# We separate this from values.py so there is no circular dependency between
# values.py and env.py.

from dataclasses import dataclass

from env import Env
from values import Value


@dataclass
class ProcedureValue(Value):
    pass


@dataclass
class PrimitiveProcedureValue(ProcedureValue):
    id: str


@dataclass
class ClosureProcedureValue(ProcedureValue):
    env: Env
    params: list[str]
    body: list[Value]


class ArityError(Exception):
    pass


class TypeError(Exception):
    pass
