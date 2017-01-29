from test_helper import *
import io
import re
from finddup.app import *

class TestOutput(unittest.TestCase):
    def test_outputDuplicateFile(self):
        outputDest = io.StringIO()
        output = Output()
        output.printOut = outputDest
        outputDuplicateFile(('file1', 'file2'))

        # output should reflect file1 (not file2), based on order
        self.assertTrue(re.compile("file1").match( outputDest.getvalue().strip() ))
