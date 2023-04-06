from html.parser import HTMLParser
from socketserver import BaseRequestHandler
import re

class PyHtmlParser(HTMLParser):
    instance = None
    def __init__(self, baseurl):
        super(PyHtmlParser, self).__init__()
        self.links = []
        self.baseurl = baseurl
        self.url = ""
        self.special_words = ["infiniteindia","http"]

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                type, data = attr
                if type == "href":
                    if self.has_baseurl(data):
                        self.links.append(self.url)
                        return
                    
        
    def has_baseurl(self,data:str):
        self.url = data.strip(".").strip("/")
        if self.endpoint() and self.match_endpoint():
            self.url = self.baseurl + "/" + self.url
            return True
        elif re.search("([.](png|pdf|JPG|webp|jpeg|jpg))$",data):
            return False
        elif data.startswith(self.baseurl) or data.startswith("https://" + self.baseurl):
            return True
        elif re.search("^http|[a-z][.][a-z][.][a-z]",data):
            return False
        else:
            self.url = self.baseurl
            return True
        
    def match_endpoint(self):
        list_base_endpoints = re.split("/*/",self.baseurl)[1:]
        list_data_endpoints = re.split("/*/",self.url)

        if len(list_base_endpoints) <= len(list_data_endpoints):
            for base_endpoint in list_base_endpoints:
                if base_endpoint != list_data_endpoints[list_base_endpoints.index(base_endpoint)]:
                    return False
            self.url = self.url.lstrip("".join(list_base_endpoints))
            self.url = self.url.strip("/")
            return True
        return False


    def endpoint(self):
        if self.url.startswith(self.special_words[0]) or self.url.startswith(self.special_words[1]):
                return False
        return True


    def get_urls(self):
        return self.links

    @staticmethod
    def parser(base_url, html):
        if PyHtmlParser.instance is None:
            PyHtmlParser.instance = PyHtmlParser(base_url)
        PyHtmlParser.instance.feed(html)
        return PyHtmlParser.instance.get_urls()
