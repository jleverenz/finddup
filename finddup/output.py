"""
This module provides a way to redirect stdout to a file, and restore normal
stdout when done.
"""

import sys

# Module global for tracking file handle for redirected stdout.
_of = None

# Module global for tracking original stdout value for restoration.
_old_stdout = None


def redirect(filename):
    """Open `filename` for appending, and redirect stdout to it."""
    global _of, _old_stdout
    _old_stdout = sys.stdout    # store original stdout
    _of = open(filename, "w+")
    sys.stdout = _of


def use_default():
    """Close previously opened file, and restore original stdout."""
    global _of, _old_stdout
    if _of is not None:
        _of.close()
        sys.stdout = _old_stdout
