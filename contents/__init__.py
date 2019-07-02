from datetime import datetime
from utilities.text import enclose_to_json_like_string

class BlogData:
    def __init__(self, header, contents):
        self.header = header
        self.contents = contents

class BlogHeader:
    def __init__(self, title, datestring, author, link):
        self.title = title
        self.date = self.format_date(datestring)
        self.author = author
        self.link = link

    def format_date(self, datestring):
        return datetime.now()

    def date_to_string(self):
        return self.date.strftime("%Y_%m_%d_%H_%M_%S")

    def __str__(self):
        header_data = f'    Title: {self.title}\n    Date: {self.date}\n    Author: {self.author}\n    Link: {self.link}'
        return enclose_to_json_like_string(header_data)

class BlogContent:
    def get_content(self):
        raise NotImplementedError()

class BlogTextContent(BlogContent):
    def __init__(self, text):
        self.text = text
    
    def get_content(self):
        return self.text
    
    def __str__(self):
        return self.text
    
class BlogImageContent(BlogContent):
    def __init__(self, image_src):
        self.image_src = image_src
    
    def get_content(self):
        return self.image_src
    
    def __str__(self):
        return self.image_src