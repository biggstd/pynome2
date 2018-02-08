"""Tests for the assemblystroage.py module of Pynome.

"""
# import logging
#
from pynome.assemblystorage import AssemblyStorage
from pynome.assembly import Assembly


def test_AssemblyStorage():
    """Test the AssemblyStorage class."""

    # Initialize an instance of AssemblyStorage with the test session.
    test_assembly_storage = AssemblyStorage(
        sqlite_path='sqlite:///:memory:'
    )

    # Create an assembly.
    # no_intra_assembly = Assembly(species='testerius', genus='genius')
