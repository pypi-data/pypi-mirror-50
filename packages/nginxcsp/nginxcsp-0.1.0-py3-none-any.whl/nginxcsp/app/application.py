from .generator import HeaderGenerator
from ..nginx_parser import NGINXParser, NGINXDumper


BLOCK_KEYWORD_INDEX = 0, 0
ASSIGNMENTS_INDEX = 1
ASSIGNMENT_KEYWORD_INDEX = 0
HEADER_NAME_INDEX = 1
ASSIGNMENT_VALUE_INDEX = 1
SERVER_KEYWORD = "server"
SERVERNAME_KEYWORD = "server_name"
LISTEN_KEYWORD = "listen"
ADDHEADER_KEYWORD = "add_header"
CSP_POSITION = 0
XCSP_POSITION = 1
XWEBKIT_POSITION = 2
CSP = "Content-Security-Policy"
XCSP = "X-Content-Security-Policy"
XWEBKIT = "X-WebKit-CSP"


class Application():

    def __init__(self, cli):
        self.cli = cli
        self.file_content = []

    def run(self):
        if self.cli.get_out_file():
            self.__add_headers_to_out_file()
        else:
            self.__print_header_only()

    def __add_headers_to_out_file(self):
        self.__clear_headers_if_override()
        self.__add_headers_to_server_blocks()

    def __print_header_only(self):
        header_gen = HeaderGenerator()
        path = self.cli.get_html_path()
        header_content = header_gen.generate_header_content(path)
        header = "{0} \"{1}\"".format(CSP, header_content)
        print(header)

    def __clear_headers_if_override(self):
        if self.cli.get_override():
            self.__clear_headers()

    def __clear_headers(self):
        file_content = self.__get_file_content()
        for data in file_content:
            self.__clear_headers_if_server(data)

    def __clear_headers_if_server(self, data):
        index_to_remove = []
        block_keyword = data[BLOCK_KEYWORD_INDEX[0]][BLOCK_KEYWORD_INDEX[1]]
        if block_keyword == SERVER_KEYWORD:
            assignments = data[ASSIGNMENTS_INDEX]
            for i in range(len(assignments)):
                assignment = assignments[i]
                if assignment[ASSIGNMENT_KEYWORD_INDEX] == ADDHEADER_KEYWORD:
                    if assignment[ASSIGNMENT_VALUE_INDEX] == CSP \
                            or assignment[ASSIGNMENT_VALUE_INDEX] == XCSP \
                            or assignment[ASSIGNMENT_VALUE_INDEX] == XWEBKIT:
                        index_to_remove.append(i)
        index_to_remove.reverse()
        for i in index_to_remove:
            data[1].pop(i)

    def __add_headers_to_server_blocks(self):
        file_content = self.__get_file_content()
        for data in file_content:
            if data[BLOCK_KEYWORD_INDEX[0]][BLOCK_KEYWORD_INDEX[1]] == \
                    SERVER_KEYWORD and self.__has_server_name(data) and \
                    self.__has_port(data):
                self.__add_headers_to_block(data)
        self.__save_file(file_content)

    def __has_server_name(self, data):
        server_name = self.cli.get_server_name()
        if server_name is None:
            return True
        assignments = data[1]
        for assignment in assignments:
            if assignment[ASSIGNMENT_KEYWORD_INDEX] == SERVERNAME_KEYWORD \
                    and server_name in assignment:
                return True
        return False

    def __has_port(self, data):
        port = self.cli.get_port()
        if port is None:
            return True
        assignments = data[1]
        for assignment in assignments:
            if assignment[ASSIGNMENT_KEYWORD_INDEX] == LISTEN_KEYWORD \
                    and port in assignment:
                return True
        return False

    def __add_headers_to_block(self, data):
        block_content = data[ASSIGNMENTS_INDEX]
        if self.__no_header_flag_set():
            self.__add_all_headers(block_content)
        else:
            self.__add_headers_one_by_one(block_content)

    def __add_all_headers(self, block_content):
        headers = self.__get_headers()
        nginx_parser = NGINXParser()
        block_content.insert(CSP_POSITION, nginx_parser.parse_text(
            headers[CSP])[BLOCK_KEYWORD_INDEX[0]])
        block_content.insert(XCSP_POSITION, nginx_parser.parse_text(
            headers[XCSP])[BLOCK_KEYWORD_INDEX[0]])
        block_content.insert(
            XWEBKIT_POSITION, nginx_parser.parse_text(
                headers[XWEBKIT])[BLOCK_KEYWORD_INDEX[0]])

    def __add_headers_one_by_one(self, block_content):
        headers = self.__get_headers()
        nginx_parser = NGINXParser()
        if self.cli.get_csp():
            block_content.insert(CSP_POSITION, nginx_parser.parse_text(
                headers[CSP])
                [BLOCK_KEYWORD_INDEX[0]])
        if self.cli.get_xcsp():
            block_content.insert(XCSP_POSITION, nginx_parser.parse_text(
                headers[XCSP])[BLOCK_KEYWORD_INDEX[0]])
        if self.cli.get_xwebkit():
            block_content.insert(
                XWEBKIT_POSITION, nginx_parser.parse_text(
                    headers[XWEBKIT])[BLOCK_KEYWORD_INDEX[0]])

    def __get_file_content(self):
        if len(self.file_content) == 0:
            nginx_parser = NGINXParser()
            out_file = self.cli.get_out_file()
            self.file_content = nginx_parser.parse_file(open(out_file))
        return self.file_content

    def __get_headers(self):
        header_gen = HeaderGenerator()
        path = self.cli.get_html_path()
        headers = header_gen.generate_headers(path)
        return headers

    def __no_header_flag_set(self):
        csp = self.cli.get_csp()
        xcsp = self.cli.get_xcsp()
        xwebkit = self.cli.get_xwebkit()
        return not csp and not xcsp and not xwebkit

    def __save_file(self, file_content):
        dumper = NGINXDumper()
        out_file = open(self.cli.get_out_file(), "w+")
        dumper.dump(out_file, file_content)
