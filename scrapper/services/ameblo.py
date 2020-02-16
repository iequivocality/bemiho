from scrapper import Scrapper
import requests
from bs4 import BeautifulSoup

from contents import BlogHeader, BlogData

class AmebloSingleEntryService:
    def __init__(self, url):
        self.url = url

    def get_header(self, article):
        header_container = article.find('div', class_='skin-entryHead')
        header_title_anchor = header_container.find('a', class_='skinArticleTitle')
        print(header_title_anchor.get_text().strip())
        return BlogHeader(header_title_anchor.get_text().strip(), '', '', '', '')

    def get_blog_link(self, article):
        pass

    def serve_contents(self):
        contents = []
        request = requests.get(self.url)
        print(self.url)
        soup = BeautifulSoup(request.text, 'lxml')
        article = soup.find('article', class_='skin-entry')
        header = self.get_header(article)
        return contents