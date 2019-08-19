from datetime import datetime
from utilities.text import enclose_to_json_like_string

class BlogData:
    def __init__(self, header, contents):
        self.header = header
        self.contents = contents

class BlogHeader:
    def __init__(self, title, datestring, author, link, page):
        self.title = title
        self.date = self.format_date(datestring)
        self.author = author
        self.link = link
        self.page = page
        self.id = self.get_id_from_link(link)

    def get_id_from_link(self, link):
        return link

    def format_date(self, datestring):
        return datetime.now()

    def date_to_string(self):
        if (self.date.minute > 0 or self.date.hour > 0):
            return self.date.strftime("%Y_%m_%d_%H%M")
        else:
            return self.date.strftime("%Y_%m_%d")

    def __str__(self):
        header_data = f'    ID: {self.id}\n    Title: {self.title}\n    Date: {self.date}\n    Author: {self.author}\n    Link: {self.link}'
        return enclose_to_json_like_string(header_data)