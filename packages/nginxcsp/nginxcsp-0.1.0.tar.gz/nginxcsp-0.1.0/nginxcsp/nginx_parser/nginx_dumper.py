from .token_types import Punctuation
from .exceptions import SyntaxError


class NGINXDumper():

    def dump(self, out_file, parse_data):
        config_text = self.dump_data(parse_data)
        out_file.write(config_text)
        out_file.close()

    def dump_data(self, parse_data, indentation_level=0):
        try:
            dump_text = ""
            for data in parse_data:
                if self.__is_block(data):
                    dump_text += self.__dump_block(data, indentation_level)
                elif self.__is_assignment(data):
                    dump_text += self.__dump_assignment(data,
                                                        indentation_level)
                elif self.__is_comment(data):
                    dump_text += self.__dump_comment(data, indentation_level)
            return dump_text
        except Exception:
            raise SyntaxError("Check syntax.")

    def __is_block(self, data):
        return len(data) == 2 and type(data[1]) is list

    def __is_assignment(self, data):
        for element in data:
            if element[0] is Punctuation.HASHTAG.value:
                return False
        return True

    def __is_comment(self, data):
        return data[0] is Punctuation.HASHTAG.value

    def __dump_block(self, data, indentation_level):
        block_keyword_and_args = data[0]
        block_content = data[1]
        buffer = ""
        buffer += Punctuation.TAB.value*indentation_level
        for word in block_keyword_and_args:
            buffer += word
            buffer += Punctuation.WHITESPACE.value
        buffer += Punctuation.LEFTBRACE.value
        buffer += Punctuation.NEWLINE.value
        buffer += self.dump_data(block_content, indentation_level+1)
        buffer += Punctuation.TAB.value*indentation_level
        buffer += Punctuation.RIGHTBRACE.value
        buffer += Punctuation.NEWLINE.value*2
        return buffer

    def __dump_assignment(self, data, indentation_level):
        buffer = ""
        buffer += Punctuation.TAB.value*indentation_level
        for element in data:
            buffer += element
            if data.index(element) != len(data)-1:
                buffer += Punctuation.WHITESPACE.value
        buffer += Punctuation.SEMICOLON.value
        buffer += Punctuation.NEWLINE.value
        return buffer

    def __dump_comment(self, data, indentation_level):
        buffer = ""
        buffer += Punctuation.TAB.value*indentation_level
        for element in data:
            buffer += element
        buffer += Punctuation.NEWLINE.value
        return buffer
