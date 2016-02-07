"""Wrappers for prompt toolkit
"""

from prompt_toolkit import application
from prompt_toolkit import buffer as buf
from prompt_toolkit import enums
from prompt_toolkit import interface
from prompt_toolkit import keys
from prompt_toolkit import shortcuts
from prompt_toolkit.key_binding import manager
from prompt_toolkit.layout import containers
from prompt_toolkit.layout import controls
from prompt_toolkit.layout import dimension
from prompt_toolkit.layout import lexers
from prompt_toolkit.layout import margins
from prompt_toolkit.layout import processors

from pygments import token
from pygments import lexers as pygments_lexers

Line = token.Token.Line
Title = token.Token.Title

Application = application.Application


def dimension_factory(*dim):
    if len(dim) == 1:
        return dimension.LayoutDimension.exact(*dim)
    return dimension.LayoutDimension(*dim)


def horizontal_line(*width_range):
    return containers.Window(height=dimension_factory(1),
                             width=dimension_factory(*width_range),
                             content=controls.FillControl('-', token=Line))


def vertical_line(*height_range):
    return containers.Window(height=dimension_factory(*height_range),
                             width=dimension_factory(1),
                             content=controls.FillControl('|', token=Line))


def title_token_factory(titles):
    title_token = [(Title, ' %s ' % title) for title in titles]

    def tokens(cli):
        return title_token

    return tokens


_KEY_BINDING_MANAGERS = {}


def key_binding_manager(name='default'):
    global _KEY_BINDING_MANAGERS
    return _KEY_BINDING_MANAGERS.setdefault(name, manager.KeyBindingManager())


def key_bindings_registry(key, handler):
    kbm = key_binding_manager()
    key_cls = getattr(keys.Keys, key)

    @kbm.registry.add_binding(key_cls, eager=True)
    def _(event):
        handler(event)


def tab_handler(private=None):
    def handler(event):
        b = event.cli.current_buffer
        b.insert_text('    ')
        if private is not None:
            private(event.cli.application)
    return handler


def exit_handler(private=None):
    def handler(event):
        event.cli.set_return_value(None)
        if private is not None:
            private(event.cli.application)
    return handler


def enter_handler(private=None):
    def handler(event):
        buf = event.cli.current_buffer

        while buf.document.current_line_after_cursor:
            buf.cursor_right()
        current_line = buf.document.current_line
        leading_space_len = len(current_line) - len(current_line.lstrip())
        trailing_space_len = len(current_line) - len(current_line.rstrip())
        buf.delete_before_cursor(trailing_space_len)
        buf.insert_text('\n')
        buf.insert_text(' ' * leading_space_len)

        if private is not None:
            private(event.cli.application)
    return handler


def window_rows(windows):
    return containers.HSplit(windows)


def window_columns(windows):
    return containers.VSplit(windows)


def normal_text_window(name=enums.DEFAULT_BUFFER, lang=None, lineno=False,
                       leading_space=False, trailing_space=False,
                       width=None, height=None):
    bf_attrs = {'buffer_name': name}
    if lang is not None:
        bf_attrs['lexer'] = lexers.PygmentsLexer(pygments_lexers.PythonLexer)
    input_processors = []
    if leading_space:
        input_processors.append(processors.ShowLeadingWhiteSpaceProcessor())
    if trailing_space:
        input_processors.append(processors.ShowTrailingWhiteSpaceProcessor())
    if input_processors:
        bf_attrs['input_processors'] = input_processors

    win_attrs = {}
    left_margins = []
    if lineno:
        left_margins.append(margins.NumberredMargin(name))
    if left_margins:
        win_attrs['left_margins'] = left_margins

    if height is not None:
        win_attrs['height'] = height
    if width is not None:
        win_attrs['width'] = width

    return containers.Window(content=controls.BufferControl(**bf_attrs),
                             **win_attrs)


def horizontal_tokenlist_window(tokens, align='left'):
    tlc_attrs = {}
    if align == 'center':
        tlc_attrs['align_center'] = True
    if align == 'right':
        tlc_attrs['align_right'] = True
    return containers.Window(
        height=dimension_factory(1),
        content=controls.TokenListControl(title_token_factory(tokens),
                                          **tlc_attrs))


def buffer_map(name=enums.DEFAULT_BUFFER):
    return {name: buf.Buffer(is_multiline=True)}


def get_content(app, name=enums.DEFAULT_BUFFER):
    return app.buffers[name].text


def set_content(app, name=enums.DEFAULT_BUFFER, content=None):
    app.buffers[name].text = content or u""


def run(app):
    eventloop = shortcuts.create_eventloop()

    try:
        cli = interface.CommandLineInterface(application=app,
                                             eventloop=eventloop)
        cli.run()
    finally:
        eventloop.close()
