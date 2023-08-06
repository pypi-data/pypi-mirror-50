"""This modules is used to create a new directory"""
from pathlib import Path

def create_directory(dirnames):
    """this function creates the directory"""
    for dirname in dirnames:
        path = Path(Path.cwd()).joinpath(dirname)
        if path.exists():
            print(f"mkdir: `{dirname}` already exists")
            continue
        else:
            Path.mkdir(path)

def run(inputs):
    """this is the main function to check the input and implements functionality"""
    if not inputs:
        print("Usage mkdir [DIRECTORY] ...")
        return
    if inputs[0] == "--help":
        print ("""Usage: mkdir DIRECTORY...
        Creates a directory
        """)
        return
    else:
        create_directory(inputs)
