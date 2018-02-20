# Pynome

Pynome, a Python command line interface tool, provides the user with a way to
download desired genome assembly files from the
[Ensembl](https://www.ensembl.org/) database.


## TODO

- [x] Gather TODOs.
- [x] Add metadata json files - one with pynome info, the other with ensembl info.
- [x] Factor out cd from prepare methods.
- [x] Docstring for prepare methods.
- [x] Update hisat2 indexing to use more than one CPU.
- [ ] Change use of FTP to context manager and re-factor download functions.
- [ ] Consider API linkage to the crawl command.
- [ ] assembly.delete()
- [ ] assembly.prepare()
- [ ] assembly.update()
- [ ] assemblystorage.update() -- test function.
- [ ] assemblystorage.download()
- [ ] assemblystorage.find_assembly()
- [ ] assemblystorage.add_source()
- [ ] assemblystorage.push_irods()
- [ ] Create api for selecting assemblies by:
  + Species
  + Genus
  + Intraspecific_name
  + Assembly_ID
- [ ] Consider the changes needed to the CLI for SRA functionality.
- [ ] cli.push_irods()


## Installation

- [ ] Go over setup.py
- [ ] Write instructions.
- [ ] Create Docker image.
