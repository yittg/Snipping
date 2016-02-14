import six

from snipping.utils import strutil


class TestEnsureText(object):

    def setup(self):
        self.number = 10
        self.string = "something"
        self.text = u"something"

    def test_ensure_text(self):
        result = strutil.ensure_text(self.string)
        assert isinstance(result, six.text_type)

    def test_ensure_text_non_str(self):
        result = strutil.ensure_text(self.number)
        assert result is self.number

    def test_ensure_text_already(self):
        result = strutil.ensure_text(self.text)
        assert isinstance(result, six.text_type)
        assert result is self.text
