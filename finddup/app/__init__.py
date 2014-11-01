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

        logging.info(str(len(filelist)) + " files examined")
        logging.info(str(len(duplicate_pairs)) + " duplicates found")
