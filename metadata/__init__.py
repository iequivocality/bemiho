
from os.path import join, exists
from json_extractor.reader import JSONExtractor

class MetadataHandler:
    def __init__(self, user_input, metadata_directory, mapper):
        self.user_input = user_input
        self.metadata_directory = metadata_directory
        self.mapper = mapper

    def parse_metadata_file(self):
        pass
        # metadata_file_path = join(self.metadata_directory, 'metadata.json')
        # if (exists(metadata_file_path)):
        #     extractor = JSONExtractor(self.metadata_directory, self.mapper)
        #     self.metadata = extractor.extract()
    
    def check_metadata_for_existence(self, data):
        return True