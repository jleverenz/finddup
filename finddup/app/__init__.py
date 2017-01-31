from finddup import *
import logging


class App():
    @staticmethod
    def run(args):
        Output(outputFile=args.output)

        if args.verbose:
            logging.basicConfig(level=logging.INFO)

        # Generate filelist and run duplicate detector
        filelist = generateFileList(args.dirs)
        duplicate_pairs = compareFiles(filelist)

        for i in duplicate_pairs:
            Output.log(i[0])

        logging.info("{} files examined".format(len(filelist)))
        logging.info("{} duplicates found".format(len(duplicate_pairs)))
