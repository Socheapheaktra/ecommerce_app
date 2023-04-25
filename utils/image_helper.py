import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions

def save_image(image: FileStorage, folder: str=None, name: str=None) -> str:
    """Takes FileStorage and saves it to a folder"""
    return IMAGE_SET.save(image, folder, name)

def get_path(filename: str=None, folder: str=None):
    """Take image name and folder and return full path"""
    return IMAGE_SET.path(filename, folder)

def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """Takes a filename and returns an image on any of the accepted formats."""
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None

def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """Take FileStorage and return the filename"""
    if isinstance(file, FileStorage):
        return file.filename
    return file

def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """Check our regex and return whether the string matches or not"""
    filename = _retrieve_filename(file)

    allowed_format = "|".join(IMAGES)  # "jpg|jpe|jpeg|png|gif|svg|bmp"
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    """
    This above regex represents the name of the file.
        - "^" = start, "$" = end
        - [a-zA-Z0-9] at the first bracket means that the first character of the filename can be [(a-z),(A-Z),(0-9)]
        - [a-zA-Z0-9_()-\.]* at the second bracket means that the second character of the file name can be like the first bracket but
                including symbols [_()-\.] NOTE: the backslash is for escaping the character "." and the asterisk(*) means that it
                can have more characters from there
        - finally comes the [\.({allowed_format})$], NOTE: the backslash. allowed_format is pre-defined above and the "$" means that
                it is the end of the regex
    """
    # Check filename against regex
    return re.match(regex, filename) is not None

def get_basename(file: Union[str, FileStorage]) -> str:
    """
    Return fullname of image in the path.
    e.g: get_basename('some/folder/image.jpg') returns 'image.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]

def get_extension(file: Union[str, FileStorage]) -> str:
    """
    Get file extension
    e.g: get_extension('image.jpg') returns '.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]