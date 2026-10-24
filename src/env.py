from dataclasses import dataclass

from values import Value


class UnknownBindingError(Exception):
    pass


@dataclass
class Env:
    values: dict[str, Value]
    parent: Env | None

    def __init__(self, parent: Env | None = None):
        self.values = {}
        self.parent = parent

    def bind(self, k: str, v: Value):
        self.values[k] = v

    def resolve(self, k: str) -> Value:
        if not k in self.values:
            if self.parent is None:
                raise UnknownBindingError()

            return self.parent.resolve(k)

        return self.values[k]
