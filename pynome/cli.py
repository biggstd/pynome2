"""This module contains the command line interface for Pynome.

.. module:: cli
    :platform: Unix
    :synopsis: This module contains the command line interface for
    Pynome.
"""

# General Python imports.
import click

# Inter-package imports.
from pynome.ensembldatabase import EnsemblDatabase
from pynome.assemblystorage import AssemblyStorage


@click.group()
def entry_point():
    """
    This is the function which the command line invocation
    of pynome calls, right now this does nothing but serve as
    a prefix to other pynome-specific commands.
    """
    pass


@entry_point.command()
def list():
    """List assemblies."""
    pass


@entry_point.command()
def download():
    """Download assembly files."""
    pass


@entry_point.command()
def prepare():
    """Prepare the downloaded files for further use."""
    pass


@entry_point.command()
def push_irods():
    """Push all of the local genome files to an iRODs server."""
    pass


@entry_point.command()
def discover():
    """Discover new genomes from a given source."""
    pass
