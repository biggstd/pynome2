"""This module contains the Assembly class used to model genome assemblies.

.. module:: assembly
    :platform: Unix
    :synopsis:

.. moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# Import general python packages.
import os


class Assembly:
    """Models a genome assembly for use by Pynome.

    Prepares identifier strings and filepaths based on its attributes. Also
    contains functions to prepare the assembly files (fasta and gff3) for
    use by creating a `.gff` file, finding splice sites, and creating an
    index with `hisat2`.
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable-msg=too-many-arguments

    def __init__(
            self,
            species,
            genus,
            intraspecific_name=None,
            assembly_id=None,
            version=None,
            gff3_remote_path=None,
            gff3_remote_size=None,
            fasta_remote_path=None,
            fasta_remote_size=None):
        """Assembly initialization requires only a species and genus.

        The remaining attributes and properties default to `None`.
        """

        # Declare public attributes, and assign them to the class instance.
        self.species = species
        self.genus = genus
        self.intraspecific_name = intraspecific_name
        self.assembly_id = assembly_id
        self.version = version
        self.gff3_remote_path = gff3_remote_path
        self.gff3_remote_size = gff3_remote_size
        self.fasta_remote_path = fasta_remote_path
        self.fasta_remote_size = fasta_remote_size

        # Declare private attributes for use by properties.
        self._taxonomy_id = None
        self._base_filename = None
        self._base_filepath = None

    @property
    def taxonomy_id(self):
        """Getter function for the assemblies taxonomy_id."""
        return '-'.join((self.base_filename, self.assembly_id))

    @property
    def base_filename(self):
        """Getter function for the assemblies base_filename.
        This is the filename used by Pynome to save assembly files locally.
        """
        if self.intraspecific_name is not None:
            name = '_'.join(
                (self.genus, self.species, self.intraspecific_name))
        else:
            name = '_'.join((self.genus, self.species))

        return '-'.join((name, self.assembly_id))

    @property
    def base_filepath(self):
        """Getter function for the base_filepath of this assembly.
        This is the path used to sort / save local assembly files.
        """
        if self.intraspecific_name is not None:

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
