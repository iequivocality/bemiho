from os.path import join

from output_processor import ScrapperOutputProcessor
from contents import BlogTextContent, BlogImageContent

from docx import Document
from docx.shared import Inches, Pt

from output_processor.docs import HeaderDocumentModifier, create_document_modifier

class BlogEntryOutputProcessor(ScrapperOutputProcessor):
    content = 'blog'
    def build_document(self, directory, blog_data):
        header = blog_data.header
        contents = blog_data.contents

        document_path = join(directory, f"{header.title}.docx")
        document = Document()
        
        HeaderDocumentModifier(header.title, level=1).change_document(document)
        HeaderDocumentModifier(header.link, level=4).change_document(document)
        
        for content in contents:
            create_document_modifier(content).change_document(document)
        document.save(document_path)

    def process_blog_data(self, blog_datas):
        directory = self.output_folder_handler.get_directory_for_member_subdirectories(self.content)
        for blog_data in blog_datas:
            self.build_document(directory, blog_data)