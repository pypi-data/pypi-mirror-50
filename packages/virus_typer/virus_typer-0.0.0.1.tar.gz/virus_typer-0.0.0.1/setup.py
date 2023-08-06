#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
setup(
    name="virus_typer",
    version="0.0.0.1",
    scripts=[os.path.join('virustyper', 'virustyper.py')],
    data_files=[('databases',
                 [os.path.join('virustyper', 'forward_typing_primers.fasta'),
                  os.path.join('virustyper', 'reverse_typing_primers.fasta'),
                  os.path.join('virustyper', 'virus_typer_alleles.fasta')])],
    packages=find_packages(),
    include_package_data=True,
    author="Adam Koziol",
    author_email="adam.koziol@canada.ca",
    url="https://github.com/adamkoziol/virustyper",
)
