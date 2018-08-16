"""The `utils` module contains helper functions that are used
throughout the PBS executor.

"""
import os


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
