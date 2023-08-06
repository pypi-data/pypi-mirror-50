"""This module implements the head command"""
from pathlib import Path

def head(number, file):
    """Returns the first n lines from the file"""
    lines = []
    with open(file, "r") as infile:
        text = infile.readlines()
        #print(text)
        if len(text) < number:
            lines = [line for line in text]
        else:
            lines = [text[i] for i in range(number)]
    return lines
#deal with the last \n

def print_file(num_arg, file_arg):
    """prints the number of lines from file"""
    lines = head(num_arg, file_arg)
    for line in lines:
        print(line, end='')

def run(inputs):
    """this function runs the head command"""
    if not inputs:
        print("Usage: head [OPTION] [FILE]..")
        return
    if inputs and inputs[0] == "--help":
        print("""Usage: head [OPTIONS] [FILE]...
        
        Print first 10 lines of each FILE to stdout
        
        -n      print first N lines""")
        return
    if inputs and inputs[-1].lstrip('-').isdigit():
        print("Usage: head [OPTION] [FILE]..")
        return
    file_list = []
    try:
        num_arg = abs(int(inputs[0]))
        file_list = inputs[1:]
    except:
        num_arg = 10
        file_list = inputs[:]
    for file in file_list:
        if Path(file).is_file():
            print(f"<========{file}=========>")
            print_file(num_arg, file)
        else:
            print(f"'{file}': No such file")
