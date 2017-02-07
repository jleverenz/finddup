import io
import sys

from pyfakefs import fake_filesystem_unittest

from test_helper import *
from finddup.__main__ import main
import finddup


class TestMain(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_output_switch(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')
        sys.argv = ['finddup', '/test', '--output', 'results.txt']
        main()
        finddup.output.use_default()

        # Test that the results file was created and is empty.
        with open('results.txt') as f:
            self.assertEqual(f.read().strip(), "/test/file2")

    def test_verbose_switch(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')
        sys.argv = ['finddup', '/test', '-v']

        finddup.output.redirect("stdout.txt")
        _old_stderr = sys.stderr
        stderr_cap = io.StringIO()
        sys.stderr = stderr_cap

        main()

        finddup.output.use_default()
        sys.stderr = _old_stderr

        with open('stdout.txt') as f:
            self.assertRegex(stderr_cap.getvalue(), "^INFO:finddup:")
