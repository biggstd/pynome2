"""This module contains utilities for Pynome not specific to any class.

.. module:: untils
    :platform: Unix
    :synopsis: Functions that are needed by Pynome, but are not specific
    to any class or module.

..moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# Import general Python packages.
import json


def read_json_config(config_file='pynome_config.json'):
    """Reads a json config file for required variables.
    """

    # Open the file, get the informaiton, then close it.
    with open(config_file) as cfg:
        config_dict = json.load(cfg)

    # Return the loaded configuration dictionary.
    return config_dict


def dir_check(dir_line, bad_dirs):
    """Checks if the input: dir_value is a directory. Assumes the input
    will be in the following format:

         ``"drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename"``

    This works by checking the first letter of the input string,
    and returns True for a directory or False otherwise.

    :param dir_line:
        A line as retrieved by ftplib.dir().

    :param bad_dirs:
        A list of directories that should cause the function to
        return False.

    :returns:
        A boolean value. True if `dir_line` represents a directory,
        and this directory does not fall into the list given in `bad_dirs`.
    """
    # Split the dir_line by whitespace.
    split_line = dir_line.split()

    # Check the first character of the dir output. If it is a 'd'
    # the corresponding line is a directory listing, and we should
    # examine that directory.
    # If the targeted directory matches an entry in bad_dirs, that
    # directory should also be passed over.
    return bool(split_line[0][0] == 'd' and \
                not any(bd == split_line[-1] for bd in bad_dirs))


def crawl_ftp_dir(ftp, top_dir, parsing_function, ignored_dirs):
    """Recursively crawl a target directory. Takes as an input a
    target directory and a parsing function. The ftplib.FTP.dir()
    function is used to retrieve a directory listing, line by line,
    in string format. These are appended to a newly generated list.
    Each item in this list is subject to the parsing function.

    :param database:
        An instance of ftplib.FTP()

    :param top_dir:
        The directory from which contents will be retrieved.

    :param parsing_function:
        The function to parse each non-directory result.

    """
    # Create an empty list to hold the callback
    retrieved_dir_list = []

    # The last argument passed to ftplib.dir acts as a callback if it
    # is a function. In this case the given function is a call to
    # append() the retrieved directory list.
    ftp.dir(top_dir, retrieved_dir_list.append)

    # For each line / directory listing retrieved.
    for line in retrieved_dir_list:

        # Check to see if this item is a (good) directory.
        # If it is, start the crawl function on that directory.
        if dir_check(line, ignored_dirs):

            # Construct the new top directory to start a crawl.
            target_dir = ''.join((top_dir, line.split()[-1], '/'))
            # Start a new crawl at this directory.
            crawl_ftp_dir(ftp, target_dir, parsing_function, ignored_dirs)

        # Otherwise the line is not a directory, and must be parsed.
        else:
            parsing_function(line, top_dir)
