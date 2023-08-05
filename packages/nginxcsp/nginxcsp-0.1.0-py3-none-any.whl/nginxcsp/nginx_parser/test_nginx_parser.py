import pytest
from io import StringIO
from .nginx_parser import NGINXParser
from .exceptions import SyntaxError


class TestNGINXParser():

    nginx_data = '''
        server {
            listen 80;
            server_name localhost;
            
            if ($http_user_agent = "wget") {
                proxy_pass http://127.0.1.0;
            }
        }

        # server comment        
        server {
            listen 443;
            server_name localhost;

            location ".well-known/acme-challenge" {
                root /acme-challenge;
            }
        }
        '''

    nginx_data_fail = '''
        server {
            listen \t 80
            server_name localhost;
        1
        '''

    def test_parse_file(self):
        nginx_file = StringIO(self.nginx_data)
        nginx_parser = NGINXParser()
        parse_data = nginx_parser.parse_file(nginx_file)
        assert (len(parse_data) > 0) is True

    def test_parse_file_fail(self):
        nginx_file = StringIO(self.nginx_data_fail)
        nginx_parser = NGINXParser()
        with pytest.raises(SyntaxError):
            nginx_parser.parse_file(nginx_file)

    def test_parse_text(self):
        nginx_parser = NGINXParser()
        parse_data = nginx_parser.parse_text(self.nginx_data)
        assert (len(parse_data) > 0) is True

    def test_parse_text_fail(self):
        nginx_parser = NGINXParser()
        with pytest.raises(SyntaxError):
            nginx_parser.parse_text(self.nginx_data_fail)
