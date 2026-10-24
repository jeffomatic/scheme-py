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


class Lexer:
    src: str
    cur: int

    def __init__(self, src: str):
        self.src = src
        self.cur = 0

    def lex(self) -> list[Token]:
        toks: list[Token] = []

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

            if (num := self.consume_number()) is not None:
                toks.append(num)
                continue

            if (qs := self.consume_quote_string()) is not None:
                toks.append(qs)
                continue

            if (ident := self.consume_ident()) is not None:
                toks.append(ident)
                continue

            raise LexError()

        return toks

    def peek(self) -> str:
        assert not self.done()
        return self.src[self.cur]

    def next(self) -> None:
        if self.done():
            return
        self.cur += 1

    def prev(self) -> None:
        if self.cur < 1:
            return
        self.cur -= 1

    def done(self) -> bool:
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

        if not text:
            raise LexError()

        return IdentifierToken(text)

    def consume_number(self) -> NumberToken | None:
        if self.consume_char("-"):
            num = self.consume_positive_number()
            if num is None:
                self.prev()  # unconsume '-' character
                return None
            return NumberToken(-num.value)

        return self.consume_positive_number()

    def consume_positive_number(self) -> NumberToken | None:
        if not self.peek() in "0123456789":
            return None

        text = ""

        while not self.done():
            c = self.peek()
            if c == ")" or c.isspace():
                break

            if c in "0123456789":
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

        if not text:
            return None

        return NumberToken(float(text))

    def consume_quote_string(self) -> QuoteStringToken | None:
        text = ""
        escape = False

        if not self.consume_char('"'):
            return None

        while True:
            if self.done():
                # no closing quote
                raise LexError()

            c = self.peek()
            if c in "\n\r":
                raise LexError()

            if escape:
                escape = False
                text += c
                self.next()
                continue

            if c == "\\":
                escape = True
                self.next()
                continue

            if c == '"':
                self.next()
                return QuoteStringToken(text)

            text += c
            self.next()
