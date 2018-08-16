"""The `utils` module collects a set of helper functions that are used
in the PBS executor.

"""
import os
import re


def makedirs(path, mode=0775):
    """
    Make a directory and all intermediate directories.

    This fixes the 'umask issue', where the mode suggested by
    ``os.makedirs`` is ignored. See
    https://stackoverflow.com/a/5231994.

    Parameters
    ----------
    path : str
      The directory path to create.
    mode : int
      The permissions of the directory.

    Examples
    --------
    Make a new directory **tmp** under the current directory:

    >>> makedirs('tmp', mode=0775)

    """
    os.makedirs(path)
    os.chmod(path, mode)


def is_in_file(path, search_string):
    """
    Determine whether a string is contained in a file.

    Like ``grep``.

    Parameters
    ----------
    path : str
      The path to a file.
    search_string : str
      The string to be located in the file.

    """
    with open(path, 'r') as filep:
        for line in filep:
            if re.search(search_string, line):
                return True
    return False


def check_permissions(path, mode):
    """
    Check whether file permissions match a given mode.

    Returns ``True`` if the file has the given mode, ``False``
    otherwise. See https://stackoverflow.com/a/5337329.

    Parameters
    ----------
    path : str
      The path the file to check.
    mode : str
      The mode to check against.

    """
    return oct(os.stat(path).st_mode)[-3:] == mode
