from .token_types import TokenCategory, String, map_character_to_punctuation


class Token():

    def __init__(self, category, content):
        self.category = category
        self.content = content

    def __str__(self):
        return '{{"category": "{0}", "content": "{1}"}}'.format(self.category,
                                                                self.content)

    def __repr__(self):
        return {"category": self.category, "content": self.content}

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.category == other.category and self.content == other.content

    @classmethod
    def from_punctuation(cls, character):
        return cls(TokenCategory.PUNCTUATION, map_character_to_punctuation(
            character))

    @classmethod
    def from_string(cls, string):
        return cls(TokenCategory.STRING, String.make_string(string))

    @classmethod
    def from_number(cls, number):
        return cls(TokenCategory.NUMBER, number)

    @classmethod
    def from_word(cls, word):
        return cls(TokenCategory.WORD, word)

    @classmethod
    def from_expression(cls, expression):
        return cls(TokenCategory.EXPRESSION, expression)

    def is_punctuation(self):
        return self.category is TokenCategory.PUNCTUATION

    def is_word(self):
        return self.category is TokenCategory.WORD

    def is_number(self):
        return self.category is TokenCategory.NUMBER

    def is_string(self):
        return self.category is TokenCategory.STRING

    def is_expression(self):
        return self.category is TokenCategory.EXPRESSION
