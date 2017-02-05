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

    def test_soft_links_not_duplicates(self):
        self.fs.CreateFile("/test/file1", contents='abcdefg')
        self.fs.CreateLink("/test/file2", "/test/file1")
        filelist = generate_filelist(['test'])

        compare_results = compare_files(filelist)
        self.assertEqual(compare_results, [])

    # NOTE decision to handle hard links as non-duplicates. Not clear if user
    # would expect them to be highlighted as duplicates or not, so assume
    # something safe.
    def test_hard_links_not_duplicates(self):
        self.fs.CreateFile("/test/file1", contents='abcdefg')
        self.fs.CreateHardLink("/test/file1", "/test/file2")
        filelist = generate_filelist(['test'])

        compare_results = compare_files(filelist)
        self.assertEqual(compare_results, [])
