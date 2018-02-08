"""This module contains the Assembly class used to model genome assemblies.

.. module:: assembly
    :platform: Unix
    :synopsis:

.. moduleauthors:: Tyler Biggs <biggstd@gmail.com>
"""

# TODO: Refactor this to use the SQLAlchemy ORM declaration.

# Import general python packages.
import os

# SQLAlchemy imports.
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

# Create the declarative base class.
Base = declarative_base()


class Assembly(Base):
    """Models a genome assembly for use by Pynome.

    Prepares identifier strings and filepaths based on its attributes. Also
    contains functions to prepare the assembly files (fasta and gff3) for
    use by creating a `.gff` file, finding splice sites, and creating an
    index with `hisat2`.
    """

    __tablename__ = 'Assemblies'

    def __init__(self, species, genus, assembly_id, intraspecific_name=None):
        """Initialization of the Assembly model class. Builds the primary
        key to be used by the SQLite database.

        :param species:

        :param genus:

        :param assembly_id:

        :param intraspecific_name:
        """
        self.species = species
        self.genus = genus
        self.assembly_id = assembly_id
        self.intraspecific_name = intraspecific_name

        self.base_filename = None

        if intraspecific_name is not None:
            name = '_'.join((
                self.genus,
                self.species,
                self.intraspecific_name
            ))
        else:
            name = '_'.join((self.genus, self.species))

        self.base_filename = '-'.join((name, self.assembly_id))

    # Declare public attributes, and assign them to the class instance.
    # Columns declared in this way can be accessed as if they were
    # self.column_name, that is, the same as other attributes.
    base_filename = Column(String, primary_key=True)
    species = Column(String)
    genus = Column(String)
    intraspecific_name = Column(String)
    assembly_id = Column(String)
    version = Column(String)
    gff3_remote_path = Column(String)
    gff3_remote_size = Column(Integer)
    fasta_remote_path = Column(String)
    fasta_remote_size = Column(Integer)
    taxonomy_id = Column(String)

    # Declare private attributes for use by properties.
    # base_filename = Column(String)
    # base_filepath = Column(String)

    @hybrid_property
    def base_filepath(self):
        """Getter function for the base_filepath of this assembly.
        This is the path used to sort / save local assembly files.
        """
        # Use the os path module to ensure the path is
        # generated correctly for the system we are on.
        os.path.join(self.base_filename, self.assembly_id)

    def update(self):
        """Update the current assembly with new information.
        TODO: Determine what to do with new files to download.
        """
        pass

    def delete(self):
        """Delete the assembly.
        """
        pass

    def prepare(self):
        """Prepare the assembly for downstream use. This creates
        splice sites, hisat2 indexes and converts the gff3 to a gtf.
        """
        pass
