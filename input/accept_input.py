import argparse

from json_extractor.reader import JSONExtractor
from json_extractor.mapper import GroupJSONObjectMapper, MemberJSONObjectMapper
from input.user_input import BemihoUserInput, BemihoUserInputBuilder
from input.exceptions import JSONDataNotFound, PageNumberNotDigits, InvalidContentInput, NumberOfPageShouldBeAtLeastOne

from args import parse_system_args

from scrapper.traversal import get_available_content_options

from logger import BemihoLogger

def group_format(index, group):
    return f"({group.index}) {group.romaji} - {group.kanji}"

def member_format(index, member):
    return f"({member.index}) {member.romaji} - {member.kanji}"

def ask_for_user_input_with_extracted(options, format, label):
    print(f"Available {label}s:")
    for index, option_item in enumerate(options):
        print(format(index, option_item))
    return input(f"Please select {label}: ")

def get_input_and_check_index(json_file, json_mapper, value_from_args, input_req_format, input_req_label, predicate_for_json_data):
    extractor = JSONExtractor(json_file, json_mapper())
    extracted_data = extractor.extract()

    input_value = None
    if (value_from_args == None):
        input_value = ask_for_user_input_with_extracted(extracted_data, input_req_format, input_req_label)
    else:
        input_value = value_from_args

    selected_group = next((datum for datum in extracted_data if predicate_for_json_data(datum, input_value)), None)
    if (selected_group == None):
        raise JSONDataNotFound(f"{input_req_label.title()} not found on Bemiho's index.")
    return selected_group

def get_group_input(group_from_args):
    def data_check(group, input_value):
        return group.kanji == input_value or group.romaji == input_value or group.code == input_value or group.index == input_value
    return get_input_and_check_index('index/index.idols', GroupJSONObjectMapper, group_from_args, group_format, "group", data_check)

def get_member_input(member_from_args, selected_group):
    def data_check(member, input_value):
        return member.kanji == input_value or member.romaji == input_value or member.kana == input_value or member.index == input_value
    return get_input_and_check_index('index/' + selected_group.index_file, MemberJSONObjectMapper, member_from_args, member_format, "member", data_check)

def get_page_input(page_from_args, default_value, label):
    logger = BemihoLogger(get_page_input).get_logger()
    logger.debug(f'Checking page or count from arguments {page_from_args} with default value {default_value}')
    if (page_from_args == None):
        page_input = input(f"Select {label}. Default is {default_value}: ")
        if (page_input == None or page_input == ''):
            page_input = default_value
        if (not page_input.isdigit()):
            raise PageNumberNotDigits()
    else:
        page_input = page_from_args
    return page_input

def get_user_input():
    args = parse_system_args()
    user_input_build = BemihoUserInputBuilder()

    if (args.list):
        user_input_build.set_list_mode(True)
        return user_input_build.build()

    selected_group = get_group_input(args.group)
    user_input_build.set_group(selected_group)
    user_input_build.set_member(get_member_input(args.member, selected_group))

    user_input_build.set_output(args.output)

    if (args.reset):
        user_input_build.set_reset_mode(True)
        return user_input_build.build()

    selected_content = None
    if (args.content == None):
        selected_content = input(f"Please select content to pull. Possible choices are ({', '.join(get_available_content_options())}). Default is photos: ")
        if (selected_content == None or selected_content == ''):
            selected_content = 'photos'
    else:
        selected_content = args.content

    if (any(selected_content == choice for choice in get_available_content_options())):
        user_input_build.set_content(selected_content)
    else:
        raise InvalidContentInput()

    firstpage = int(get_page_input(args.firstpage, '1', "first page"))
    number_of_pages = int(get_page_input(args.number, '1', "last page"))
    if (number_of_pages < 1):
        raise NumberOfPageShouldBeAtLeastOne()
    else:
        user_input_build.set_firstpage(firstpage)
        user_input_build.set_number_of_page(number_of_pages)

    return user_input_build.build()