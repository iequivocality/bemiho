from datetime import datetime

import requests

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

from scrapper import Scrapper
from contents.header import BlogHeader

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
    def __init__(self, user_input):
        super().__init__(user_input)

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

    def traverse_for_photos_only(self, content):
        contents = []
        children = content.children
        for child in children:
            if type(child) is Tag:
                if child.name == 'img':
                    contents.append(child.get('src'))
                elif child.name == 'div' or child.name == 'span':
                    contents.extend(self.traverse_for_photos_only(child))
        return contents

    def traverse_for_entire_blog(self, content):
        contents = []
        children = content.children
        for child in children:
            if type(child) is NavigableString:
                # print child
                contents.append(child)
            elif type(child) is Tag:
                if child.name == 'p':
                    contents.extend(self.traverse_for_entire_blog(child))
                elif child.name == 'b':
                    contents.append(child.get_text())
                elif child.name == 'img':
                    contents.append(child.get('src'))
                elif child.name == 'br':
                    contents.append('')
                elif child.name == 'div' or child.name == 'span':
                    contents.extend(self.traverse_for_entire_blog(child))
        return contents
 
    def start_web_scrape(self):
        firstpage = self.user_input.firstpage
        lastpage = self.user_input.lastpage
        content_for_traversal = self.user_input.content
        for number in range(firstpage - 1, lastpage):
            link = self.format_url(number)
            print(link)
            request = requests.get(link)
            soup = BeautifulSoup(request.text, 'lxml')
            for article in soup.find_all('div', class_='p-blog-article'):
                header = self.get_header(article)
                content = article.find('div', class_='c-blog-article__text')
                if (content_for_traversal == 'photos'):
                    for image in self.traverse_for_photos_only(content):
                        print(image)
                # print(header)
        print(self.user_input.output)
    
