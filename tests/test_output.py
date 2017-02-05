from pyfakefs import fake_filesystem_unittest

from test_helper import *
from finddup import output
import finddup.output


class TestOutput(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        # TODO - hack internals to reset Output. Investigate better method.
        finddup.output._of = finddup.output._old_stdout = None

    def test_output_redirection(self):
        output.redirect("output.txt")
        print("a message")
        output.use_default()

        # check that output was captured
        with open('output.txt') as x:
            actual = x.read().strip()
        self.assertEqual(actual, "a message")

    def test_double_redirect_asserts(self):
        with self.assertRaises(AssertionError):
            output.redirect("output.txt")
            output.redirect("output.txt")

    def test_output_closes_correctly(self):
        output.redirect("output.txt")
        print("a message")
        output.use_default()

        # TODO hacky way to test internals, needs investigation
        self.assertEqual(finddup.output._of, None)
