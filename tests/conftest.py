"""This module contains fixtures for pytest.

This file is read by pytest, so fixtures defined here do not need to
be imported in other test modules.

By default fixture functions are run for every test functino which uses them.
If we wish to change this behavior, the `scope` argument can be used. The
options for scope include 'module', 'session'.
"""

# Import testing package of choice.
import pytest

# Import Pynome-specific classes and functions.
from pynome.ensembldatabase import EnsemblDatabase
from pynome.assemblystorage import AssemblyStorage
from pynome.utils import read_json_config


@pytest.fixture
def test_config():
    """Load the test configuration .json file. This file is loaded from
    "test/test_config.json".
    """
    return read_json_config()
