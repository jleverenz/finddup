from test_helper import *
import mock
from pyfakefs import fake_filesystem_unittest


class TestGeneratedFiles(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_duplicate_source_dirs(self):
        self.fs.CreateFile('/test/file.txt')

        filelist = generate_filelist(['test', 'test'])

        # should only collect file once
        self.assertEqual(filelist, ['test/file.txt'])

    def test_overlapping_subdir_sources(self):
        self.fs.CreateFile('/test/file.txt')
        self.fs.CreateFile('/test/sub/file.txt')

        # Should still only include each file once in the generated file list
        fileset = set(generate_filelist(['test/sub', 'test']))
        self.assertEqual(fileset, set(['test/file.txt', 'test/sub/file.txt']))
