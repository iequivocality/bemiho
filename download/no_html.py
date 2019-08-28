from os.path import join
from download.base import BlogDownloadContent
from utilities.text import clean_file_name
from logger import BemihoLogger

class NoHTMLTextBlogDownloadContent(BlogDownloadContent):
    def __init__(self, header, content):
        super().__init__(header, content)
        self.logger = BemihoLogger(__class__).get_logger()

    def download_to_text_file(self, directory):
        self.logger.debug(f'Writing no HTML content from {self.header.title} with size {len(self.content)}.')
        with open(self.get_text_file_path(directory), 'w') as new_text_file:
            new_text_file.write(self.content)
        self.logger.debug(f'Writing no HTML content with size {len(self.content)} successful.')

    def get_text_file_path(self, directory):
        header_date_string = self.header.date_to_string()
        download_url = join(directory, '%s (%s).txt' % (header_date_string, clean_file_name(self.header.title)))
        return download_url