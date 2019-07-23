class MetadataHandlerNotFound(Exception):
    def __init__(self, content):
        self.message = f'Metadata handler not found for content {content}'