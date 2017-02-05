from pyfakefs import fake_filesystem_unittest

from test_helper import *
from finddup import output


class TestOutput(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_outputDuplicateFile(self):
        output.redirect("output.txt")
        print("a message")
        output.use_default()

        # check that output was captured
        with open('output.txt') as x:
            actual = x.read().strip()
        self.assertEqual(actual, "a message")
