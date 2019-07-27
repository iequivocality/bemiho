from os.path import exists
from datetime import datetime

from metadata import MetadataHandler, Metadata
from json_extractor.mapper import JSONObjectMapper
from utilities.text import enclose_to_json_like_string
from logger import BemihoLogger

class PhotosMetadataJSONMapper(JSONObjectMapper):
    def map_to_object(self, data):
        metadata = PhotosContentMetadata(data['id'], data['title'], data['link'], data['author'], datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S"))
        for photo_parsed in data['photos']:
            metadata.add_photo(PhotosData(photo_parsed['image_url'], photo_parsed['download_url'], photo_parsed['successful']))
        return metadata

class PhotosData(Metadata):
    def __init__(self, image_url, download_url, successful):
        self.image_url = image_url
        self.download_url = download_url
        self.successful = successful

    def __str__(self):
        pd_string = f"    Image URL: {self.image_url}\n    Download URL: {self.download_url}\n    Successful: {self.successful}\n"
        return enclose_to_json_like_string(pd_string)

    def to_json(self):
        photo_json = {
            'image_url' : self.image_url,
            'download_url' : self.download_url,
            'successful' : self.successful
        }
        return photo_json

class PhotosContentMetadata(Metadata):
    def __init__(self, _id, title, link, author, date):
        super().__init__(_id)
        self.title = title
        self.link = link
        self.author = author
        self.date = date
        self.photos = []
    
    def add_photo(self, photo):
        self.photos.append(photo)

    def does_photo_exist(self, content_data):
        existing = any(content_data.image_url == photo.image_url and content_data.download_url == photo.download_url and exists(photo.download_url) for photo in self.photos)
        return existing is not None

    def __str__(self):
        pd_string = f"    Title: {self.title}\n    Link: {self.link}\n    Author: {self.author}\n    Photos: {len(self.photos)}"
        return enclose_to_json_like_string(pd_string)

    def to_json(self):
        photos_json = []
        for photo in self.photos:
            photos_json.append(photo.to_json())
        return {
            'id' : self.id,
            'title' : self.title,
            'link' : self.link,
            'author' : self.author,
            'date' : self.date.strftime("%Y-%m-%d %H:%M:%S"),
            'photos' : photos_json
        }

class PhotosMetadataHandler(MetadataHandler):
    content = 'photos'

    def create_mapper(self):
        return PhotosMetadataJSONMapper()

    def __init__(self, user_input, metadata_directory):
        super().__init__(user_input, metadata_directory)
        self.logger = BemihoLogger(self.__class__).get_logger()

    def check_duplicates(self, header, content):
        if (header.id in self.metadata.keys()):
            md = self.metadata[header.id]
            if (md.does_photo_exist(content) and exists(content.download_url)):
                self.logger.debug(f'Duplicate photo found for photo url {content.image_url} and output url {content.download_url}. Output process will be cancelled.')
                return True
            else:
                return False
            return True    
        return False

    def add_to_metadata(self, header, content):
        if (header.id in self.metadata.keys()):
            self.metadata[header.id].add_photo(content)
        else:
            self.logger.debug(f'Added metadata for post {header.id}')
            self.metadata[header.id] = PhotosContentMetadata(header.id, header.title, header.link, header.author, header.date)
            self.metadata[header.id].add_photo(content)
    
    def build_content_object_from_data(self, **kwargs):
        return PhotosData(kwargs['image_url'], kwargs['download_url'], kwargs['successful'])