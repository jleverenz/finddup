from test_helper import *
import io


class TestOutput(unittest.TestCase):
    def test_outputDuplicateFile(self):
        outputDest = io.StringIO()
        output = Output()
        output.printOut = outputDest
        Output.log("a message")

        # check that output was captured
        self.assertTrue(outputDest.getvalue().strip(), "a message")
