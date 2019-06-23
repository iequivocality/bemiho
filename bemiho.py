from bs4 import BeautifulSoup
from json_extractor.reader import JSONExtractor
from json_extractor.mapper import GroupJSONObjectMapper, MemberJSONObjectMapper
from input.accept_input import get_user_input
from input.exceptions import JSONDataNotFound, FirstPageLargerThanLastPage, PageNumberNotDigits, InvalidContentInput
from scrapper import create_scrapper_based_on_input

try:
    user_input = get_user_input()
    print(user_input)
    create_scrapper_based_on_input(user_input).start_web_scrape()
except (JSONDataNotFound, PageNumberNotDigits, FirstPageLargerThanLastPage, InvalidContentInput) as e:
    print(e)

