from values import Value


class UnknownBindingError(Exception):
    pass


class Env:
    parent: Env | None
    values: dict[str, Value]

    def __init__(self, parent: Env | None = None):
        self.parent = parent
        self.values = {}

    def bind(self, k: str, v: Value):
        self.values[k] = v

    def resolve(self, k: str) -> Value:
        if k in self.values:
            return self.values[k]

        if self.parent is None:
            raise UnknownBindingError()

        return self.parent.resolve(k)
