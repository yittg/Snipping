"""snipping.prompt_toolkit

wrappers for prompt_toolkit
"""

from prompt_toolkit import shortcuts
from prompt_toolkit import interface
from prompt_toolkit import application

Application = application.Application


def run(app):
    eventloop = shortcuts.create_eventloop()

    try:
        cli = interface.CommandLineInterface(application=app,
                                             eventloop=eventloop)
        cli.run(reset_current_buffer=False)
    finally:
        eventloop.close()
