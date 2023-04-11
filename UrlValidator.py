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
    
    def get_validated(self, url: str, throwError=False):

        # if it has schema just return.
        if re.match(r'^\w+://', url):
            return self.get_fullUrl(url)
        
        # have domain name. append schema
        elif re.match(r'^\w+(.)\w+', url):
            url = "https://" + url
            return self.get_fullUrl(url)
        
        # url has format like "/../.." or "../.."
        elif self.baseUrl and re.match(r'^(/[^\s]*)+$', url):
            return self.baseUrl + url
        else:
            None

    # change url ("https://domain.com") to ("https://www.domain.com")
    def get_fullUrl(self, url):
        sub_url = url.split("/")
        if(len(sub_url) > 2 and len(sub_url[2].split(".")) == 2):
                url = sub_url[0] + "//www." + sub_url[2]
        return url

    def set_baseUrl(self, url):
        self.baseUrl = url




    


