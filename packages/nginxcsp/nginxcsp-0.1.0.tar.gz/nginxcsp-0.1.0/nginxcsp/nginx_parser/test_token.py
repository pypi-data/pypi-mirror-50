from .token_types import Punctuation, TokenCategory
from .token import Token


class TestToken():
    punctuation_token = Token(
        TokenCategory.PUNCTUATION, Punctuation.LEFTBRACE)
    word_token = Token(TokenCategory.WORD, "")
    string_token = Token(TokenCategory.STRING, '""')
    expression_token = Token(TokenCategory.EXPRESSION, "()")
    number_token = Token(TokenCategory.NUMBER, 0)

    def test_str(self):
        assert '{"category": "TokenCategory.WORD", "content": ""}' == \
            self.word_token.__str__()

    def test_repr(self):
        assert {"category": TokenCategory.WORD, "content": ""} == \
            self.word_token.__repr__()

    def test_eq_return_false(self):
        assert self.punctuation_token.__eq__(1) is False

    def test_from_punctuation(self):
        token = Token.from_punctuation(self.punctuation_token.content.value)
        assert token == self.punctuation_token

    def test_from_string(self):
        token = Token.from_string("")
        assert token == self.string_token

    def test_from_number(self):
        token = Token.from_number(self.number_token.content)
        assert token == self.number_token

    def test_from_word(self):
        token = Token.from_word(self.word_token.content)
        assert token == self.word_token

    def test_from_expression(self):
        token = Token.from_expression(self.expression_token.content)
        assert token == self.expression_token

    def test_is_punctuation(self):
        assert self.punctuation_token.is_punctuation() is True

    def test_is_word(self):
        assert self.word_token.is_word() is True

    def test_is_number(self):
        assert self.number_token.is_number() is True

    def test_is_string(self):
        assert self.string_token.is_string() is True

    def test_is_expression(self):
        assert self.expression_token.is_expression() is True
