from test_helper import *
import mock
from pyfakefs import fake_filesystem_unittest


class TestGeneratedFiles(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def testDuplicateSourceDirectories(self):
        self.fs.CreateFile('/test/file.txt')

        filelist = generateFileList(['test', 'test'])

        # should only collect file once
        self.assertEqual(filelist, ['test/file.txt'])

    def testOverlappingSubDirectorySources(self):
        self.fs.CreateFile('/test/file.txt')
        self.fs.CreateFile('/test/sub/file.txt')

        # Should still only include each file once in the generated file list
        fileset = set(generateFileList(['test/sub', 'test']))
        self.assertEqual(fileset, set(['test/file.txt', 'test/sub/file.txt']))
