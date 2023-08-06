#!/usr/bin/env python3
from olctools.accessoryFunctions.accessoryFunctions import SetupLogging
from argparse import ArgumentParser
from glob import glob
import warnings
import os

# Import all the Biopython modules
from Bio import BiopythonParserWarning, BiopythonWarning, SeqIO, Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq

# Suppress certain Biopython warnings
warnings.simplefilter('ignore', BiopythonParserWarning)
warnings.simplefilter('ignore', BiopythonWarning)

__author__ = 'adamkoziol'


class VirusTypeDB(object):

    def main(self):
        self.load_database_sequences()
        if not os.path.isfile(self.allele_database):
            self.create_allele_database()

    def load_database_sequences(self):
        """
        Read in all the .gb files, and create a FASTA-formatted database of all sequences with dashes removed,
        as well as creating a set of all the dash-free sequences
        """
        with open(self.record_database, 'w') as record_db:
            for db_file in self.db_files:
                # Read in the records in GenBank format
                for record in SeqIO.parse(db_file, 'gb'):
                    # Remove any dashes from the sequence data
                    record.seq._data = record.seq._data.replace('-', '')
                    # Create the FASTA-formatted database file
                    SeqIO.write(record, record_db, 'fasta')
                    # Add the sequence data to a the set of all records
                    self.sequence_set.add(str(record.seq))

    def create_allele_database(self):
        """
        Create a FASTA file containing all the unique allele sequences encountered
        """
        with open(self.allele_database, 'w') as allele_database:
            # Use enumerate to extract the current iterator
            for i, allele in enumerate(self.sequence_set):
                # Pad the iterator to five digits
                allele_number = '{:05d}'.format(i)
                # Create a SeqRecord from the Seq object of the allele sequence with IUPAC unambiguous DNA
                record = SeqRecord(Seq(allele, IUPAC.unambiguous_dna),
                                   id=allele_number,
                                   description='')
                # Write the allele record to file
                SeqIO.write(record, allele_database, 'fasta')

    def __init__(self, db_path):
        if db_path.startswith('~'):
            self.db_path = os.path.abspath(os.path.expanduser(os.path.join(db_path)))
        else:
            self.db_path = os.path.abspath(os.path.join(db_path))
        assert os.path.isdir(self.db_path), 'Cannot locate supplied database path: {db_path}' \
            .format(db_path=self.db_path)
        self.db_files = sorted(glob(os.path.join(self.db_path, '*.gb')))
        assert self.db_files, 'Cannot located .gb database files in the supplied database path: {db_path}'\
            .format(db_path=self.db_path)
        self.sequence_set = set()
        self.record_database = os.path.join(self.db_path, 'virus_typer_sequences.fasta')
        self.allele_database = os.path.join(self.db_path, 'virus_typer_alleles.fasta')


def cli():
    parser = ArgumentParser(description='Perform virus typing')
    parser.add_argument('-db', '--dbpath',
                        required=True,
                        help='Path of folder containing .gb database files to process.')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Allow debug-level logging to be printed to the terminal')
    # Get the arguments into an object
    arguments = parser.parse_args()
    SetupLogging(debug=arguments.debug)
    virus_typer_db = VirusTypeDB(db_path=arguments.dbpath)
    virus_typer_db.main()


if __name__ == '__main__':
    cli()
