"""Engine
"""

from snipping.utils import importutil

DRIVER_MODULE = {'python': 'snipping.py_driver.PyDriver'}


class Engine(object):

    def __init__(self, driver='python', from_file=None):
        self.driver = importutil.import_class(DRIVER_MODULE[driver])(
            from_file=from_file)

    def contents(self):
        return self.driver.contents()

    def execute(self, snippet):
        return self.driver.execute(snippet)

    def compile(self, snippet):
        return self.driver.compile(snippet)

    def indent(self, prev_line):
        return self.driver.indent(prev_line)
