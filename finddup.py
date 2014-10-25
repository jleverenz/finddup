#!/usr/bin/env python

import argparse
import filecmp
import itertools
import os
import subprocess
import sys
import logging

from math import factorial

# Class for sending output to either stdout or an output file, based on
# configuration. This is where a list of duplicate filenames will be sent.
class Output():
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
            self.of.write(msg + "\n")
            self.of.flush()
        else:
            self.printOut.write(msg + "\n")

    def _close(self):
        if self.of:
            self.of.close()

    @staticmethod
    def log(msg):
        Output._out._log(msg)

    @staticmethod
    def close():
        Output._out._close()

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
                logging.info("Comparing ({}/{}): already identified as duplicate, skipping:".format(i,total))
                logging.info("   " + pair[1])
                logging.info("   " + pair[0])
                continue

            logging.info("Comparing ({}/{}):".format(i,total))
            logging.info("   " + pair[1])
            logging.info("   " + pair[0])
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
    Output.log(duplicates[0])


# combinations for small n,r
def nCr(n,r):
    return factorial(n) / (factorial(r) * factorial(n-r))

# Return a list of files from filelist that are duplicates. For any group of
# duplicate files, all but one will be included in the list
def compareFiles(filelist):
    logging.info(str(len(filelist)) + " files to be examined")

    # Hash by file size and create files_to_compare, a list of lists of files
    # with the same size.
    sizegroup = groupBySize(filelist)
    files_to_compare = [i[1] for i in sizegroup.iteritems() if len(i[1]) > 1]

    combinations = reduce(lambda a,i: a + nCr(len(i), 2), files_to_compare, 0)

    duplicate_files = []
    for comp_files in files_to_compare:
        logging.info("{} diffs left to complete".format(combinations))
        f = FileComparer(*comp_files)
        dupes = f.compare()
        duplicate_files += dupes
        for i in dupes:
            outputDuplicateFile(i)
        combinations -= nCr(len(comp_files), 2)
    return duplicate_files
