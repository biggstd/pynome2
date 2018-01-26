"""This module contains the Assembly class used to model genome assemblies.

.. module:: assembly
    :platform: Unix
    :synopsis:

.. moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""


class Assembly:
    """Models a genome assembly for use by Pynome.

    Prepares identifier strings and filepaths based on its attributes. Also
    contains functions to prepare the assembly files (fasta and gff3) for
    use by creating a `.gff` file, finding splice sites, and creating an
    index with `hisat2`.
    """

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

        # Declare private attributes for use by properties.
        self._pynome_id = None
        self._taxonomy_id = None
        self._base_filename = None
        self._base_filepath = None

    @property
    def pynome_id(self):
        """Getter function for the pynome_id attribute."""
        pass

    @property
    def taxonomy_id(self):
        """Getter function for the assemblies taxonomy_id."""
        pass

    @property
    def base_filename(self):
        """Getter function for the assemblies base_filename.
        This is the filename used by Pynome to save assembly files locally.
        """
        pass

    @property
    def base_filepath(self):
        """Getter function for the base_filepath of this assembly.
        This is the path used to sort / save local assembly files.
        """
        pass

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
