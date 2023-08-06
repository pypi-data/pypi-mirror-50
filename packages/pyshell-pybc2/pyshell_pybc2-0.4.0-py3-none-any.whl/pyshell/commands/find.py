"""This module implements find command"""
from pathlib import Path

def run(cmd):
    """This function is used to find the file or directory"""
    if not cmd:
        print("Usage: find [PATH]... [FILENAME]")
        return
    if cmd and cmd[0] == "--help":
        print("""Usage: find [PATH]... [FILENAME]
 
        Search for files in given path.
        Defaults: PATH is current directory, action is '-print'""")
        return
    filename = cmd[-1]
    path = Path.cwd().joinpath(cmd[0])
    for name in path.rglob(filename):
        print(name)
