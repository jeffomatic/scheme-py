from default_env import make_default_env
from evaluate import evaluate
from read import read
from values import EmptyListValue, Value


def evaluate_src(src: str) -> Value:
    top_level = read(src)
    env = make_default_env()

    res = EmptyListValue()
    for v in top_level:
        res = evaluate(env, v)

    return res
