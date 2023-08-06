#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
setup(
    name="virus_typer",
    version="0.0.0.2",
    scripts=[os.path.join('virustyper', 'virustyper.py')],
    packages=find_packages(),
    include_package_data=True,
    author="Adam Koziol",
    author_email="adam.koziol@canada.ca",
    url="https://github.com/adamkoziol/virustyper",
)
