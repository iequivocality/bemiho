import requests
from os.path import join
import mimetypes

from concurrent.futures import ThreadPoolExecutor, as_completed

from output_processor import ScrapperOutputProcessor
from contents import BlogImageContent
from logger import BemihoLogger

class PhotosOutputProcessor(ScrapperOutputProcessor):
    content = 'photos'

    def __init__(self, user_input, metadata_handler_class):
        super().__init__(user_input, metadata_handler_class)
        self.logger = BemihoLogger(self.__class__).get_logger()

    def process_blog_data(self, blog_datas):
        directory = self.member_path
        self.logger.debug(f'Starting saving photos content to {self.member_path}.')
        self.logger.debug(f'Blog data number {len(blog_datas)}.')
        for blog_data in blog_datas:
            header = blog_data.header
            contents = blog_data.contents
            self.logger.debug(f'Saving contents from {header.title} with content count {len(contents)}.')
            for (index, content) in enumerate(contents):
                self.save_photo(directory, index, header, content)
        self.metadata_handler.save_metadata()
            # with ThreadPoolExecutor(max_workers=10) as executor:
            #     futures = []
            #     for (index, content) in enumerate(contents):
            #         self.logger.debug(f'Starting thread execution for saving photos.')
            #         futures.append(executor.submit(self.save_photo, directory, index, header, content))
            #     for future in as_completed(futures):
            #         try:
            #             future.result()
            #         except Exception:
            #             self.logger.error("Exception occurred on thread", exc_info=True)

    def save_photo(self, directory, index, header, content):
        if (isinstance(content, BlogImageContent)):
            image_url = content.get_content()
            if (image_url and not image_url == ''):
                self.logger.debug(f'Image url is not empty. Building download path from {image_url}.')
                save_url = self.build_url(header, image_url, directory, index)
                self.save_photo_to_file(header, image_url, save_url)
            else:
                self.logger.debug('Image url is empty.')

    def save_photo_to_file(self, header, image_url, save_url):
        try:
            request = requests.get(image_url, allow_redirects=True)
            with open(save_url, 'wb') as image_file:
                image_file.write(request.content)
            content_data = self.metadata_handler.build_content_object_from_data(True, image_url=image_url, download_url=save_url)
            self.metadata_handler.add_success_to_metadata(header, content_data)
            self.logger.debug(f'Download from {image_url} to {save_url} is successful.')
        except:
            content_data = self.metadata_handler.build_content_object_from_data(False, image_url=image_url, download_url=save_url)
            self.metadata_handler.add_success_to_metadata(header, content_data)
            self.logger.error(f'Download from {image_url} to {save_url} is unsuccessful due to issue.', exc_info=True)

    def build_url(self, header, image_url, directory, index):
        header_date_string = header.date_to_string()
        guessed_ext = self.get_mime_type_extension(image_url)
        self.logger.debug(f'Extension for image URL ({image_url}): {guessed_ext}')
        save_url = join(directory, '%s_%s%s' % (header_date_string, index, guessed_ext))
        self.logger.debug(f'Download path for image URL {image_url} created: {save_url}')
        return save_url

    def get_mime_type_extension(self, image_url):
        mime_type = mimetypes.guess_type(image_url)
        return mimetypes.guess_all_extensions(mime_type[0])[-1]