"""grep  searches the named input FILEs for lines containing  a  match to the given PATTERN."""
import argparse
import re
#import sys
import os
#import traceback
from ArgumentError import ArgumentError

PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("pattern",
                    action="store",
                    default="*",
                    help="the pattern to find")
PARSER.add_argument("-i", "--ignore-case",
                    action="store_true",
                    dest="ignore_case",
                    default=False,
                    help="Ignore case distinctions in  both  the  PATTERN  and  the  input files.")
PARSER.add_argument("-v", "--invert-match",
                    action="store_true",
                    dest="invert_match",
                    default=False,
                    help="Invert the sense of matching, to select non-matching lines.")
PARSER.add_argument("-c", "--count",
                    action="store_true",
                    dest="count",
                    default=False,
                    help="Ignore case distinctions in  both  the  PATTERN  and  the  input files.")
PARSER.add_argument("argss", nargs="*", help="enter the filenames")
ARG_ERR = ArgumentError("pattern", ("-i", "-v", "-c"), 1)
def run(*args):
    """grep  searches the named input FILEs for lines containing a match to the given PATTERN."""
    try:
        options = PARSER.parse_args(*args)
        args = options.argss
    except ValueError as err:
        print(err)
        return err
    files = args
    if options.count:
        res = 0
    else:
        res = None
    result = ""
    for file in files:
        try:
            with open(file, "r") as infile:
                for line in infile:
                    params = (options.pattern, line)
                    if options.ignore_case:
                        params += (re.I,)
                    if options.count:
                        res += len(re.findall(*params))
                    else:
                        res = re.search(*params)
                        if options.invert_match:
                            if not res:
                                print(f"{os.path.basename(file)}:{line.strip()}")
                                result += f"{os.path.basename(file)}:{line.strip()}\n"
                        else:
                            if res:
                                print(f"{os.path.basename(file)}:{line.strip()}")
                                result += f"{os.path.basename(file)}:{line.strip()}\n"
                if options.count:
                    print(f"{os.path.basename(file)}:{res}")
                    result += f"{os.path.basename(file)}:{res}\n"
                    res = 0
        except IOError as err:
            print(err.strerror)
            result += err.strerror
    return result

# To test independently, uncomment the line below
# run(sys.argv[1:])
