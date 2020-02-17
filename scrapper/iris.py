import requests
from bs4 import BeautifulSoup

from scrapper import Scrapper
from logger import BemihoLogger
from contents import BlogHeader, BlogData
from services.lineblog import LineBlogApiCrawler, LineBlogGroupService
from concurrent.futures import ThreadPoolExecutor, as_completed

from services.ameblo import AmebloSingleEntryService

class IrisScrapper(Scrapper):
    code = 'Iris'
    def __init__(self, user_input, page_number, traversal):
        super().__init__(user_input, page_number, traversal)
        self.logger = BemihoLogger(self.__class__).get_logger()

    @staticmethod
    def get_proper_page_index(page_number):
        return page_number

    def format_url(self, page_number):
        member = self.user_input.member
        page_string = "theme" + str(page_number)
        return f"{member.blog.replace('theme', page_string)}"

    def scrape_single_url(self, entry):
        service = AmebloSingleEntryService(self.user_input, entry, self.page_number)
        return service.serve_contents()
    
    def start_web_scrape(self):
        contents = []
        futures = []
        link = self.format_url(self.page_number)
        request = requests.get(link)
        soup = BeautifulSoup(request.text, 'lxml')
        archive_list = soup.find('ul', class_='skin-archiveList', attrs={'data-uranus-component' : 'archiveList'})

        with ThreadPoolExecutor(max_workers=5) as executor:
            for article in archive_list.find_all('div', attrs={'data-uranus-component' : 'entryItem'}):
                futures.append(executor.submit(self.scrape_single_url, article))
            for future in as_completed(futures):
                try:
                    contents.append(future.result())
                except Exception:
                    self.logger.error("Exception occurred on thread", exc_info=True)
        return contents