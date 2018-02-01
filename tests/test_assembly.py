"""Tests for the assembly.py module of Pynome.

"""

from pynome.assembly import Assembly


def test_assembly():
    """Tests for the Assembly class."""

    # Create an assembly.
    no_intra_assembly = Assembly(
        species='testerius',
        genus='genius',
    )

    assert no_intra_assembly.species == 'testerius'
