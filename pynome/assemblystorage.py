"""This module contains the AssemblyStorage class.

.. module:: assemblystorage
    :platform: Unix
    :synopsis: This class handles multiple instances of AssemblyDatabase.

.. moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# General Python imports.
import os
import subprocess

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
            sqlite_path=None,
            base_path=None,
            irods_base_path=None):
        """Initialization of the AssemblyStorage class.

        :param [sqlite_path]:
            The local path to the sqlite database used to store metadata of
            the found genome assemblies. If no value is given, this defaults
            to `"sqlite:///genomes.db"`.

        :param base_path:
            The local filepath where Pynome will save its files. If no value
            is given, the file "Genomes" will be created and used within the
            current working directory.

        :param irods_base_path:
            The base path to be used with iRODs integration.
        """

        # If the sqlite path is not give, create one in the current directory.
        if sqlite_path is None:
            sqlite_path = "sqlite:///genomes.db"

        self.sqlite_path = sqlite_path

        # If no base_path is given, creata a folder named "Genomes" in
        # the current working directory for use as the base_path.
        if base_path is None:
            base_path = 'genomes'

        self.base_path = base_path

        # Define the public attributes of the class.
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
        """Save a given assembly object to the SQLite database.

        :param new_assembly:
            A pynome.Assembly object to be saved in the local sql database.
        """
        self.session.merge(new_assembly)
        self.session.commit()

    def save_assemblies(self):
        """Save a list of assembly objects to the SQLite database.
        """
        for source in self.sources:
            for assembly in source.assemblies:
                self.save_assembly(assembly)

    def update_assembly(self, assembly_base_filename, update_dict):
        """
        TODO: Write test for this function, currently untested.
        """
        self.session.query(Assembly).filter_by(
            base_filename=assembly_base_filename).update(update_dict)


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
        assembly_database.crawl(urls)

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
        for src in self.sources:
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

    def decompress(self, assembly):
        """Decompress (GNU Unzip) a single set of assembly files.

        :param assembly:
            An assembly object stored within the local SQLite database.
        """

        fasta_gz = os.path.join(
            self.base_path,
            assembly.base_filepath,
            assembly.base_filename + '.fa.gz')

        gff3_gz = os.path.join(
            self.base_path,
            assembly.base_filepath,
            assembly.base_filename + '.gff3.gz')

        cmd = ['gunzip', '-f', fasta_gz]
        subprocess.run(cmd)

        cmd = ['gunzip', '-f', gff3_gz]
        subprocess.run(cmd)

    def hisat_index(self, assembly):
        """Generate hisat2 indecies for a given assembly.

        This function calls `hisat2-build -f` from the command line.

        See the HISAT2 manual for more:
        https://ccb.jhu.edu/software/hisat2/manual.shtml#running-hisat2

        :param assembly:
            An assembly object stored within the local SQLite database.
        """

        # Construct the path to the input file.
        file_path = os.path.join(
            self.base_path,
            assembly.base_filepath,
            assembly.base_filename + '.fa')

        # Construct the base filename of the output files.
        out_base = os.path.join(
            self.base_path,
            assembly.base_filepath,
            assembly.base_filename)

        # Count the number of processors available to HISAT2. This value must
        # be a string for it to function within subprocess.run().
        # TODO: Make this value an option within the .json config file.
        numb_proc = str(os.cpu_count())

        cmd = ['hisat2-build', '--quiet', '-p', numb_proc,
               '-f', file_path, out_base]

        subprocess.run(cmd)

    def gtf(self, assembly):
        """Generates a `.gtf` file from a corresponding `.gff3` file.

        :param assembly:
            An assembly object stored within the local SQLite database.
        """
        gff3_file = os.path.join(
            self.base_path,
            assembly.base_filepath,
            assembly.base_filename)

        cmd = ['gffread', '-T', gff3_file + '.gff3', '-o', gff3_file + '.gtf']

        subprocess.run(cmd)

    def splice_site(self, assembly):
        """Generates the splice sites of a given assembly from a `.gtf` file.

        :param assembly:
            An assembly object stored within the local SQLite database.
        """
        gft_file = os.path.join(
            self.base_path,
            assembly.base_filepath,
            assembly.base_filename + '.gtf')

        splice_output = os.path.join(
            self.base_path,
            assembly.base_filepath,
            assembly.base_filename + '.Splice_sites')

        with open(splice_output, 'w') as f:
            cmd = ['hisat2_extract_splice_sites.py', gft_file]

            subprocess.run(cmd, stdout=f)
