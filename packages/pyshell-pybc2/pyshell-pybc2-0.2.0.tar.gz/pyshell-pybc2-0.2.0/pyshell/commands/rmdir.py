"""This module is to remove a directory if it is empty"""
from pathlib import Path

def run(dir_allnames):
    """This function implements the way to delete a directory"""
    if not dir_allnames:
        print("Usage : rmdir directory ...")
        return
    if dir_allnames[0] == "--help":
        print("""Usage: rmdir DIRECTORY...
        Delete the directory if it is empty
        """)
        return
    for dir_name in dir_allnames:
        if not Path(dir_name).is_dir():
            print(f'`{dir_name}` is not a folder.')
            continue
        is_empty = [x for x in Path(dir_name).rglob('*')]
        if not is_empty:
            Path(dir_name).rmdir()
        else:
            print(f'`{dir_name}` is not empty.')
            