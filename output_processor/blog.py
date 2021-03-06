import re, errno
from os.path import join, sep

from concurrent.futures import ThreadPoolExecutor, as_completed

from output_processor import ScrapperOutputProcessor
from utilities.text import clean_file_name, clean_file_separators

from docx import Document
from docx.shared import Inches, Pt

from logger import BemihoLogger
from output_processor.docs import HeaderDocumentModifier

from metadata.blog import BlogMetadataHandler

class BlogEntryOutputProcessor(ScrapperOutputProcessor):
    content = 'blog'
    
    def __init__(self, user_input):
        super().__init__(user_input)
        self.logger = BemihoLogger(self.__class__).get_logger()

    def get_metadata_handler_class(self, user_input, member_path):
        return BlogMetadataHandler(user_input, member_path)

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
        document_path = join(directory, f"{date_string} ({clean_file_separators(header.title)}).docx")

        try:
            content_data = self.metadata_handler.build_content_object_from_data(download_url=document_path, successful=False)
            self.save_to_document(header, contents, content_data, document_path)
        except OSError as os_error:
            if os_error.errno == errno.EILSEQ:
                document_path = join(directory, f"{date_string} ({clean_file_name(header.title)}).docx")
                content_data = self.metadata_handler.build_content_object_from_data(download_url=document_path, successful=False)
                self.save_to_document(header, contents, content_data, document_path)
            else:
                raise os_error
        except:
            content_data = self.metadata_handler.build_content_object_from_data(download_url=document_path, successful=False)
            self.metadata_handler.add_to_metadata(header, content_data)
            self.logger.error(f'Download from {header.link} to {document_path} is unsuccessful due to issue.', exc_info=True)
    
    def save_to_document(self, header, contents, content_data, document_path):
        if not self.metadata_handler.check_duplicates(header, content_data):
            document = Document()
            paragraph_format = document.styles['Normal'].paragraph_format
            paragraph_format.line_spacing = 1
            
            HeaderDocumentModifier(header.title, level=1).change_document(document)
            HeaderDocumentModifier(header.date.strftime("%Y-%m-%d %H:%M:%S"), level=4).change_document(document)
            HeaderDocumentModifier(header.link, level=4).change_document(document)
            
            for content in contents:
                content.download_to_document(document)
            document.save(document_path)
            content_data.successful = True
            self.metadata_handler.add_to_metadata(header, content_data)