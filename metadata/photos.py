from metadata import MetadataHandler, Metadata
from json_extractor.mapper import JSONObjectMapper

class PhotosMetadataJSONMapper(JSONObjectMapper):
    def map_to_object(self, data):
        return {}

class PhotosData:
    def __init__(self, image_url, download_url, successful):
        self.image_url = image_url
        self.download_url = download_url
        self.successful = successful

class PhotosContentMetadata(Metadata):
    def __init__(self, id_, title, link, author):
        self.id = id_
        self.title = title
        self.link = link
        self.author = author
        self.photos = []
    
    def add_photo(self, photo):
        self.photos.append(photo)

    def __str__(self):
        return len(self.photos)

    def to_json(self):
        photos_json = []
        for photo in self.photos:
            photo_json = {
                'image_url' : photo.image_url,
                'download_url' : photo.download_url,
                'successful' : photo.successful
            }
            photos_json.append(photo_json)
        return {
            'id' : self.id,
            'title' : self.title,
            'link' : self.link,
            'author' : self.author,
            'photos' : photos_json
        }

class PhotosMetadataHandler(MetadataHandler):
    content = 'photos'

    def create_mapper(self):
        return PhotosMetadataJSONMapper()

    def __init__(self, user_input, metadata_directory):
        super().__init__(user_input, metadata_directory)

    def check_duplicates(self, header, content):
        return False

    def add_success_to_metadata(self, header, content):
        if (header.id in self.metadata.keys()):
            self.metadata[header.id].add_photo(content)
        else:
            self.metadata[header.id] = PhotosContentMetadata(header.id, header.title, header.link, header.author)
            self.metadata[header.id].add_photo(content)
    
    def build_content_object_from_data(self, success, **kwargs):
        return PhotosData(kwargs['image_url'], kwargs['download_url'], success)

    def add_unsuccess_to_metadata(self, header, content):
        pass

    def repair_metadata(self):
        pass