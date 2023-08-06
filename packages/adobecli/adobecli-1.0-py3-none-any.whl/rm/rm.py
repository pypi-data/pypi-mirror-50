"""
usage: rm [filename] | [-r]
"""
import argparse
import os
import sys

PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("-r", "--recursive",
                    action="store_true",
                    dest="recursive",
                    default=False,
                    help="recursively remove all files and directories")
PARSER.add_argument("args", nargs="*", help="enter the filenames")
def run(*args):
    """  Returns list of files and directories in the given directory  """
    options = PARSER.parse_args(*args)
    args = options.args
    if len(args) < 1:
        print("Too many/less arguments")
        return "Too many/less arguments"
    directory = args
    result = []
    if not options.recursive: ##it is a file
        files = directory
        for file in files:
            try:
                os.remove(file)
            except OSError as error:
                print(error.strerror, file)
                result.append(error.strerror + f" {file}")
                continue
    else:
        for dir in directory:
            if not os.path.isdir(dir):
                print("Argument not a directory")
                return "Argument not a directory"
            for (dirpath, _, filenames) in os.walk(dir):
                    for file_n in filenames:
                        try:
                            file_path = os.path.join(dirpath, file_n)
                            # skip if it is symbolic link
                            if not os.path.islink(file_path):
                                print("file removed ", file_n)
                                result.append("file removed ", file_n)
                                os.remove(file_path)
                        except OSError as err:
                            print(err.strerror, file_n)
                            continue
    return result
# To test independently, uncomment the line below
run(sys.argv[1:])
