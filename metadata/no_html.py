from metadata import MetadataHandler
from metadata.blog import BlogMetadataJSONMapper, BlogContentMetadata, BlogMetadata

class NoHTMLTextMetadataHandler(MetadataHandler):
    content = 'no_html'

    def check_duplicates(self, header, content):
        if (isinstance(content, BlogMetadata) and header.id in self.metadata.keys()):
            md = self.metadata[header.id]
            if md.blog_data.download_url == content.download_url:
                self.logger.debug(f'Duplicate document found for url {header.link} and output url {content.download_url}. Output process will be cancelled.')
                return True
            else:
                return False
            return True    
        return False

    def create_mapper(self):
        return BlogMetadataJSONMapper()

    def build_content_object_from_data(self, **kwargs):
        return BlogMetadata(kwargs['download_url'], kwargs['successful'])

    def add_to_metadata(self, header, content):
        if (header.id not in self.metadata.keys()):
            self.logger.debug(f'Added metadata for post {header.id}')
            self.metadata[header.id] = BlogContentMetadata(header.id, header.title, header.link, header.author, header.date, content)