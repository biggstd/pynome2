"""This module contains the AssemblyStorage class.

.. module:: assemblystorage
    :platform: Unix
    :synopsis: This class handles multiple instances of AssemblyDatabase.

.. moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# SQLAlchemy imports.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Inter-package imports.
from pynome.assemblydatabase import AssemblyDatabase
from pynome.assembly import Base


class AssemblyStorage:
    """Models a group of AssemblyDatabase instances.

    Provides functions for interacting with those instances.
    """

    def __init__(
            self,
            sqlite_path,
            sources=None,
            base_path=None,
            irods_base_path=None):
        """Initialization of the AssemblyStorage class.
        """
        # TODO: Comment the init function paramaters.
        # Define the public attributes of the class.
        self.base_path = base_path
        self.sources = sources

        # self.sqlite_session = sqlite_session
        self.irods_base_path = irods_base_path

        # Prepare the SQLite engine and session.
        self.engine = create_engine(sqlite_path)
        # Create the tables.
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)

    def crawl(self, assembly_database):
        """Call the crawl function on the given assembly_database.

        This the assembly database should return something for this class
        to handle saving.
        """
        # TODO: Impelment / plan me.
        retrieved_genomes = assembly_database.crawl()

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

        This is a local query.
        """
        pass

    def add_source(self, new_source):
        """Append a new source to the sources list."""
        pass

    def push_irods(self):
        """Pushes all the files within each source to an iRODs server.
        """
        pass
