"""PyDriver
"""

from snipping import driver
from snipping.utils import executil


class PyDriver(driver.DriverBase):

    _inner_name = ['__name__', '__doc__', '__package__', '__builtins__']
    _fields = ['RESULT', 'GLOBALS']

    def __init__(self, from_file=None):
        self.from_file = from_file
        self.snippet = None
        self.compiled = None
        self.err_lineno = None
        super(PyDriver, self).__init__()

    def contents(self):
        return self._fields

    def execute(self, snippet):
        if not snippet or snippet == self.snippet:
            return {}
        self.snippet = snippet
        if self._compile(self.snippet) is not None:
            return {}
        output, globals_ = executil.execwrap(self.compiled,
                                             from_file=self.from_file)

        global_tuples = []
        for k, v in globals_.items():
            if k in PyDriver._inner_name:
                continue
            global_tuples.append((k, v))

        globals_text = '\n'.join([u"%s: %r" % (k, v) for k, v
                                  in sorted(global_tuples,
                                            key=lambda t: u"%r" % t[1])])
        return {'RESULT': output, 'GLOBALS': globals_text}

    def _compile(self, snippet):
        try:
            self.compiled = executil.compile_text(snippet, self.from_file)
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
