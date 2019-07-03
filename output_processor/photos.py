import urllib.request as request
from os.path import join
import mimetypes

from output_processor import ScrapperOutputProcessor
from contents import BlogImageContent

class PhotosOutputProcessor(ScrapperOutputProcessor):
    content = 'photos'
    def get_mime_type_extension(self, image_url):
        mime_type = mimetypes.guess_type(image_url)
        return mimetypes.guess_all_extensions(mime_type[0])[-1]

    def build_url(self, header, image_url, directory, index):
        header_date_string = header.date_to_string()
        guessed_ext = self.get_mime_type_extension(image_url)
        save_url = join(directory, '%s_%s%s' % (header_date_string, index, guessed_ext))
        return save_url

    def process_blog_data(self, blog_datas):
        directory = self.member_path
        for blog_data in blog_datas:
            header = blog_data.header
            contents = blog_data.contents
            for (index, content) in enumerate(contents):
                if (isinstance(content, BlogImageContent)):
                    image_url = content.get_content()
                    if (image_url and not image_url == ''):
                        save_url = self.build_url(header, image_url, directory, index)
                        request.urlretrieve(content.get_content(), save_url)