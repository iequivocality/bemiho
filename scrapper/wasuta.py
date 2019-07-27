import requests
from bs4 import BeautifulSoup

from scrapper import Scrapper
from logger import BemihoLogger
from contents import BlogHeader, BlogData
from services.lineblog import LineBlogApiCrawler
from concurrent.futures import ThreadPoolExecutor, as_completed

class WasutaScrapper(Scrapper):
    code = 'Wasuta'
    def __init__(self, user_input, page_number, traversal):
        super().__init__(user_input, page_number, traversal)
        self.logger = BemihoLogger(self.__class__).get_logger()

    @staticmethod
    def get_proper_page_index(page_number):
        return page_number - 1

    def format_url(self, page_number):
        member = self.user_input.member
        group = self.user_input.group
        return f"{member.blog}&{group.pageformat}{page_number}"

    def scrape_single_url(self, header):
        contents = []
        self.logger.debug(f'Extracting data from {header.link} for {self.code}')
        request = requests.get(header.link)
        soup = BeautifulSoup(request.text, 'lxml')
        for article in soup.find_all('article', class_='first-article'):
            article_body = article.find('div', class_='article-body')
            article_body_inner = article_body.find('div', class_='article-body-inner')
            contents = self.traversal.traverse(article_body_inner)
            self.logger.debug(f'Contents extracted from {header.link} with size {len(contents)}')
        return BlogData(header, contents)
    
    def start_web_scrape(self):
        contents = []
        futures = []
        url = self.format_url(self.page_number)
        headers = LineBlogApiCrawler(url, self.page_number, self.user_input.member.kanji).crawl_api_for_headers()
        with ThreadPoolExecutor(max_workers=5) as executor:
            for header in headers:
                futures.append(executor.submit(self.scrape_single_url, header))
            for future in as_completed(futures):
                try:
                    contents.append(future.result())
                except Exception:
                    self.logger.error("Exception occurred on thread", exc_info=True)
        return contents