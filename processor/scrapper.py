from logger import BemihoLogger
from processor import BemihoProcessor
from scrapper.traversal import get_traversal_based_on_content_request
from scrapper import get_scrapper_class_based_on_input

from concurrent.futures import ThreadPoolExecutor, as_completed

class BemihoScrapProcessor(BemihoProcessor):
    def __init__(self, user_input, output_processor_class):
        self.user_input = user_input
        self.traversal = get_traversal_based_on_content_request(user_input)
        self.scrapper_class = get_scrapper_class_based_on_input(user_input)
        
        self.output_processor = output_processor_class(user_input)
        self.logger = BemihoLogger(self.__class__).get_logger()

    def execute_single_scraper(self, page_number):
        content = self.user_input.content
        self.logger.debug(f'Starting fetch {content} for page {page_number}')
        scrapper = self.scrapper_class(self.user_input, page_number, self.traversal)
        blog_data = scrapper.start_web_scrape()
        self.output_processor.process_blog_data(blog_data)
        return page_number

    def start(self):
        group = self.user_input.group
        member = self.user_input.member
        firstpage = self.user_input.firstpage
        number_of_pages = self.user_input.number_of_pages
        content = self.user_input.content
        self.logger.debug(f'Starting scrap process for {member.kanji} ({member.romaji}) from {group.kanji} ({group.romaji}) with content {content} and {number_of_pages} page count from page {firstpage}')
        self.output_processor.create_output_directory()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            page_index = self.scrapper_class.get_proper_page_index(firstpage)
            for page_number in range(page_index, page_index + number_of_pages):
                futures.append(executor.submit(self.execute_single_scraper, page_number))
            for future in as_completed(futures):
                try:
                    data = future.result()
                    self.logger.debug(f"Successfully fetched {content} data for page {data}")
                except Exception:
                    self.logger.error("Exception occurred on thread", exc_info=True)