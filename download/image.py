import requests, io, errno
from download.base import BlogDownloadContent
from os.path import join
from utilities.file import get_extension_for_image
from utilities.text import clean_file_name, clean_file_separators
from docx.shared import Inches

from logger import BemihoLogger

class ImageBlogDownloadContent(BlogDownloadContent):
    def __init__(self, header, content):
        super().__init__(header, content)
        self.logger = BemihoLogger(__class__).get_logger()

    def download_to_file(self, directory, index, on_save, on_except):
        image_url = self.content
        if (image_url and not image_url == ''):
            self.logger.debug(f'Image url is not empty. Building download path from {image_url}.')
            download_url = self.format_download_url(directory, self.header.title, index)
            self.save_to_file(directory, download_url, index, on_save, on_except)

    def format_download_url(self, directory, title, index):
        image_url = self.content
        header_date_string = self.header.date_to_string()
        guessed_ext = get_extension_for_image(image_url)
        self.logger.debug(f'Extension for image URL ({image_url}): {guessed_ext}')
        save_url = join(directory, '%s_%s (%s)%s' % (header_date_string, index, clean_file_separators(title), guessed_ext))
        self.logger.debug(f'Download path for image URL {image_url} created: {save_url}')
        return save_url
    
    def save_to_file(self, directory, download_url, index, on_save, on_except):
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        try:
            request = requests.get(self.content, allow_redirects=True, headers=headers)
            with open(download_url, 'wb') as download_file:
                download_file.write(request.content)
            on_save(download_url)
        except OSError as os_err:
            if os_err.errno == errno.EILSEQ:
                rollback_save_url = self.format_download_url(directory, clean_file_name(self.header.title), index)
                self.logger.error(f'Download from {self.content} to {download_url} is unsuccessful due to illegal byte sequence on file name. Will re-download with a cleaned name ({rollback_save_url}).')
                self.save_to_file(directory, rollback_save_url, index, on_save, on_except)
            else:
                on_except(download_url)
                raise os_err
        except Exception as other_error:
            on_except(download_url)
            raise other_error
    
    def download_to_document(self, document):
        image_content = self.content
        if (image_content and image_content != ''):
            try:
                response = requests.get(image_content, stream=True)
                image = io.BytesIO(response.content)
                document.add_picture(image, width=Inches(4))
            except Exception:
                document.add_paragraph(image_content)
                self.logger.debug(f'Unable to fetch {image_content}. The URL was added instead.')