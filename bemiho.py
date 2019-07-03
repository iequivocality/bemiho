from bs4 import BeautifulSoup
from json_extractor.reader import JSONExtractor
from json_extractor.mapper import GroupJSONObjectMapper, MemberJSONObjectMapper
from input.accept_input import get_user_input
from input.exceptions import JSONDataNotFound, FirstPageLargerThanLastPage, PageNumberNotDigits, InvalidContentInput
from scrapper import BemihoScrapProcessor
from logger import BemihoLogger

from output_processor import get_output_processor_class_for_content

if __name__ == '__main__':
    BemihoLogger('bemiho').get_logger().debug('Starting Bemiho: the utility for Japanese idols')
    try:
        user_input = get_user_input()
        output_processor_class = get_output_processor_class_for_content(user_input.content)
        processor = BemihoScrapProcessor(user_input, output_processor_class)
        processor.start()
    except (JSONDataNotFound, PageNumberNotDigits, FirstPageLargerThanLastPage, InvalidContentInput) as e:
        pass

