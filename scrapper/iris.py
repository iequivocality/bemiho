import requests
from bs4 import BeautifulSoup

from scrapper import Scrapper
from logger import BemihoLogger
from contents import BlogHeader, BlogData
from scrapper.services.lineblog import LineBlogApiCrawler, LineBlogGroupService
from concurrent.futures import ThreadPoolExecutor, as_completed

from scrapper.services.ameblo import AmebloSingleEntryService

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

    def scrape_single_url(self, url):
        service = AmebloSingleEntryService(url)
        return service.serve_contents()
    
    def start_web_scrape(self):
        contents = []
        futures = []
        link = self.format_url(self.page_number)
        group = self.user_input.group
        request = requests.get(link)
        soup = BeautifulSoup(request.text, 'lxml')
        archive_list = soup.find('ul', class_='skin-archiveList')

        with ThreadPoolExecutor(max_workers=5) as executor:
            for article in archive_list.find_all('li', class_='skin-borderQuiet'):
                title_container = article.find('h2', attrs={'data-uranus-component' : 'entryItemTitle' })
                title_anchor = title_container.find('a')
                article_url = group.homepage + title_anchor.get('href')
                futures.append(executor.submit(self.scrape_single_url, article_url))
            for future in as_completed(futures):
                try:
                    contents.append(future.result())
                except Exception:
                    self.logger.error("Exception occurred on thread", exc_info=True)
        return contents