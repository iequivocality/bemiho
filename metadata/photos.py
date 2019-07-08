from metadata import MetadataHandler
from json_extractor.mapper import JSONObjectMapper

class PhotosMetadataJSONMapper(JSONObjectMapper):
    def map_to_object(self, data):
        return None


class PhotosContentMetadata:
    def __init__(self, id_, title, url, author, photos = []):
        self.id = id_
        self.title = title
        self.url = url
        self.author = author
        self.photos = photos
    
    def add_photo(self, photo):
        self.photos.append(photo)

class PhotosMetadataHandler(MetadataHandler):
    content = 'photos'

    def __init__(self, user_input, metadata_directory, mapper):
        super().__init__(user_input, metadata_directory)

    def check_duplicates(self, header, content):
        return False

    def add_success_to_metadata(self, header, content):
        raise NotImplementedError()

    def add_unsuccess_to_metadata(self, header, content):
        raise NotImplementedError()

    def repair_metadata(self):
        raise NotImplementedError()