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

class PhotosOutputProcessor(ScrapperOutputProcessor):
    content = 'photos'

    def __init__(self, user_input):
        super().__init__(user_input)
        self.logger = BemihoLogger(self.__class__).get_logger()

    def get_metadata_handler_class(self, user_input, member_path):
        return PhotosMetadataHandler(user_input, member_path)

    def process_blog_data(self, blog_datas):
        self.logger.debug(f'Starting saving photos content to {self.member_path}.')
        self.logger.debug(f'Blog data number {len(blog_datas)}.')
        for blog_data in blog_datas:
            header = blog_data.header
            contents = blog_data.contents
            self.logger.debug(f'Saving contents from {header.title} with content count {len(contents)}.')
            for (index, download_content) in enumerate(contents):
                self.download_file(header, index, download_content)
        self.metadata_handler.save_metadata()

    def download_file(self, header, index, download_content):
        image_url = download_content.content
        download_url = download_content.format_download_url(self.member_path, header.title, index)
        metadata_content = self.metadata_handler.build_content_object_from_data(image_url=image_url, download_url=download_url, successful=True)
        try:
            if self.metadata_handler.check_duplicates(header, metadata_content):
                self.logger.debug(f'Duplicate found. Download from {image_url} to {download_url} is cancelled.')
            else:
                metadata_content.download_url = download_content.format_download_url(self.member_path, clean_file_name(header.title), index)
                if self.metadata_handler.check_duplicates(header, metadata_content):
                    self.logger.debug(f'Duplicate found. Download from {image_url} to {download_url} is cancelled.')
                else:
                    download_content.download_to_file(self.member_path, index)
                    print("DOWNLOAD ")
                    self.metadata_handler.add_to_metadata(header, metadata_content)
        except Exception:
            self.logger.error(f'Download from {image_url} to {download_url} is unsuccessful due to issue.', exc_info=True)
            content_data = self.metadata_handler.build_content_object_from_data(image_url=image_url, download_url=download_url, successful=False)
            self.metadata_handler.add_to_metadata(header, content_data)