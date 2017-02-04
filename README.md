**finddup** is a Python3 script that searches directories for duplicate files
using the filecmp module. It will print a list of files that have duplicates in
the fileset, suitable for further action (e.g. use xargs to move/remove).

**WARNING** This should be considered _alpha_ software. Use it with caution on
any files/data that are important to you. Note that this script itself will not
modify anything, but using the resulting output should be done with care.

Usage
-----

        finddup [-h] [-v] [dirs [dirs ...]]

**finddup** can be provided a list of directories. It will consider the order
of directories to be a "priority" ordering for selecting original/duplicate
pairs.  Files selected as original will be from earlier directories in the
list, and duplicates from the latter directories if possible. Note that due to
the underlying use of os.walk, the preference for original/duplicate files in
any one directory tree is arbitrary.

=== Examples

Find duplicates recursively in current directory:

        finddup

Find duplicates recursively across a few directories (anywhere on filesystem):

        finddup dir1 dir2 /tmp/dir3

Find duplicates, with verbose output:

        finddup -v dir1

Get help:

        finddup -h

Development
-----------

'invoke' is used for common tasks.

Environment:

        virtualenv -p python3 venv
        source ./venv/bin/activate
        pip install -r requirements.txt

Unit tests:

        invoke test

Also:

        tox
        invoke html       # sphinx docs
        invoke html -l    # sphinx-autobuild

### TODO

* Add -0 support to list files with NULL delimiters (for xargs -0)
* Protect against duplicates found between soft/hard links
* Support operations like moving duplicates without clobbering same filenames?
* Support continuing from last known comparison across process quits
* Revisit progress method to avoid up-front calcuation; consider bytes, not just file count
* Replace Output module with something more straightforward
