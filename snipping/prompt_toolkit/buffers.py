"""snipping.prompt_toolkit.buffers

wrappers for buffers
"""

from prompt_toolkit import enums
from prompt_toolkit import buffer as buf
from prompt_toolkit import buffer_mapping  # noqa

DEFAULT_BUFFER = enums.DEFAULT_BUFFER


def get_buffer_mapping(buffers=None, include_default=True):
    bm = {}
    if include_default:
        bm.update({DEFAULT_BUFFER: buf.Buffer(is_multiline=True)})
    if bm is not None:
        bm.update(dict([(b, buf.Buffer(is_multiline=True)) for b in buffers]))
    return buffer_mapping.BufferMapping(bm)


def get_content(app, name=DEFAULT_BUFFER):
    return app.buffers[name].text


def set_content(app, name=DEFAULT_BUFFER, content=None):
    app.buffers[name].text = content or u""
