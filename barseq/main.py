#!/usr/bin/env python3

"""
Main pipeline for barseq software

"""

import os
from copy import deepcopy
import sys
import logging
from pathlib import Path

# Module import
from .utils import *
from .process_reads import *


__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"

# Get logger
logger = logging.getLogger("barseq")


class Cd:
    """ Context manager for moving directories. """
    def __init__(self, new_path):
        self.new_path = new_path

    def __enter__(self):
        self.old_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.old_path)


class Run:
    """ Class that stores settings for barseq processes. """
    def __init__(self, args):
        # Required parameters
        self.experiment = args.experiment
        self.sequence_dir = Path(args.input)
        self.sequence_files = Path(self.sequence_dir)
        self.barcodes = args.barcodes
        self.sample_ids = read_sample_ID(Path(args.samples))
        self.reference_free = args.reference_free
        # Settings for sequence search
        self.flanking_left = args.flanking_left
        self.flanking_right = args.flanking_right
        self.barcode_length = args.barcode_length
        self.pattern = f"({self.flanking_left}){{e<=1}}([ATGC]{{18}})({self.flanking_right}){{e<=1}}"
        # If barcoded provided
        if not self.reference_free:
            if not Path(self.barcodes).exists():
                logger.error('Reference barcode library provided does not exist. '
                             'If you do not have one, run --reference-free')
            self.barcodes = Path(args.barcodes)
        # If barcodes provided, grab sample
        if self.reference_free:
            if not Path(args.samples).exists():
                logger.error("You selected to run barseq using --reference-free "
                             "but did not provide a file for sample names")
            self.min_count = args.min_count
        # self.barseq_sample_collection = list()
        self.sample_dict = dict()
        self.path = Path(args.output).joinpath(f'results/{self.experiment}')
        self.log = self.path.joinpath('log.txt')
        self.force = args.force

    def get_sample_name(self, seq_tag):
        """ Gets sample id given the sequence file tag"""
        # TODO: Use grep or regex to find the tag, may be given different ones
        return self.sample_ids[seq_tag.name.split('_')[0]]


class SampleRecord:
    """ Class for storing sample properties. """
    def __init__(self, sample: str, filename: str, barcode_dict):
        self.sample = sample
        self.filename = filename
        self.barcode_dict = deepcopy(barcode_dict)
        self.LEFT_SEQUENCE = ""
        self.RIGHT_SEQUENCE = ""


def main(args) -> None:
    """
    Main pipeline for analyzing barseq data. Will be changed to be more modular

    """
    # ---- SET UP SETTINGS ---- #
    runner = Run(args)
    make_barseq_directories(runner)

    # Add file handler
    fh = logging.FileHandler(runner.log, mode="w")
    fh.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M"))
    logger.addHandler(fh)

    logger.info("***** Starting barseq *****")

    # Read in barcode if needed
    if runner.reference_free:
        logger.info('Will find putative unique barcodes and count without referencing a library')

    else:
        logger.info(f"Reading in barcodes from {runner.barcodes.name}")
        barcodes = read_barcodes(runner.barcodes)

    # Process each sequencing file
    data_collection = []
    for seq_file in runner.sequence_files.glob('*R1*'):
        # Split seq_file name into its suffixes
        if '.fastq' in seq_file.suffixes or '.gz' in seq_file.suffixes:
            sample = runner.get_sample_name(seq_file)
            logger.info(f"Counting Barcodes in {sample}")
            # IF GIVEN BARCODES
            if not runner.reference_free:
                runner.sample_dict[sample] = deepcopy(barcodes)
                count_barcodes(seq_file, runner.sample_dict[sample], runner)
                # Write to output
                logger.info(f"Writing results to {runner.path}")
            # REFERENCE FREE
            if runner.reference_free:
                # Skip control and undetermined fastq files
                if seq_file.stem.startswith('Undetermined_S0') or seq_file.stem.startswith('S1000'):
                    pass
                else:
                    # Find sample name
                    sample_name = runner.get_sample_name(seq_file)
                    barcode_counts_dict, good_barcode_counts = count_barcodes_reference_free(seq_file=seq_file, runner=runner)
                    # Calculate stats on barcode counts
                    stats_barcode_dict = calculate_barcode_perc(barcode_counts_dict,
                                                                total_barcodes=good_barcode_counts,
                                                                min_count=runner.min_count)

                    # Get formatted row
                    row = format_sample_data(stats_barcode_dict, good_barcode_counts, sample_id=sample_name)
                    data_collection.append(row)

    if data_collection:
        save_results(data_collection, runner)

    else:
        write_output(runner.sample_dict, runner)

    # Confirm completion of barseq
    logger.info("***** barseq is complete! *****")


if __name__ == "__main__":
    """ # -------- START HERE --------  # """
    args = sys.argv[1:]
    main(args)

