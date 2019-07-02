import os
from os.path import join, exists, isdir

import logging

def create_directory(directory_path):
    try:
        if (not exists(directory_path)):
            os.mkdir(directory_path)
        else:
            pass
    except OSError:
        pass