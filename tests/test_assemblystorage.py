"""Tests for the assemblystroage.py module of Pynome.

"""

from pynome.assemblystorage import init_sql_db, AssemblyStorage
from pynome.assembly import Assembly


def test_init_sql_db():
    """Test the sqlite database initialization."""

    # Create an sqlite session in memory.
    test_session = init_sql_db('sqlite://')


# Don't run these both at the same time! It crashes.
def test_AssemblyStorage():
    """Test the AssemblyStorage class."""

    # Create an sqlite session in memory.
    test_session = init_sql_db('sqlite://')

    # Initialize an instance of AssemblyStorage with the test session.
    test_assembly_storage = AssemblyStorage(test_session)

    # Create an assembly.
    # no_intra_assembly = Assembly(species='testerius', genus='genius')
