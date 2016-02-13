"""Application
"""

from snipping import engine
from snipping import key_bindings
from snipping import layout
from snipping import prompt_toolkit
from snipping.prompt_toolkit import buffers
from snipping.prompt_toolkit import style


class Application(prompt_toolkit.Application):

    def __init__(self, **kwargs):
        self.engine = kwargs.pop('engine', None)
        super(Application, self).__init__(**kwargs)


def get_application():
    app_engine = engine.Engine()
    contents = app_engine.contents()
    key_binding_manager = key_bindings.registry()
    return Application(engine=app_engine,
                       layout=layout.create_layout(contents),
                       buffers=buffers.get_buffer_mapping(contents),
                       style=style.default_style,
                       key_bindings_registry=key_binding_manager.registry,
                       use_alternate_screen=True)


default_app = get_application()
