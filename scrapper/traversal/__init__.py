import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module

from logger import BemihoLogger
from utilities.reflect import get_qualified_name

from .exceptions import TraversalClassNotFound

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
    logger = BemihoLogger(get_traversal_based_on_content_request).get_logger()
    qualified_name = get_qualified_name(ScrapperTraversal)
    logger.debug(f'Getting traversal method ({qualified_name}) class for content {user_input.content}.')
    traversal = None
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module('.' + name, package=__name__)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, ScrapperTraversal) and attribute.content == user_input.content:
                traversal = attribute
    if (traversal == None):
        raise TraversalClassNotFound(user_input.content)
    logger.debug(f'Traversal method ({get_qualified_name(traversal)}) found.')
    return traversal()