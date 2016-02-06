"""Application
"""

from snipping import engine
from snipping import key_bindings
from snipping import pts

HEADER = ['Snipping']
FOOTER = ['Quit: ctrl-c']


class Application(pts.Application):

    def __init__(self, **kwargs):
        self.engine = kwargs.pop('engine', None)
        super(Application, self).__init__(**kwargs)


def get_buffers(contents):
    buffers = pts.buffer_map()
    for content in contents:
        buffers.update(pts.buffer_map(content))
    return buffers


def get_screen_layout(contents):
    result_windows = []
    for content in contents:
        if result_windows:
            result_windows.append(pts.horizontal_line(40, 80))
        result_windows.append(pts.normal_text_window(
            name=content, width=pts.dimension_factory(40, 80))
        )
    result_layout = pts.window_rows(result_windows)
    editor_window = pts.normal_text_window(lang='python', lineno=True,
                                           trailing_space=True)
    main_layout = pts.window_columns([
        editor_window, pts.vertical_line(), result_layout
    ])
    screen = pts.window_rows([
        pts.horizontal_tokenlist_window(HEADER, align='center'),
        pts.horizontal_line(),
        main_layout,
        pts.horizontal_tokenlist_window(FOOTER),
    ])
    return screen


def get_application():
    app_engine = engine.Engine()
    contents = app_engine.contents()
    key_binding_manager = pts.key_binding_manager()
    return Application(engine=app_engine,
                       layout=get_screen_layout(contents),
                       buffers=get_buffers(contents),
                       key_bindings_registry=key_binding_manager.registry,
                       use_alternate_screen=True)

key_bindings.registry()
default_app = get_application()
