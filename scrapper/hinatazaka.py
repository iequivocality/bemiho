from datetime import datetime

import urllib.request
import requests
import os

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

from scrapper import Scrapper
from contents.header import BlogHeader

from concurrent.futures import ThreadPoolExecutor

class HinatazakaBlogInfo:
    def __init__(self, datestring, author):
        self.datestring = datestring
        self.author = author

class HinatazakaBlogHeader(BlogHeader):
    def format_date(self, datestring):
        #2019.5.26 00:48
        return datetime.strptime(datestring, "%Y.%m.%d %H:%M")

class HinatazakaScrapper(Scrapper):
    code = 'Hinatazaka'
    def __init__(self, user_input, traversal):
        super().__init__(user_input, traversal)

    def format_url(self, page_number):
        member = self.user_input.member
        group = self.user_input.group
        return f"{member.blog}&{group.pageformat}{page_number}"

    def get_header(self, article):
        header_element = article.find('div', class_='p-blog-article__head')
        header_title_element = header_element.find('div', class_='c-blog-article__title')
        
        header_info = self._get_header_info(header_element)
        # header_title_content = convert_nav_string_to_str(header_title_element.contents[0]),
        header_title_content = header_title_element.contents[0].strip()
        return HinatazakaBlogHeader(header_title_content, header_info.datestring, header_info.author)

    def _get_header_info(self, header):
        info_element = header.find('div', class_='p-blog-article__info')
        info_date = info_element.find('div', class_='c-blog-article__date')
        info_author = info_element.find('div', class_='c-blog-article__name')
        
        info_content = HinatazakaBlogInfo(info_date.contents[0].strip(), info_author.contents[0].strip())
        return info_content

    def read_image(self, url):
        with urllib.request.urlopen(url) as response:
            return response.read()

    def __onfinish(self):
        pass

    def execute_single_page_scrape(self, page):
        link = self.format_url(page)
        print(link)
        request = requests.get(link)
        soup = BeautifulSoup(request.text, 'lxml')
        for article in soup.find_all('div', class_='p-blog-article'):
            header = self.get_header(article)
            content = article.find('div', class_='c-blog-article__text')
            for index, image in enumerate(self.traversal.traverse(content)):
                print(image)
                # with open(os.path.join(output, f"{header.title}_{index}.jpeg"), 'wb') as f:
                #     f.write(self.read_image(image))
            # print(header)
 
    def start_web_scrape(self):
        firstpage = self.user_input.firstpage
        lastpage = self.user_input.lastpage

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for number in range(firstpage - 1, lastpage):
                futures.append(executor.submit(self.execute_single_page_scrape, number))
