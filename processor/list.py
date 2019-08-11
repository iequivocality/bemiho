from os.path import join, exists, isdir
import os, shutil

from logger import BemihoLogger
from .base import BemihoProcessor

from json_extractor.reader import JSONExtractor
from json_extractor.mapper import GroupJSONObjectMapper, MemberJSONObjectMapper

class BemihoDataOptionsProcessor(BemihoProcessor):
    def __init__(self, user_input):
        super().__init__(user_input)

    def start(self):
        extractor = JSONExtractor('index/index.idols', GroupJSONObjectMapper())
        group_data = extractor.extract()
        for group in group_data:
            print(f'({group.index}) {group.romaji} - {group.kanji}')
            extractor = JSONExtractor(f'index/{group.index_file}', MemberJSONObjectMapper())
            member_data = extractor.extract()
            for member in member_data:
                print(f'    ({member.index}) {member.romaji} - {member.kanji}')