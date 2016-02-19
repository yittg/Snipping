"""Application
"""

from snipping import engine
from snipping import key_bindings
from snipping import layout
from snipping import prompt_toolkit
from snipping.prompt_toolkit import buffers
from snipping.prompt_toolkit import style
from snipping.utils import fileutil


class Application(prompt_toolkit.Application):

    def __init__(self, **kwargs):
        self.engine = kwargs.pop('engine', None)
        snippet_file = kwargs.pop('snippet_file')
        if snippet_file is None:
            snippet_file = 'snippet.py'
        self.snippet_file = snippet_file
        super(Application, self).__init__(**kwargs)

    @property
    def snippet(self):
        return fileutil.base_name(self.snippet_file)

    def buffer_display(self, name):
        if name is buffers.DEFAULT_BUFFER:
            return self.snippet
        return name


def get_application(init_file=None):
    app_engine = engine.Engine()

    init_contents = {}
    if init_file is not None:
        init_content = fileutil.read_from_file(init_file)
        if init_content is not None:
            init_contents[buffers.DEFAULT_BUFFER] = init_content
    contents = app_engine.contents()
    key_binding_manager = key_bindings.registry()
    screen = layout.create_layout(contents, key_binding_manager)
    bm = buffers.get_buffer_mapping(contents, init_contents=init_contents)

    return Application(engine=app_engine,
                       snippet_file=init_file,
                       layout=screen,
                       buffers=bm,
                       style=style.default_style,
                       key_bindings_registry=key_binding_manager.registry,
                       use_alternate_screen=True)
