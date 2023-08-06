"""this module is to implement pwd command"""
def run(*args):
    """this function prints the user current working directory"""
    if not args and args[0][0] == "--help":
        print("""Usage: pwd
        
Prints the present working directory
        """)
        return
    from pathlib import Path
    print(Path(".").absolute().as_posix())
