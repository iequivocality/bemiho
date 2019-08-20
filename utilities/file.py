import os, shutil, mimetypes, imghdr, requests

from os.path import join, exists, isdir
from utilities.text import check_valid_url_format

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

def get_extension_for_image(image_src):
    if (check_valid_url_format(image_src)):
        mime_type = mimetypes.guess_type(image_src)
        if (mime_type[0] is not None and mime_type[0].startswith(IMAGE_MIME_TYPE)):
            return mimetypes.guess_all_extensions(mime_type[0])[-1]
        else:
            request = requests.get(image_src, allow_redirects=True)
            extension = imghdr.what(None, request.content)
            if (extension in VALID_PHOTO_EXTENSIONS):
                return f".{extension}"
    return None