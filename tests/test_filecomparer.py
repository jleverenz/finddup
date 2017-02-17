from test_helper import *
from pyfakefs import fake_filesystem_unittest


class TestFileComparer(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_compare_no_duplicates(self):
        self.fs.CreateFile('/test/file1.txt', contents='file1')
        self.fs.CreateFile('/test/file2.txt', contents='file2')
        self.fs.CreateFile('/test/file3.txt', contents='file3')

        filelist = ['/test/file1.txt',
                    '/test/file2.txt',
                    '/test/file3.txt']
        dups = compare(filelist)
        self.assertEqual(dups, {})

    def test_compare_one_duplicate(self):
        self.fs.CreateFile('/test/file1.txt', contents='file1')
        self.fs.CreateFile('/test/file2.txt', contents='file2')
        self.fs.CreateFile('/copy/file1.txt', contents='file1')

        filelist = ['/test/file1.txt',
                    '/test/file2.txt',
                    '/copy/file1.txt']
        dups = compare(filelist)
        self.assertEqual(dups, {'/test/file1.txt': ['/copy/file1.txt']})

    def test_compare_with_multiple_matches(self):
        self.fs.CreateFile('/test/file1.txt', contents='file1')
        self.fs.CreateFile('/test/file2.txt', contents='file2')
        self.fs.CreateFile('/copy/file1.txt', contents='file1')
        self.fs.CreateFile('/other/file1.txt', contents='file1')

        filelist = ['/test/file1.txt',
                    '/test/file2.txt',
                    '/copy/file1.txt',
                    '/other/file1.txt']
        dups = compare(filelist)

        expected = {'/test/file1.txt': ['/copy/file1.txt', '/other/file1.txt']}
        self.assertEqual(dups, expected)
