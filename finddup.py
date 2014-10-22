#!/usr/bin/env python

import argparse
import filecmp
import itertools
import os
import subprocess
import sys

# Simple logging class to support --verbose switch
class Log():
    is_verbose = False
    of = sys.stdout

    @classmethod
    def setOutput(cls, of):
        cls.of = of

    @classmethod
    def verbose(cls, msg):
        if cls.is_verbose:
            cls.printl(msg)

    @classmethod
    def log(cls, msg):
        cls.printl(msg)

    @classmethod
    def printl(cls, msg):
        cls.of.write(msg + "\n")
        cls.of.flush()

class FileComparer:

    def __init__(self, *args):
        self.filelist = list(args)
        self.__comparitor = FileComparer.defaultComparitor

    def addFiles(self, *args):
        self.filelist += args

    def compare(self):
        checked = []
        duplicate_files = []
        pairs = itertools.combinations(self.filelist, 2)

        # For each pair, we are checking if the second is a duplicate of the
        # first. This maintains the original preference order.
        for pair in pairs:
            # Skip if the second has already been determined to be a duplicate
            if pair[1] in checked:
                continue
            if self.__comparitor(pair[1], pair[0]):
                duplicate_files.append((pair[1], pair[0])) # duplicate, and original
                checked.append(pair[1])                    # track duplicates found
        return duplicate_files

    def compareWith(self, method):
        self.__comparitor = method

    @staticmethod
    def defaultComparitor(file1, file2):
        return filecmp.cmp(file1, file2, shallow=False)

# Use the shell 'find' command to search the input list of directories
# recusrively, and generate a list of filenames.
def generateFileList(directories):
    rv = []
    for directory in directories:
        find_out = subprocess.check_output("find \"" + directory + "\" -type f -print0", shell=True)
        rv += [i for i in find_out.strip().split("\0") if len(i) > 0]  # clean up, strip
    return rv

# Create a dict, where file size is the key, and a list of files of that size
# are the values, for all files provided in filelist.
def groupBySize(filelist):
    size_hash = {}
    for filename in filelist:
        size = os.stat(filename).st_size
        if(size in size_hash):
            size_hash[size].append(filename)
        else:
            size_hash[size] = [filename]
    return size_hash


# duplicate_original is a tuple with the duplicate listed first
def outputDuplicateFile(duplicates):
    if Log.is_verbose:
        Log.verbose(duplicates[0] + " (dupe of " + duplicates[1] + ")")
    else:
        Log.log(duplicates[0])


# Return a list of files from filelist that are duplicates. For any group of
# duplicate files, all but one will be included in the list
def compareFiles(filelist):
    # Hash by file size and create files_to_compare, a list of lists of files
    # with the same size.
    sizegroup = groupBySize(filelist)
    files_to_compare = [i[1] for i in sizegroup.iteritems() if len(i[1]) > 1]

    duplicate_files = []
    for i in files_to_compare:
        f = FileComparer(*i)
        dupes = f.compare()
        duplicate_files += dupes
        for i in dupes:
            outputDuplicateFile(i)
    return duplicate_files
