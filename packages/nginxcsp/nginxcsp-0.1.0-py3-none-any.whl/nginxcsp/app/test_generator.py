import os
from .generator import HeaderGenerator


class TestGenerator():

    def test_generate_headers_multi_files(self):
        dirpath = os.getcwd()
        path = os.path.join(dirpath, "test_files")
        header_generator = HeaderGenerator()
        headers = header_generator.generate_headers(path)
        assert (len(headers) > 0) is True

    def test_generate_headers_one_file(self):
        dirpath = os.getcwd()
        path = os.path.join(dirpath, "test_files/index.html")
        header_generator = HeaderGenerator()
        headers = header_generator.generate_headers(path)
        assert (len(headers) > 0) is True
