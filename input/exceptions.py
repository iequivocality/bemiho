class Error(Exception):
    pass

class JSONDataNotFound(Error):
    def __init__(self, message):
        self.message = message

class PageNumberNotDigits(Error):
    def __init__(self):
        self.message = "Page numbers have to be digits."

class InvalidContentInput(Error):
    def __init__(self):
        self.message = "Invalid input for content. Must be photos or blog"

class FirstPageLargerThanLastPage(Error):
    def __init__(self):
        self.message = "First page cannot be larger than last page."