"""
commands module
"""
from importlib import import_module
import shlex
import argparse
from command_dispatch import CommandDispatch

SHELL = CommandDispatch()

@SHELL.for_command("history")
def history(*args):
    """gives history"""
    parser = argparse.ArgumentParser(prog=__doc__)
    parser.add_argument("argss", nargs="*", default=None, help="takes no arguments")
    _ = parser.parse_args(args)
    for cmd in SHELL.cmd_hist[::-1]:
        print(cmd)

@SHELL.for_command("date")
def date(*args):
    """
    returns date in the provided format
    u: UTC
    default: IST
    """
    import time
    from datetime import datetime
    parser = argparse.ArgumentParser(prog=__doc__)
    parser.add_argument("-u", "--utc",
                        action="store_true", dest="utc", default=False,
                        help="print date in UTC format")
    parser.add_argument("argss", nargs="*", default=None, help="enter the filenames")

    try:
        args = args[1:]
        options = parser.parse_args(args)
        args = options.argss
        length = len(args)
        if (not options.utc) and (length == 0):
            print(time.strftime(("%a %b %d %T %Z %Y")))
        if options.utc:
            print(datetime.utcnow().strftime("%a %b %-d %I:%M:%S UTC %Y"))
        if args:
            try:
                print((time.strftime(args)).split('+')[1])
            except ValueError:
                print("date: illegal time format")
    except ValueError:
        print("date: illegal time format")
    except PermissionError:
        print("Permission denied")

@SHELL.for_command("hostname")
def hostname(*args):
    """
    NAME
         hostname -- set or print name of current host system
    SYNOPSIS
         hostname [-fs] [name-of-host]
    DESCRIPTION
         The hostname utility prints the name of the current host.  The super-user
         can set the hostname by supplying an argument.  To keep the hostname
         between reboots, run `scutil --set HostName name-of-host'.
    """
    import socket
    parser = argparse.ArgumentParser(prog=__doc__)
    parser.add_argument("-i", "--ip-address",
                        action="store_true", dest="ip", default=False,
                        help="Display the IP address(es) of the host")
    parser.add_argument("-s", "--short",
                        action="store_true", dest="short", default=False,
                        help="Display the short hostname")
    parser.add_argument("-f", "--fqdn",
                        action="store_true", dest="fqdn", default=False,
                        help="Display the FQDN")
    parser.add_argument("argss", nargs="*", default=None, help="enter the filenames")

    try:
        args = args[1:]
        options = parser.parse_args(args)
        args = options.argss
        length = len(args)
        res = ""
        if options.ip:
            print(socket.gethostbyname(socket.gethostname()))
            res = socket.gethostbyname(socket.gethostname())
        elif options.short:
            print(socket.gethostname().split(".")[0])
            res = socket.gethostname().split(".")[0]
        elif options.fqdn:
            print(socket.getfqdn())
            res = socket.getfqdn()
        elif length == 0:
            print(socket.gethostname())
            res = socket.gethostname()
        else:
            raise ValueError
        return res
    except ValueError:
        print("hostname: illegal option ")
        print("usage: hostname [-fs] [name-of-host]")
        return "hostname: illegal option \nusage: hostname [-fs] [name-of-host]"

@SHELL.for_command("whoami")
def whoami(*args):
    """Print the user name associated with the current effective user ID."""
    parser = argparse.ArgumentParser(prog=__doc__)
    parser.add_argument("argss", nargs="*", default=None, help="takes no arguments")
    _ = parser.parse_args(args)
    import getpass

    try:
        #print(args)
        args = args[1:]
        result = ""
        number_of_args = len(args)
        if number_of_args == 0:
            print(getpass.getuser())
            result = getpass.getuser()
        else:
            raise ValueError
        return result
    except ValueError:
        print(f"whoami: illegal option {args[0]}")
        return f"whoami: illegal option {args[0]}"

@SHELL.for_command("timeit")
def time_it(*args):
    """Tool for measuring execution time of small code snippets"""
    import time
    parser = argparse.ArgumentParser(prog=__doc__)
    parser.add_argument("argss", nargs="*", default=None, help="takes no arguments")
    _ = parser.parse_args(args)
    args = args[1:]
    if args[0] == "timeit":
        print("can cause loop condition")
        return "can cause loop condition"
    try:
        start = time.time()
        res = SHELL.commands.get(args, SHELL.importlibfn)(*args)
        if res == 1:
            raise ModuleNotFoundError
        end = time.time()
        print(f"{' '.join(args)} took {end-start} seconds.")
        return f"{' '.join(args)} took {end-start} seconds."
    except ModuleNotFoundError:
        return ''



@SHELL.for_command("exit")
def exit_shell(*args):
    """exists shell"""
    parser = argparse.ArgumentParser(prog=__doc__)
    parser.add_argument("argss", nargs="*", default=None, help="takes no arguments")
    _ = parser.parse_args(args)
    raise KeyboardInterrupt

@SHELL.importmod
def importmodulefn(*args):
    """imports modules"""
    commandname = args[0]
    args = args[1:]
    try:
        if commandname not in SHELL.compiled_modules:
            SHELL.compiled_modules[commandname] = import_module(commandname)
        res = SHELL.compiled_modules.get(commandname).run(args)
        return res
    except ModuleNotFoundError:
        print(f"{commandname}: command not found")
        return 1

@SHELL.invalid
def invalid_command(*args):
    """check for invalid commands"""
    print("Invalid command - ", args[0])

@SHELL.input
def get_input():
    """input function"""
    # import rlcompleter
    args = input("Adobe-cli> ")
    SHELL.cmd_hist.append(args)
    SHELL.cmd_hist = SHELL.cmd_hist if len(SHELL.cmd_hist) < SHELL.limit \
                    else SHELL.cmd_hist[-SHELL.limit:]
    args = shlex.split(args)
    return args

if __name__ == '__main__':
    try:
        SHELL.run()
    except KeyboardInterrupt as err:
        print("exiting prompt")
