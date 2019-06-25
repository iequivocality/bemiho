import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module

class ScrapperTraversal:
    content = ''
    def traverse(self, element):
        raise NotImplementedError()

def get_available_content_options():
    traversal_options = []
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module('.' + name, package=__name__)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, ScrapperTraversal) and attribute.content != None:
                traversal_options.append(attribute.content)
    return traversal_options


def get_traversal_based_on_content_request(user_input):
    traversal = None
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module('.' + name, package=__name__)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, ScrapperTraversal) and attribute.content == user_input.content:
                traversal = attribute
    return traversal()