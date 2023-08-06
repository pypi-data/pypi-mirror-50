"""This module is for removing modules"""
from pathlib import Path

def run(filestoremove):
    """This removes files"""
    if not filestoremove:
        print("Usage: rm [OPTION] [FILE]..")
        return
    if filestoremove and filestoremove[0] == "--help":
        print("""Usage: rm FILE...
 
        Remove (unlink) FILEs""")
    if filestoremove[0] == '-r':
        remove(filestoremove[1:])
    else:
        for file in filestoremove:
            if Path(file).is_file():
                Path(file).unlink()
            elif Path(file).is_dir():
                print("rm :", file, "is a directory")
            else:
                print("cannot remove", file, ":doesnt exist")

def remove(toremove):
    """This removes dirs or files"""
    import shutil
    for file_or_dir in toremove:
        if Path(file_or_dir).is_dir():
            shutil.rmtree(file_or_dir)
        elif Path(file_or_dir).is_file():
            Path(file_or_dir).unlink()
        else:
            print("cannot remove", file_or_dir, ":doesnt exist")
