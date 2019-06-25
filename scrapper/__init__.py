import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module
from scrapper.traversal import get_traversal_based_on_content_request

class Scrapper:
    code = 'Scrapper'
    def __init__(self, user_input, traversal):
        self.user_input = user_input
        self.traversal = traversal

    def format_url(self, page_number):
        raise NotImplementedError()
    
    def start_web_scrape(self):
        raise NotImplementedError()

    def get_header(self):
        raise NotImplementedError()

def create_scrapper_based_on_input(user_input):
    scrapper = None
    traversal = get_traversal_based_on_content_request(user_input)
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module('.' + name, package=__name__)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, Scrapper) and attribute.code == user_input.group.code:
                scrapper = attribute
    return scrapper(user_input, traversal)