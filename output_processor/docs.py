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