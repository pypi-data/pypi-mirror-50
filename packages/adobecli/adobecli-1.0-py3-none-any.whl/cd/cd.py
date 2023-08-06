import argparse
import os
import sys

PARSER = argparse.ArgumentParser()
PARSER.add_argument("directory",
                    action="store",
                    default="./",
                    help="the directory to change to.")
def run(*args):
    """Makes a new directory"""
    options = PARSER.parse_args(*args)
    args = options.directory
    path = args
    try:
        os.chdir(path)
        print(os.getcwd())
        return(os.getcwd())
    except:
        print("Path does not exist")
        return "Path does not exist"

# To test independently, uncomment the line below
# run(sys.argv[1:])
