from os.path import join
from download.base import BlogDownloadContent
from utilities.text import clean_emojis, clean_file_separators
from logger import BemihoLogger

class NoHTMLTextBlogDownloadContent(BlogDownloadContent):
    def __init__(self, header, content):
        super().__init__(header, content)
        self.logger = BemihoLogger(__class__).get_logger()

    def download_to_text_file(self, directory, on_save, on_except):
        self.logger.debug(f'Writing no HTML content from {self.header.title} with size {len(self.content)}.')
        text_file_path = self.get_text_file_path(directory)
        try:
            self.do_save(text_file_path, on_save)
        except OSError as os_err:
            if os_err.errno == 92:
                text_file_path = clean_emojis(self.get_text_file_path(directory))
                self.do_save(text_file_path, on_save)
            else:
                on_except(text_file_path)
                raise os_err
        except Exception as other_err:
            on_except(text_file_path)
            raise other_err
        self.logger.debug(f'Writing no HTML content with size {len(self.content)} successful.')

    def do_save(self, file_path, on_save):
        with open(file_path, 'w') as new_text_file:
            date_string = self.header.date.strftime("%Y-%m-%d %H:%M:%S")
            new_text_file.write(f"Title: {self.header.title}\n")
            new_text_file.write(f"Date: {date_string}\n")
            new_text_file.write(f"Link: {self.header.link}\n")
            new_text_file.write("===============\n")
            new_text_file.write(self.content)
            on_save(file_path)

    def get_text_file_path(self, directory):
        header_date_string = self.header.date_to_string()
        download_url = join(directory, '%s (%s).txt' % (header_date_string, clean_file_separators(self.header.title)))
        return download_url