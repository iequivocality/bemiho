from datetime import datetime
import requests

from contents import BlogHeader
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
            print(LineBlogHeader(row['title'], row['createdAt'], self.author, row['url'], self.page_number, row['id']))
            headers.append(LineBlogHeader(row['title'], row['createdAt'], self.author, row['url'], self.page_number, row['id']))
        return headers
