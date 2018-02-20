"""Tests for the assemblystroage.py module of Pynome.

"""
# import logging
#
from pynome.assemblystorage import AssemblyStorage
from pynome.assembly import Assembly


def test_AssemblyStorage(test_config, test_ed):
    """Test the AssemblyStorage class.

    This is the primary test case for now.
    """

    # Initialize an instance of AssemblyStorage with the test session.
    test_assembly_storage = AssemblyStorage(
        sqlite_path=test_config["storage_config"]["sqlite_path"],
        base_path=test_config["storage_config"]["base_path"])

    # Add the test EnsemblDatabase fixture to the sources list.
    test_assembly_storage.sources.append(test_ed)

    # Initiate a crawl through the AssemblyStorage API.
    test_assembly_storage.crawl(
        test_ed, test_config['ensembl_config']['test_urls'])

    # Download the metadata file.
    # TODO: Consider API linkage to the crawl command.
    test_ed.download_metadata()

    # Save those assemblies found.
    test_assembly_storage.save_assemblies()

    # Get a list of all asemblies found by the crawl.
    assemblies_from_crawl = test_assembly_storage.query_local_assemblies()

    # Search for matching taxonomy IDs within the species.txt metadata file,
    # and update the assemblies with that information.
    tax_id_update = test_ed.add_taxonomy_ids(assemblies_from_crawl)


    # Save (update) each of these assembly ids.
    for pk, update_dict in tax_id_update:
        test_assembly_storage.update_assembly(pk, update_dict)

    # Assign all found genomes to a list.
    found_genomes = test_assembly_storage.query_local_assemblies()

    # print([a for a in found_genomes])

    # Download these found genome files.
    test_ed.download(
        found_genomes,
        test_config["storage_config"]["base_path"])

    # Display all entries.
    # print([a for a in found_genomes])

    for a in found_genomes:
        test_assembly_storage.decompress(a)
        test_assembly_storage.hisat_index(a)
        test_assembly_storage.gtf(a)
        test_assembly_storage.splice_site(a)
