from bs4 import BeautifulSoup
from json_extractor.reader import JSONExtractor
from json_extractor.mapper import GroupJSONObjectMapper, MemberJSONObjectMapper
from input.accept_input import get_user_input
from input.exceptions import JSONDataNotFound, FirstPageLargerThanLastPage, PageNumberNotDigits, InvalidContentInput
from scrapper import BemihoScrapProcessor

try:
    user_input = get_user_input()
    print(user_input)
    processor = BemihoScrapProcessor(user_input, None)
    processor.start()
except (JSONDataNotFound, PageNumberNotDigits, FirstPageLargerThanLastPage, InvalidContentInput) as e:
    print(e)

