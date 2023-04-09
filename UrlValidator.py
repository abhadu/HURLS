import re

class UrlValiator():
    def __init__(self):
        self.baseUrl = None

    def get_validatedAll(self, urls, throwError=False):
        _urls = []
        for url in urls:
            _url = self.get_validated(url, throwError)
            if _url:
                _urls.append(_url)

        return _urls
    
    def get_validated(self, url, throwError=False):

        # if it has schema just return.
        if re.match(r'^\w+://', url):
            return url
        # have domain name. append schema
        elif re.match(r'\w+(.)\w+', url):
            return "https://" + url
        # url has format like "/../.." or "../.."
        elif self.baseUrl and re.match(r'^(/[^\s]*)+$', url):
            return self.baseUrl + url
        else:
            None

    def set_baseUrl(self, url):
        self.baseUrl = url




    


