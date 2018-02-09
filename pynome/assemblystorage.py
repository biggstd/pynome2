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
from pynome.assembly import Base
from pynome.assembly import Assembly


class AssemblyStorage:
    """Models a group of AssemblyDatabase instances.

    Provides functions for interacting with those instances.
    """

    def __init__(
            self,
            sqlite_path,
            base_path=None,
            irods_base_path=None):
        """Initialization of the AssemblyStorage class.
        """
        # TODO: Comment the init function paramaters.
        # Define the public attributes of the class.
        self.base_path = base_path
        self.sources = list()

        # self.sqlite_session = sqlite_session
        self.irods_base_path = irods_base_path
        Session = sessionmaker()

        # Prepare the SQLite engine and session.
        self.engine = create_engine(sqlite_path)
        # Create the tables.
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def save_assembly(self, new_assembly):
        """Go through the lists of Assemblies (within the list of sources)
        and save each of those assembly objects to the SQLite database.
        """
        self.session.merge(new_assembly)
        self.session.commit()

    def save_assemblies(self):
        """
        """
        for source in self.sources:
            for assembly in source.assemblies:
                self.save_assembly(assembly)

    def query_local_assemblies(self):
        """
        """
        query = self.session.query(Assembly).all()
        return query


    def crawl(self, assembly_database, urls):
        """Call the crawl function on the given assembly_database.

        This the assembly database should return something for this class
        to handle saving.
        """
        # TODO: Impelment / plan me.
        retrieved_genomes = assembly_database.crawl(urls)

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
