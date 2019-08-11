import os, shutil
from os.path import join, exists, isdir

import logging

IMAGE_MIME_TYPE = 'image/'

VALID_PHOTO_EXTENSIONS = ['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr']

def create_directory(directory_path):
    try:
        if (not exists(directory_path)):
            os.mkdir(directory_path)
        else:
            pass
    except OSError:
        pass