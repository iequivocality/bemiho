import re
from os.path import join

from concurrent.futures import ThreadPoolExecutor, as_completed

from output_processor import ScrapperOutputProcessor
from contents import BlogTextContent, BlogImageContent

from docx import Document
from docx.shared import Inches, Pt

from logger import BemihoLogger
from output_processor.docs import HeaderDocumentModifier, create_document_modifier

class BlogEntryOutputProcessor(ScrapperOutputProcessor):
    content = 'blog'
    
    def __init__(self, user_input, metadata_handler):
        super().__init__(user_input, metadata_handler)
        self.logger = BemihoLogger(self.__class__).get_logger()

    def process_blog_data(self, blog_datas):
        self.logger.debug(f'Starting saving blog content to {self.member_path}.')
        directory = self.member_path
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for blog_data in blog_datas:
                self.logger.debug(f'Starting thread execution for building document.')
                futures.append(executor.submit(self.build_document, directory, blog_data))
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    self.logger.error("Exception occurred on thread", exc_info=True)

    def build_document(self, directory, blog_data):
        header = blog_data.header
        contents = blog_data.contents
        date_string = header.date.strftime("%Y.%m.%d")
        document_path = join(directory, f"{date_string} {header.title}.docx")
        document = Document()
        
        HeaderDocumentModifier(header.title, level=1).change_document(document)
        HeaderDocumentModifier(header.link, level=4).change_document(document)
        
        for content in contents:
            create_document_modifier(content).change_document(document)
        document.save(self.remove_emoji_from_document_path(document_path))

    def remove_emoji_from_document_path(self, document_path):
        RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
        return RE_EMOJI.sub(r'', document_path)