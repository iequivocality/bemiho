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
    
    def __init__(self, user_input, metadata_handler_class):
        super().__init__(user_input, metadata_handler_class)
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
        self.metadata_handler.save_metadata()

    def build_document(self, directory, blog_data):
        content_data = None
        header = blog_data.header
        contents = blog_data.contents
        date_string = header.date.strftime("%Y.%m.%d")
        document_path = join(directory, f"{date_string} {header.title}.docx")

        try:
            content_data = self.metadata_handler.build_content_object_from_data(download_url=document_path, successful=False)
            if not self.metadata_handler.check_duplicates(header, content_data):
                document = Document()
                
                HeaderDocumentModifier(header.title, level=1).change_document(document)
                HeaderDocumentModifier(header.link, level=4).change_document(document)
                
                for content in contents:
                    create_document_modifier(content).change_document(document)
                # document.save(self.remove_emoji_from_document_path(document_path))
                document.save(document_path)
                # content_data = self.metadata_handler.build_content_object_from_data(download_url=document_path, successful=True)
                content_data.successful = True
                self.metadata_handler.add_to_metadata(header, content_data)
        except:
            content_data = self.metadata_handler.build_content_object_from_data(download_url=document_path, successful=False)
            self.metadata_handler.add_to_metadata(header, content_data)
            self.logger.error(f'Download from {header.link} to {document_path} is unsuccessful due to issue.', exc_info=True)
        # finally:

    # def remove_emoji_from_document_path(self, document_path):
    #     RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    #     return RE_EMOJI.sub(r'', document_path)