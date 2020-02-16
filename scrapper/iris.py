import requests
from bs4 import BeautifulSoup

from scrapper import Scrapper
from logger import BemihoLogger
from contents import BlogHeader, BlogData
from scrapper.services.lineblog import LineBlogApiCrawler, LineBlogGroupService
from concurrent.futures import ThreadPoolExecutor, as_completed

class IrisScrapper(Scrapper):
    code = 'Iris'
    def __init__(self, user_input, page_number, traversal):
        super().__init__(user_input, page_number, traversal)
        self.logger = BemihoLogger(self.__class__).get_logger()

    @staticmethod
    def get_proper_page_index(page_number):
        raise NotImplementedError()
        # return page_number - 1

    def format_url(self, page_number):
        raise NotImplementedError()
        # member = self.user_input.member
        # group = self.user_input.group
        # return f"{member.blog}&{group.pageformat}{page_number}"
    
    def start_web_scrape(self):
        raise NotImplementedError()
        # url = self.format_url(self.page_number)
        # services = LineBlogGroupService(url, self.page_number, self.user_input.member.kanji, self.traversal)
        # contents = services.serve_contents()
        # return contents