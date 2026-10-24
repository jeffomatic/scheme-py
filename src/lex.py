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


class _Lexer:
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

            num = self.consume_number()
            if num:
                toks.append(num)
                continue

            qs = self.consume_quote_string()
            if qs:
                toks.append(qs)
                continue

            ident = self.consume_ident()
            if ident:
                toks.append(ident)
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
        text = ""

        while not self.done():
            c = self.peek()
            if c.isspace() or c == ")":
                break

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
        if not self.peek().isnumeric():
            return None

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

    def consume_quote_string(self) -> QuoteStringToken | None:
        text = ""
        backquote = False

        if not self.consume_char('"'):
            return None

        while not self.done():
            c = self.peek()
            if c == "\n" or c == "\r":
                raise LexError()

            if backquote:
                backquote = False
                text += c
                self.next()
                continue

            if c == "\\":
                backquote = True
                self.next()
                continue

            if c == '"':
                self.next()
                break

            text += c
            self.next()

        if len(text) < 1:
            return None

        return QuoteStringToken(text)


def lex(input: str) -> list[Token]:
    return _Lexer(input).lex()
