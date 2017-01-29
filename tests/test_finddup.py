from test_helper import *
import mock
from collections import namedtuple

class TestCompareFiles(unittest.TestCase):

    def stat_mock(filename):
        s = namedtuple("MockStat", ['st_size'])
        s.st_size = 100
        return s

    # Mock will always return a filesize of 100
    @mock.patch('os.stat', side_effect=stat_mock)
    def testGroupBySize(self, stat_function):
        filelist = ["file1", "file2"]
        size_hash = groupBySize(filelist)
        self.assertEqual(list(size_hash.keys()), [100])
        self.assertEqual(len(size_hash[100]), 2)

    # Mock will always return a filesize of 100, file2 as the duplicate
    @mock.patch('finddup.FileComparer.compare', return_value=["file2"])
    @mock.patch('os.stat', side_effect=stat_mock)
    def testFileComparer(self, stat_function, compare_function):
        compare_results = compareFiles(["file1", "file2"])
        self.assertEqual(compare_results, ["file2"])
