import json

class JSONExtractor:
    def __init__(self, filename, mapper):
        self.filename = filename
        self.mapper = mapper
    
    def extract(self):
        items = []
        with open(self.filename) as jsonfile:
            data = json.load(jsonfile)
            for d in data:
                items.append(self.mapper.map_to_object(d))
        return items