"""The `utils` module contains helper functions that are used
throughout the PBS executor.

"""
import os
import re


def makedirs(path, mode=0775):
    """
    Makes a directory and all intermediate directories.

    This fixes the `umask` issue, where the mode suggested by
    `os.makedirs` is ignored. See https://stackoverflow.com/a/5231994.

    Parameters
    ----------
    path : str
      The directory path to create.
    mode : int
      The umask of the directory.

    """
    os.makedirs(path)
    os.chmod(path, mode)


def find_in_file(filename, search_str):
    """
    Determine whether a string is contained in a file.

    Like `grep`.

    Parameters
    ----------
    filename : str
      The path to a file.
    search_str : str
      The string to be found in the file.

    """
    with open(filename, 'r') as fp:
        for line in fp:
            if re.search(search_str, line):
                return True
    return False
