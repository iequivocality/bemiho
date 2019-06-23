import requests

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

from scrapper import Scrapper

class HinatazakaScrapper(Scrapper):
    code = 'Hinatazaka'
    def __init__(self, user_input):
        super().__init__(user_input)

    def format_url(self, page_number):
        member = self.user_input.member
        group = self.user_input.group
        return f"{member.blog}&{group.pageformat}{page_number}"

    def _get_header(self, article):
        header_element = article.find('div', class_='p-blog-article__head')
        header_title = header_element.find('div', class_='c-blog-article__title')
        print(str(header_title.contents[0].string).strip())
        print(type(header_title.contents[0].string))
        self._get_header_info(header_element)

    def _get_header_info(self, header):
        info_element = header.find('div', class_='p-blog-article__info')
        info_date = info_element.find('div', class_='c-blog-article__date')
        info_author = info_element.find('div', class_='c-blog-article__name')

        print(str(info_date.contents[0].string).strip())
        print(str(info_author.contents[0].string).strip())
 
    def start_web_scrape(self):
        firstpage = self.user_input.firstpage
        lastpage = self.user_input.lastpage
        for number in range(firstpage - 1, lastpage):
            link = self.format_url(number)
            print(link)
            request = requests.get(link)
            soup = BeautifulSoup(request.text, 'lxml')
            for article in soup.find_all('div', class_='p-blog-article'):
                self._get_header(article)