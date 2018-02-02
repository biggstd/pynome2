"""This module contains the AssemblyStorage class.

.. module:: assemblystorage
    :platform: Unix
    :synopsis: This class handles multiple instances of AssemblyDatabase.

.. moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# General Python imports.
import os

# SQLAlchemy imports
from sqlalchemy import Table, MetaData, Column, String, Integer, create_engine
from sqlalchemy.orm import mapper, sessionmaker

# Inter-package imports.
from pynome.assemblydatabase import AssemblyDatabase
from pynome.assembly import Assembly


def init_sql_db(sql_path):
    """Initialize a local SQLite database to track Assemblies.

    This function maps the Assembly class to an SQL table, then creates
    or loads an sqlite database at the given `sql_path`.

    :param sql_path:
        A filepath where the sqlite database should be loaded from,
        or created at.

    :returns:
        An instance of Session from SQLAlchemy for accessing the databse.
    """

    # SQLalchemy Metadata object.
    metadata = MetaData()

    # TODO: Pick a primary key! primary_key=True
    # SQLAlchemy table and mapper for the Assembly object.
    assembly_table = Table(
        'Assemblies',
        metadata,
        # The base_filename attribute is the most unique name.
        Column('base_filename', String()),
        Column('species', String(), primary_key=True),
        Column('genus', String()),
        Column('intraspecific_name', String()),
        Column('assembly_id', String()),
        Column('version', String()),
        Column('gff3_remote_path', String()),
        Column('gff3_remote_size', Integer()),
        Column('fasta_remote_path', String()),
        Column('fasta_remote_size', Integer()),
        Column('taxonomy_id', String()),
        Column('base_filepath', String()),
    )

    # Create the database engine. This function returns an instance of
    # `Engine`. It is the core interface to the database.
    engine = create_engine(sql_path)

    # Use the metadata object to create and bind the sql table(s).
    metadata.create_all(engine)

    # Now instantiate the session class.
    # Define a Session class, which will be our access point to the
    # sqlite databse.
    session = sessionmaker(bind=engine)

    # Map the Assembly class to the Table object created above. This must be
    # done after the above commands. The documentation is very unclear.
    mapper(Assembly, assembly_table)

    return session


class AssemblyStorage:
    """Models a group of AssemblyDatabase instances.

    Provides functions for interacting with those instances.
    """

    def __init__(
            self,
            sqlite_session,
            sources=None,
            base_path=None,
            irods_base_path=None):
        """Initialization of the AssemblyStorage class.
        """
        # TODO: Comment the init function paramaters.
        # Define the public attributes of the class.
        self.base_path = base_path
        self.sqlite_session = sqlite_session
        self.irods_base_path = irods_base_path

        # Prepare the sources attribute, ensure it is a list.
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
