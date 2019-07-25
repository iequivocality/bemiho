import requests
from bs4 import BeautifulSoup

from scrapper import Scrapper
from contents import BlogHeader, BlogData
from services.lineblog import LineBlogApiCrawler

class WasutaScrapper(Scrapper):
    code = 'Wasuta'
    def __init__(self, user_input, page_number, traversal):
        super().__init__(user_input, page_number, traversal)

    @staticmethod
    def get_proper_page_index(page_number):
        return page_number - 1

    def format_url(self, page_number):
        member = self.user_input.member
        group = self.user_input.group
        return f"{member.blog}&{group.pageformat}{page_number}"
    
    def start_web_scrape(self):
        contents = []
        url = self.format_url(self.page_number)
        headers = LineBlogApiCrawler(url, self.page_number, self.user_input.member.kanji).crawl_api_for_headers()
        for header in headers:
            print(header.link)
            request = requests.get(header.link)
            soup = BeautifulSoup(request.text, 'lxml')
            for article in soup.find_all('article', class_='first-article'):
                article_body = article.find('div', class_='article-body')
                article_body_inner = article_body.find('div', class_='article-body-inner')
                contents.append(BlogData(header, self.traversal.traverse(article_body_inner)))
        return contents