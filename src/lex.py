from dataclasses import dataclass


class Token:
    pass


@dataclass
class IdentifierToken(Token):
    text: str


@dataclass
class OpenParenToken(Token):
    pass


@dataclass
class CloseParenToken(Token):
    pass


@dataclass
class QuoteStringToken(Token):
    text: str


@dataclass
class NumberToken(Token):
    value: float


@dataclass
class BooleanToken(Token):
    value: bool


class LexError(Exception):
    pass


def _is_ident_char(s: str) -> bool:
    return s.isalnum() or s == "_"


def _is_ident_prefix(s: str) -> bool:
    return s.isalpha() or s == "_"


class _Src:
    src: str
    cur: int

    def __init__(self, src: str):
        self.src = src
        self.cur = 0

    def lex(self) -> list[Token]:
        toks = []

        while not self.done():
            if self.peek().isspace():
                self.next()
                continue

            if self.consume_char("("):
                toks.append(OpenParenToken())
                continue

            if self.consume_char(")"):
                toks.append(CloseParenToken())
                continue

            ident = self.consume_ident()
            if ident:
                toks.append(ident)
                continue

            num = self.consume_number()
            if num:
                toks.append(num)
                continue

            raise LexError()

        return toks

    def peek(self) -> str:
        assert not self.done()
        return self.src[self.cur]

    def next(self):
        if self.done():
            return
        self.cur += 1

    def prev(self):
        if self.cur < 1:
            return
        self.cur -= 1

    def done(self):
        return self.cur >= len(self.src)

    def consume_char(self, char: str) -> bool:
        if char == self.peek():
            self.next()
            return True
        return False

    def consume_ident(self) -> IdentifierToken | None:
        if not _is_ident_prefix(self.peek()):
            return None

        text = ""

        while not self.done():
            c = self.peek()
            if c.isspace() or c == ")":
                break

            if not _is_ident_char(c):
                raise LexError(Exception)

            text += c
            self.next()

        if len(text) < 1:
            raise LexError()

        return IdentifierToken(text)

    def consume_number(self) -> NumberToken | None:
        if self.consume_char("-"):
            num = self.consume_positive_number()
            if num == None:
                self.prev()  # unconsume '-' character
                return None
            return NumberToken(-num.value)

        return self.consume_positive_number()

    def consume_positive_number(self) -> NumberToken | None:
        text = ""

        while not self.done():
            c = self.peek()
            if c == ")" or c.isspace():
                break

            if c.isnumeric():
                text += c
                self.next()
                continue

            if c == ".":
                if len(text) < 1:
                    raise LexError()
                if "." in text:
                    raise LexError()

                text += "."
                self.next()
                continue

            raise LexError()

        if len(text) < 1:
            return None

        return NumberToken(float(text))


def lex(input: str) -> list[Token]:
    return _Src(input).lex()
