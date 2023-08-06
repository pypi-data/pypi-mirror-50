"""This module implements grep functionality"""
from pathlib import Path

def run(input_lst):
    """This function runs grep"""
    if input_lst and input_lst[0] == "--help":
        print("""grep [-n] PATTERN FILE [FILE]...
        
        Search for PATTERN in FILEs

        -n      Add 'line_no:' prefix
        """)
        return
    if len(input_lst) < 2:
        print("Usage: grep [-n] [PATTERN] [FILE]..")
        return
    num = False
    if input_lst[0] == '-n':
        files = input_lst[2:]
        num = True
        search_str = input_lst[1]
    else:
        files = input_lst[1:]
        search_str = input_lst[0]
    append_str = ''
    if not files:
        print("Usage: grep [-n] [PATTERN] [FILE]..")
        return
    for file in files:
        if len(files) > 1:
            append_str = str(file)+":"
        if not Path(file).is_file():
            print(f"grep: {file}: No such file or directory")
            return
        linenum = 0
        flag = 0
        with open(file, "r") as outfile:
            line = outfile.readline()
            original_str = append_str
            while line:
                if num is True:
                    linenum += 1
                    append_str = append_str + str(linenum) + ":"
                if search_str in line:
                    flag = 1
                    print(append_str+line)
                line = outfile.readline()
                append_str = original_str
        if not flag:
            print(f"No such word in the file : {file}")
