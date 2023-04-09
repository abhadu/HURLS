from Url import Url


class UrlFilter():
    def __init__(self, baseUrl, filters:dict):
        self.baseUrl = baseUrl
        self.filters = filters # filters with data

    def filter(self, url, headers, status):

        # only to know what filters are there
        filters = [] 

        if not self.has_baseurl(url):
            return None
        
        if not self.has_subDomains(url) and self.filters.get("Sub"):
            return None
        else:
            filters.append("Sub")

        if not self.has_anyStatus(url, status) and self.filters.get("Status"):
            return None
        else:
            filters.append(status)

        return Url(url, filters)

    # filter out urls that has base url
    def has_baseurl(self, url):
        if url.startswith(self.baseUrl):
            return True
        return False
    
    # filter out urls that has specified Subdomains
    def has_subDomains(self, url):
         pass
    
    def has_anyStatus(self, url, headers):
        pass
    

