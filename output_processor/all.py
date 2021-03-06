from os.path import join

from output_processor import ScrapperOutputProcessor

from docx import Document
from docx.shared import Inches, Pt

from output_processor import get_output_processor_classes_for_content_except

from concurrent.futures import ThreadPoolExecutor, as_completed
from logger import BemihoLogger

from contents import BlogData

class AllOutputProcessor(ScrapperOutputProcessor):
    content = 'all'
    
    def __init__(self, user_input):
        super().__init__(user_input)
        self.logger = BemihoLogger(self.__class__).get_logger()
        other_processors = []
        self.logger.debug('Getting other output processors for all context implementation.')
        self.other_processors_blog_datas = {}
        for output_p in get_output_processor_classes_for_content_except(self.content):
            other_processors.append(output_p(user_input))
            self.other_processors_blog_datas[output_p.content] = []
        self.other_processors = other_processors
        self.logger.debug(f'Found the following other output processor classes: {other_processors}')

    def get_metadata_handler_class(self, user_input, member_path):
        pass

    def create_output_directory(self):
        for processor in self.other_processors:
            processor.create_output_directory()

    def do_blog_datas_remapping(self, blog_datas):
        self.logger.debug('Performing remapping for blog data for performing output processor for all.')
        for blog_data in blog_datas:
            header = blog_data.header
            contents = blog_data.contents
            for content in contents:
                for content_key in content.keys():
                    self.other_processors_blog_datas[content_key].append(BlogData(header, content[content_key]))

    def process_blog_data(self, blog_datas):
        self.logger.debug('Starting blog data processing for all processor. One thread is created per output processor.')
        self.do_blog_datas_remapping(blog_datas)
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for processor in self.other_processors:
                self.logger.debug(f'Starting thread execution for processing {processor.content} content.')
                futures.append(executor.submit(processor.process_blog_data, self.other_processors_blog_datas[processor.content]))
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    self.logger.error("Exception occurred on thread", exc_info=True)