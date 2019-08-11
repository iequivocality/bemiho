from os.path import join, exists, isdir
import os, shutil

from logger import BemihoLogger
from .base import BemihoProcessor

from json_extractor.reader import JSONExtractor
from json_extractor.mapper import GroupJSONObjectMapper, MemberJSONObjectMapper

from utilities.collections import split_list_for_column_output, print_matrix

class BemihoDataOptionsProcessor(BemihoProcessor):
    def __init__(self, user_input):
        super().__init__(user_input)

    def start(self):
        extractor = JSONExtractor('index/index.idols', GroupJSONObjectMapper())
        group_data = extractor.extract()
        for group in group_data:
            print(f'({group.index}) {group.romaji} - {group.kanji}')
            print('    The kanji of the group and its members can also be used for -g and -m options, respectively.')
            print('    Showing only the romaji is only for formatting purposes.')
            extractor = JSONExtractor(f'index/{group.index_file}', MemberJSONObjectMapper())
            member_data = extractor.extract()
            print_matrix(split_list_for_column_output(member_data, 3), lambda member: f'({member.index}) {member.romaji}')
        
            