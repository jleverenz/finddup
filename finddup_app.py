from finddup import *

class FinddupApp():
    @staticmethod
    def run(args):
        Log.is_verbose = args.verbose

        # Generate filelist and run duplicate detector
        filelist = generateFileList(args.dirs)
        duplicate_pairs = compareFiles(filelist)

        Log.verbose(str(len(filelist)) + " files examined")
        Log.verbose(str(len(duplicate_pairs)) + " duplicates found")
