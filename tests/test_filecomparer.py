from test_helper import *


class TestFileComparer(unittest.TestCase):

    @staticmethod
    def compare(file1, file2):
        return file1.split('/')[-1] == file2.split('/')[-1]

    def setUp(self):
        self.f = FileComparer()
        self.f.compareWith(self.compare)

    def testInitialization(self):
        f = FileComparer()
        self.assertEqual(f.filelist, [])

        dirs = ['dir/file1', 'dir/file2']
        f = FileComparer(*dirs)
        self.assertEqual(f.filelist, dirs)

    def testAddFiles(self):
        f = FileComparer()
        dirs = ['dir/file1', 'dir/file2']
        f.addFiles(*dirs)
        self.assertEqual(f.filelist, dirs)

    def testCompareNoDuplicates(self):
        self.f.addFiles('dir/file1', 'dir/file2', 'copy/file3')
        dups = self.f.compare()
        self.assertEqual(dups, [])

    def testCompareOneDuplicate(self):
        self.f.addFiles('dir/file1', 'dir/file2', 'copy/file1')
        dups = self.f.compare()
        self.assertEqual(dups, [('copy/file1', 'dir/file1')])

    def testCompareWithMultipleMatches(self):
        self.f.addFiles('dir/file1', 'dir/file2', 'copy/file1', 'other/file1')
        dups = self.f.compare()

        self.assertEqual(dups, [('copy/file1', 'dir/file1'),
                                ('other/file1', 'dir/file1')])
