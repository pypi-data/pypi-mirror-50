#!/usr/bin/env python3
from olctools.accessoryFunctions.accessoryFunctions import make_path, MetadataObject, SetupLogging, run_subprocess
from argparse import ArgumentParser
from glob import glob
import statistics
import warnings
import json
import os

# Import all the Biopython modulese
from Bio import BiopythonParserWarning, BiopythonWarning, SeqIO, Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq

# Suppress certain Biopython warnings
warnings.simplefilter('ignore', BiopythonParserWarning)
warnings.simplefilter('ignore', BiopythonWarning)

__author__ = 'adamkoziol'


class VirusTyping(object):

    def main(self):
        self.file_list()
        self.file_parse()
        self.primer_load()
        self.primer_trim()
        self.parse_reports()
        self.load_trimmed_sequence()
        self.load_allele_database()
        self.type_alleles()
        self.update_alleles()
        self.report()

    def file_list(self):
        """
        Create metadata objects for every .ab1 file in the supplied sequence path
        """
        # Glob and sort a list of all the paths to the .ab1 files
        file_list = sorted(glob(os.path.join(self.sequencepath, '*.ab1')), reverse=True)
        for seq_file in file_list:
            # P19954_2019_VI482_11_GI_B03_M13-R17_E10_072.ab1
            file_name = os.path.splitext(os.path.basename(seq_file))[0]
            # Create a metadata object for each sample
            sample = MetadataObject()
            sample.name = file_name
            sample.filepath = seq_file
            self.samples.append(sample)

    def file_parse(self):
        """
        Use SeqIO to read in .ab1 files, parse the raw sequence, and convert the file to FASTQ format for downstream
        processing
        """
        for sample in self.samples:
            # Create attributes
            sample.fastq = sample.filepath.replace('.ab1', '.fastq')
            sample.rev_comp_fastq = sample.fastq.replace('.fastq', '_rev_comp.fastq')
            with open(sample.fastq, 'w') as fastq:
                # Read in the .ab1 file
                for record in SeqIO.parse(sample.filepath, 'abi'):
                    # Store the string of the raw sequence
                    sample.raw_seq = str(record.seq)
                    # Output the record in FASTQ format
                    SeqIO.write(record, fastq, 'fastq')

    def primer_load(self):
        """
        Use SeqIO to read in the primers used for virus typing
        """
        for primer_file in [self.forward_primers, self.reverse_primers]:
            # Set the directionality of the primers
            direction = 'forward' if primer_file == self.forward_primers else 'reverse'
            # Create a set of the primer sequences for the current direction
            self.primer_sequences[direction] = set()
            for record in SeqIO.parse(primer_file, 'fasta'):
                # Add the string of the sequence to the set
                self.primer_sequences[direction].add(str(record.seq))

    def primer_trim(self):
        """
        Use cutadapt to trim the raw FASTQ sequence with the 5` and 3` primer files
        """
        # Run cutadapt with the following arguments: -g: 5` adapters, -a: 3` adapters, -n: remove up to two adapters
        # from the read,
        for sample in self.samples:
            # Create the necessary attributes
            sample.trimmed_fastq = os.path.join(self.sequencepath, '{sn}_trimmed.fastq'.format(sn=sample.name))
            sample.cutadapt_report = os.path.join(self.sequencepath, '{sn}_cutadapt_report.txt'.format(sn=sample.name))
            sample.cutadapt_out = str()
            sample.cutadapt_err = str()
            sample.cutadapt_cmd = 'cutadapt -g file:{forward_primers} -a file:{reverse_primers} -n 2 ' \
                                  '{fastq_file} -o {trimmed_fastq} 1> {report}'\
                .format(forward_primers=self.forward_primers,
                        reverse_primers=self.reverse_primers,
                        fastq_file=sample.fastq,
                        trimmed_fastq=sample.trimmed_fastq,
                        report=sample.cutadapt_report)
            # Run the system call if the trimmed output file doesn't exist
            if not os.path.isfile(sample.trimmed_fastq):
                # Store the stdout and stderr to attributes
                sample.cutadapt_out, sample.cutadapt_err = run_subprocess(command=sample.cutadapt_cmd)

    def parse_reports(self):
        """
        Parse the cutadapt reports to extract which primers were used to trim the raw sequence. Also determine whether
        the sequence is in reverse complement orientation
        :return:
        """
        for sample in self.samples:
            # Read in the report as a list
            report = open(sample.cutadapt_report, 'r').readlines()
            # Initialise temporary variables to store values related to primer trimming
            adapter = str()
            primers = dict()
            # Create the attributes
            sample.primer_matches = {
                'forward': dict(),
                'reverse': dict()
            }
            # Iterate through the list of the report
            for line in report:
                # Ignore empty lines
                if line != '\n':
                    # Strip off newline characters
                    line = line.rstrip()
                    # === Adapter NOVGI_QNIF4_F ===
                    if '=== Adapter ' in line:
                        # Extract the adapter name from the line
                        adapter = line.split()[2]
                    # Sequence: CGCTGGATGCGNTTCCAT; Type: regular 5'; Length: 18; Trimmed: 1 times.
                    if '1 times.' in line:
                        # Extract the sequence from the line
                        sequence = line.split()[1].strip(';')
                        # Update the dictionary with primer name: primer sequence
                        primers[adapter] = sequence
            # Figure out the orientation of the sequence
            for primer_name, primer_sequence in primers.items():
                # Bin primers based on whether they are forward (end with 'F') or reverse (end with 'R')
                if primer_name.endswith('F'):
                    # Update the sample dictionary with the primer information
                    sample.primer_matches['forward'][primer_name] = primer_sequence
                    # If the primer sequence is not in the set of all forward primers, then it must be in reverse
                    # complement orientation
                    if primer_sequence in self.primer_sequences['forward']:
                        # Update the attribute to reflect that the primer sequence was found in the set
                        sample.orientation = 'normal'
                    else:
                        # Set the attribute
                        sample.orientation = 'reverse_complement'
                # Update the dictionary for the reverse primer as well
                else:
                    sample.primer_matches['reverse'][primer_name] = primer_sequence

    def load_trimmed_sequence(self):
        """
        Use SeqIO to read in the cutadapt output FASTQ file
        """
        for sample in self.samples:
            with open(sample.trimmed_fastq, 'r') as trimmed_fastq:
                for record in SeqIO.parse(trimmed_fastq, 'fastq'):
                    # Create a variable to store the unwieldy quality scores
                    quality = record.letter_annotations['phred_quality']
                    # Calculate the mean and standard deviation of the quality scores
                    sample.trimmed_quality_mean = '{:.2f}'.format(statistics.mean(quality))
                    sample.trimmed_quality_stdev = '{:.2f}'.format(statistics.stdev(quality))
                    # Extract the max and min quality scores
                    sample.trimmed_quality_max = str(max(quality))
                    sample.trimmed_quality_min = str(min(quality))
                    # Extract the trimmed sequence in the appropriate orientation
                    if sample.orientation == 'reverse_complement':
                        sample.trimmed_seq = str(record.reverse_complement().seq)
                    else:
                        sample.trimmed_seq = str(record.seq)

    def load_allele_database(self):
        """
        Read in the database of all virus alleles
        """
        with open(self.allele_database, 'r') as allele_database:
            for record in SeqIO.parse(allele_database, 'fasta'):
                self.allele_dict[str(record.seq)] = record.id
                # Store the last allele number in case this file needs to be updated later
                self.max_allele = int(record.id)

    def type_alleles(self):
        """
        Find exact matches to previously record alleles. If there are no matches, prepare the allele to be entered
        into the database
        """
        for sample in self.samples:
            # Test to see if the allele is already in the database
            try:
                # Set the allele number as the extracted value
                sample.allele = self.allele_dict[sample.trimmed_seq]
            except KeyError:
                # If this is a new allele, see if it has already been entered into the new allele dictionary by another
                # sample from the current analysis
                try:
                    sample.allele = self.new_alleles[sample.trimmed_seq]
                # If this is the first time this allele has been encountered, add it to the dictionary with the
                # appropriately formatted allele number
                except KeyError:
                    # Increment the max allele, as this new allele is now has the highest number of observed alleles
                    self.max_allele += 1
                    sample.allele = '{:05d}'.format(self.max_allele)
                    self.new_alleles[sample.trimmed_seq] = sample.allele

    def update_alleles(self):
        """
        If there are new alleles, add them to the database with SeqIO
        """
        if self.new_alleles:
            with open(self.allele_database, 'a+') as allele_database:
                for allele_sequence, allele_number in self.new_alleles.items():
                    # Create a SeqRecord with a Seq object of the allele sequence as IUPAC unambiguous DNA
                    record = SeqRecord(Seq(allele_sequence, IUPAC.unambiguous_dna),
                                       id=allele_number,
                                       description='')
                    # Update the database
                    SeqIO.write(record, allele_database, 'fasta')

    def report(self):
        """
        Create a JSON-formatted report
        """
        for sample in self.samples:
            # Add the sample to the output dictionary as sample name: attribute name: attribute: value
            self.output_dict[sample.name] = sample.dump()
            # Remove the 'unwanted keys' key from the dictionary, as this is only useful for metadata objects
            self.output_dict[sample.name].pop('unwanted_keys', None)
        # Open the metadata file to write
        with open(self.json_report, 'w') as metadatafile:
            # Write the json dump of the object dump to the metadata file
            json.dump(self.output_dict, metadatafile, sort_keys=True, indent=4, separators=(',', ': '))

    def __init__(self, sequencepath, reportpath):
        # Allow for relative paths
        if sequencepath.startswith('~'):
            self.sequencepath = os.path.abspath(os.path.expanduser(os.path.join(sequencepath)))
        else:
            self.sequencepath = os.path.abspath(os.path.join(sequencepath))
        assert os.path.isdir(self.sequencepath), 'Cannot locate supplied sequence path: {seq_path}'\
            .format(seq_path=self.sequencepath)
        if reportpath.startswith('~'):
            self.reportpath = os.path.abspath(os.path.expanduser(os.path.join(reportpath)))
        else:
            self.reportpath = os.path.abspath(os.path.join(reportpath))
        make_path(self.reportpath)
        assert os.path.isdir(self.reportpath), 'Could not create the requested report directory: {rep_path}'\
            .format(rep_path=self.reportpath)
        # Initialise class variables
        self.max_allele = int()
        self.samples = list()
        self.allele_dict = dict()
        self.record_dict = dict()
        self.output_dict = dict()
        self.new_alleles = dict()
        self.primer_sequences = dict()
        self.json_report = os.path.join(self.reportpath, 'virus_typer_outputs.json')
        # Extract the path of this file - will be used to find the necessary accessory files
        self.homepath = os.path.split(os.path.abspath(__file__))[0]
        self.forward_primers = os.path.join(self.homepath, 'forward_typing_primers.fasta')
        self.reverse_primers = os.path.join(self.homepath, 'reverse_typing_primers.fasta')
        self.allele_database = os.path.join(self.homepath, 'virus_typer_alleles.fasta')


def cli():
    parser = ArgumentParser(description='Perform virus typing')
    parser.add_argument('-s', '--sequencepath',
                        required=True,
                        help='Path of folder containing .ab1 files to process.')
    parser.add_argument('-r', '--reportpath',
                        required=True,
                        help='Path in which reports are to be created')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Allow debug-level logging to be printed to the terminal')
    # Get the arguments into an object
    arguments = parser.parse_args()
    SetupLogging(debug=arguments.debug)
    virus_typer = VirusTyping(sequencepath=arguments.sequencepath,
                              reportpath=arguments.reportpath)
    virus_typer.main()


if __name__ == '__main__':
    cli()
