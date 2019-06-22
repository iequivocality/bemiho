class Error(Exception):
    pass

class JSONDataNotFound(Error):
    def __init__(self, message):
        self.message = message

class PageNumberNotDigits(Error):
    def __init__(self):
        self.message = "Page numbers have to be digits."