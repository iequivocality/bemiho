from pprint import pprint
from bs4 import BeautifulSoup
from extractor.json_extractor import JSONExtractor
from extractor.json_mapper import GroupJSONObjectMapper, MemberJSONObjectMapper

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--group", help="Select group to pull")
parser.add_argument("-m", "--member", help="Select member to pull")
parser.add_argument("-o", "--output", help="Output folder", default="output")
parser.add_argument("-c", "--content", help="Content to pull for member", choices=['photos', 'blog'])
parser.add_argument("-f", "--firstpage", help="First page", default=1)
parser.add_argument("-l", "--lastpage", help="Last page", default=1)
args = parser.parse_args()
print(args)

group_extractor = JSONExtractor('index/index.idols', GroupJSONObjectMapper())
extracted_groups = group_extractor.extract()
if (args.group == None):
    print("No group")
    print("Available groups:")
    for index, group in enumerate(extracted_groups):
        print(f"({index + 1}) {group.romaji} - {group.kanji}")
    group_input = input("Please select group: ")
else:
    group_arg = args.group
    selected_group = None
    for group in extracted_groups:
        if (group.kanji == group_arg or group.romaji == group_arg or group.code == group_arg):
            selected_group = group
    if (selected_group != None):
        member_extractor = JSONExtractor('index/' + group.index, MemberJSONObjectMapper())
        for member in member_extractor.extract():
            print(member.kanji)
    else:
        print("Group not available on Bemiho's index")


extractor = JSONExtractor('index/index.idols', GroupJSONObjectMapper())
for group in extractor.extract():
#     print(group.code)
    member_extractor = JSONExtractor('index/' + group.index, MemberJSONObjectMapper())
#     for member in member_extractor.extract():
        # print(member.kanji)
