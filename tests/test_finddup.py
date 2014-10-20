import unittest

from finddup import FileComparer

class TestFileComparer(unittest.TestCase):
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

    @staticmethod
    def compare(file1, file2):
        return file1.split('/')[-1] == file2.split('/')[-1]

    def testCompareNoDuplicates(self):
        f = FileComparer('dir/file1', 'dir/file2', 'copy/file3')
        f.compareWith(self.compare)
        dups = f.compare()
        self.assertEqual(dups, [])

    def testCompareOneDuplicate(self):
        f = FileComparer('dir/file1', 'dir/file2', 'copy/file1')
        f.compareWith(self.compare)
        dups = f.compare()
        self.assertEqual(dups, [('copy/file1', 'dir/file1')])

    # Need to flip -- first found is kept, duplicates are collected

    def testCompareWithMultipleMatches(self):
        f = FileComparer('dir/file1', 'dir/file2', 'copy/file1', 'other/file1')
        f.compareWith(self.compare)
        dups = f.compare()
        self.assertEqual(dups, [('copy/file1', 'dir/file1'), ('other/file1', 'dir/file1')])

if __name__ == '__main__':
    unittest.main()
