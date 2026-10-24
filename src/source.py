from default_env import make_default_env
from evaluate import evaluate
from lexer import Lexer
from reader import Reader
from values import EmptyListValue, Value


def read_source(src: str) -> list[Value]:
    return Reader(Lexer(src).lex()).read()


def evaluate_source(src: str) -> Value:
    top_level = read_source(src)
    env = make_default_env()

    res = EmptyListValue()
    for v in top_level:
        res = evaluate(env, v)

    return res
