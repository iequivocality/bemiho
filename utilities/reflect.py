import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module

def get_qualified_name(clazz):
    module = clazz.__module__
    if module is None or module == str.__class__.__module__:
        return clazz.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + clazz.__name__

def get_classes_in_module(module_file, module_name, clazz, predicate):
    classes = []
    for (_, name, _) in pkgutil.iter_modules([Path(module_file).parent]):
        imported_module = import_module('.' + name, package=module_name)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, clazz) and predicate(attribute):
                classes.append(attribute)
    return classes

def get_class_in_module(module_file, module_name, super_clazz, predicate):
    clazz = None
    for (_, name, _) in pkgutil.iter_modules([Path(module_file).parent]):
        imported_module = import_module('.' + name, package=module_name)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, super_clazz) and predicate(attribute):
                clazz = attribute
    return clazz
