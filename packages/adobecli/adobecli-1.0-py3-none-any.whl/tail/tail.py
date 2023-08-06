"""
usage: tail [filename]| [-n] | [-v]
"""
import argparse
import sys
from collections import deque
import os

PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("-n", "--lines",
                    action="store",
                    dest="nlines",
                    default=10,
                    help="specify no. of lines to be displayed",
                    type=int)
PARSER.add_argument("-v", "--verbose",
                    action="store_true",
                    dest="verbose",
                    default=False,
                    help="data from the specified file is always preceded by its file name")
PARSER.add_argument("args", nargs="*", help="enter the filenames")
def run(*args):
    """  Returns n lines from the tail/bottom of a file"""
    options = PARSER.parse_args(*args)
    args = options.args
    #print(options,args)
    if len(args) < 1:
        print("Too few Arguments")
        return "Too few Arguments"
    nlines = options.nlines
    file_names = args
    for file_name in file_names:
        if not os.path.isfile(file_name):
            print("Arguments other than filename given or file does not exist")
            return "Arguments other than filename given or file does not exist"
    result = ""
    for file_name in file_names:
        lines = deque(open(file_name), nlines)
        if options.verbose:
            print(f"==> {file_name} <==")
            result += f"==> {file_name} <=="
        for line in lines:
            print(line.strip())
            result += line.strip()
            result += "\n"
    return result

# To test independently, uncomment the line below
#run(sys.argv[1:])
