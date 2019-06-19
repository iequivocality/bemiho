import argparse

from extractor.json_extractor import JSONExtractor
from extractor.json_mapper import GroupJSONObjectMapper, MemberJSONObjectMapper

class BemihoUserInput:
    def __init__(self, group, member, output, content, firstpage, lastpage):
        self.group = group
        self.member = member
        self.output = output
        self.content = content
        self.firstpage = firstpage
        self.lastpage = lastpage

class BemihoUserInputBuilder:
    def set_group(self, group):
        self.group = group

    def set_member(self, member):
        self.member = member

    def set_output(self, output):
        self.output = output

    def set_content(self, content):
        self.content = content

    def set_firstpage(self, firstpage):
        self.firstpage = firstpage

    def set_lastpage(self, lastpage):
        self.lastpage = lastpage

    def build(self):
        return BemihoUserInput(self.group, self.member, self.output, self.content, self.firstpage, self.lastpage)
    

def parse_system_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--group", help="Select group to pull")
    parser.add_argument("-m", "--member", help="Select member to pull")
    parser.add_argument("-o", "--output", help="Output folder", default="output")
    parser.add_argument("-c", "--content", help="Content to pull for member", choices=['photos', 'blog'])
    parser.add_argument("-f", "--firstpage", help="First page", default=1)
    parser.add_argument("-l", "--lastpage", help="Last page", default=1)
    return parser.parse_args()

def get_user_input():
    args = parse_system_args()
    print(args)

    group_extractor = JSONExtractor('index/index.idols', GroupJSONObjectMapper())
    extracted_groups = group_extractor.extract()

    user_input_build = BemihoUserInputBuilder()
    group_input = None
    if (args.group == None):
        print("Available groups:")
        for index, group in enumerate(extracted_groups):
            print(f"({index + 1}) {group.romaji} - {group.kanji}")
        group_input = input("Please select group: ")
    else:
        group_input = args.group
        # user_input_build.set_group(args.group)

    selected_group = next((group for group in extracted_groups if group.kanji == group_input or group.romaji == group_input or group.code == group_input), None)
    if (selected_group == None):
        print("Group not found on Bemiho's index.")
        quit()
    
    member_extractor = JSONExtractor('index/' + selected_group.index, MemberJSONObjectMapper())
    extracted_members = member_extractor.extract()
    
    member_input = None
    if (args.member == None):
        print("Available members:")
        for index, group in enumerate(extracted_members):
            print(f"({index + 1}) {group.romaji} - {group.kanji}")
        member_input = input("Please select member: ")
    else:
        member_input = args.member

    selected_member = next((member for member in extracted_members if member.kanji == member_input or member.romaji == member_input or member.kana == member_input), None)
    if (selected_member == None):
        print("Member not found on Bemiho's index.")
        quit()
    else:
        print(selected_member)