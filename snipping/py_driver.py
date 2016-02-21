"""PyDriver
"""

from snipping import driver
from snipping.utils import executil


class PyDriver(driver.DriverBase):

    def __init__(self):
        self.fields = ['RESULT', 'GLOBALS']
        self.snippet = None
        self.compiled = None
        self.err_lineno = None

    def contents(self):
        return self.fields

    def execute(self, snippet):
        if not snippet or snippet == self.snippet:
            return {}
        self.snippet = snippet
        if self._compile(self.snippet) is not None:
            return {}
        output, globals_text = executil.execwrap(self.compiled)

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

    def indent(self, prev_line):
        if prev_line.endswith(':'):
            return '    '
        return None
