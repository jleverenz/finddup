import sys

import argparse
import atexit
import logging

from finddup import *
import finddup.output

logger = logging.getLogger('finddup')


def _parse_args():
    """Parse sys.argv command line options."""

    parser = argparse.ArgumentParser(prog='finddup',
                                     description='Find duplicate files.')
    parser.add_argument('dirs', nargs='+',
                        help='directories to recursively search for '
                        'duplicate files')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbose output')
    parser.add_argument('-m', '--mark', action='store_true',
                        help='marked (annotated) output, '
                             'showing originals and dupes')
    parser.add_argument('--output', default=None,
                        help='output file for list of duplicate files')
    return parser.parse_args()


def main():
    """Main entry point for the `finddup` script."""

    atexit.register(finddup.output.use_default)  # Close output on exit
    args = _parse_args()

    if args.output:
        finddup.output.redirect(args.output)

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    # Generate filelist and run duplicate detector
    filelist = generate_filelist(args.dirs)
    duplicate_pairs = compare_files(filelist)

    if args.mark:
        for k, v in duplicate_pairs.items():
            print("o {}".format(k))
            for i in v:
                print("d {}".format(i))
    else:
        for k, v in duplicate_pairs.items():
            for i in v:
                print(i)

    logger.info("{} files examined".format(len(filelist)))
    logger.info("{} duplicates found".format(len(duplicate_pairs)))


if __name__ == "__main__":
    main()
