import urllib.request as request
from os.path import join
import mimetypes

from output_processor import ScrapperOutputProcessor

class PhotosOutputProcessor(ScrapperOutputProcessor):
    content = 'photos'
    def get_mime_type_extension(self, image_url):
        mime_type = mimetypes.guess_type(image_url)
        return mimetypes.guess_all_extensions(mime_type[0])[-1]

    def build_url(self, header, image_url, directory, index):
        header_date_string = header.date_to_string()
        # # Need to get MIME type here
        guessed_ext = self.get_mime_type_extension(image_url)
        save_url = join(directory, self.content, '%s_%s%s' % (header_date_string, index, guessed_ext))
        # print(mimetypes.guess_type(content))
        return save_url

    # def write(self):
    #     contents = self.blog_data.contents
    #     directory = self.output_folder_handler.get_member_path
    #     for (index, content) in enumerate(contents):
    #         save_url = self.build_url(directory, index)
    #         request.urlretrieve(content.get_content(), save_url)

    def process_blog_data(self, blog_datas):
        directory = self.output_folder_handler.get_member_path()
        for blog_data in blog_datas:
            header = blog_data.header
            print(header.date_to_string())
            contents = blog_data.contents
            for (index, content) in enumerate(contents):
                image_url = content.get_content()
                if (image_url and not image_url == ''):
                    save_url = self.build_url(header, image_url, directory, index)
                    print(save_url)
                    request.urlretrieve(content.get_content(), save_url)
                # save_url = self.build_url(header, content, directory, index)
                # request.urlretrieve(content.get_content(), save_url)
                # print(mimetypes.guess_type(content))
                
                # print(content)
        # with urllib.request.urlopen(build_url()) as response:
        #     return response.read()