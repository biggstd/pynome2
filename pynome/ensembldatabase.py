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
import itertools

# Inter-package imports.
from pynome.assembly import Assembly
from pynome.assemblydatabase import AssemblyDatabase
from pynome.utils import crawl_ftp_dir


# Define module level function(s).
# These functions are specific to the Ensembl module / use by the
# EnsemblDatabase class, but do not require an instance of self to be run.


def parse_ensembl_dir_line(in_line):
    """Parse an individual line item from an ftp.dir() call.

    This function splits a line retrieved from the ensembl ftp server
    from a call to ftp.dir().

    :param in_line:
        A filename (string). This function assumes these strings are from
        the Ensembl database, and parses them appropriately.

    :returns:
        A dictionary of keywords that can be used in the construction of a
        GenomeAssembly object.


    An example line is shown below::

        ``"drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename"
           [0]        [1][2]   [3]    [4]  [5] [6] [7]  [8] or [-1]``

    Parses a filename to retrieve the species, assembly, version and other
    information needed to greate a new instance of GenomeAssembly.

    The filenames themselves are assumed to be either gff3 or fasta files.
    Examples of these files, extracted from README files, are shown below.

    gff3 files::

        ``<species>.<assembly>.<_version>.gff3.gz``

    fasta files::

        ``<species>.<assembly>.<sequence type>.<id type>.<id>.fa.gz``
    """

    # Split the input string by whitespace.
    dir_list = in_line.split()

    # Pull needed information out of this list. It is always the last item.
    file_name = dir_list[-1]
    file_size = dir_list[4]

    # Split the file_name by the first two '.'.
    # This will give a string that contains the genus and species informaiton,
    # and a string that contains the assembly name.
    genus_species, assembly_name = file_name.split('.', 2)

    # Begin the parsing of the genus_species string. These strings can be
    # further split by intraspecific names and identifiers.
    try:

        # Split the genus and species by underscores.
        gen_species_list = genus_species.split('_')

        # Some entries have leading underscores -- this caueses 'None' to
        # appear in the list. 'None' entries must be removed.
        gen_species_list = list(filter(None, gen_species_list))

        # If the length of gen_species_list is greater than 2, an
        # intraspecific name is present.
        if len(gen_species_list) > 2:

            # intraspecific name is present, and should be the third
            # element in the list to the end of the list.
            intraspecific_name = '_'.join(gen_species_list[2:])

        # Otherwise there is no intraspecific name.
        else:

            # Set intraspecific_name to None.
            intraspecific_name = None

            # Get the genus and species from the gen_species_list.
            # Since there is no intraspecific name, simply split the list once.
            genus, species = genus_species.split('_', 1)

    except Exception as error:
        print('Unable to parse ensembl ftp filename.', error)

    # Return the dictionary of values parsed from the directory listing.
    return {
        'genus': genus,
        'assebly_name': assembly_name,
        'species': species,
        'intraspecific_name': intraspecific_name,
        'file_name': file_name,
        'file_size': file_size,
    }


# pylint: disable=too-many-instance-attributes


