from bs4.element import Tag, NavigableString

from scrapper.traversal import ScrapperTraversal
from contents import BlogImageContent, BlogTextContent

class PhotosScrapperTraversal(ScrapperTraversal):
    content = 'photos'
    def traverse(self, element):
        contents = []
        # children = element.children
        children = element.find_all('img')
        for child in children:
            if type(child) is Tag:
                if child.name == 'img':
                    contents.append(BlogImageContent(child.get('src')))
                    # contents.append(child.get('src'))
                # elif child.name == 'div' or child.name == 'span':
                #     contents.extend(self.traverse(child))
        return contents

class BlogScrapperTraversal(ScrapperTraversal):
    content = 'blog'
    def traverse(self, element):
        contents = []
        children = element.children
        for child in children:
            if type(child) is NavigableString:
                # print child
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
                elif child.name == 'br':
                    contents.append('')
                elif child.name == 'div' or child.name == 'span':
                    contents.extend(self.traverse(child))
        return contents

# class AllScrapperTraversal(BlogScrapperTraversal):
#     content = 'all' 