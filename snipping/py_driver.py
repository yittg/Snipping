"""PyDriver
"""

from snipping import driver
from snipping.utils import executil


class PyDriver(driver.DriverBase):

    def __init__(self):
        self.fields = ['RESULT', 'GLOBALS']

    def contents(self):
        return self.fields

    def execute(self, snippet):
        output, globals_text = executil.execwrap(snippet)
        return {'RESULT': output,
                'GLOBALS': globals_text}

    def newline(self):
        pass
