"""snipping.prompt_toolkit.buffers

wrappers for buffers
"""

from prompt_toolkit import enums
from prompt_toolkit import buffer as pt_buffer
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
        bm.update({DEFAULT_BUFFER: pt_buffer.Buffer(
            is_multiline=True, initial_document=init_doc)})
    if bm is not None:
        bm.update(dict([(b, pt_buffer.Buffer(
            is_multiline=True, read_only=True)) for b in buffers]))
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
    buf = app.buffers.get(name, None)
    if buf.read_only():
        display = "- %s -" % display
    return display, buf.read_only()


def prev_line(buf):
    text_before = buf.document.text_before_cursor.split('\n')
    if len(text_before) > 1:
        return text_before[-2]
    return None


def next_line(buf):
    text_after = buf.document.text_after_cursor.split('\n')
    if len(text_after) > 1:
        return text_after[1]
    return None


def leading_space(buf):
    return buf.document.leading_whitespace_in_current_line


def strip_trailing_space(buf):
    current_line = buf.document.current_line
    after_cursor_len = len(buf.document.current_line_after_cursor)
    trailing_space_len = len(current_line) - len(current_line.rstrip())
    buf.cursor_left(max(trailing_space_len - after_cursor_len, 0))
    after_cursor_len = len(buf.document.current_line_after_cursor)
    buf.cursor_right(max(after_cursor_len - trailing_space_len, 0))
    buf.delete(trailing_space_len)
    buf.cursor_left(max(after_cursor_len - trailing_space_len, 0))


def indent(buf, indent_text=None):
    buf.insert_text(indent_text or u"    ")
