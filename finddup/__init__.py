#!/usr/bin/env python

import filecmp
import itertools
import logging
import os

logger = logging.getLogger('finddup')


def _default_comparitor(file1, file2):
    return filecmp.cmp(file1, file2, shallow=False)


def compare(filelist, comparitor=_default_comparitor):
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


def generate_filelist(directories):
    """Walk `directories` recursively and return a `list` of filenames
    found.
    """
    rv = []

    # Reminder: os.walk does not guarantee order of files in any single
    # directory. However, high level file list ordering is stable based on
    # input 'directories' order.

    # Reminder: by default, os.walk skip symlinks to directories

    visited_directories = set()

    # NOTE os.walk `followlinks` default is False, will not descend into
    # directory links
    for directory in directories:
        if os.path.abspath(directory) in visited_directories:
            continue
        for dirpath, dirlist, filelist in os.walk(directory):
            # TODO - repeatedly tries to add the visited dir?
            visited_directories.add(os.path.abspath(dirpath))
            dirlist[:] = [d for d in dirlist
                          if os.path.abspath(d) not in visited_directories]

            for fname in [f for f in filelist
                          if not os.path.islink(os.path.join(dirpath, f))]:
                rv.append(os.path.join(dirpath, fname))
    return rv


def group_by_size(filepaths):
    """Group `filepaths` into a `dict` keyed on filesize.

    For all files provided, returns a `dict`, with file size as keys, and a
    list of files of that size as values.

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


def _filter_hard_links(filelist):
    """
    Return a new list from filelist with any files detected as hard
    links removed. Order is preserved.

    Hard links are defined as files with equal st_dev and st_ino stats.
    """
    visited = set()
    updated = list()
    for fname in filelist:
        st = os.stat(fname)
        key = (st.st_dev, st.st_ino)
        if key not in visited:
            visited.add(key)
            updated.append(fname)
    return updated


def compare_files(filelist):
    """Return a list of files from `filelist` that are duplicates.

    The ordering of `filelist` is relevant. For any group of duplicate files,
    all but the first to appear in `filelist` will be included in the returned
    list.
    """

    logger.info("{} files to be examined".format(len(list(filelist))))

    # Hash by file size and remove any hard links found.
    sizegroup = dict([(k, _filter_hard_links(v))
                      for (k, v) in group_by_size(filelist).items()])

    # Iterate the hash size group and create a list of lists. Each list elmt is
    # a list of files with matching sizes.
    files_to_compare = [i[1] for i in sizegroup.items() if len(i[1]) > 1]

    duplicate_files = []
    for comp_files in files_to_compare:
        duplicate_files += compare(comp_files)

    return duplicate_files
