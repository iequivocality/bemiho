import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module

from output_processor.file_handler import OutputFolderHandler

class ScrapperOutputProcessor:
    content = ''
    def __init__(self, user_input, metadata_handler):
        self.user_input = user_input
        self.metadata_handler = metadata_handler
        self.output_folder_handler = OutputFolderHandler(self.user_input)
        self.output_folder_handler.create_member_directory()
    
    def build_metadata_file(self):
        pass

    def process_blog_data(self, blog_data):
        raise NotImplementedError()
        # for content in blog_datum.contents:
        #     print(content)

def get_output_processor_class_for_content(user_input):
    writer = None
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module('.' + name, package=__name__)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, ScrapperOutputProcessor) and attribute.content == user_input.content:
                writer = attribute
    return writer