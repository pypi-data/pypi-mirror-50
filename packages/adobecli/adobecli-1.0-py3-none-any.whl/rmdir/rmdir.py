"""
Removes directory
"""
import argparse
import os
import sys

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-p",
                    action="store",
                    dest="parentDir",
                    default=False,
                    help="the directories along the would be removed.")
PARSER.add_argument("--ignore-fail-on-non-empty",
                    action="store",
                    dest="ignore",
                    default=False,
                    help="ignores failure on removal of non empty dir")
PARSER.add_argument("args", nargs="+", help="enter the filenames")

def run(*args):
    """Removes directory"""
    options = PARSER.parse_args(*args)
    args = options.args
    folders = args
    res = ""
    for folder in folders:
        try:
            os.removedirs(folder)
        except OSError as err:
            print(err.strerror)
            res += err.strerror
            if options.ignore:
                continue
    return res
# To test independently, uncomment the line below
#run(sys.argv[1:])
