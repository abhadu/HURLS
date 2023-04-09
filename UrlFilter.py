

class UrlFilter():
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl

    def filter(self, urls):
        _urls = set()

        for url in urls:
            if self.has_baseurl(url):
                _urls.add(url)
        return _urls

    # filter out urls that has base url
    def has_baseurl(self, url):
        if url.startswith(self.baseUrl):
            return True
        return False
