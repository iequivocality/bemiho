from bs4 import BeautifulSoup
from extractor.json_extractor import JSONExtractor
from extractor.json_mapper import GroupJSONObjectMapper, MemberJSONObjectMapper
from input import get_user_input

user_input = get_user_input()
print(user_input)