class EnsemblDatabase(AssemblyDatabase):
    """Class to handle the crawling, parsing and downloading of
    genome assembly files from the Ensembl database.
    """

    def __init__(self, ignored_dirs, data_types, ftp_url, kingdoms,
                 release_version, **kwargs):
        """The initialization function for EnsemblDatabase.

        Calls the constructor of AssemblyDatabase, and creates
        attributes and properties specific to the Ensembl database.

        :param ignored_dirs:
            Names of directories the crawler should never enter.

        :param ftp_url:
            The base URL of the ensembl FTP server to be connected to.

        :param data_types:
            The types of data to be considered. Used in construction of
            starting url paths for the crawler. Parsers only currenlty
            support the 'gff3' and 'fasta' data types.

        :param kingdoms:
            A list of genome kingdoms to be used in the construction of
            starting url paths. Available options include ['fungi', 'metazoa',
            'plants', 'protists']
        """

        # Call the parent constructor / __init__ function, pass keywords
        # to the parent constructor.
        super().__init__(**kwargs)

        # Define public attributes of the class.
        self.ftp = ftplib.FTP()
        self.ignored_dirs = ignored_dirs
        self.ftp_url = ftp_url
        self.data_types = data_types
        self.kingdoms = kingdoms
        self.release_version = release_version

        # Define private attributes of the class.
        self._metadata_uri = None
        self._top_dirs = None

    @property
    def metadata_uri(self):
        """Getter function for the metadata_uri property.

        Builds the sub-directory of the Ensembl FTP server wherein the
        species.txt metadata file can be found.
        """
        return '/'.join(('pub', self.release_version, 'species.txt'))

    @property
    def top_dirs(self):
        """Getter function for the top_dirs property.
            # Then this file is a fasta file.

        Builds a list of URIs that will act as the starting points for the
        crawling function.
        """

        # Create the list to be output.
        uri_list = list()

        # Generate the ordered pairs of datatypes and kingdoms.
        datatype_kingdom_pairs = itertools.product(
            self.data_types, self.kingdoms)

        # For each pair, generate the corresponding URI.
        for datatype, kingdom in datatype_kingdom_pairs:
            uri = '/'.join(('pub', kingdom, self.release_version, datatype, ''))
            uri_list.append(uri)

        # Return the list of uris.
        return uri_list

    def ensembl_file_parser(self, line, top_dir):
        """Examines a line and add creates a GenomeAssembly if appropriate.

        This function parses one 'line' at a time retrieved from an
        ``ftp.dir()`` command. This line has already been confirmed to
        not be a directory.

        :param line:
            An input line, described in detail below.

        :param top_dir:
            The parent directory.

        :param bad_dirs:
            A list of words / strings. Files found with these terms in
            them will be rejected by the parser.
        """

        # Parse the line.
        parsed_line = parse_ensembl_dir_line(line)

        # Examine the parsed output to determine if a GenomeAssembly object
        # should be created. Create a dictinoary of kwargs and filter off
        # any values of 'None', then use this dictinoaryto create a
        # new Assembly instance.
        if parsed_line['file_name'].endswith('dna.toplevel.fa.gz'):

            # Then this file is a fasta file.
            # Create the corresponding argument dictionary.
            # TODO: Write a private function for this.
            new_assembly_kwargs = {
                'species': parsed_line['species'],
                'genus': parsed_line['genus'],
                'intraspecific_name': parsed_line['intraspecific_name'],
                'assembly_id': parsed_line['assebly_name'],
                'version': self.release_version,
                'fasta_remote_path': ''.join((
                    top_dir, parsed_line['item_name'])),
                'fasta_remote_size': parsed_line['file_size'],
            }

            # Create the new Assembly object.
            new_genome_assembly = Assembly(**new_assembly_kwargs)

            # Append it to the assemblies list, which is defined in the
            # AssemblyDatabase parent class.
            self.assemblies.append(new_genome_assembly)

            # Exit the if loop.
            return


        elif parsed_line['file_name'].endswith('gff3.gz'):

            # Then this file is a gff3 file.
            new_assembly_kwargs = {
                'species': parsed_line['species'],
                'genus': parsed_line['genus'],
                'intraspecific_name': parsed_line['intraspecific_name'],
                'assembly_id': parsed_line['assebly_name'],
                'version': self.release_version,
                'gff3_remote_path': ''.join((
                    top_dir, parsed_line['item_name'])),
                'gff3_remote_size': parsed_line['file_size'],
            }

            # Create the new Assembly object.
            new_genome_assembly = Assembly(**new_assembly_kwargs)

            # Save the new Assembly object to the database.
            # TODO: This should also handle updates. ie. a single assembly
            # object should contain both fasta and gff3 information.

            # Append it to the assemblies list, which is defined in the
            # AssemblyDatabase parent class.
            self.assemblies.append(new_genome_assembly)

            # Exit the if loop.
            return

    def crawl(self):
        """Begin the Ensembl-specific crawl at...
        """

        # Connect to the FTP server and login with anonymous credentials.
        self.ftp.connect(self.ftp_url)
        self.ftp.login()

        # Start a crawl at each uri.
        for uri in self.top_dirs:
            crawl_ftp_dir(
                ftp=self.ftp,
                top_dir=uri,
                parsing_function=self.ensembl_file_parser,
                ignored_dirs=self.ignored_dirs
            )

        # Close the FTP connection.
        self.ftp.quit()
