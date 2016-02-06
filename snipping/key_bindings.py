"""Key binding
"""

from snipping import pts


def enter_handler(app):
    snippet = pts.get_content(app)
    result = app.engine.execute(snippet)
    for key, val in result.items():
        pts.set_content(app, key, val)


def registry():
    pts.key_bindings_registry('Tab', pts.tab_handler())
    pts.key_bindings_registry('ControlC', pts.exit_handler())
    # Enter Key
    pts.key_bindings_registry('ControlJ', pts.enter_handler(enter_handler))
    return pts.key_binding_manager()
