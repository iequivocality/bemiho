def get_qualified_name(clazz):
    module = clazz.__module__
    if module is None or module == str.__class__.__module__:
        return clazz.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + clazz.__name__