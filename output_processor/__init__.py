import os
import sys
import inspect
import pkgutil

from logger import BemihoLogger
from utilities.file import create_directory
from utilities.reflect import get_qualified_name, get_class_in_module, get_classes_in_module
from output_processor.base import ScrapperOutputProcessor

from .exceptions import OutputProcessorNotFound

def get_output_processor_class_for_content(content):
    logger = BemihoLogger(get_output_processor_class_for_content).get_logger()
    qualified_name = get_qualified_name(ScrapperOutputProcessor)
    logger.debug(f'Getting output processor ({qualified_name}) class for content {content}.')
    writer = get_class_in_module(__file__, __name__, ScrapperOutputProcessor, lambda clazz : clazz.content == content)
    if (writer == None):
        raise OutputProcessorNotFound(content)
    logger.debug(f'Output processor ({get_qualified_name(writer)}) found.')
    return writer

def get_output_processor_classes_for_content_except(not_included):
    processor_classes = get_classes_in_module(__file__, __name__, ScrapperOutputProcessor, lambda clazz : clazz != ScrapperOutputProcessor and clazz.content != not_included)
    return processor_classes