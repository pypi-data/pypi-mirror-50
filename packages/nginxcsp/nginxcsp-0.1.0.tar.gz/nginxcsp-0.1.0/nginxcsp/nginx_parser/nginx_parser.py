from .tokenizer import Tokenizer
from .token_types import Punctuation
from .exceptions import SyntaxError


class NGINXParser():

    def __init__(self):
        self.tokens = []

    def parse_file(self, file_):
        file_data = file_.read()
        tokenizer = Tokenizer(file_data)
        self.tokens = tokenizer.tokens()
        parse_data = self.parse_tokens(self.tokens)
        return parse_data

    def parse_text(self, text):
        tokenizer = Tokenizer(text)
        self.tokens = tokenizer.tokens()
        parse_data = self.parse_tokens(self.tokens)
        return parse_data

    def parse_tokens(self, tokens):
        index = 0
        parse_data = []
        while index < len(tokens):
            data = []
            token = tokens[index]
            if token.is_punctuation():
                data, index = self.__parse_punctuation(index, tokens)
            elif token.is_word() or token.is_string():
                data, index = self.__parse_word(index, tokens)
            else:
                raise SyntaxError("Check syntax.")
            index += 1
            if len(data) > 0:
                parse_data.append(data)
        return parse_data

    def __parse_punctuation(self, index, tokens):
        token = tokens[index]
        if token.content is Punctuation.HASHTAG:
            comment, end_index = self.__parse_comment(index, tokens)
            return comment, end_index
        else:
            return [], index

    def __parse_word(self, index, tokens):
        if self.__is_block(index, tokens):
            block, end_index = self.__parse_block(index, tokens)
            return block, end_index
        else:
            assignment, end_index = self.__parse_assignment(index, tokens)
            return assignment, end_index

    def __is_block(self, start_index, tokens):
        braces = 0
        for i in range(start_index, len(tokens)):
            token = tokens[i]
            if token.content is Punctuation.NEWLINE \
                    or token.content is Punctuation.SEMICOLON:
                if braces == 0:
                    return False
            elif token.content is Punctuation.LEFTBRACE:
                braces += 1
            elif token.content is Punctuation.RIGHTBRACE:
                if braces == 1:
                    return True
                braces -= 1
        return False

    def __parse_block(self, start_index, tokens):
        block_start_index, block_end_index = self.__get_block_span(start_index,
                                                                   tokens)
        block = []
        block_keyword_and_args = self.__get_block_keyword_and_args(start_index,
                                                                   tokens)
        block_tokens = tokens[block_start_index:block_end_index]
        block_content = self.parse_tokens(block_tokens)
        block.append(block_keyword_and_args)
        block.append(block_content)
        return block, block_end_index

    def __parse_assignment(self, start_index, tokens):
        assignment = []
        assignment_end_index = start_index
        for i in range(start_index, len(tokens)):
            token = tokens[i]
            if token.is_punctuation():
                if token.content is Punctuation.SEMICOLON:
                    assignment_end_index = i
                    break
            else:
                assignment.append(token.content)
        return assignment, assignment_end_index

    def __parse_comment(self, start_index, tokens):
        comment = []
        comment_end_index = start_index
        for i in range(start_index, len(tokens)):
            token = tokens[i]
            if token.is_punctuation():
                if token.content is Punctuation.NEWLINE:
                    comment_end_index = i
                    break
                comment.append(token.content.value)
            else:
                comment.append(token.content)
        return comment, comment_end_index

    def __get_block_span(self, start_index, tokens):
        braces = 0
        block_start_index = start_index
        block_end_index = len(tokens)
        for i in range(start_index, len(tokens)):
            token = tokens[i]
            if token.content is Punctuation.LEFTBRACE:
                if braces == 0:
                    block_start_index = i
                braces += 1
            elif token.content is Punctuation.RIGHTBRACE:
                if braces == 1:
                    block_end_index = i
                    break
                braces -= 1
        return block_start_index, block_end_index

    def __get_block_keyword_and_args(self, start_index, tokens):
        block_keyword_and_args = []
        keyword = tokens[start_index].content
        block_keyword_and_args.append(keyword)
        for i in range(start_index+1, len(tokens)):
            token = tokens[i]
            if not token.is_punctuation():
                block_arg = token.content
                block_keyword_and_args.append(block_arg)
            else:
                if token.content is Punctuation.LEFTBRACE:
                    break
        return block_keyword_and_args
