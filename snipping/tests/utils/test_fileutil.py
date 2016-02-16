import os
import shutil
import six

from snipping.utils import fileutil


class TestFileOps(object):

    def setup(self):
        self.old_home = six.moves.getcwd()
        self.home = os.path.realpath(os.path.join(self.old_home,
                                                  os.path.dirname(__file__),
                                                  ".unittest"))
        self.already_file = "already_file"
        self.already_dir = "already_dir"
        self.content = u"hello \u4f60\u597d"
        if not os.path.exists(self.home):
            os.mkdir(self.home)
        os.chdir(self.home)
        with open(self.already_file, 'w'):
            pass
        if not os.path.exists(self.already_dir):
                os.mkdir(self.already_dir)

    def teardown(self):
        os.chdir(self.old_home)
        shutil.rmtree(self.home)

    def _compare_content(self, filename):
        content = fileutil.read_content(filename)
        assert content == self.content

    def test_write_file(self):
        filename = "filename"
        fileutil.write_to_file(filename, self.content)
        assert os.path.exists(filename)
        self._compare_content(filename)

    def test_write_file_exist(self):
        fileutil.write_to_file(self.already_file, self.content)
        assert os.path.exists(self.already_file)
        assert os.path.exists("%s.1" % self.already_file)
        self._compare_content(self.already_file)

    def test_write_file_exist_dir(self):
        fileutil.write_to_file(self.already_dir, self.content)
        realfile = os.path.join(self.already_dir, fileutil.DEFAULT_FILE_NAME)
        assert os.path.exists(realfile)
        self._compare_content(realfile)
