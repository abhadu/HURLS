from html.parser import HTMLParser

class PyHtmlParser(HTMLParser):
    instance = None
    def __init__(self):
        super(PyHtmlParser, self).__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                type, url = attr
                if type == "href":
                    self.links.append(url)
                    
        
    def get_urls(self):
        links = self.links
        self.links = []
        return links

    @staticmethod
    def parse(html):
        if PyHtmlParser.instance is None:
            PyHtmlParser.instance = PyHtmlParser()
        PyHtmlParser.instance.feed(html)
        return PyHtmlParser.instance.get_urls()
