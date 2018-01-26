"""This module contains the AssemblyStorage class.

.. module:: assemblystorage
    :platform: Unix
    :synopsis: This class handles multiple instances of AssemblyDatabase.

.. moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# Inter-package imports.
from pynome.assemblydatabase import AssemblyDatabase


class AssemblyStorage:
    """Models a group of AssemblyDatabase instances.

    Provides functions for interacting with those instances.
    """

    def __init__(self, sources=None, base_path=None, irods_base_path=None):
        """Initialization of the AssemblyStorage class.
        """

        # Define the public attributes of the class.
        self.base_path = base_path
        self.irods_base_path = irods_base_path

        # Define the private attributes of the class for use by properties.
        if sources is None:
            self.__sources = list()
        else:
            self.__sources = sources

    @property
    def sources(self):
        """A list container for AssemblyDatabase objects.

        This is the getter function for this property.
        """
        return self.__sources

    @sources.setter
    def sources(self, val):
        """The setter for the sources list.

        Ensures that all objects passed to / stored in this private attribute
        are isntances of the AssemblyDatabase class.
        """
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, AssemblyDatabase) for x in val):
                self.__sources = list(val)
        else:
            raise AttributeError(
                '{0} sources must be a list containing AssemblyDatabase'
                'objects.'.format(type(self).__name__))

    def crawl(self, assembly_database):
        """Call the crawl function on the given assembly_database.
        """
        assembly_database.crawl()

    def crawl_all(self):
        """Call the crawl function on every AssemblyDatabase in sources.
        """
        for source in self.sources:
            source.crawl()

    def download(self, assembly):
        """Download a specific assembly."""
        pass

    def download_all(self):
        """Downloads all assemblies found within each source."""
        pass

    def find_assembly(self):
        """Return an assembly, or list of assemblies that match given criteria.
        """
        pass

    def add_source(self, new_source):
        """Append a new source to the sources list."""
        pass

    def push_irods(self):
        """Pushes all the files within each source to an iRODs server.
        """
        pass
