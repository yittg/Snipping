"""PyDriver
"""

from snipping import driver
from snipping.utils import executil


class PyDriver(driver.DriverBase):

    def __init__(self):
        self.fields = ['RESULT', 'GLOBALS']
        self.compiled = None
        self.err_lineno = None
        self.none_res = {'RESULT': None, 'GLOBALS': None}

    def contents(self):
        return self.fields

    def execute(self, snippet):
        if not snippet:
            return self.none_res
        if self._compile(snippet) is not None:
            return self.none_res
        output, globals_text = executil.execwrap(snippet)

        return {'RESULT': output, 'GLOBALS': globals_text}

    def _compile(self, snippet):
        try:
            self.compiled = executil.compile_text(snippet)
            self.err_lineno = None
        except SyntaxError as e:
            self.compiled = None
            self.err_lineno = e.lineno
            return self.err_lineno
        return None

    def compile(self, snippet):
        return self.err_lineno

    def newline(self):
        pass
