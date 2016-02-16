"""snipping.prompt_toolkit.buffers

wrappers for buffers
"""

from prompt_toolkit import enums
from prompt_toolkit import buffer as buf
from prompt_toolkit import buffer_mapping
from prompt_toolkit import document

DEFAULT_BUFFER = enums.DEFAULT_BUFFER


def get_buffer_mapping(buffers=None, include_default=True,
                       init_contents=None):
    bm = {}
    if include_default:
        init_doc = None
        if init_contents is not None:
            content = init_contents.get(DEFAULT_BUFFER, None)
            if content:
                init_doc = document.Document(content, 0)
        bm.update({DEFAULT_BUFFER: buf.Buffer(is_multiline=True,
                                              initial_document=init_doc)})
    if bm is not None:
        bm.update(dict([(b, buf.Buffer(is_multiline=True)) for b in buffers]))
    return buffer_mapping.BufferMapping(bm)


def get_content(app, name=DEFAULT_BUFFER):
    return app.buffers[name].text


def set_content(app, name=DEFAULT_BUFFER, content=None):
    app.buffers[name].text = content or u""
