from env import Env
from primitives import eval_primitive
from procedures import ArityError, ClosureProcedureValue, PrimitiveProcedureValue
from values import EmptyListValue, NumberValue, PairValue, SymbolValue, Value


class UnknownValueTypeError(Exception):
    pass


class InvalidOperatorError(Exception):
    pass


class MalformedProcedureCall(Exception):
    pass


def evaluate(env: Env, v: Value) -> Value:
    match v:
        case EmptyListValue() | NumberValue():
            return v
        case SymbolValue(text):
            return env.resolve(text)
        case PairValue(car, cdr):
            match car:
                case SymbolValue(car):
                    match car:
                        case "lambda":
                            raise NotImplementedError()
                        case "define":
                            raise NotImplementedError()
                        case _:
                            return eval_procedure(car, env, cdr)

                case _:
                    raise InvalidOperatorError()

        case _:
            raise UnknownValueTypeError()


def eval_procedure(name: str, env: Env, arg_list: Value) -> Value:
    proc = env.resolve(name)
    args = eval_arg_list(env, arg_list)
    match proc:
        case PrimitiveProcedureValue(id):
            return eval_primitive(id, args)
        case ClosureProcedureValue():
            return eval_closure(proc, args)
        case _:
            raise UnknownValueTypeError()


def eval_arg_list(env: Env, arg_list: Value) -> list[Value]:
    match arg_list:
        case EmptyListValue():
            return []
        case PairValue(car, cdr):
            return [evaluate(env, car)] + eval_arg_list(env, cdr)
        case _:
            raise MalformedProcedureCall()


def eval_closure(closure: ClosureProcedureValue, args: list[Value]) -> Value:
    if len(closure.params) != len(args):
        raise ArityError()

    eval_env = Env(closure.env)
    for i, name in enumerate(closure.params):
        eval_env.bind(name, args[i])

    ret = EmptyListValue()
    for v in closure.body:
        ret = evaluate(eval_env, v)

    return ret
