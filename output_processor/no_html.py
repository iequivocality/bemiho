import requests
import imghdr
from os.path import join, sep
import mimetypes

from concurrent.futures import ThreadPoolExecutor, as_completed

from output_processor import ScrapperOutputProcessor
from download.image import ImageBlogDownloadContent
from logger import BemihoLogger
from utilities.text import clean_file_name, check_valid_url_format
from utilities.file import IMAGE_MIME_TYPE, VALID_PHOTO_EXTENSIONS

from metadata.no_html import NoHTMLTextMetadataHandler

class NoHTMLTextOutputProcessor(ScrapperOutputProcessor):
    content = 'no_html'

    def __init__(self, user_input):
        super().__init__(user_input)
        self.logger = BemihoLogger(self.__class__).get_logger()

    def get_metadata_handler_class(self, user_input, member_path):
        return NoHTMLTextMetadataHandler(user_input, member_path)

    def process_blog_data(self, blog_datas):
        self.logger.debug(f'Blog data number {len(blog_datas)}.')
        for blog_data in blog_datas:
            header = blog_data.header
            contents = blog_data.contents
            self.logger.debug(f'Saving text only contents from {header.title} with content count {len(contents)}.')
            for download_content in contents:
                self.save_to_file_and_metadata(header, download_content)
            self.metadata_handler.save_metadata()

    def on_save(self, header, content_data, file_path):
        content_data.download_url = file_path
        content_data.successful = True
        self.metadata_handler.add_to_metadata(header, content_data)
    
    def on_except(self, header, content_data, file_path):
        content_data.download_url = file_path
        content_data.successful = False
        self.metadata_handler.add_to_metadata(header, content_data)

    def save_to_file_and_metadata(self, header, download_content):
        download_url = download_content.get_text_file_path(self.member_path)
        try:
            content_data = self.metadata_handler.build_content_object_from_data(download_url=download_url, successful=False)
            if not self.metadata_handler.check_duplicates(header, content_data):
                download_content.download_to_text_file(self.member_path,
                    lambda file_path : self.on_save(header, content_data, file_path),
                    lambda file_path : self.on_except(header, content_data, file_path))
            else:
                self.logger.debug(f'Duplicate found for {header.title} with content count {len(contents)}.')
        except:
            self.logger.error(f'Download of no_html from {header.link} to {download_url} is unsuccessful due to issue.', exc_info=True)