from logger import BemihoLogger

class BlogDownloadContent:
    def __init__(self, header, content):
        self.header = header
        self.content = content
        self.logger = BemihoLogger(__class__).get_logger()

    def download_to_file(self, directory, index):
        pass
    
    def download_to_document(self, document):
        pass

    def download_to_text_file(self, directory):
        pass