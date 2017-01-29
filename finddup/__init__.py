#!/usr/bin/env python

import argparse
import filecmp
import itertools
import os
import subprocess
import sys
import logging
from functools import reduce

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
        if Output._out == None:
            return
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

# Walk the input list of directories recusrively, and generate a list of
# filenames.
def generateFileList(directories):
    rv = []

    # Reminder: os.walk does not guarantee order of files in any single
    # directory. However, high level file list ordering is stable based on
    # input 'directories' order.

    # Reminder: by default, os.walk skip symlinks to directories

    for directory in directories:
        for dirName, subdirList, fileList in os.walk(directory):
            for fname in fileList:
                rv.append(os.path.join(dirName, fname))
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

# Return a list of files from filelist that are duplicates. For any group of
# duplicate files, all but one will be included in the list
def compareFiles(filelist):
    logging.info(str(len(filelist)) + " files to be examined")

    # Hash by file size and create files_to_compare, a list of lists of files
    # with the same size.
    sizegroup = groupBySize(filelist)

    # Iterate the hash size group and create a list of lists. Each list elmt is
    # a list of files with matching sizes.
    files_to_compare = [i[1] for i in sizegroup.items() if len(i[1]) > 1]

    duplicate_files = []
    for comp_files in files_to_compare:
        f = FileComparer(*comp_files)
        dupes = f.compare()
        duplicate_files += dupes

    return duplicate_files
