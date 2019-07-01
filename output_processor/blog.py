from os.path import join

import io
import requests

from output_processor import ScrapperOutputProcessor
from contents import BlogTextContent, BlogImageContent

from docx import Document
from docx.shared import Inches

class BlogEntryOutputProcessor(ScrapperOutputProcessor):
    content = 'blog'
    def build_document(self, directory, blog_data):
        header = blog_data.header
        contents = blog_data.contents

        document_path = join(directory, f"{header.title}.docx")
        document = Document()
        style = document.styles['Normal']
        
        for content in contents:
            if (isinstance(content, BlogTextContent)):
                # print("text")
                document.add_paragraph(content.get_content())
            elif (isinstance(content, BlogImageContent)):
                response = requests.get(content.get_content(), stream=True)
                image = io.BytesIO(response.content)
                document.add_picture(image, width=Inches(6))
        document.save(document_path)

    def process_blog_data(self, blog_datas):
        directory = self.output_folder_handler.get_directory_for_member_subdirectories(self.content)
        for blog_data in blog_datas:
            self.build_document(directory, blog_data)
