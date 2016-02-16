"""Main
"""

import sys

from snipping import application
from snipping import prompt_toolkit


def main():
    init_file = None
    if len(sys.argv) > 1:
        init_file = sys.argv[1]
    app = application.get_application(init_file=init_file)

    return prompt_toolkit.run(app)
