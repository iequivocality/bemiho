from datetime import datetime
from utilities.text import enclose_to_json_like_string

class BlogHeader:
    def __init__(self, title, datestring, author):
        self.title = title
        self.date = self.format_date(datestring)
        self.author = author

    def format_date(self, datestring):
        return datetime.now()

    def __str__(self):
        header_data = f'    Title: {self.title}\n    Date: {self.date}\n    Author: {self.author}'
        return enclose_to_json_like_string(header_data)