"""DriverBase
"""

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class DriverBase(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def contents(self):
        pass

    @abc.abstractmethod
    def execute(self, snippet):
        pass

    @abc.abstractmethod
    def newline(self):
        pass
