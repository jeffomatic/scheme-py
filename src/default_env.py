from env import Env
from procedures import PrimitiveProcedureValue


def make_default_env() -> Env:
    env = Env()
    for p in ["+", "-", "*", "/"]:
        env.bind(p, PrimitiveProcedureValue(p))
    return env
