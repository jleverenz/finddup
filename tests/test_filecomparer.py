from test_helper import *
from pyfakefs import fake_filesystem_unittest


class TestFileComparer(fake_filesystem_unittest.TestCase):

    @staticmethod
    def compare(file1, file2):
        return file1.split('/')[-1] == file2.split('/')[-1]

    def setUp(self):
        self.setUpPyfakefs()
        self.f = FileComparer()
        self.f.compareWith(self.compare)

    def testInitialization(self):
        f = FileComparer()
        self.assertEqual(f.filelist, [])

        files = ['dir/file1', 'dir/file2']
        f = FileComparer(*files)
        self.assertEqual(f.filelist, files)

    def testAddFiles(self):
        f = FileComparer()
        files = ['dir/file1', 'dir/file2']
        f.addFiles(*files)
        self.assertEqual(f.filelist, files)

    def testCompareNoDuplicates(self):
        self.fs.CreateFile('/test/file1.txt', contents='file1')
        self.fs.CreateFile('/test/file2.txt', contents='file2')
        self.fs.CreateFile('/test/file3.txt', contents='file3')

        self.f.addFiles('/test/file1.txt',
                        '/test/file2.txt',
                        '/test/file3.txt')
        dups = self.f.compare()
        self.assertEqual(dups, [])

    def testCompareOneDuplicate(self):
        self.fs.CreateFile('/test/file1.txt', contents='file1')
        self.fs.CreateFile('/test/file2.txt', contents='file2')
        self.fs.CreateFile('/copy/file1.txt', contents='file1')

        self.f.addFiles('/test/file1.txt',
                        '/test/file2.txt',
                        '/copy/file1.txt')
        dups = self.f.compare()
        self.assertEqual(dups, [('/copy/file1.txt', '/test/file1.txt')])

    def testCompareWithMultipleMatches(self):
        self.fs.CreateFile('/test/file1.txt', contents='file1')
        self.fs.CreateFile('/test/file2.txt', contents='file2')
        self.fs.CreateFile('/copy/file1.txt', contents='file1')
        self.fs.CreateFile('/other/file1.txt', contents='file1')

        self.f.addFiles('/test/file1.txt',
                        '/test/file2.txt',
                        '/copy/file1.txt',
                        '/other/file1.txt')
        dups = self.f.compare()

        self.assertEqual(dups, [('/copy/file1.txt', '/test/file1.txt'),
                                ('/other/file1.txt', '/test/file1.txt')])
