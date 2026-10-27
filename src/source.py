from analyze import analyze
from env import Env
from evaluate import evaluate
from lexer import Lexer
from primitives import PRIMITIVES
from reader import Reader
from values import EmptyListValue, PrimitiveProcValue, Value


def make_default_env() -> Env:
    env = Env()
    for name in PRIMITIVES:
        env.bind(name, PrimitiveProcValue(name))

    return env


def read_source(src: str) -> list[Value]:
    return Reader(Lexer(src).lex()).read()


def evaluate_source(src: str, env: Env | None = None) -> Value:
    top_level = read_source(src)
    env = env or make_default_env()

    res = EmptyListValue()
    for v in top_level:
        res = evaluate(env, analyze(v))

    return res
