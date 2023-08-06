"""This module implements size of functionality"""
from pathlib import Path

def run(filename):
    """This runs sizeof"""
    if not filename:
        print("Usage: sizeof [FILE]")
        return
    if filename[0] == "--help":
        print(    """Usage: sizeof [FILE]
        To find the sizeof a file""")
        return
    file = Path(filename[0])
    if file.exists():
        size = file.stat().st_size
        print(size, "bytes")
    else:
        print(filename[0], ":doesnt exist")
