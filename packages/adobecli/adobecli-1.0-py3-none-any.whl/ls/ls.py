"""
usage : ls [-r]
"""
import argparse
import os
import sys

PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("-r", "--recursive",
                    action="store_true",
                    dest="recursive",
                    default=False,
                    help="recursively print all files and directories")
PARSER.add_argument("args", nargs="*", help="enter the filenames",default=("./",))
def run(*args):
    """  Returns list of files and directories in the given directory  """
    options = PARSER.parse_args(*args)
    args = options.args
    #print(args)
    result = ""
    if len(args) > 1:
        print("Too many arguments")
        return "Too many arguments"
    directories = args[0]
    if not os.path.isdir(directories):
        print("Argument not a directory exception")
        return "Argument not a directory exception"
    for (dirpath, dirs, filenames) in os.walk(directories):
        try:
            for file_n in filenames:
                file_path = os.path.join(dirpath, file_n)
                # skip if it is symbolic link
                if not os.path.islink(file_path):
                    print(file_n)
                    result += file_n
                    result += "\n"
            for directory in dirs:
                if not os.path.islink(os.path.join(dirpath, directory)):
                    print(directory)
                    result += directory
                    result += "\n"
            if not options.recursive:
                break
        except OSError:
            continue
    return result
# To test independently, uncomment the line below
run(sys.argv[1:])
