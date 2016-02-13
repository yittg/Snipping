"""Main
"""

from snipping import application
from snipping import prompt_toolkit


def main():
    return prompt_toolkit.run(application.default_app)
