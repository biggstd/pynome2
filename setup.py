"""This is the setup script for Pynome.

It should install Pynome on the local system / environment.

#TODO: Add instructions on how to use this file.
"""


from setuptools import setup, find_packages


# A good blog entry on entry points:
# http://amir.rachum.com/blog/2017/07/28/python-entry-points/
# Run the setup function to install the program.

# TODO: Add proper instructions in here and in the README.md file.
setup(
    name='pynome',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        # TODO: List all of the required packages here.
        'Click',
        'SQLAlchemy'
    ],
    entry_points={
        # Console scripts are those that can be run directly from the terminal.
        # String entries here will be the cli invocation for their corresponding
        # python modulefiles:functions.
        'console_scripts': [
            'pynome = pynome.cli:pynome',
        ]
    }
)
