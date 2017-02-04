import sys


class Output():
    """Class for redirecting stdout, based on configuration."""

    _out = None

    def __init__(self, **kwargs):
        self.printOut = sys.stdout
        self.of = None
        self.outputFile = None
        if 'outputFile' in kwargs:
            self.outputFile = kwargs['outputFile']
        if self.outputFile:
            self.of = open(self.outputFile, "w+")
        Output._out = self

    def _log(self, msg):
        if self.of:
            self.of.write("{}\n".format(msg))
            self.of.flush()
        else:
            self.printOut.write("{}\n".format(msg))

    def _close(self):
        if self.of:
            self.of.close()

    @staticmethod
    def log(msg):
        Output._out._log(msg)

    @staticmethod
    def close():
        if Output._out is None:
            return
        Output._out._close()
