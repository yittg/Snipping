"""String util
"""

import six


def ensure_text(s):
    if isinstance(s, six.string_types) and not isinstance(s, six.text_type):
        s = s.decode('utf-8')
    return s
