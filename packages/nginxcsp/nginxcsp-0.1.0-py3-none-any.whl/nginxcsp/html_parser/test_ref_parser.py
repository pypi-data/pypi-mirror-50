from .ref_parser import RefParser


class TestRefParser():

    html = '''
    <html>
        <head>
            <script src="https://cloudfare.com/some-script.js"></script>
            <link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet"/> 
        </head>
        <body>
            <img src="https://path.com" />
        </body>
    </html>
    '''

    # Test if `feed` method html.parser.HTMLParser is working as intended.
    def test_feed(self):
        parser = RefParser()
        parser.feed(self.html)
        assert (len(parser.script_src) > 0) is True
        assert (len(parser.img_src) > 0) is True
        assert (len(parser.link_href) > 0) is True
