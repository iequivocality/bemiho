import imghdr, io
from os.path import join

from download.base import BlogDownloadContent
from download.image import ImageBlogDownloadContent
from services.session_img import SessionImageService
from utilities.file import get_extension_for_bit_content
from utilities.text import clean_file_name, clean_file_separators

from docx.shared import Inches
from logger import BemihoLogger

class SessionBasedImageBlogDownloadContent(BlogDownloadContent):
    def __init__(self, header, content, element):
        super().__init__(header, content)
        self.element = element
        self.session_img_service = SessionImageService()
        self.session_img_service.start()
        self.bit_content = None
        self.logger = BemihoLogger(__class__).get_logger()

    def download_to_file(self, directory, index, on_save, on_except):
        ( image_url ) = self.content
        if (image_url and not image_url == ''):
            self.logger.debug(f'Image url is not empty. Building download path from {image_url}.')
            bit_content = self.get_bit_content()
            if bit_content is not None:
                download_url = self.format_download_url(directory, self.header.title, index)
                self.save_to_file(directory, download_url, bit_content, index, on_save, on_except)
            else:
                smaller_image = self.element.find('img')
                if (smaller_image is not None):
                    ImageBlogDownloadContent(self.header, smaller_image.get('src')).download_to_file(directory, index, on_save, on_except)
    
    def format_download_url(self, directory, title, index):
        header_date_string = self.header.date_to_string()
        bit_content = self.get_bit_content()
        if bit_content is not None:
            guessed_ext = get_extension_for_bit_content(bit_content)
            self.logger.debug(f'Extension for image URL ({self.content[0]}): {guessed_ext}')
            download_url = join(directory, '%s_%s (%s)%s' % (header_date_string, index, clean_file_separators(title), guessed_ext))
            self.logger.debug(f'Download path for image URL {self.content[0]} created: {download_url}')
            return download_url
        else:
            smaller_image = self.element.find('img')
            if (smaller_image is not None):
                return ImageBlogDownloadContent(self.header, smaller_image.get('src')).format_download_url(directory, title, index)

    def save_to_file(self, directory, download_url, bit_content, index, on_save, on_except):
        try:
            with open(download_url, 'wb') as download_file:
                download_file.write(bit_content)
            on_save(download_url)
        except OSError as os_err:
            if os_err.errno == 92:
                rollback_save_url = self.format_download_url(directory, clean_file_name(self.header.title), index)
                self.logger.error(f'Download from {self.content} to {download_url} is unsuccessful due to OS issue. Will re-download with a cleaned name ({rollback_save_url}).', exc_info=True)
                self.save_to_file(directory, rollback_save_url, bit_content, index, on_save, on_except)
            else:
                on_except(download_url)
                raise os_err
        except Exception as other_error:
            on_except(download_url)
            raise other_error
    
    def download_to_document(self, document):
        ( image_url ) = self.content
        if (image_url and not image_url == ''):
            try:
                bit_content = self.get_bit_content()
                if bit_content is not None:
                    image = io.BytesIO(bit_content)
                    document.add_picture(image, width=Inches(4))
                else:
                    smaller_image = self.element.find('img')
                    if (smaller_image is not None):
                        ImageBlogDownloadContent(self.header, smaller_image.get('src')).download_to_document(document)
            except Exception:
                document.add_paragraph(image_url)
                self.logger.debug(f'Unable to fetch {image_url}. The URL was added instead.')

    def get_bit_content(self):
        if self.bit_content is None:
            ( image_url, image_selector ) = self.content
            return self.session_img_service.get_image_content(image_url, image_selector)
        else:
            return self.bit_content

    def clear(self):
        self.session_img_service.stop()