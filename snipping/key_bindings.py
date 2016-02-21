"""Key binding
"""

from snipping.prompt_toolkit import key_binding
from snipping.prompt_toolkit import buffers
from snipping.utils import fileutil
from snipping.utils import strutil


def write_file_handler(app):
    snippet = buffers.get_content(app)
    filename = app.snippet_file
    fileutil.write_to_file(filename, snippet)


def next_handler(app):
    buffer_names = app.engine.contents()
    next_buf = buffers.next_buffer(buffer_names,
                                   app.buffers.current_name(None))
    app.buffers.push_focus(None, strutil.ensure_text(next_buf))


def prev_handler(app):
    bm = app.buffers
    if len(bm.focus_stack) > 1:
        bm.pop_focus(None)


def execute_handler(app):
    snippet = buffers.get_content(app)
    result = app.engine.execute(snippet)
    for key, val in result.items():
        buffers.set_content(app, key, val)


def auto_indent_handler(app):
    current_buffer = app.buffers.current(None)
    prev_line = buffers.prev_line(current_buffer)

    if prev_line is not None:
        indent_text = app.engine.indent(prev_line)
        if indent_text is not None:
            buffers.indent(current_buffer, indent_text)


REGISTER_KEYS = [('^c', 'Quit'),
                 ('^n', 'Next'),
                 ('^p', 'Prev'),
                 ('F4', 'Save')]


def registry():
    key_binding.key_bindings_registry(
        'Tab', key_binding.tab_handler())
    key_binding.key_bindings_registry(
        'ControlC', key_binding.exit_handler())
    # Enter Key
    key_binding.key_bindings_registry(
        'ControlJ', key_binding.enter_handler(auto_indent_handler))
    key_binding.key_bindings_registry(
        'ControlN',
        key_binding.raw_handler(next_handler),
        condition=key_binding.ViNormalMode())
    key_binding.key_bindings_registry(
        'ControlP',
        key_binding.raw_handler(prev_handler),
        condition=key_binding.ViNormalMode())
    key_binding.key_bindings_registry(
        'F4', key_binding.raw_handler(write_file_handler))
    key_binding.key_bindings_rewrite(
        'Escape', key_binding.raw_handler(execute_handler))
    return key_binding.key_binding_manager()
