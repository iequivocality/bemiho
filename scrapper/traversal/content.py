import imghdr
import mimetypes
import requests
from bs4.element import Tag, NavigableString

from scrapper.traversal import ScrapperTraversal
from download.image import ImageBlogDownloadContent
from download.text import TextBlogDownloadContent
from download.no_html import NoHTMLTextBlogDownloadContent
from utilities.text import check_valid_url_format
from utilities.file import IMAGE_MIME_TYPE, VALID_PHOTO_EXTENSIONS

from scrapper.traversal import get_traversal_based_on_content_except_all
from requests.exceptions import ReadTimeout

class PhotosScrapperTraversal(ScrapperTraversal):
    content = 'photos'
    def get_generated_link(self, image_src):
        if (check_valid_url_format(image_src)):
            mime_type = mimetypes.guess_type(image_src)
            if (mime_type[0] is not None and mime_type[0].startswith(IMAGE_MIME_TYPE)):
                return image_src
            else:
                try:
                    request = requests.get(image_src, allow_redirects=True)
                    extension = imghdr.what(None, request.content)
                    if (extension in VALID_PHOTO_EXTENSIONS):
                        return f'{image_src}.{extension}'
                except ReadTimeout:
                    pass
        return None

    def traverse(self, header, element):
        contents = []
        children = element.find_all(['img', 'a'])
        for child in children:
            if type(child) is Tag:
                if child.name == 'img':
                    generated = self.get_generated_link(child.get('src'))
                    if (generated is not None):
                        contents.append(ImageBlogDownloadContent(header, generated))
                elif child.name == 'a':
                    generated = self.get_generated_link(child.get('href'))
                    if (generated is not None):
                        contents.append(ImageBlogDownloadContent(header, generated))
        return contents

class BlogScrapperTraversal(ScrapperTraversal):
    content = 'blog'
    def traverse(self, header, element):
        contents = []
        children = element.children
        for child in children:
            if type(child) is NavigableString:
                contents.append(TextBlogDownloadContent(header, child))
            elif type(child) is Tag:
                if child.name == 'p':
                    contents.extend(self.traverse(header, child))
                elif child.name == 'b':
                    contents.append(TextBlogDownloadContent(header, child.get_text()))
                elif child.name == 'img':
                    contents.append(ImageBlogDownloadContent(header, child.get('src')))
                elif child.name == 'br':
                    contents.append(TextBlogDownloadContent(header, ''))
                elif child.name == 'a':
                    href = child.get('href')
                    if check_valid_url_format(href):
                        request = requests.get(href, allow_redirects=True)
                        if (imghdr.what(None, request.content) in VALID_PHOTO_EXTENSIONS):
                            contents.append(ImageBlogDownloadContent(header, child.get('href')))
                        else:
                            contents.append(TextBlogDownloadContent(header, f"{child.get_text()} ({href})"))
                    else:
                        contents.append(TextBlogDownloadContent(header, f"{child.get_text()} ({href})"))
                elif child.name == 'div':
                    contents.extend(self.traverse(header, child))
                    contents.append(TextBlogDownloadContent(header, ''))
                elif child.name == 'span':
                    contents.extend(self.traverse(header, child))
        return contents

class NoHTMLTextBlogTraversal(ScrapperTraversal):
    content = 'no_html'
    def traverse(self, header, element):
        contents = []
        contents.append(NoHTMLTextBlogDownloadContent(header, element.get_text(strip = True)))
        return contents

class AllScrapperTraversal(ScrapperTraversal):
    content = 'all'
    def __init__(self):
        self.traversals = get_traversal_based_on_content_except_all()
    
    def traverse(self, header, element):
        contents = []
        content_object = {}
        for traversal in self.traversals:
            content_object[traversal.content] = traversal().traverse(header, element)
        contents.append(content_object)
        return contents
    