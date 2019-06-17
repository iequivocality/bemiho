from pprint import pprint
from bs4 import BeautifulSoup
from extractor.json_extractor import JSONExtractor
from extractor.json_mapper import GroupJSONObjectMapper, MemberJSONObjectMapper

extractor = JSONExtractor('index/index.idols', GroupJSONObjectMapper())
for group in extractor.extract():
    print(group.code)
    member_extractor = JSONExtractor('index/' + group.index, MemberJSONObjectMapper())
    for member in member_extractor.extract():
        print(member.kanji)
