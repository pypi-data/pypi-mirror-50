"""This is the main module to implement PyShell"""
import rlcompleter
import shlex
import os
from pathlib import Path
# import test_module
from importlib import import_module
import sys

def date(args):
    #pylint: disable=unused-argument
    """This method prints the syatem date and time"""
    import time
    l_t = time.localtime()
    t_format = f"{l_t.tm_year}/{l_t.tm_mon}/{l_t.tm_mday} {l_t.tm_hour}:{l_t.tm_min}:{l_t.tm_sec}"
    #we hard-coded the GMT
    print(time.strftime("%a %b %d %Y %T GMT%z", time.strptime(t_format, "%Y/%m/%d %H:%M:%S")))

def whoami(args):
    #pylint: disable=unused-argument
    """This method prints the logged username"""
    import getpass
    print(getpass.getuser())

def hostname(args):
    #pylint: disable=unused-argument
    """This method prints the hostname"""
    import socket
    print(socket.gethostname())

def timeit(args):
    """This method prints the time taken to run a command"""
    args.pop(0)
    import time
    start = time.time()
    run(args)
    end = time.time()
    print("\'", " ".join(args).strip(), "\' took ", end - start, 'seconds.')

def exit(args):
    #pylint: disable=unused-argument
    """This method is used to exit from the PyShell"""
    quit()

def history(args):
    #pylint: disable=unused-argument
    """This method prints the history of commands executed"""
    with open(os.path.join(Path.home(), "cmds_list.txt"), "r") as out:
        for i, line in enumerate(out):
            print(f"{i} {line}")

def run(args):
    """This method is used for parsing commands"""
    if args[0] in globals():
        globals()[args[0]](args)
    else:
        try:
            cmd_parser = import_module("."+args[0], package="commands")
            cmd_parser.run(args[1:])
        except KeyError as e:
            print(str(e))
            print("command not found")

def py_shell():
    """This is the main method to implement Pyshell"""
    # mod_list = dict()
    # extension = '*.py'
    # print(os.path.dirname(sys.executable))
    # path = os.path.dirname(sys.executable)
    # length = len(str(path))
    # for name in Path(path).rglob(extension):
    #     module = name.as_posix()[length:]
    #     key = module
    #     cmd_parser = None
    #     if '/' in module:
    #         ind = module.rfind("/")
    #         val, key = module[:ind], module[ind+1:]
    #         if key == "ipython":
    #             continue
    #         val = val.replace("/", ".")
    #         cmd_parser = import_module("."+key[:len(key)-3], package=val)
    #     mod_list[key] = cmd_parser
    # print("Commands are:")
    # for key in mod_list.keys():
    #     print(key[:len(key)-3],end = " ")
    # print()
    while True:
        try:
            cmd = input(f"{Path.cwd()}> ")
            if not cmd.strip():
                continue
            with open(os.path.join(Path.home(), "cmds_list.txt"), "a+") as infile:
                print(cmd.strip(), file=infile)
            cmd_args = shlex.split(cmd.strip())
            run(cmd_args)
        except (KeyboardInterrupt, EOFError, ValueError):
            print("\nPython Shell Exited!")
            return

if __name__ == '__main__':
    # test_module.test_run()
    py_shell()
