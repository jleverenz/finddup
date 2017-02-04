#!/usr/bin/env python

import filecmp
import itertools
import logging
import os

logger = logging.getLogger('finddup')


def _defaultComparitor(file1, file2):
    return filecmp.cmp(file1, file2, shallow=False)


def compare(filelist, comparitor=_defaultComparitor):
    checked = []
    duplicate_files = []
    pairs = itertools.combinations(filelist, 2)

    # For each pair, we are checking if the second is a duplicate of the
    # first. This maintains the original preference order.
    for pair in pairs:
        # Skip if the second has already been determined to be a duplicate
        if pair[1] in checked:
            continue

        # (pair[1], pair[0]) = (duplicate, original)
        if comparitor(pair[1], pair[0]):
            duplicate_files.append((pair[1], pair[0]))

            # track duplicates found
            checked.append(pair[1])

    return duplicate_files


def generateFileList(directories):
    """Walk `directories` recursively and return a `list` of filenames
    found.
    """
    rv = []

    # Reminder: os.walk does not guarantee order of files in any single
    # directory. However, high level file list ordering is stable based on
    # input 'directories' order.

    # Reminder: by default, os.walk skip symlinks to directories

    visited_directories = set()

    for directory in directories:
        if os.path.abspath(directory) in visited_directories:
            continue
        for dirpath, dirlist, filelist in os.walk(directory):
            # TODO - repeatedly tries to add the visited dir?
            visited_directories.add(os.path.abspath(dirpath))
            dirlist[:] = [d for d in dirlist
                          if os.path.abspath(d) not in visited_directories]

            for fname in filelist:
                rv.append(os.path.join(dirpath, fname))
    return rv


def groupBySize(filepaths):
    """For all files provided, returns a `dict`, with file size as keys, and a list
    of files of that size as values.

    :param filepaths: iteratable collection of file paths to group
    """

    size_hash = {}
    for filename in filepaths:
        size = os.stat(filename).st_size
        if(size in size_hash):
            size_hash[size].append(filename)
        else:
            size_hash[size] = [filename]
    return size_hash


def compareFiles(filelist):
    """Return a list of files from `filelist` that are duplicates.

    The ordering of `filelist` is relevant. For any group of duplicate files,
    all but the first to appear in `filelist` will be included in the returned
    list.
    """

    logger.info("{} files to be examined".format(len(list(filelist))))

    # Hash by file size and create files_to_compare, a list of lists of files
    # with the same size.
    sizegroup = groupBySize(filelist)

    # Iterate the hash size group and create a list of lists. Each list elmt is
    # a list of files with matching sizes.
    files_to_compare = [i[1] for i in sizegroup.items() if len(i[1]) > 1]

    duplicate_files = []
    for comp_files in files_to_compare:
        duplicate_files += compare(comp_files)

    return duplicate_files
