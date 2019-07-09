
import os
import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module

from os.path import join, exists
import json

from json_extractor.reader import JSONExtractor
from json_extractor.mapper import JSONObjectMapper

from logger import BemihoLogger
from utilities.reflect import get_qualified_name

from .exceptions import MetadataHandlerNotFound

class Metadata:
    def to_json(self):
        return self.__dict__

class EmptyMapper(JSONObjectMapper):
    def map_to_object(self, data):
        return {}

class MetadataHandler:
    content = ''
    def __init__(self, user_input, metadata_directory):
        self.user_input = user_input
        self.metadata_directory = metadata_directory
        self.metadata_file = join(metadata_directory, 'metadata.json')
        self.mapper = self.create_mapper()
        self.metadata = {}

    def create_mapper(self):
        return EmptyMapper()

    def load_metadata(self):
        if (exists(self.metadata_file)):
            md_extractor = JSONExtractor(self.metadata_file, self.mapper)
            self.metadata = md_extractor.extract()
        else:
            self.metadata = {}
            with open(self.metadata_file, "w") as write_file:
                json.dump(self.metadata, write_file)

    def check_duplicates(self, header, content):
        raise NotImplementedError()

    def build_content_object_from_data(self, **kwargs):
        raise NotImplementedError()

    def add_success_to_metadata(self, header, content):
        raise NotImplementedError()

    def add_unsuccess_to_metadata(self, header, content):
        raise NotImplementedError()

    def save_metadata(self):
        json_metadata = []
        for md in list(self.metadata.values()):
            json_metadata.append(md.to_json())
        with open(self.metadata_file, "w") as write_file:
            json.dump(json_metadata, write_file, indent=4, ensure_ascii=False)

    def repair_metadata(self):
        raise NotImplementedError()

def get_metadata_class_for_content(content):
    logger = BemihoLogger(get_metadata_class_for_content).get_logger()
    qualified_name = get_qualified_name(MetadataHandler)
    logger.debug(f'Getting metadata handler ({qualified_name}) class for content {content}.')
    writer = None
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module('.' + name, package=__name__)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, MetadataHandler) and attribute.content == content:
                writer = attribute
    if (writer == None):
        raise MetadataHandlerNotFound(content)
    logger.debug(f'Output processor ({get_qualified_name(writer)}) found.')
    return writer