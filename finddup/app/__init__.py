from finddup import *
import logging

# duplicates is a tuple with the duplicate listed first, and the original found second
def outputDuplicateFile(duplicates):
    Output.log(duplicates[0])

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
            outputDuplicateFile(i)

        logging.info(str(len(filelist)) + " files examined")
        logging.info(str(len(duplicate_pairs)) + " duplicates found")
