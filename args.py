import argparse

from extractor.json_extractor import JSONExtractor
from extractor.json_mapper import GroupJSONObjectMapper, MemberJSONObjectMapper
from user_input import BemihoUserInput, BemihoUserInputBuilder

CONTENT_CHOICES = ['photos', 'blog']

def parse_system_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--group", help="Select group to pull")
    parser.add_argument("-m", "--member", help="Select member to pull")
    parser.add_argument("-o", "--output", help="Output folder", default="output")
    parser.add_argument("-c", "--content", help="Content to pull for member", choices=CONTENT_CHOICES)
    parser.add_argument("-f", "--firstpage", help="First page", type=int)
    parser.add_argument("-l", "--lastpage", help="Last page", type=int)
    return parser.parse_args()

def group_format(index, group):
    return f"({index + 1}) {group.romaji} - {group.kanji}"

def member_format(index, member):
    return f"({index + 1}) {member.romaji} - {member.kanji}"

def ask_for_user_input_with_extracted(options, format, label):
    print(f"Available {label}s:")
    for index, option_item in enumerate(options):
        print(format(index, option_item))
    return input(f"Please select {label}: ")

def get_user_input():
    args = parse_system_args()

    group_extractor = JSONExtractor('index/index.idols', GroupJSONObjectMapper())
    extracted_groups = group_extractor.extract()

    user_input_build = BemihoUserInputBuilder()
    group_input = None
    if (args.group == None):
        group_input = ask_for_user_input_with_extracted(extracted_groups, group_format, "group")
    else:
        group_input = args.group

    selected_group = next((group for group in extracted_groups if group.kanji == group_input or group.romaji == group_input or group.code == group_input), None)
    if (selected_group == None):
        print("Group not found on Bemiho's index.")
        quit()
    user_input_build.set_group(selected_group)

    member_extractor = JSONExtractor('index/' + selected_group.index, MemberJSONObjectMapper())
    extracted_members = member_extractor.extract()
    
    member_input = None
    if (args.member == None):
        member_input = ask_for_user_input_with_extracted(extracted_members, member_format, "member")
    else:
        member_input = args.member

    selected_member = next((member for member in extracted_members if member.kanji == member_input or member.romaji == member_input or member.kana == member_input), None)
    if (selected_member == None):
        print("Member not found on Bemiho's index.")
        quit()
    user_input_build.set_member(selected_member)

    selected_content = None
    if (args.content == None):
        selected_content = input(f"Please select content to pull. Possible choices are ({', '.join(CONTENT_CHOICES)}). Default is photos: ")
        if (selected_content == None or selected_content == ''):
            selected_content = 'photos'
    else:
        selected_content = args.content

    # selected_content = input(f"Please select content to pull. Possible choices are ({', '.join(CONTENT_CHOICES)}). Default is {args.content}: ")
    if (any(selected_content == choice for choice in CONTENT_CHOICES)):
        user_input_build.set_content(args.content)
    else:
        print("Invalid content set by the user.")
        quit()
        
    select_firstpage = None
    select_lastpage = None

    if (args.firstpage == None):
        select_firstpage = input(f"Select first page. Default is 1: ")
        if (not select_firstpage.isdigit()):
            print("Page numbers have to be digits.")
            quit()
    else:
        select_firstpage = args.firstpage

    if (args.lastpage == None):
        select_lastpage = input(f"Select last page. Default is 1: ")
        if (not select_lastpage.isdigit()):
            print("Page numbers have to be digits.")
            quit()
    else:
        select_lastpage = args.lastpage

    firstpage = int(select_firstpage)
    lastpage = int(select_lastpage)
    if (firstpage > lastpage):
        print("First page cannot be larger than the last page.")
        quit()
    else:
        user_input_build.set_firstpage(firstpage)
        user_input_build.set_lastpage(lastpage)
    return user_input_build.build()