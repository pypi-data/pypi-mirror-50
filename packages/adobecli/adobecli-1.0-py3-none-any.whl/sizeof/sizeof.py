"""
usage: sizeof [fileName]|[directoryName]
"""
import argparse
import os
#import sys

PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("args", nargs="*", help="enter the filenames")
def run(*args):
    """  Returns size details  """
    options = PARSER.parse_args(*args)
    args = options.args
    result = []
    #print(options,args)
    if len(args) != 1:
        print("Too many/less arguments")
        return "Too many/less arguments"
    total_size = 0
    directories = args[0]
    if os.path.isfile(directories):
        print(f"{os.path.getsize(directories)} bytes")
        return f"{os.path.getsize(directories)} bytes"
    elif os.path.isdir(directories):
        for (dirpath, _, filenames) in os.walk(directories):
            try:
                for file_n in filenames:
                    file_path = os.path.join(dirpath, file_n)
                    # skip if it is symbolic link
                    if not os.path.islink(file_path):
                        total_size += os.path.getsize(file_path)
            except OSError:
                continue
        print(f"{total_size} bytes")
        result.append(f"{total_size} bytes")
        print()
        return f"{total_size} bytes\n"
    else:
        print("Not a directory or file")
        return "Not a directory or file"
# To test independently, uncomment the line below
#run(sys.argv[1:])
