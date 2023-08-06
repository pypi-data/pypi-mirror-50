"""This module implements tail command"""
import sys
from pathlib import Path

def print_last_lines(file, number):
    """prints last lines of a file"""
    print(f"<=== {file} ===>")
    with open(file, "r") as infile:
        for line in infile.readlines()[number:]:
            print(line, end="")
        print() 

def tail(files, number):
    """Checks validity of file"""
    for filename in files:
        filename = Path(filename)
        if not filename.is_file():
            print(f"'{filename}': No such file")
            continue
        print_last_lines(filename, number)

def run(inputs):
    """This funciton runs the tail command"""
    if inputs and inputs[0] == "--help":
        print("""Usage: tail [OPTIONS] [FILE]...
        
Print last 10 lines of each FILE to stdout

-n      print last N lines
        """)
        return
    if inputs and inputs[-1].lstrip('-').isdigit():
        print("Usage: tail [OPTION] [FILE]..")
        return  
    file_list = []
    
    try:
        num_arg = int(inputs[0])
        file_list = inputs[1:]
    except Exception as e:
        num_arg = -10
        file_list = inputs[0:]
    tail(file_list, num_arg)
