class JSONObjectMapper:
    def map_to_object(self, data):
        return None

class MemberData:
    def __init__(self, blog, kanji, romaji, kana):
        self.blog = blog
        self.kanji = kanji
        self.romaji = romaji
        self.kana = kana
    
    def __str__(self):
        formatted = f"    Blog: {self.blog}\n    Kanji: {self.kanji}\n    Romaji: {self.romaji}\n    Kana: {self.kana}"
        return "{\n" + formatted + "\n}"

class MemberJSONObjectMapper(JSONObjectMapper):
    def map_to_object(self, data):
        group_data = MemberData(data['blog'], data['kanji'], data['romaji'], data['kana'])
        return group_data

class GroupData:
    def __init__(self, kanji, romaji, index, code, pageformat):
        self.kanji = kanji
        self.romaji = romaji
        self.index = index
        self.code = code
        self.pageformat = pageformat
    
    def __str__(self):
        formatted = f"    Index: {self.index}\n    Code: {self.code}\n    Kanji: {self.kanji}\n    Romaji: {self.romaji}\n    Page Format: {self.pageformat}"
        return "{\n" + formatted + "\n}"

class GroupJSONObjectMapper(JSONObjectMapper):
    def map_to_object(self, data):
        group_data = GroupData(data['kanji'], data['romaji'], data['index'], data['code'], data['pageformat'])
        return group_data