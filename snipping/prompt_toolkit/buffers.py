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
        bm.update(dict([(b, buf.Buffer(is_multiline=True,
                                       read_only=True)) for b in buffers]))
    return buffer_mapping.BufferMapping(bm)


def get_content(app, name=DEFAULT_BUFFER):
    return app.buffers[name].text


def set_content(app, name=DEFAULT_BUFFER, content=None):
    if content is None:
        return
    app.buffers[name].set_document(document.Document(content or u"", 0),
                                   bypass_readonly=True)


def next_buffer(buffer_list, curr):
    buffer_list = buffer_list + [DEFAULT_BUFFER]
    if curr not in buffer_list:
        return buffer_list[0]
    return buffer_list[(buffer_list.index(curr) + 1) % len(buffer_list)]


def buffer_display(app, name):
    display = app.buffer_display(name).upper()
    buffer = app.buffers.get(name, None)
    if buffer.read_only():
        display = "- %s -" % display
    return display, buffer.read_only()
