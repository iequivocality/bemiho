import imghdr
import mimetypes
import requests
from bs4.element import Tag, NavigableString

from scrapper.traversal import ScrapperTraversal
from contents import BlogImageContent, BlogTextContent
from utilities.text import check_valid_url_format

IMAGE_MIME_TYPE = 'image/'
VALID_PHOTO_EXTENSIONS = ['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr']

class PhotosScrapperTraversal(ScrapperTraversal):
    content = 'photos'
    def image_check(self, image_src):
        if (not check_valid_url_format(image_src)):
            return (False, None)
        #Get initial from mimetypes
        mime_type = mimetypes.guess_type(image_src)
        if (mime_type[0] is not None):
            return (mime_type[0].startswith(IMAGE_MIME_TYPE), mimetypes.guess_all_extensions(mime_type[0])[-1])
        else:
            request = requests.get(image_src, allow_redirects=True)
            extension = imghdr.what(None, request.content)
            return (extension in VALID_PHOTO_EXTENSIONS, extension)

    def traverse(self, element):
        contents = []
        children = element.children
        # children = element.find_all('img')
        for child in children:
            if type(child) is Tag:
                if child.name == 'img':
                    contents.append(BlogImageContent(child.get('src')))
                elif child.name == 'a':
                    href = child.get('href')
                    checker = self.image_check(href)
                    if (checker[0]):
                        generated_link = f"{href}.{checker[1]}"
                        contents.append(BlogImageContent(generated_link))
                elif child.name == 'div' or child.name == 'span':
                    contents.extend(self.traverse(child))
        return contents

class BlogScrapperTraversal(ScrapperTraversal):
    content = 'blog'
    def traverse(self, element):
        contents = []
        children = element.children
        for child in children:
            if type(child) is NavigableString:
                # contents.append(child)
                contents.append(BlogTextContent(child))
            elif type(child) is Tag:
                if child.name == 'p':
                    contents.extend(self.traverse(child))
                elif child.name == 'b':
                    contents.append(BlogTextContent(child.get_text()))
                    # contents.append(child.get_text())
                elif child.name == 'img':
                    contents.append(BlogImageContent(child.get('src')))
                    # contents.append(child.get('src'))
                # elif child.name == 'br':
                    # contents.append(BlogTextContent(''))
                elif child.name == 'div' or child.name == 'span':
                    contents.extend(self.traverse(child))
                    contents.append(BlogTextContent(''))
        return contents

class AllScrapperTraversal(BlogScrapperTraversal):
    content = 'all' 