"""This module contains the command line interface for Pynome.

.. module:: cli
    :platform: Unix
    :synopsis: This module contains the command line interface for
    Pynome.
"""

# General Python imports.
import click
from click.testing import CliRunner

# Inter-package imports.
from pynome.ensembldatabase import EnsemblDatabase
from pynome.assemblystorage import AssemblyStorage
from pynome.utils import read_json_config


@click.group()
def pynome():
    """
    This is the function which the command line invocation
    of pynome calls.

    This function is run whenever a sub-command of it is called. Since
    all of these requre the database to be initialized, the code to do
    so is placed here.
    """

    # Read the configuration file to get values for the databases.
    cfg = read_json_config()

    click.echo(cfg)


# Since it is bad form to redefine Python primatives, pass the
# `name` argument to the click command decorator.
@pynome.command(name='list')
def list_assemblies():
    """List assemblies."""
    pass


@pynome.command()
def download():
    """Download assembly files."""
    pass


@pynome.command()
def prepare():
    """Prepare the downloaded files for further use."""
    pass


@pynome.command()
def push_irods():
    """Push all of the local genome files to an iRODs server."""
    pass


@pynome.command()
def discover():
    """Discover new genomes from a given source."""
    pass
