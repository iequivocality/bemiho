from datetime import datetime
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

from logger import BemihoLogger
from contents import BlogHeader, BlogData
from scrapper import Scrapper

class LineBlogHeader(BlogHeader):
    def __init__(self, title, createdAt, author, url, page_number, _id):
        self.id = _id
        super().__init__(title, createdAt, author, url, page_number)

    def get_id_from_link(self, link):
        return self.id

    def format_date(self, datestring):
        return datetime.utcfromtimestamp(datestring)

class LineBlogApiCrawler:
    def __init__(self, url, page_number, author):
        self.url = url
        self.page_number = page_number
        self.author = author

    def crawl_api_for_headers(self):
        headers = []
        resp = requests.get(self.url)
        data = resp.json()
        for row in data['rows']:
            headers.append(LineBlogHeader(row['title'], row['createdAt'], self.author, row['url'], self.page_number, row['id']))
        return headers

class LineBlogService:
    def __init__(self, url, page_number, author, traversal):
        self.url = url
        self.page_number = page_number
        self.author = author
        self.logger = BemihoLogger(self.__class__).get_logger()
        self.traversal = traversal

    def scrape_single_url(self, header):
        contents = []
        self.logger.debug(f'Extracting data from {header.link} from {header.author}')
        request = requests.get(header.link)
        soup = BeautifulSoup(request.text, 'lxml')
        for article in soup.find_all('article', class_='first-article'):
            article_body = article.find('div', class_='article-body')
            article_body_inner = article_body.find('div', class_='article-body-inner')
            contents = self.traversal.traverse(article_body_inner)
            self.logger.debug(f'Contents extracted from {header.link} with size {len(contents)}')
        return BlogData(header, contents)

    def serve_contents(self):
        contents = []
        futures = []
        headers = LineBlogApiCrawler(self.url, self.page_number, self.author).crawl_api_for_headers()
        self.logger.debug(f'Headers extracted from api url {self.url} with size {len(headers)}. Proceeding to fetch data.')
        with ThreadPoolExecutor(max_workers=5) as executor:
            for header in headers:
                futures.append(executor.submit(self.scrape_single_url, header))
            for future in as_completed(futures):
                try:
                    contents.append(future.result())
                except Exception:
                    self.logger.error("Exception occurred on thread", exc_info=True)
        return contents
