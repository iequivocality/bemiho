from bs4 import NavigableString

def enclose_to_json_like_string(string_for_enclose):
    return '{\n' + string_for_enclose + '\n}'