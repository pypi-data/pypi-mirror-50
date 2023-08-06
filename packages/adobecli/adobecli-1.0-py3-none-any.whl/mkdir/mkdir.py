"""
Makes a new directory
"""
import argparse
import os
#import sys

PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("-p",
                    action="store",
                    dest="parentDir",
                    default=False,
                    help="If the parent directories don't exist, this option creates them.")
PARSER.add_argument("args", nargs="+", help="enter the filenames")

def run(*args):
    """Makes a new directory"""
    try:
        options = PARSER.parse_args(*args)
        args = options.args
    except ValueError as err:
        print(err.strerror)
        return err.strerror
    folders = args
    for folder in folders:
        try:
            os.makedirs(folder)
        except FileExistsError:
            print(f"mkdir: {folder}: File exists")
            return f"mkdir: {folder}: File exists"
# To test independently, uncomment the line below
#run(sys.argv[1:])
