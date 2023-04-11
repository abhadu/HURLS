from Url import Url


class UrlFilter():
    def __init__(self, baseUrl: str, filters:dict):
        self.baseUrl = baseUrl
        self.filters = filters # filters with data

    def filter(self, url, headers, status):

        # only to know what filters are there
        filters = [] 
        has_base = False


        if self.has_baseurl(url):
            if self.filters.get("sub") == "only":
                return None
            has_base = True
        

        if not has_base:
            if self.filters.get("sub") and self.has_subDomains(url):
                filters.append("sub")
            else:
                return None


        if not self.filters.get("status") or self.has_anyStatus(url, status):
            filters.append(status)
        else:
            return None

        return Url(url, filters)

    # filter out urls that has base url
    def has_baseurl(self, url: str):
        if url.startswith(self.baseUrl):
            return True
        return False
    
    # filter out urls that has specified Subdomains
    def has_subDomains(self, url: str):
        sub_domain = url.split("/")[2].split(".")[-2]
        base_domain = self.baseUrl.split("/")[2].split(".")[-2]
        if sub_domain == base_domain:
            return True
        return False
    
    def has_anyStatus(self, url, headers):
        pass
    

