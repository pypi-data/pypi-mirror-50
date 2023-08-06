"""This module implements the cd command"""
from pathlib import Path
import os

def change_directory(dest):
    """this function is used to change directory"""
    if not Path(dest).exists():
        print(f"cd : can't cd to {dest}")
    else:
        os.chdir(dest)

def run(inputstring):
    """This is the main function to implement cd command"""
    if len(inputstring) == 0:
        os.chdir(Path.cwd())
        return
    if inputstring[0] == "--help":
        print("""Usage 'cd [FOLDERNAME]' 
or cd [PATH]

Changes the working directory to given PATH or FOLDER
        """)
        return
    else:
        change_directory(inputstring[0])
