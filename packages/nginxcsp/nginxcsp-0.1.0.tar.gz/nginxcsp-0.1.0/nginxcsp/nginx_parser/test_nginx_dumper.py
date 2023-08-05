import pytest
from .nginx_dumper import NGINXDumper
from io import StringIO
from .exceptions import SyntaxError


class TestNGINXDumper():

    parse_data = [
        [
            ['server'],
            [
                ['listen', '80'],
                [
                    ['location', '".well-known/acme-challenge"'],
                    [
                        ['#', ' ', 'Letsencrypt'],
                        ['root', '/acme-challenge']
                    ]
                ],
                [
                    ['if', '($http_user_agent = "wget")'],
                    [
                        ['proxy_pass', 'http://127.0.1.0']
                    ]
                ]
            ]
        ]
    ]

    parse_data_fail = None

    def test_dump(self):
        output_file = StringIO()
        dumper = NGINXDumper()
        dumper.dump(output_file, self.parse_data)

    def test_dump_fail(self):
        output_file = StringIO()
        dumper = NGINXDumper()
        with pytest.raises(SyntaxError):
            dumper.dump(output_file, self.parse_data_fail)
