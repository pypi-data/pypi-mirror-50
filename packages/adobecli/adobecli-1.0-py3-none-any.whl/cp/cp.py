"""
NAME
    cp - copy files and directories
SYNOPSIS
    cp [OPTION]... [-T] SOURCE DEST
    cp [OPTION]... SOURCE... DIRECTORY
    cp [OPTION]... -t DIRECTORY SOURCE...
DESCRIPTION
    Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.
"""
import argparse
import os
import shutil

PARSER = argparse.ArgumentParser(prog=__doc__)
PARSER.add_argument("args", nargs='*', help="Enter file/directory names")

def run(*args):
    """copy command"""
    try:
        res = ""
        options = PARSER.parse_args(*args)
        args = options.args
        if not options:
            res = "invalid command, no option supported"
        number_of_files = len(args) - 1
        destination = args[-1:][0]
        if number_of_files < 1:
            res = "not enough arguments"
        elif number_of_files > 1 and not os.path.isdir(destination):
            res = f"cp : {destination} should be directory"
        #elif number_of_files == 1 and os.path.isdir(args[0]) and os.path.isdir(destination):
        #    pass
        elif number_of_files >= 1 and os.path.isdir(destination):
            i = 0
            while i < number_of_files:
                if os.path.isfile(args[i]):
                    shutil.copy(args[i], destination)
                elif os.path.isdir(args[i]):
                    res += f"{args[i]} should not be a directory"
                else:
                    res += f"{args[i]} : no such file exist."
                i += 1
        elif number_of_files == 1:
            shutil.copy(args[0], destination)
        else:
            res = "Invalid Arguments."
        print(res)
        return res
    except PermissionError:
        print("Permission Denied.")
        return "Permission Denied."
    except IOError:
        print("No such file/directory exist.")
        return "No such file/directory exist."
