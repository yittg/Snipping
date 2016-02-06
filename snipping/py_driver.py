"""PyDriver
"""

from snipping import driver
from snipping.utils import executil


class PyDriver(driver.DriverBase):

    def __init__(self):
        self.fields = ['RESULT', 'LOCALS']

    def contents(self):
        return self.fields

    def execute(self, snippet):
        output, locals_text = executil.execwrap(snippet)
        return {'RESULT': output,
                'LOCALS': locals_text}

    def newline(self):
        pass
