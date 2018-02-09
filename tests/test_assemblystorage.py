"""Tests for the assemblystroage.py module of Pynome.

"""
# import logging
#
from pynome.assemblystorage import AssemblyStorage
from pynome.assembly import Assembly


def test_AssemblyStorage(test_config, test_ed):
    """Test the AssemblyStorage class."""

    # Initialize an instance of AssemblyStorage with the test session.
    test_assembly_storage = AssemblyStorage(sqlite_path='sqlite:///:memory:')

    test_assembly_storage.sources.append(test_ed)

    test_assembly_storage.crawl(
        test_ed, test_config['ensembl_config']['test_urls'])

    test_assembly_storage.save_assemblies()

    print([a for a in test_assembly_storage.query_local_assemblies()])
