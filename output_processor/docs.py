import io
import requests

from contents import BlogTextContent, BlogImageContent

from docx.shared import Inches, Pt

class DocumentModifier:
    def __init__(self, text_container):
        self.text_container = text_container
    
    def change_document(self, document):
        raise NotImplementedError()

class HeaderDocumentModifier(DocumentModifier):
    def __init__(self, text_container, level=1):
        super().__init__(text_container)
        self.level = level

    def change_document(self, document):
        document.add_heading(self.text_container, level=1)

class BlogTextDocumentModifier(DocumentModifier):
    def change_document(self, document):
        document.add_paragraph(self.text_container.get_content())

class BlogImageDocumentModifier(DocumentModifier):
    def change_document(self, document):
        response = requests.get(self.text_container.get_content(), stream=True)
        image = io.BytesIO(response.content)
        document.add_picture(image, width=Inches(4))

def create_document_modifier(content):
    if (isinstance(content, BlogTextContent)):
        return BlogTextDocumentModifier(content)
    elif (isinstance(content, BlogImageContent)):
        return BlogImageDocumentModifier(content)
    else:
        return None