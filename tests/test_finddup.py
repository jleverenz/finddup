from test_helper import *
from collections import namedtuple
from pyfakefs import fake_filesystem_unittest


class TestCompareFiles(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def testGroupBySize(self):
        self.fs.CreateFile("/test/file1", contents='abcdefg')
        self.fs.CreateFile("/test/file2", contents='1234567')
        filelist = ["/test/file1", "/test/file2"]
        size_hash = groupBySize(filelist)
        self.assertEqual(list(size_hash.keys()), [7])
        self.assertEqual(len(size_hash[7]), 2)

    def testFileComparer(self):
        self.fs.CreateFile("/test/file1", contents='abcdefg')
        self.fs.CreateFile("/test/file2", contents='abcdefg')
        filelist = ["/test/file1", "/test/file2"]

        compare_results = compareFiles(filelist)
        self.assertEqual(compare_results, [("/test/file2", "/test/file1")])
