import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module
import traceback

from logger import BemihoLogger
from utilities.reflect import get_class_in_module

class Scrapper:
    code = 'Scrapper'
    def __init__(self, user_input, page_number, traversal):
        self.user_input = user_input
        self.traversal = traversal
        self.page_number = page_number
        
    @staticmethod
    def get_proper_page_index(page_number):
        raise NotImplementedError()

    def format_url(self, page_number):
        raise NotImplementedError()
    
    def start_web_scrape(self):
        raise NotImplementedError()

    def get_header(self, article):
        pass

    def get_blog_link(self, article):
        pass

def get_scrapper_class_based_on_input(user_input):
    scrapper = get_class_in_module(__file__, __name__, Scrapper, lambda clazz : clazz.code == user_input.group.code)
    return scrapper