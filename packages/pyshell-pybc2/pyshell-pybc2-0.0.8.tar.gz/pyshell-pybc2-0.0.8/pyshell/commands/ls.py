"""This module is the implementation of ls command"""
import os
from pathlib import Path
def recur():
    """this is to print the files recursively in a directory"""
    length = len(str(Path.cwd()))
    for dirname, dirnames, filenames in os.walk(Path.cwd()):
    # print path to all subdirectories first.
        count = 0
        print(dirname[length+1:]+":")
        for subdirname in dirnames:
            print(subdirname.ljust(20),end=" ")
            if count != 3:
                count += 1
            else:
                print()
                count = 0
        # print path to all filenames.
        for filename in filenames:
            print(filename.ljust(20),end=" ")
            if count != 3:
                count += 1
            else:
                print()
                count = 0
        print()
        print()

def root_directory(sub_folder):
    """this is to print the sub-folders for root directory"""
    root = Path.cwd().parts[0]
    if Path(root).joinpath(sub_folder).is_dir():
        count = 0
        for filename in Path(root).joinpath(sub_folder).glob('*'):
            file = filename.as_posix()
            length = len(str(Path(root).joinpath(sub_folder)))
            file = file[length:]
            print(file.ljust(20),end=" ")
            if count != 3:
                count += 1
            else:
                print()
                count = 0
    else:
        print("*** Unhandled `FileNotFoundError` exception:" + \
                       f"[Errno 2] No such file or directory: {sub_folder}")

def run(cmd_args):
    """ This is to execute the ls command and its cross-functionalities"""
    if cmd_args and cmd_args[0] == "--help":
        print("""Usage: ls [-R] [FILE]
        Lists all the files and sub directories in the current directory
        [-R] Recurse
        """)
        return
    if cmd_args and cmd_args[0] == "-R":
        recur()
        return
    if cmd_args and cmd_args[0].startswith("-") and cmd_args[0] != "-R":
        print("Invalid Option")
        return
    sub_folder = ""
    if cmd_args:
        sub_folder = " ".join(cmd_args)
    if sub_folder.startswith('/'):
        root_directory(sub_folder)
    else:
        if Path.cwd().joinpath(sub_folder).is_dir():
            count = 0
            for filename in Path.cwd().joinpath(sub_folder).glob('*'):
                file = filename.as_posix()
                length = len(str(Path.cwd().joinpath(sub_folder)))
                file = file[length+1:]
                print(file.ljust(20),end=" ")
                if count != 3:
                    count += 1
                else:
                    print()
                    count = 0
        else:
            print("*** Unhandled `FileNotFoundError` exception:" + \
                       f"[Errno 2] No such file or directory: {sub_folder}")
    print()
