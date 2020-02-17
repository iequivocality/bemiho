from scrapper import Scrapper
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from contents import BlogHeader, BlogData

class AmebloBlogHeader(BlogHeader):
    def __init__(self, id, title, datestring, author, link, page):
        super().__init__(title, datestring, author, link, page)
        self.id = id

    def get_id_from_link(self, link):
        return ''

    def format_date(self, datestring):
        # return datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S")
        return datetime.now()

class AmebloSingleEntryService:
    def __init__(self, user_input, entry, page_number):
        self.user_input = user_input
        self.entry = entry
        self.page_number = page_number

    def get_header(self, article):
        header_container = article.find('div', class_='skin-entryHead')
        header_title_anchor = header_container.find('a', class_='skinArticleTitle')
        # header_date_container = header_container.find('p', attrs={ 'data-uranus-component' : 'entryDate' })
        print('someting', self.entry.find('div', attrs={ 'data-uranus-component' : 'entryItemMeta' }))
        header_date = self.entry.find('p', attrs={ 'data-uranus-component' : 'entryItemDatetime' })
        print('time', header_date)
        header_author = header_container.find('a', attrs={'rel' : 'tag' })
        # print(header_title_anchor.get_text().strip())
        # print(article.get('data-unique-entry-id'))
        # header_date.get_text().strip()
        return AmebloBlogHeader(article.get('data-unique-entry-id'), header_title_anchor.get_text().strip(), '', 'header_author.get_text().strip()', header_title_anchor.get('href'), self.page_number)

    def get_blog_link(self, article):
        pass

    def serve_contents(self):
        entry_title_container = self.entry.find('h2', attrs={'data-uranus-component' : 'entryItemTitle' })
        group = self.user_input.group
        title_anchor = entry_title_container.find('a')
        article_url = group.homepage + title_anchor.get('href')

        contents = []
        request = requests.get(article_url)
        print(article_url)
        soup = BeautifulSoup(request.text, 'lxml')
        article = soup.find('article', class_='skin-entry')
        header = self.get_header(article)
        print(header)
        return contents