"""Key binding
"""

from snipping.prompt_toolkit import key_binding
from snipping.prompt_toolkit import buffers


def enter_handler(app):
    snippet = buffers.get_content(app)
    result = app.engine.execute(snippet)
    for key, val in result.items():
        buffers.set_content(app, key, val)


def registry():
    key_binding.key_bindings_registry('Tab',
                                      key_binding.tab_handler())
    key_binding.key_bindings_registry('ControlC',
                                      key_binding.exit_handler())
    # Enter Key
    key_binding.key_bindings_registry('ControlJ',
                                      key_binding.enter_handler(enter_handler))
    return key_binding.key_binding_manager()
