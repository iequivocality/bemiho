import io
import requests
from docx.shared import Inches, Pt

from logger import BemihoLogger

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

# class BlogTextDocumentModifier(DocumentModifier):
#     def change_document(self, document):
#         document.add_paragraph(self.text_container.get_content())

# class BlogImageDocumentModifier(DocumentModifier):
#     def __init__(self, text_container):
#         super().__init__(text_container)
#         self.logger = BemihoLogger(self.__class__).get_logger()

#     def change_document(self, document):
#         image_content = self.text_container.get_content()
#         if (image_content and image_content != ''):
#             try:
#                 response = requests.get(self.text_container.get_content(), stream=True)
#                 image = io.BytesIO(response.content)
#                 document.add_picture(image, width=Inches(4))
#             except Exception:
#                 document.add_paragraph(image_content)
#                 self.logger.debug(f'Unable to fetch {image_content}. The URL was added instead.')


# def create_document_modifier(content):
#     if (isinstance(content, BlogTextContent)):
#         return BlogTextDocumentModifier(content)
#     elif (isinstance(content, BlogImageContent)):
#         return BlogImageDocumentModifier(content)
#     else:
#         return None