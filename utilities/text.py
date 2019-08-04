from os.path import sep
import re
from bs4 import NavigableString

def enclose_to_json_like_string(string_for_enclose):
    return '{\n' + string_for_enclose + '\n}'

def clean_file_name(file_path):
    processed = file_path.replace(sep, '')
    emoji_pattern = re.compile("["
            u"\U00010000-\U0010ffff"
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"  
            u"\U0001F1E0-\U0001F1FF"  
                            "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', processed)