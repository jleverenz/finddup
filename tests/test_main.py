from test_helper import *
from pyfakefs import fake_filesystem_unittest
from finddup.__main__ import main
import sys
import finddup


class TestMain(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_it(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')
        sys.argv = ['finddup', '/test', '--output', 'results.txt']
        main()
        finddup.output.use_default()

        # Test that the results file was created and is empty.
        with open('results.txt') as f:
            self.assertEqual(f.read().strip(), "/test/file2")
