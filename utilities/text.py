import re

from os.path import sep
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

def check_valid_url_format(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None