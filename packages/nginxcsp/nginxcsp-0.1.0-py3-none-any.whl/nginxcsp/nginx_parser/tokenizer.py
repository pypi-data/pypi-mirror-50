from .token import Token
from .token_types import TokenCategory, Expression, is_punctuation, \
    is_string_character, is_expression_character


class Tokenizer():

    def __init__(self, source_data=[]):
        self.source_data = source_data
        self.__tokens = []

    def tokens(self, source_data=[]):
        self.__set_source_data(source_data)
        if len(self.__tokens) == 0:
            self.__create_tokens()
        return self.__tokens

    def __set_source_data(self, source_data):
        if len(source_data) > 0:
            self.source_data = source_data

    def __create_tokens(self):
        index = 0
        while index < len(self.source_data):
            character = self.source_data[index]
            if is_punctuation(character):
                self.__create_punctuation_token(character)
            elif is_string_character(character):
                index = self.__create_string_token(index)
            elif is_expression_character(character):
                index = self.__create_expression_token(index)
            else:
                index = self.__create_default_token(index)
            index += 1

    def __create_punctuation_token(self, character):
        self.__tokens.append(Token.from_punctuation(character))

    def __create_string_token(self, index):
        string_character = self.source_data[index]
        index_after_opening = index + 1
        buffer = ""
        end_index = index_after_opening
        for i in range(index_after_opening, len(self.source_data)):
            character = self.source_data[i]
            if character is string_character:
                end_index = i
                break
            else:
                buffer += character
            end_index = i
        self.__tokens.append(Token.from_string(buffer))
        return end_index

    def __create_expression_token(self, index):
        character = self.source_data[index]
        if character is Expression.LEFTPARENTHESES.value:
            expression_span = self.__get_expression_span(index)
            buffer = ""
            for i in range(expression_span[0], expression_span[1]):
                character = self.source_data[i]
                buffer += character
            self.__tokens.append(Token.from_expression(buffer))
            return expression_span[1]

    def __create_default_token(self, index):
        category = TokenCategory.NUMBER
        buffer = ""
        end_index = index
        for i in range(index, len(self.source_data)):
            end_index = i
            character = self.source_data[i]
            if is_punctuation(character):
                end_index = i-1
                break
            if not character.isdigit():
                category = TokenCategory.WORD
            buffer += character
        if category is TokenCategory.NUMBER:
            self.__create_number_token(buffer)
        else:
            self.__create_word_token(buffer)
        return end_index

    def __get_expression_span(self, index):
        parentheses = 0
        start_index = index
        end_index = index
        for i in range(index, len(self.source_data)):
            end_index = i
            character = self.source_data[i]
            if character is Expression.LEFTPARENTHESES.value:
                parentheses += 1
            elif character is Expression.RIGHTPARENTHESES.value:
                parentheses -= 1
                if parentheses == 0:
                    break
        return start_index, end_index+1

    def __create_number_token(self, buffer):
        self.__tokens.append(Token.from_number(buffer))

    def __create_word_token(self, buffer):
        self.__tokens.append(Token.from_word(buffer))
