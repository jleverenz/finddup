#!/usr/bin/env python

import argparse
import filecmp
import itertools
import os
import subprocess
import sys

from math import factorial

# Simple logging class to support verbosity log levels
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
        i = 0
        total = nCr(len(self.filelist), 2)
        for pair in pairs:
            i += 1
            # Skip if the second has already been determined to be a duplicate
            if pair[1] in checked:
                Log.verbose("Comparing ({}/{}): already identified as duplicate, skipping:".format(i,total))
                Log.verbose("   " + pair[1])
                Log.verbose("   " + pair[0])
                continue

            Log.verbose("Comparing ({}/{}):".format(i,total))
            Log.verbose("   " + pair[1])
            Log.verbose("   " + pair[0])
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
    Log.log(duplicates[0])


# combinations for small n,r
def nCr(n,r):
    return factorial(n) / (factorial(r) * factorial(n-r))

# Return a list of files from filelist that are duplicates. For any group of
# duplicate files, all but one will be included in the list
def compareFiles(filelist):
    Log.verbose(str(len(filelist)) + " files to be examined")

    # Hash by file size and create files_to_compare, a list of lists of files
    # with the same size.
    sizegroup = groupBySize(filelist)
    files_to_compare = [i[1] for i in sizegroup.iteritems() if len(i[1]) > 1]

    combinations = reduce(lambda a,i: a + nCr(len(i), 2), files_to_compare, 0)

    duplicate_files = []
    for comp_files in files_to_compare:
        Log.verbose("{} diffs left to complete".format(combinations))
        f = FileComparer(*comp_files)
        dupes = f.compare()
        duplicate_files += dupes
        for i in dupes:
            outputDuplicateFile(i)
        combinations -= nCr(len(comp_files), 2)
    return duplicate_files
