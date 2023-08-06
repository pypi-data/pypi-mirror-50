#!/usr/bin/env python3
from setuptools import setup, find_packages
setup(
    name="virus_typer",
    version="0.0.0.3",
    packages=find_packages(),
    entry_points={
       'console_scripts': [
            'virustyper = virustyper.virustyper:main',
            'virustyper_create_db = virustyper.virustyper_db:main'
       ],
    },
    include_package_data=True,
    author="Adam Koziol",
    author_email="adam.koziol@canada.ca",
    url="https://github.com/adamkoziol/virustyper",
)
