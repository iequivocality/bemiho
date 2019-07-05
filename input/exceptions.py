class JSONDataNotFound(Exception):
    def __init__(self, message):
        self.message = message

class PageNumberNotDigits(Exception):
    def __init__(self):
        self.message = "Page numbers have to be digits."

class InvalidContentInput(Exception):
    def __init__(self):
        self.message = "Invalid input for content. Must be photos or blog"

class NumberOfPageShouldBeAtLeastOne(Exception):
    def __init__(self):
        self.message = "Number of pages should at least be one"