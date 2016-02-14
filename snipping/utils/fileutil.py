"""file utils
"""

import os
import six

DEFAULT_FILE_NAME = "file"


def write_content(content):
    if six.PY2:
        return content.encode('utf-8')
    return content


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
    with open(fullname, 'w') as target_file:
        target_file.write(write_content(content))
