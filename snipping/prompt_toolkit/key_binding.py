"""snipping.prompt_toolkit.key_binding

wrappers for key bindings
"""

from prompt_toolkit import keys
from prompt_toolkit.key_binding import manager


_KEY_BINDING_MANAGERS = {
    'default': manager.KeyBindingManager(enable_vi_mode=True)}


def key_binding_manager(name='default'):
    global _KEY_BINDING_MANAGERS
    return _KEY_BINDING_MANAGERS[name]


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
