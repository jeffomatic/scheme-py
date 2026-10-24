from env import Env
from primitives import PRIMITIVES
from values import PrimitiveProcedureValue


def make_default_env() -> Env:
    env = Env()
    for name in PRIMITIVES:
        env.bind(name, PrimitiveProcedureValue(name))
    return env
