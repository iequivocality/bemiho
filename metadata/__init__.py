
from os.path import join, exists
import json

from json_extractor.reader import JSONExtractor

class MetadataHandler:
    content = ''
    def __init__(self, user_input, metadata_directory, mapper):
        self.user_input = user_input
        self.metadata_directory = metadata_directory
        self.metadata_file = join(metadata_directory, 'metadata.json')
        self.mapper = mapper

    def load_metadata(self):
        if (exists(self.metadata_file)):
            md_extractor = JSONExtractor(self.metadata_file, self.mapper)
            self.metadata = md_extractor.extract()
        else:
            self.metadata = []
            with open(self.metadata_file, "w") as write_file:
                json.dump(self.metadata, write_file)

    def check_duplicates(self, header, content):
        return False

    def add_success_to_metadata(self, header, content):
        raise NotImplementedError()

    def add_unsuccess_to_metadata(self, header, content):
        raise NotImplementedError()

    def save_metadata(self):
        with open(self.metadata_file, "w") as write_file:
            json.dump(self.metadata, write_file)

    def repair_metadata(self):
        raise NotImplementedError()