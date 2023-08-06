""" It reads data from the file and gives their content as output."""
import argparse
import itertools

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-n", "--number",
                    action="store_true",
                    dest="linenum",
                    default=False,
                    help="To view contents of a file preceding with line numbers.")
PARSER.add_argument("args", nargs="+", help="enter the filenames")

def run(*args):
    """It reads data from the file and displays its contents"""
    options = PARSER.parse_args(*args)
    args = options.args
    files = args
    result = ""
    for file in files:
        try:
            with open(file, "r") as infile:
                ##itertools.count() starts from 0. So, printing i+1 below.
                for i, line in zip(itertools.count(), infile):
                    if options.linenum:
                        line = f"{i+1}) " + line
                    print(line.strip())
                    result += line.strip()
                    result += "\n"
            return result
        except IOError as err:
            print(err.strerror)
            return err.strerror
    return result

# To test independently, uncomment the line below
# run(sys.argv[1:])
