from lexer import (
    BoolToken,
    CloseParenToken,
    IdentifierToken,
    NumberToken,
    OpenParenToken,
    Token,
)
from values import (
    EMPTY_LIST,
    FALSE,
    TRUE,
    EmptyListValue,
    NumberValue,
    PairValue,
    SymbolValue,
    Value,
)


class ReadError(Exception):
    pass


class Reader:
    toks: list[Token]
    cur: int

    def __init__(self, toks: list[Token]):
        self.toks = toks
        self.cur = 0

    def read(self) -> list[Value]:
        top_level: list[Value] = []
        while self.cur < len(self.toks):
            top_level.append(self.read_single_value())
        return top_level

    def read_single_value(self) -> Value:
        t = self.toks[self.cur]
        self.cur += 1

        match t:
            case OpenParenToken():
                return self.read_list()
            case NumberToken(val):
                return NumberValue(val)
            case IdentifierToken(text):
                return SymbolValue(text)
            case BoolToken(val):
                return TRUE if val else FALSE
            case _:
                raise ReadError()

    def read_list(self) -> PairValue | EmptyListValue:
        """
        Read list, starting after the open paren, all the way to the matching
        closing paren.
        """
        first = self.toks[self.cur]

        if isinstance(first, CloseParenToken):
            self.cur += 1
            return EMPTY_LIST

        car = self.read_single_value()
        cdr = self.read_list()
        return PairValue(car, cdr)
