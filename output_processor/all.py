from os.path import join

from output_processor import ScrapperOutputProcessor
from contents import BlogTextContent, BlogImageContent

from docx import Document
from docx.shared import Inches, Pt

from output_processor import get_output_processor_classes_for_content_except
from output_processor.docs import HeaderDocumentModifier, create_document_modifier

from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

class AllOutputProcessor(ScrapperOutputProcessor):
    content = 'all'
    def __init__(self, user_input, metadata_handler):
        super().__init__(user_input, metadata_handler)
        other_processors = []
        for output_p in get_output_processor_classes_for_content_except(self.content):
            other_processors.append(output_p(user_input, metadata_handler))
        self.other_processors = other_processors

    def create_output_directory(self):
        for processor in self.other_processors:
            processor.create_output_directory()

    def process_blog_data(self, blog_datas):
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for processor in self.other_processors:
                futures.append(executor.submit(processor.process_blog_data, blog_datas))
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as exc:
                    traceback.print_exc()