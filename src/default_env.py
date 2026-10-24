from env import Env
from values import PrimitiveProcedureValue


def make_default_env() -> Env:
    env = Env()
    for p in ["+", "-", "*", "/"]:
        env.bind(p, PrimitiveProcedureValue(p))
    return env
