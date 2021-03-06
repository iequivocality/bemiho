from datetime import datetime

import urllib.request
import requests
import os

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

from scrapper import Scrapper
from contents import BlogHeader, BlogData

from concurrent.futures import ThreadPoolExecutor

class HinatazakaBlogHeader(BlogHeader):
    def get_id_from_link(self, link):
        removed_prefix = link.replace('https://www.hinatazaka46.com/s/official/diary/detail/', '')
        question_mark_index = removed_prefix.find('?')
        return removed_prefix[0:question_mark_index]

    def format_date(self, datestring):
        return datetime.strptime(datestring, "%Y.%m.%d %H:%M")

class HinatazakaScrapper(Scrapper):
    code = 'Hinatazaka'
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
        header_element = article.find('div', class_='p-blog-article__head')
        header_title_element = header_element.find('div', class_='c-blog-article__title')

        info_element = header_element.find('div', class_='p-blog-article__info')
        info_date = info_element.find('div', class_='c-blog-article__date')
        info_author = info_element.find('div', class_='c-blog-article__name')

        link = self.get_blog_link(article)
        header_title_content = header_title_element.contents[0].strip()
        return HinatazakaBlogHeader(header_title_content, info_date.contents[0].strip(), info_author.contents[0].strip(), link, self.page_number)

    def get_blog_link(self, article):
        group = self.user_input.group
        link_element_container = article.find('div', class_='p-button__blog_detail')
        link_element = link_element_container.find('a', class_='c-button-blog-detail')
        return f"{group.homepage}{link_element.get('href')}"
 
    def start_web_scrape(self):
        contents = []
        link = self.format_url(self.page_number)
        request = requests.get(link)
        soup = BeautifulSoup(request.text, 'lxml')
        for article in soup.find_all('div', class_='p-blog-article'):
            header = self.get_header(article)
            content = article.find('div', class_='c-blog-article__text')
            contents.append(BlogData(header, self.traversal.traverse(header, content)))
        return contents