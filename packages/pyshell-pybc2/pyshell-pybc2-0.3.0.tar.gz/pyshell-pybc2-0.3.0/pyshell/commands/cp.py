"""This module implements cp command"""
import sys
from pathlib import Path

def copy_one_file(src, dst):
    """This copies one file to destination"""
    try:
        Path(dst).write_bytes(Path(src).read_bytes())
    except IOError as excep:
        print(f"{sys.argv[0]}: {excep}")
    else:
        print(f"'{src.name}' copied to '{dst.name}'")

def copy_files(src, dst):
    """This copies files to multiple destinations"""
    for filename in src:
        source = Path(filename)
        if not source.is_file():
            print(f"{sys.argv[0]}: '{filename}': File does not exist.")
            continue
        if Path(dst).is_dir():
            dest = Path(dst).joinpath(filename)
        elif Path(dst).is_file():
            choice = input(f"Overwrite '{dst}' (y/n) ?")
            if choice[0] not in 'yY':
                print(f"{sys.argv[0]}: aborted.")
                exit(1)
            else:
                dest = Path(dst)
        else:
            dest = Path(dst)

        copy_one_file(source, dest)

def run(inputs):
    """This runs the cp command"""
    if not inputs:
        print("Usage: cp [OPTIONS] SOURCE... DEST")
        return
    if inputs[0] == "--help":
        print("""Usage: cp [OPTIONS] SOURCE... DEST
        
Copy Source(s) to Dest
        """)
        return
    if len(inputs) < 2:
        print(f"usage: {inputs[0]} source [...] destination.", file=sys.stderr)

    elif len(inputs) > 2 and not Path(sys.argv[-1]).is_dir():
        print(f"{sys.argv[0]}: {sys.argv[-1]}: Not a directory.", file=sys.stderr)

    else:
        destination = inputs.pop()
        source = inputs
        copy_files(source, destination)
