from test_helper import *
from pyfakefs import fake_filesystem_unittest

import finddup


class TestRemoveHardLinkDupes(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_does_not_prune_nonhardlinks(self):
        self.fs.CreateFile("/test/file1", contents='abcdefg')
        self.fs.CreateFile("/test/file2", contents='abcdefg')
        filelist = ["/test/file1", "/test/file2"]
        removed = finddup._filter_hard_links(filelist)
        self.assertEqual(filelist, removed)

    def test_prune_hardlinks(self):
        self.fs.CreateFile("/test/file1", contents='abcdefg')
        self.fs.CreateHardLink("/test/file1", "/test/file2")
        filelist = ["/test/file1", "/test/file2"]
        removed = finddup._filter_hard_links(filelist)
        self.assertEqual(["/test/file1"], removed)
