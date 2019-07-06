import requests
from datetime import datetime
from bs4 import BeautifulSoup

from scrapper import Scrapper
from contents import BlogHeader, BlogData

from concurrent.futures import ThreadPoolExecutor

class KeyakizakaBlogHeader(BlogHeader):
    def format_date(self, datestring):
        #2019.5.26 00:48
        return datetime.strptime(datestring, "%Y.%m.%d")

class KeyakizakaScrapper(Scrapper):
    code = 'Keyakizaka'
    def __init__(self, user_input, page_number, traversal):
        super().__init__(user_input, page_number, traversal)

    @staticmethod
    def get_proper_page_index(page_number):
        return page_number - 1

    def format_url(self, page_number):
        member = self.user_input.member
        group = self.user_input.group
        return f"{member.blog}&{group.pageformat}{page_number}"

    def get_header(self, article):
        header_element = article.find("div", class_="innerHead")
        header_title_element = header_element.find("div", class_="box-ttl")
        header_title_heading = header_title_element.find("h3")
        header_title = header_title_heading.get_text().strip()

        info_author_element = header_title_element.find('p', class_='name')
        info_author = info_author_element.get_text().strip()

        link = self.get_blog_link(article)

        date_box = header_element.find("div", class_="box-date")
        date_box_children = date_box.find_all('time')
        date_box_string = f'{date_box_children[0].get_text()}.{date_box_children[1].get_text()}'
        return KeyakizakaBlogHeader(header_title, date_box_string, info_author, link)

    def get_blog_link(self, article):
        group = self.user_input.group
        header_element = article.find("div", class_="innerHead")
        header_title_element = header_element.find("div", class_="box-ttl")
        header_title_anchor = header_title_element.find("a")
        return f'{group.homepage}{header_title_anchor.get("href")}'
 
    def start_web_scrape(self):
        contents = []
        link = self.format_url(self.page_number)
        request = requests.get(link)
        soup = BeautifulSoup(request.text, 'lxml')
        for article in soup.find_all('article'):
            self.get_header(article)
            header = self.get_header(article)
            content = article.find("div", class_="box-article")
            contents.append(BlogData(header, self.traversal.traverse(content)))
        return contents