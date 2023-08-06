import unittest
from io import TextIOWrapper, BytesIO
import sys
from shell import run
import os
from pathlib import Path

class TestStringMethods(unittest.TestCase):
    """This is the class for unit testing"""
    def setUp(self):
        self._old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

    def _output(self):
        sys.stdout.seek(0)
        return sys.stdout.read()

    def test_pwd(self):
        """testing pwd function"""
        run(['pwd'], {'pwd.py':'directory_commands'})
        self.assertEqual(str(Path.cwd())+"\n", os.path.normpath(self._output()))

    def test_tail(self):
        """testing tail function"""
        run(['tail', '-3', 'a.txt'], {'tail.py':'file_commands'})
        self.assertEqual("'a.txt': No such file"+"\n", self._output())

    def test_grep1(self):
        """testing grep function"""
        run(['grep'], {'grep.py':'file_commands'})
        self.assertEqual('Usage: grep [-n] [PATTERN] [FILE]..'+"\n", self._output())

    def test_grep2(self):
        """testing grep function"""
        run(['grep', 'g', 'testfile1.txt'], {'grep.py':'file_commands'})
        self.assertEqual('line with \'g\''+"\n\n", self._output())

    def test_grep3(self):
        """testing grep function"""
        run(['grep', '-n', 'g', 'testfile1.txt'], {'grep.py':'file_commands'})
        self.assertEqual('4:line with \'g\''+"\n\n", self._output())

    def test_grep4(self):
        """testing grep function"""
        run(['grep', '-n', 'g', 'testfile1.txt', 'testfile2.txt'], {'grep.py':'file_commands'})
        self.assertEqual('testfile1.txt:4:line with \'g\'\n\ntestfile2.txt:1:Test String\n\ntestfile2.txt:2:eaha.sgd'+"\n\n", self._output())

    def test_grep5(self):
        """testing grep function"""
        run(['grep', 'g', 'testfile1.txt', 'testfile2.txt'], {'grep.py':'file_commands'})
        self.assertEqual('testfile1.txt:line with \'g\'\n\ntestfile2.txt:Test String\n\ntestfile2.txt:eaha.sgd'+"\n\n", self._output())

    def test_mkdir1(self):
        """testing mkdir function"""
        run(['mkdir'], {'mkdir.py':'directory_commands'})
        self.assertEqual('Usage mkdir [DIRECTORY] ...\n', self._output())

    def test_mkdir2(self):
        """testing mkdir function"""
        run(['mkdir', 'test_dir'], {'mkdir.py':'directory_commands'})
        self.assertEqual(True, Path('test_dir').is_dir())

    def test_rmdir1(self):
        """testing rmdir function"""
        run(['rmdir'], {'rmdir.py':'directory_commands'})
        self.assertEqual('Usage : rmdir directory ...\n', self._output())

    def test_rmdir2(self):
        """testing rmdir function"""
        run(['rmdir', 'test_dir'], {'rmdir.py':'directory_commands'})
        self.assertEqual(False, Path('test_dir').is_dir())

    def test_cat(self):
        """testing cat function"""
        run(['cat'], {'cat.py':'file_commands'})
        self.assertEqual('Usage: cat [FILE] ..\n', self._output())

    def test_cat2(self):
        """testing cat function"""
        run(['cat', 'testfile1.txt'], {'cat.py':'file_commands'})
        self.assertEqual('ae\n\nbbe\n\nahee\n\nline with \'g\'\n\nlakhdes\n', self._output())

    def test_head(self):
        run(['head', '-3', 'a.txt'], {'head.py':'file_commands'})
        self.assertEqual("'a.txt': No such file"+"\n",self._output()) 

    def test_sizeof1(self):
        """testing sizeof function"""
        run(['sizeof','file_commands/sizeof.py'],{'sizeof.py':'file_commands'})
        self.assertEqual('511 bytes'+'\n',self._output())
    
    def test_sizeof2(self):
        """testing sizeof function"""
        run(['sizeof'],{'sizeof.py':'file_commands'})
        self.assertEqual('Usage: sizeof [FILE]'+'\n',self._output())

    def test_sizeof3(self):
        """testing sizeof function"""
        run(['sizeof','testforsizeof'],{'sizeof.py':'file_commands'})
        self.assertEqual('testforsizeof :doesnt exist'+'\n',self._output())

unittest.main()
