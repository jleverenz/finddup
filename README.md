**finddup** is a Python script that searches directories for duplicate files
using the filecmp module. It will print a list of files that have duplicates in
the fileset, suitable for further action (e.g. use xargs to move/remove).

*WARNING* This is a simple script that served some immediate needs, so use it
with caution on any files/data that are important to you. Note that this script
itself will not modify anything, but using the resulting output should be done
with care.

Usage
-----

        finddup [-h] [-v] [dirs [dirs ...]]

**finddup** can be provided a list of directories. It will consider the order
of directories to be a "priority" ordering for selecting original/duplicate
pairs.  Files selected as original will be from earlier directories in the
list, and duplicates from the latter directories if possible. Note that due to
the underlying use of system 'find', that preference for original/duplicate
listing within any one directory tree is non-deterministic.

=== Examples

Find duplicates recursively in current directory:

        finddup

Find duplicates recursively across a few directories (anywhere on filesystem):

        finddup dir1 dir2 /tmp/dir3

Find duplicates, show duplicate pairs, and print a summary:

        finddup -v dir1

Get help:

        finddup --help

Development
-----------

Run unit tests:

        python -m unittest discover tests/

### TODO

* Replace find shell call with Python-only calls
* Add -0 support to list files with NULL delimiters (for xargs -0)
* Protect against duplicates found between soft/hard links
* Support operations like moving duplicates without clobbering same filenames?
* Support continuing from last known comparison across process quits
* Show percent complete progress based on bytes to diff
