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
        if tag == "a":
            for attr in attrs:
                type, data = attr
                if type == "href":
                    if self.has_baseurl(data):
                        self.links.append(data)
                        return
                    
        
    def has_baseurl(self,data:str):
        if data.startswith(self.baseurl):
            return True
        return False
        
    def get_urls(self):
        return self.links

    @staticmethod
    def parser(base_url, html):
        if PyHtmlParser.instance is None:
            PyHtmlParser.instance = PyHtmlParser(base_url)
        PyHtmlParser.instance.feed(html)
        return PyHtmlParser.instance.get_urls()
