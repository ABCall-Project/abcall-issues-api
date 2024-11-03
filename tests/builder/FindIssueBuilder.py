from math import ceil


class FindIssueBuilder:
    def __init__(self):
        self.page = 1
        self.limit = 2
        self.data =[]
        self.total_pages = ceil(len(self.data)/self.limit)
        self.has_next = self.page < self.total_pages
    
    def with_page(self,page:int):
        self.page = page
        self.with_has_next(self.page < self.total_pages)
        return self
    
    def with_limit(self,limit:int):
        self.limit = limit
        return self
    
    def with_data(self,data:list):
        self.data = data
        self.with_total_pages(len(data))
        return self

    def with_total_pages(self,total_pages:int):
        self.total_pages = total_pages
        self.with_has_next(self.page < self.total_pages)
        return self
    
    def with_has_next(self,has_next:bool):
        self.has_next = has_next
        return self
    
    def build(self):
        return {
            "page": self.page,
            "limit": self.limit,
            "total_pages": self.total_pages,
            "has_next": self.has_next,
            "data": self.data
        }
