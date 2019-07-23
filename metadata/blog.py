from datetime import datetime

from logger import BemihoLogger
from . import MetadataHandler, Metadata
from utilities.text import enclose_to_json_like_string
from json_extractor.mapper import JSONObjectMapper

class BlogMetadataJSONMapper(JSONObjectMapper):
    def map_to_object(self, data):
        blog_data = BlogData(data['download_url'], data['successful'])
        metadata = BlogContentMetadata(data['id'], data['title'], data['link'], data['author'], int(data['page']), datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S"), blog_data)
        return metadata

class BlogContentMetadata(Metadata):
    def __init__(self, _id, title, link, author, page, date, blog_data):
        super().__init__(_id)
        self.title = title
        self.link = link
        self.author = author
        self.page = page
        self.date = date
        self.blog_data = blog_data

    def __str__(self):
        pd_string = f"    Title: {self.title}\n    Link: {self.link}\n    Author: {self.author}\n    Page: {self.page}\n    Photos: {str(self.blog_data)}"
        return enclose_to_json_like_string(pd_string)

    def to_json(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'link' : self.link,
            'author' : self.author,
            'date' : self.date.strftime("%Y-%m-%d %H:%M:%S"),
            'page' : self.page,
            'successful' : self.blog_data.successful,
            'download_url' : self.blog_data.download_url
        }

class BlogData(Metadata):
    def __init__(self, download_url, successful):
        self.download_url = download_url
        self.successful = successful

    def __str__(self):
        pd_string = f"    Download URL: {self.download_url}\n    Successful: {self.successful}\n"
        return enclose_to_json_like_string(pd_string)

    def to_json(self):
        blog_json = {
            'download_url' : self.download_url,
            'successful' : self.successful
        }
        return blog_json

class BlogMetadataHandler(MetadataHandler):
    content = 'blog'

    def __init__(self, user_input, metadata_directory):
        super().__init__(user_input, metadata_directory)
        self.logger = BemihoLogger(self.__class__).get_logger()

    def create_mapper(self):
        return BlogMetadataJSONMapper()

    def check_duplicates(self, header, content):
        if (header.id in self.metadata.keys()):
            md = self.metadata[header.id]
            if md.blog_data.download_url == content.download_url:
                self.logger.debug(f'Duplicate document found for url {header.link} and output url {content.download_url}. Output process will be cancelled.')
                return True
            else:
                return False
            return True    
        return False

    def build_content_object_from_data(self, **kwargs):
        return BlogData(kwargs['download_url'], kwargs['successful'])

    def add_to_metadata(self, header, content):
        if (header.id not in self.metadata.keys()):
            self.logger.debug(f'Added metadata for post {header.id}')
            self.metadata[header.id] = BlogContentMetadata(header.id, header.title, header.link, header.author, header.page, header.date, content)
            