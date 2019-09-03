#Nogi refactor here
from logger import BemihoLogger
from utilities.reflect import get_qualified_name, get_class_in_package, get_classes_in_package
from scrapper.traversal import ScrapperTraversal
from scrapper.traversal.content import PhotosScrapperTraversal
from scrapper.traversal.exceptions import TraversalClassNotFound

from download.text import TextBlogDownloadContent
from download.image import ImageBlogDownloadContent
from download.session_img import SessionBasedImageBlogDownloadContent
from download.no_html import NoHTMLTextBlogDownloadContent

from bs4 import Tag, NavigableString

class NogizakaTraversal(ScrapperTraversal):
    pass

class NogizakaPhotosTraversal(PhotosScrapperTraversal, NogizakaTraversal):
    content = 'photos'
    def traverse(self, header, element):
        contents = []
        children = element.find_all(['img', 'a'])
        for child in children:
            if type(child) is Tag:
                if (child.name == 'a'):
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
        return contents

class NogizakaBlogTraversal(PhotosScrapperTraversal, NogizakaTraversal):
    content = 'blog'
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

class NoHTMLTextBlogTraversal(NogizakaTraversal):
    content = 'no_html'
    def traverse(self, header, element):
        contents = []
        contents.append(NoHTMLTextBlogDownloadContent(header, element.get_text(strip = True)))
        return contents

class NogiAllScrapperTraversal(NogizakaTraversal):
    content = 'all'
    def __init__(self):
        self.traversals = get_nogi_traversal_based_on_content_except_all()
    
    def traverse(self, header, element):
        contents = []
        content_object = {}
        for traversal in self.traversals:
            content_object[traversal.content] = traversal().traverse(header, element)
        #     if traversal.content not in ['blog', 'photos']:
        #         content_object[traversal.content] = traversal().traverse(header, element)
        # content_object['blog'] = NogizakaBlogTraversal().traverse(header, element)
        # content_object['photos'] = NogizakaBlogTraversal().traverse(header, element)
        contents.append(content_object)
        return contents

def get_nogi_traversal_based_on_content_except_all():
    traversals = get_classes_in_package(__name__, NogizakaTraversal, lambda clazz : clazz != NogizakaTraversal and clazz.content != 'all')
    return traversals

def get_nogi_traversal_based_on_content_request(user_input):
    logger = BemihoLogger(get_nogi_traversal_based_on_content_request).get_logger()
    qualified_name = get_qualified_name(ScrapperTraversal)
    logger.debug(f'Getting traversal method ({qualified_name}) class for content {user_input.content}.')
    traversal = get_class_in_package(__name__, NogizakaTraversal, lambda clazz : clazz.content == user_input.content)
    if (traversal == None):
        raise TraversalClassNotFound(user_input.content)
    else:
        logger.debug(f'Traversal method ({get_qualified_name(traversal)}) found.')
        return traversal()