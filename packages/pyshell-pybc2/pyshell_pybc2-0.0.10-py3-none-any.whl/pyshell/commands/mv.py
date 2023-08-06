"""This module implements move command"""
import sys
from pathlib import Path

def move_one_file(src, dst):
    """This function moves one file"""
    print("move_one_file func")
    if dst.is_file():
        choice = input(f"Overwrite '{dst}' (y/n) ?")
        if choice[0] not in 'yY':
            print(f" `mv` : {src} -> {dst}: skipped.")
            return
    try:
        Path(dst).write_bytes(src.read_bytes())
        Path.unlink(src)
    except IOError as err:
        print(f"mv : {err}")
    else:
        print(f"'{src}' copied to '{dst}'")

def move_files(src, dst):
    """This function moves multiple files"""
    print("in move_files fun")
    print(src)
    for filename in src:
        source = Path(filename)
        if not source.is_file():
            print(f" `mv` : '{filename}': File does not exist.")
            continue

        if Path(dst).is_dir():
            dest = Path(dst).joinpath(filename)
        else:
            dest = Path(dst)

        move_one_file(source, dest)

def run(inputs):
    """This function runs the move command"""
    if inputs and inputs[0]=="--help":
        print("""Usage: mv SOURCE DEST
or: mv SOURCE... DIRECTORY

Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY
        """)
        return
    if len(inputs) < 2:
        print(f"usage: `mv` source [...] destination.", file=sys.stderr)

    elif len(inputs) > 2 and not Path(inputs[-1]).is_dir():
        print(f"`mv`: {inputs[-1]}: Not a directory.", file=sys.stderr)

    else:
        destination = inputs[-1]
        source = inputs[0:-1]
        print(source, destination)
        move_files(source, destination)
    