import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module

from concurrent.futures import ThreadPoolExecutor

from scrapper.traversal import get_traversal_based_on_content_request

class Scrapper:
    code = 'Scrapper'
    def __init__(self, user_input, page_number, traversal):
        self.user_input = user_input
        self.traversal = traversal
        self.page_number = page_number

    def format_url(self, page_number):
        raise NotImplementedError()
    
    def start_web_scrape(self):
        raise NotImplementedError()

    def get_header(self):
        raise NotImplementedError()

def get_scrapper_class_based_on_input(user_input):
    scrapper = None
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module('.' + name, package=__name__)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, Scrapper) and attribute.code == user_input.group.code:
                scrapper = attribute
    return scrapper

class BemihoScrapProcessor:
    def __init__(self, user_input, output_processor_class):
        self.user_input = user_input
        self.traversal = get_traversal_based_on_content_request(user_input)
        self.scrapper_class = get_scrapper_class_based_on_input(user_input)
        self.output_processor_class = output_processor_class

    def execute_single_scraper(self, page_number):
        scrapper = self.scrapper_class(self.user_input, page_number, self.traversal)
        output_processor = self.output_processor_class(self.user_input, None)
        blog_data = scrapper.start_web_scrape()
        for blog_datum in blog_data:
            output_processor.process_blog_data(blog_datum)
            # print(content.contents)

    def start(self):
        firstpage = self.user_input.firstpage
        lastpage = self.user_input.lastpage

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for page_number in range(firstpage - 1, lastpage):
                futures.append(executor.submit(self.execute_single_scraper, page_number)) 