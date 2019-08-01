
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
    def __init__(self, _id):
        self.id = _id

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
        self.logger = BemihoLogger(self.__class__).get_logger()

    def create_mapper(self):
        return EmptyMapper()

    def load_metadata(self):
        if (exists(self.metadata_file)):
            md_extractor = JSONExtractor(self.metadata_file, self.mapper)
            metadata_array = md_extractor.extract()
            for metadata in metadata_array:
                self.metadata[metadata.id] = metadata
        else:
            self.metadata = {}

    def check_duplicates(self, header, content):
        raise NotImplementedError()

    def build_content_object_from_data(self, **kwargs):
        raise NotImplementedError()

    def add_to_metadata(self, header, content):
        raise NotImplementedError()

    def save_metadata(self):
        json_metadata = []
        for md in list(self.metadata.values()):
            json_metadata.append(md.to_json())
        with open(self.metadata_file, "w") as write_file:
            json.dump(json_metadata, write_file, indent=4, ensure_ascii=False)
