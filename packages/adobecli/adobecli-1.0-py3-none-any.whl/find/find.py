"""
NAME
     find -- walk a file hierarchy
DESCRIPTION
    The find utility recursively descends the directory tree for each path listed,
    evaluating an expression (composed of the ``primaries'' and ``operands'' listed below)
    in terms of each file in the tree.
"""
import os
import fnmatch
import argparse

PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("-name", "--name",
                    action="store", dest="name", type=str, default=None,
                    help="expression determines what to find")
PARSER.add_argument("args", nargs="*", default=None, help="enter the filenames")
def run(*args):
    """
    find in the specified directory
    """
    try:
        options = PARSER.parse_args(*args)
        args = options.args
        length = len(args)
        result = ""
        #print(options)
        if options.name is None or (length == 0):
            result =  "usage: find [-h] [-name NAME] [args [args ...]]\nfind [-h] [-name NAME] [args [args ...]]"
        for dirpath, dirnames, filenames in os.walk(args[0]):
            #print(dirnames)
            for filename in filenames:
                if fnmatch.fnmatch(filename, options.name): # Match search string
                    result =  os.path.join(dirpath, filename)
            for subdir in dirnames:
                #print(subdir,options.name)
                if fnmatch.fnmatch(subdir, options.name):
                    result = os.path.join(dirpath, subdir)
        print(result)
        return result
    except PermissionError:
        return None
    except ValueError:
        return None
#run(sys.argv[1:])
