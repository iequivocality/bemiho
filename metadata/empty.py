from metadata import MetadataHandler

class EmptyMetadataHandler(MetadataHandler):
    content = ''

    def load_metadata(self):
        pass

    def check_duplicates(self, header, content):
        pass

    def build_content_object_from_data(self, **kwargs):
        pass

    def add_to_metadata(self, header, content):
        pass

    def save_metadata(self):
        pass
            