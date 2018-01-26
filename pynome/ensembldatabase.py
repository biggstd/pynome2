"""This module contains the EnsemblDatabase class.

.. module:: ensembldatabase
    :platform: Unix
    :synopsis: A child class of AssemblyDatabase that implements Ensembl
    specific functions for crawling, parsing and downloading genome
    assembly files.

.. moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# General Python imports.
import ftplib

# Inter-package imports.
from pynome.assemblydatabase import AssemblyDatabase


class EnsemblDatabase(AssemblyDatabase):
    """Class to handle the crawling, parsing and downloading of
    genome assembly files from the Ensembl database.
    """

    def __init__(self):
        """The initialization function for EnsemblDatabase.

        Calls the constructor of AssemblyDatabase, and creates
        attributes and properties specific to the Ensembl database.
        """

        # Call the parent constructor / __init__ function.
        super().__init__()

        # Define public attributes of the class.
        self.ftp = ftplib.FTP()

        # Define the private attributes of the class.

    def crawl(self):
        pass
