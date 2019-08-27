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

from metadata.photos import PhotosMetadataHandler

class NoHTMLTextOutputProcessor(ScrapperOutputProcessor):
    content = 'no_html'

    def __init__(self, user_input):
        super().__init__(user_input)
        self.logger = BemihoLogger(self.__class__).get_logger()

    def process_blog_data(self, blog_datas):
        self.logger.debug(f'Blog data number {len(blog_datas)}.')
        for blog_data in blog_datas:
            header = blog_data.header
            contents = blog_data.contents
            self.logger.debug(f'Saving text only contents from {header.title} with content count {len(contents)}.')
            for download_content in contents:
                download_content.download_to_text_file(self.member_path)