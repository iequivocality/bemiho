from . import MetadataHandler, Metadata



class BlogMetadataHandler(MetadataHandler):
    content = 'blog'

    def check_duplicates(self, header, content):
        raise NotImplementedError()

    def build_content_object_from_data(self, **kwargs):
        raise NotImplementedError()

    def add_to_metadata(self, header, content):
        raise NotImplementedError()