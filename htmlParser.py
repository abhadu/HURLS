from html.parser import HTMLParser
from socketserver import BaseRequestHandler
import re

class PyHtmlParser(HTMLParser):
    instance = None
    def __init__(self, baseurl):
        super(PyHtmlParser, self).__init__()
        self.links = []
        self.baseurl = baseurl

    def handle_starttag(self, tag, attrs):
        if tag == "a" or tag == "link":
            for attr in attrs:
                type, url = attr
                if type == "href":
                    self.links.append(self.url)
        return
                    
        
    def get_urls(self):
        links = self.links
        self.links = []
        return links

    @staticmethod
    def parser(base_url, html):
        if PyHtmlParser.instance is None:
            PyHtmlParser.instance = PyHtmlParser(base_url)
        PyHtmlParser.instance.feed(html)
        return PyHtmlParser.instance.get_urls()
