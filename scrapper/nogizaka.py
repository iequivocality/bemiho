from datetime import datetime
import requests

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

from scrapper import Scrapper
from scrapper.traversal import ScrapperTraversal
from scrapper.traversal.content import PhotosScrapperTraversal
from download.image import ImageBlogDownloadContent
from download.text import TextBlogDownloadContent
from download.session_img import SessionBasedImageBlogDownloadContent
from contents import BlogHeader, BlogData

class NogizakaBlogHeader(BlogHeader):
    def get_id_from_link(self, link):
        #http://blog.nogizaka46.com/miona.hori/2019/08/052085.php
        last_part = link.split('/')[-1]
        return last_part.replace('.php', '')
        # removed_prefix = link.replace('https://www.hinatazaka46.com/s/official/diary/detail/', '')
        # question_mark_index = removed_prefix.find('?')
        # return removed_prefix[0:question_mark_index]

    def format_date(self, datestring):
        #2019/08/05 18:00
        return datetime.strptime(datestring, "%Y/%m/%d %H:%M")

class NogizakaBlogTraversal(PhotosScrapperTraversal):
    code = 'photos'
    def traverse(self, header, element):
        contents = []
        for child in element.children:
            if type(child) is Tag:
                if child.name == 'p':
                    contents.extend(self.traverse(header, child))
                elif child.name == 'b':
                    contents.append(TextBlogDownloadContent(header, child.get_text()))
                elif (child.name == 'br'):
                    contents.append(TextBlogDownloadContent(header, ''))
                elif (child.name == 'a'):
                    href = child.get('href')
                    if 'http://dcimg.awalker.jp' in href:
                        contents.append(SessionBasedImageBlogDownloadContent(header, (href, 'original_image'), child))
                    else:
                        contents.append(TextBlogDownloadContent(header, f"{child.get_text()} ({href})"))
                elif (child.name == 'img'):
                    generated = self.get_generated_link(child.get('src'))
                    if (len(generated) > 0):
                        contents.append(ImageBlogDownloadContent(header, generated))
                elif (child.name == 'div' or child.name == 'span'):
                    contents.extend(self.traverse(header, child))
            elif type(child) is NavigableString:
                contents.append(TextBlogDownloadContent(header, child))
        return contents
                

class NogizakaSeparatedContent:
    def __init__(self, header_elem):
        self.header_elem = header_elem

    def set_content(self, content_elem):
        self.content_elem = content_elem

    def set_bottom(self, bottom_elem):
        self.bottom_elem = bottom_elem

    def __str__(self):
        return self.content_elem

class NogizakaContentSeparator:
    def separate_elements(self, element):
        sep_contents = []
        sep_content = None
        for child in element.children:
            if type(child) is Tag:
                if (sep_content is None and child.name == 'h1' and child.get('class')[0] == 'clearfix'):
                    sep_content = NogizakaSeparatedContent(child)
                elif (sep_content is not None and child.name == 'div' and 'entrybody' in child.get('class')):
                    sep_content.set_content(child)
                elif (sep_content is not None and child.name == 'div' and 'entrybottom' in child.get('class')):
                    sep_content.set_bottom(child)
                    sep_contents.append(sep_content)
                    sep_content = None
        return sep_contents
        

class NogizakaScrapper(Scrapper):
    code = 'Nogizaka'
    def __init__(self, user_input, page_number, traversal):
        super().__init__(user_input, page_number, NogizakaBlogTraversal())
        self.separator = NogizakaContentSeparator()

    @staticmethod
    def get_proper_page_index(page_number):
        return page_number

    def format_url(self, page_number):
        member = self.user_input.member
        group = self.user_input.group
        return f"{member.blog}?{group.pageformat}{page_number}"
    
    def start_web_scrape(self):
        contents = []
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        link = self.format_url(self.page_number)
        request = requests.get(link, headers=headers)
        print(request)
        print(link)
        soup = BeautifulSoup(request.text, 'lxml')
        container = soup.find('div', id='container')
        sheet = container.find('div', id='sheet')
        separated = self.separator.separate_elements(sheet)
        print(separated)
        for blog in separated:
            header = self.get_header(blog)
            contents.append(BlogData(header, self.traversal.traverse(header, blog.content_elem)))
        return contents

    def get_header(self, element):
        header_elem = element.header_elem
        bottom_elem = element.bottom_elem
        date = self.get_date(bottom_elem)
        author = self.get_author(header_elem)
        title_and_link = self.get_title_and_link(header_elem)
        return NogizakaBlogHeader(title_and_link['title'], date, author, title_and_link['link'], self.page_number)

    def get_title_and_link(self, header):
        heading_container = header.find('span', class_='heading')
        title_container = heading_container.find('span', class_='entrytitle')
        title_link = title_container.find('a')
        return { 'title' : title_link.get_text(), 'link' : title_link.get('href') }

    def get_author(self, header):
        heading_container = header.find('span', class_='heading')
        author_container = heading_container.find('span', class_='author')
        return author_container.get_text()

    def get_date(self, bottom):
        return bottom.get_text().split('｜')[0]