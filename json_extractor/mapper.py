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
    def __init__(self, kanji, romaji, index, code, pageformat):
        self.kanji = kanji
        self.romaji = romaji
        self.index = index
        self.code = code
        self.pageformat = pageformat
    
    def __str__(self):
        formatted = f"    Index: {self.index}\n    Code: {self.code}\n    Kanji: {self.kanji}\n    Romaji: {self.romaji}\n    Page Format: {self.pageformat}"
        return enclose_to_json_like_string(formatted)

class GroupJSONObjectMapper(JSONObjectMapper):
    def map_to_object(self, data):
        group_data = GroupData(data['kanji'], data['romaji'], data['index'], data['code'], data['pageformat'])
        return group_data