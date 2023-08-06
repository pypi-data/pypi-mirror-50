"""
Reads top n lines from a file
"""
import argparse
# import sys
#import os

PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("-n", "--lines",
                    action="store",
                    dest="nlines",
                    type=int,
                    default=10,
                    help="specify no. of lines to be displayed")
PARSER.add_argument("-v", "--verbose",
                    action="store_true",
                    dest="verbose",
                    default=False,
                    help="data from the specified file is always preceded by its file name")
PARSER.add_argument("args", nargs="+", help="enter the filenames")
def run(*args):
    """  Returns n lines from the head of a file"""
    options = PARSER.parse_args(*args)
    args = options.args
    nlines = options.nlines
    file_names = args
    result = ""
    for file_name in file_names:
        try:
            if options.verbose:
                print(f"==> {file_name} <==")
                result += f"==> {file_name} <=="
            with open(file_name, "r") as infile:
                for _, line in zip(range(nlines), infile):
                    print(line.strip())
                    result += line.strip()
                    result += "\n"
        except IOError as error:
            print(error.strerror)
            result += error.strerror
    return result

# To test independently, uncomment the line below
# run(sys.argv[1:])
