from env import Env
from primitives import eval_primitive
from procedures import ArityError, ClosureProcedureValue, PrimitiveProcedureValue
from values import EmptyListValue, NumberValue, PairValue, SymbolValue, Value


class UnknownValueTypeError(Exception):
    pass


class InvalidOperatorError(Exception):
    pass


class MalformedProcedureCallError(Exception):
    pass


def evaluate(env: Env, expr: Value) -> Value:
    match expr:
        case EmptyListValue() | NumberValue():
            return expr
        case SymbolValue(text):
            return env.resolve(text)
        case PairValue(SymbolValue("lambda"), _):
            raise NotImplementedError()
        case PairValue(SymbolValue("define"), _):
            raise NotImplementedError()
        case PairValue(SymbolValue(name), cdr):
            return eval_procedure(env, name, cdr)
        case PairValue():
            raise InvalidOperatorError()
        case _:
            raise UnknownValueTypeError()


def eval_procedure(env: Env, name: str, arg_list: Value) -> Value:
    proc = env.resolve(name)
    args = eval_arg_list(env, arg_list)
    match proc:
        case PrimitiveProcedureValue(primitive):
            return eval_primitive(primitive, args)
        case ClosureProcedureValue():
            return eval_closure(proc, args)
        case _:
            raise UnknownValueTypeError()


def eval_arg_list(env: Env, arg_list: Value) -> list[Value]:
    args: list[Value] = []
    while True:
        match arg_list:
            case EmptyListValue():
                break
            case PairValue(car, cdr):
                args.append(evaluate(env, car))
                arg_list = cdr
            case _:
                raise MalformedProcedureCallError()

    return args


def eval_closure(closure: ClosureProcedureValue, args: list[Value]) -> Value:
    if len(closure.params) != len(args):
        raise ArityError()

    eval_env = Env(closure.env)
    for k, v in zip(closure.params, args, strict=True):
        eval_env.bind(k, v)

    ret = EmptyListValue()
    for v in closure.body:
        ret = evaluate(eval_env, v)

    return ret
