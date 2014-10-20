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
    @classmethod
    def verbose(cls, msg):
        if cls.is_verbose:
            print(msg)

    @classmethod
    def log(cls, msg):
        print(msg)

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
        for pair in pairs:
            if pair[1] in checked:
                continue
            if self.__comparitor(pair[1], pair[0]):
                duplicate_files.append((pair[1], pair[0]))
                checked.append(pair[1])
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


def outputDuplicateFile(duplicates):
    msg = duplicates[1]
    if Log.is_verbose:
        Log.verbose(duplicates[1] + " (dupe of " + duplicates[0] + ")")
    else:
        Log.log(duplicates[1])


# Return a list of files from filelist that are duplicates. For any group of
# duplicate files, all but one will be included in the list
def compareFiles(filelist):
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
