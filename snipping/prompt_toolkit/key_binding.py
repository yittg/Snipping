"""snipping.prompt_toolkit.key_binding

wrappers for key bindings
"""

from prompt_toolkit import keys
from prompt_toolkit import filters
from prompt_toolkit.key_binding import manager
from prompt_toolkit.key_binding import vi_state


_KEY_BINDING_MANAGERS = {
    'default': manager.KeyBindingManager(enable_vi_mode=True,
                                         enable_extra_page_navigation=True)}


def key_binding_manager(name='default'):
    global _KEY_BINDING_MANAGERS
    return _KEY_BINDING_MANAGERS[name]


class ViNormalMode(filters.Filter):
    def __init__(self):
        self.state = vi_state.InputMode.NAVIGATION

    def __call__(self, cli):
        kbm = key_binding_manager()
        return kbm.get_vi_state(cli).input_mode == self.state


def key_bindings_registry(key, handler, condition=None):
    kbm = key_binding_manager()
    key_cls = getattr(keys.Keys, key)

    attr = {'eager': True}
    if condition is not None:
        attr.update({'filter': condition})

    @kbm.registry.add_binding(key_cls, **attr)
    def _(event):
        handler(event)


def key_bindings_rewrite(key, handler, condition=None, origin=True):
    kbm = key_binding_manager()
    key_cls = getattr(keys.Keys, key)

    attr = {'eager': True}
    if condition is not None:
        attr.update({'filter': condition})

    origin_handlers = None
    if origin:
        origin_handlers = kbm.registry.get_bindings_for_keys((key_cls,))

    @kbm.registry.add_binding(key_cls, **attr)
    def _(event):
        # FIXME: May not a good way
        if origin_handlers is not None:
            filter_handlers = [h for h in origin_handlers
                               if h.filter(event.cli)]
            if len(filter_handlers) > 1:
                filter_handlers[-2].call(event)
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


def raw_handler(private=None):
    def handler(event):
        if private is not None:
            private(event.cli.application)
    return handler
