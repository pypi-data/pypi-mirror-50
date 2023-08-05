from urllib.parse import urlparse
from html.parser import HTMLParser


class RefParser(HTMLParser):
    '''
    RefParser searches for import of sources in HTML files for `script`, `link`
    and `img` tags.
    '''

    script_src = []
    link_href = []
    img_src = []

    def handle_starttag(self, tag, attrs):
        if (tag == "script"):
            for prop in attrs:
                if (prop[0] == "src"):
                    url = urlparse(prop[1])
                    if url.netloc != "":
                        src = {"scheme": url.scheme, "netloc": url.netloc}
                        if src not in self.script_src:
                            self.script_src.append(src)

    def handle_startendtag(self, tag, attrs):
        if tag == "link":
            for prop in attrs:
                if prop[0] == "href":
                    url = urlparse(prop[1])
                    if url.netloc != "":
                        href = {"scheme": url.scheme if url.scheme !=
                                "" else "", "netloc": url.netloc}
                        if href not in self.link_href:
                            self.link_href.append(href)
        elif tag == "img":
            for prop in attrs:
                if prop[0] == "src":
                    url = urlparse(prop[1])
                    if url.netloc != "":
                        src = {"scheme": url.scheme, "netloc": url.netloc}
                        if src not in self.img_src:
                            self.img_src.append(src)
