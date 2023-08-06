"""This module implements cat function"""
from pathlib import Path

def cat_each_to_dest(src, dest):
    """This function writes to each destination"""
    if not Path(src).is_file():
        print(f"File {src} does not exxist")
        return
    src_file = open(src, 'r')
    dest_file = open(dest, 'a')
    line = (src_file.readline())
    while line:
        dest_file.write(line)
        line = (src_file.readline())

def run(cat_inp):
    """This is the run function for cat command"""
    if not cat_inp:
        print("Usage: cat [FILE] ..")
        return
    if cat_inp and cat_inp[0] == "--help":
        print("""Usage: cat FILEs
        prints FILEs content to stdout
        
        (or)
        cat > FILE 
        Promts user for input and stores it in the FILE
        
        (or)
        cat SRCFILEs > DESTFILE
        Appends the contents in SRCFILEs to DESTFILE
        """)
        return
    if '>' in cat_inp:
        if len(cat_inp) < 2:
            print("Usage: cat [FILE] > [FILE]..")
            return
        if cat_inp[0] == '>':
            new_file = cat_inp[1]
            if not Path(new_file).is_dir():
                file_var = open(new_file, "w")
                input_line = input()
                while input_line:
                    if 'exit' in input_line:
                        break
                    file_var.write(input_line+"\n")
                    input_line = input()
            else:
                print(f"sh: can't create {new_file}: Is a directory")
        else:
            brk_pnt = cat_inp.index('>')
            scr = cat_inp[:brk_pnt]
            dest = cat_inp[-1]
            for file in scr:
                cat_each_to_dest(file, dest)
    else:
        for file in cat_inp:
            if Path(file).is_dir():
                print(f"cat: read error: Is a directory")
            elif not Path(file).is_file():
                print(f"can't open '{file}': No such file or directory")
            else:
                with open(file, "r") as infile:
                    for line in infile:
                        print(line)
            