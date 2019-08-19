from logger import BemihoLogger
from download.base import BlogDownloadContent

class TextBlogDownloadContent(BlogDownloadContent):
    def __init__(self, header, content):
        self.header = header
        self.content = content
        self.logger = BemihoLogger(__class__).get_logger()
    
    def download_to_document(self, document):
        document.add_paragraph(self.content)