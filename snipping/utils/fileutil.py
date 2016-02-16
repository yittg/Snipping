"""file utils
"""

import os
import six

DEFAULT_FILE_NAME = "file"


def read_content(filename):
    with open(filename, 'r') as from_file:
        content = from_file.read()
        if six.PY2:
            content = content.decode('utf-8')
        return content


def write_content(filename, content):
    with open(filename, 'w') as target_file:
        if six.PY2:
            content = content.encode('utf-8')
        target_file.write(content)


def read_from_file(filename):
    fullname = os.path.abspath(filename)
    if os.path.exists(fullname) and os.path.isfile(fullname):
        return read_content(fullname)


def write_to_file(filename, content):
    fullname = os.path.abspath(filename)
    if os.path.exists(fullname):
        if os.path.isdir(fullname):
            fullname = os.path.join(fullname, DEFAULT_FILE_NAME)
        elif os.path.isfile(fullname):
            origin_file_suffix = 1
            origin_file = "%s.%d" % (fullname, origin_file_suffix)
            while os.path.exists(origin_file):
                origin_file_suffix += 1
                origin_file = "%s.%d" % (fullname, origin_file_suffix)
            os.rename(fullname, origin_file)
    directory = os.path.dirname(fullname)
    if not os.path.exists(directory):
        os.mkdir(directory)
    write_content(fullname, content)
