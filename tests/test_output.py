from test_helper import *
import StringIO
import re

class TestOutput(unittest.TestCase):
    def test_outputDuplicateFile(self):
        outputDest = StringIO.StringIO()
        output = Output()
        output.printOut = outputDest
        outputDuplicateFile(('file1', 'file2'))

        # output should reflect file1 (not file2), based on order
        self.assertTrue(re.compile("file1").match( outputDest.getvalue().strip() ))
