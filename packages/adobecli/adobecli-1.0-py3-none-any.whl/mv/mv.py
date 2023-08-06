"""
NAME
     mv -- move files

SYNOPSIS
     mv [-h] [-i] [args [args ...]] source target
     mv [-h] [-i] [args [args ...]] source ... directory

DESCRIPTION
    In its first form, the mv utility renames the file named by the source operand to the
    destination path named by the target operand.  This form is assumed when the last operand
    does not name an already existing directory.
"""
import os
import shutil
import argparse
import sys
PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("-i", "--interactive",
                    action="store_true", dest="interactive", default=False,
                    help="command ask the user for confirmation")
PARSER.add_argument("args", nargs="*", default=None, help="enter the filenames")
def run(*args):
    """move a file from source to destination"""
    try:
        options = PARSER.parse_args(*args)
        args = options.args
        length = len(args)
        if length == 0:
            print("usage: mv [-h] [-i] [args [args ...]] source target")
            print("mv [-h] [-i] [args [args ...]] source ... directory")
            return "usage: mv [-h] [-i] [args [args ...]] source target\nmv [-h] [-i] [args [args ...]] source ... directory"
        src = args[0]
        dst = args[1]
        if not os.path.exists(src):
            raise IOError
        else:
            if os.path.exists(src) and options.interactive:
                confirm = input("mv: overwrite '", dst, "'?")
                if not confirm:
                    return ""
            if os.path.isdir(src):
                filelist = os.listdir(src)
                filelist.sort()
                for files in filelist:
                    os.rename(os.path.join(src, files), os.path.join(dst, files))
                    shutil.move(os.path.join(src, files), os.path.join(dst, files))
                os.remove(src)
            else:
                shutil.move(src, dst)
            return ""
    except PermissionError:
        print("Permission denied")
        return "Permission denied"
    except IOError:
        print("File not found error")
        return "File not found error"
# To test independently, uncomment the line below
# run(sys.argv[1:])
