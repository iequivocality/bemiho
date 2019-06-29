from utilities.text import enclose_to_json_like_string

class JSONObjectMapper:
    def map_to_object(self, data):
        return None

class MemberData:
    def __init__(self, blog, kanji, romaji, kana, index):
        self.blog = blog
        self.kanji = kanji
        self.romaji = romaji
        self.kana = kana
        self.index = index
    
    def __str__(self):
        formatted = f"    Blog: {self.blog}\n    Kanji: {self.kanji}\n    Romaji: {self.romaji}\n    Kana: {self.kana}\n    Index: {self.index}"
        return enclose_to_json_like_string(formatted)

class MemberJSONObjectMapper(JSONObjectMapper):
    def map_to_object(self, data):
        member_data = MemberData(data['blog'], data['kanji'], data['romaji'], data['kana'], data['index'])
        return member_data

class GroupData:
    def __init__(self, kanji, romaji, index_file, code, pageformat, index):
        self.kanji = kanji
        self.romaji = romaji
        self.index_file = index_file
        self.code = code
        self.pageformat = pageformat
        self.index = index
    
    def __str__(self):
        formatted = f"    Index File: {self.index_file}\n    Code: {self.code}\n    Kanji: {self.kanji}\n    Romaji: {self.romaji}\n    Page Format: {self.pageformat}\n    Index: {self.index}"
        return enclose_to_json_like_string(formatted)

class GroupJSONObjectMapper(JSONObjectMapper):
    def map_to_object(self, data):
        group_data = GroupData(data['kanji'], data['romaji'], data['index_file'], data['code'], data['pageformat'], data['index'])
        return group_data