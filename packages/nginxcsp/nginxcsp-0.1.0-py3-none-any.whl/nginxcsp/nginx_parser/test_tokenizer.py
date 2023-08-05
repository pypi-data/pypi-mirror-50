from .token_types import Punctuation
from .tokenizer import Tokenizer


class TestTokenizer():
    tokenizer = Tokenizer()

    def test_tokens(self):
        nginx_data = '''
        server {
            listen 80;
            server_name localhost;
            
            if ($http_user_agent = "wget") {
                proxy_pass http://127.0.1.0;
            }
        }
        
        server {
            listen 443;
            server_name localhost;

            location ".well-known/acme-challenge" {
                root /acme-challenge;
            }
        }
        '''
        tokens = self.tokenizer.tokens(source_data=nginx_data)
        assert (len(tokens) > 0) is True
