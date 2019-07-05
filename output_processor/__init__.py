import os
import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module
from os.path import join, exists, isdir

from logger import BemihoLogger
from utilities.file import create_directory
from utilities.reflect import get_qualified_name

from .exceptions import OutputProcessorNotFound

class ScrapperOutputProcessor:
    content = ''
    def __init__(self, user_input, metadata_handler):
        self.user_input = user_input
        self.metadata_handler = metadata_handler
        
        base_path = Path(__file__).parent
        file_path = (base_path / user_input.output).resolve()
        self.output_path = file_path
        self.member_path = self.format_path()
    
    def build_metadata_file(self):
        pass

    def format_path(self):
        group = self.user_input.group.kanji
        member = self.user_input.member.kanji
        print(join(self.output_path, group, member, self.content))
        return join(self.output_path, group, member, self.content)

    def create_output_directory(self):
        if (not exists(self.member_path)):
            path = Path(self.member_path)
            path.mkdir(parents=True)

    def process_blog_data(self, blog_data):
        raise NotImplementedError()

def get_output_processor_class_for_content(content):
    # print(get_output_processor_class_for_content.__name__)
    logger = BemihoLogger(get_output_processor_class_for_content).get_logger()
    qualified_name = get_qualified_name(ScrapperOutputProcessor)
    logger.debug(f'Getting output processor ({qualified_name}) class for content {content}.')
    writer = None
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module('.' + name, package=__name__)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, ScrapperOutputProcessor) and attribute.content == content:
                writer = attribute
    if (writer == None):
        raise OutputProcessorNotFound(content)
    logger.debug(f'Output processor ({get_qualified_name(writer)}) found.')
    return writer

def get_output_processor_classes_for_content_except(not_included):
    processor_classes = []
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module('.' + name, package=__name__)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, ScrapperOutputProcessor) and attribute != ScrapperOutputProcessor and attribute.content != not_included:
                processor_classes.append(attribute)
    return processor_classes