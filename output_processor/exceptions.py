class OutputProcessorNotFound(Exception):
    def __init__(self, content):
        self.message = f'Output processor not found for content {content}'