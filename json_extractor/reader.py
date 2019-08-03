import json

import logging
from logger import BemihoLogger
from utilities.reflect import get_qualified_name

class JSONExtractor:
    def __init__(self, filename, mapper):
        self.filename = filename
        self.mapper = mapper
        self.logger = BemihoLogger(self.__class__, logging.INFO).get_logger()
    
    def extract(self):
        items = []
        self.logger.debug(f'Extracting data from {self.filename} with the mapper {get_qualified_name(self.mapper.__class__)}.')
        with open(self.filename) as jsonfile:
            data = json.load(jsonfile)
            for d in data:
                items.append(self.mapper.map_to_object(d))
        self.logger.debug(f'Data successfully extracted from {self.filename} with {len(items)} items.')
        return items