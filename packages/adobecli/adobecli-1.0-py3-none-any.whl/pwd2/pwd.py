"""
gets current path
"""
import os
import argparse
#import sys
PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("argss", nargs="*", help="no arguments needed")

def run(*args):
    """Gets current path"""
    _ = PARSER.parse_args(*args)
    print(os.getcwd())
    return os.getcwd()

# To test independently, uncomment the line below
#run(sys.argv[1:])
