from bs4 import BeautifulSoup
from extractor.json_extractor import JSONExtractor
from extractor.json_mapper import GroupJSONObjectMapper, MemberJSONObjectMapper
from input.accept_input import get_user_input
from input.exceptions import JSONDataNotFound

try:
    user_input = get_user_input()
    print(user_input)
except JSONDataNotFound as e:
    print(e)

