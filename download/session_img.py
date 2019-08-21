import imghdr, io
from os.path import join

from download.base import BlogDownloadContent
from download.image import ImageBlogDownloadContent
from services.selenium import SeleniumService
from utilities.file import get_extension_for_bit_content
from utilities.text import clean_file_name

from docx.shared import Inches

class SessionBasedImageBlogDownloadContent(BlogDownloadContent):
    def __init__(self, header, content, element):
        super().__init__(header, content)
        self.element = element
        self.selenium_service = SeleniumService()

    def download_to_file(self, directory, index):
        self.selenium_service.start()
        ( image_url, image_selector ) = self.content
        if (image_url and not image_url == ''):
            self.logger.debug(f'Image url is not empty. Building download path from {image_url}.')
            bit_content = self.selenium_service.get_image_content(image_url, image_selector)
            if bit_content is not None:
                download_url = self.format_download_url(directory, self.header.title, index)
                self.save_to_file(directory, download_url, bit_content, index)
            else:
                smaller_image = self.element.find('img')
                if (smaller_image is not None):
                    ImageBlogDownloadContent(self.header, smaller_image.get('src')).download_to_file(directory, index)
    
    def format_download_url(self, directory, title, index):
        self.selenium_service.start()
        header_date_string = self.header.date_to_string()
        ( image_url, image_selector ) = self.content
        bit_content = self.selenium_service.get_image_content(image_url, image_selector)
        if bit_content is not None:
            guessed_ext = get_extension_for_bit_content(bit_content)
            self.logger.debug(f'Extension for image URL ({self.content[0]}): {guessed_ext}')
            download_url = join(directory, '%s_%s (%s)%s' % (header_date_string, index, title, guessed_ext))
            self.logger.debug(f'Download path for image URL {self.content[0]} created: {download_url}')
            return download_url
        else:
            smaller_image = self.element.find('img')
            if (smaller_image is not None):
                return ImageBlogDownloadContent(self.header, smaller_image.get('src')).format_download_url(directory, title, index)

    def save_to_file(self, directory, download_url, bit_content, index):
        try:
            with open(download_url, 'wb') as download_file:
                download_file.write(bit_content)
        except OSError as os_err:
            if os_err.errno == 92:
                rollback_save_url = self.format_download_url(directory, clean_file_name(self.header.title), index)
                self.logger.error(f'Download from {self.content} to {download_url} is unsuccessful due to OS issue. Will re-download with a cleaned name ({rollback_save_url}).', exc_info=True)
                self.save_to_file(directory, rollback_save_url, bit_content, index)
            else:
                raise os_err
        except Exception as other_error:
            raise other_error
    
    def download_to_document(self, document):
        self.selenium_service.start()
        ( image_url, image_selector ) = self.content
        if (image_url and not image_url == ''):
            try:
                bit_content = self.selenium_service.get_image_content(image_url, image_selector)
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
            