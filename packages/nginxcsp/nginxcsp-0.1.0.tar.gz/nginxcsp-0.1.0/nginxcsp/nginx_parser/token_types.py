from enum import Enum


class TokenCategory(Enum):
    NUMBER = "NUMBER"
    PUNCTUATION = "PUNCTUATION"
    STRING = "STRING",
    WORD = "WORD"
    EXPRESSION = "EXPRESSION"


class Expression(Enum):
    LEFTPARENTHESES = "("
    RIGHTPARENTHESES = ")"


class Punctuation(Enum):
    LEFTBRACE = "{"
    RIGHTBRACE = "}"
    SEMICOLON = ";"
    HASHTAG = "#"
    NEWLINE = "\n"
    TAB = "\t"
    WHITESPACE = " "

    CHARACTERS = [LEFTBRACE, RIGHTBRACE, SEMICOLON,
                  HASHTAG, NEWLINE, TAB, WHITESPACE]

    @classmethod
    def is_punctuation(cls, character):
        punctuation_characters = cls.CHARACTERS.value
        for punctuation in punctuation_characters:
            if character is punctuation:
                return True
        return False

    @classmethod
    def map_character_to_punctuation(cls, character):
        MAP = {"{": cls.LEFTBRACE, "}": cls.RIGHTBRACE,
               ";": cls.SEMICOLON, "#": cls.HASHTAG, "\n": cls.NEWLINE,
               "\t": cls.TAB, " ": cls.WHITESPACE}
        return MAP[character]


class String(Enum):
    APOSTROPHE = "'"
    QUOTATIONMARK = "\""

    @classmethod
    def is_string_character(cls, character):
        return character is cls.APOSTROPHE.value \
            or character is cls.QUOTATIONMARK.value

    @classmethod
    def make_string(cls, string):
        return '"{0}"'.format(string)


def is_punctuation(character):
    return Punctuation.is_punctuation(character)


def map_character_to_punctuation(character):
    return Punctuation.map_character_to_punctuation(character)


def is_string_character(character):
    return String.is_string_character(character)


def is_expression_character(character):
    return character is Expression.LEFTPARENTHESES.value \
        or character is Expression.RIGHTPARENTHESES.value
