#!/usr/bin/env python3

"""
Main pipeline for barseq software

"""

import os
from copy import deepcopy
import sys
import logging

# Module import
from .utils import write_output, read_barcodes, format_filename
from .process_reads import count_barcodes


__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"

# Get logger
logger = logging.getLogger("barseq")

class Run:
    """ Class that stores settings for barseq processes. """
    def __init__(self, args):
        self.experiment = args.experiment
        self.sequences = args.input
        self.barcodes = args.barcodes
        #self.barseq_sample_collection = list()
        self.sample_dict = dict()


class Cd:
    """ Context manager for moving directories. """
    def __init__(self, new_path):
        self.new_path = new_path

    def __enter__(self):
        self.old_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.old_path)


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
    Main pipeline for analyzing barseq data. Will be changed to be more modular, for now
    I just need the algorithm worked out.
    """
    # ---- SET UP SETTINGS ---- #
    runner = Run(args)

    # Read in barcode
    logger.info("Reading in barcodes from file")
    barcodes = read_barcodes(runner.barcodes)
    # for seq in os.listdir(runner.sequences):
    #     with Cd(runner.sequences):
    #         count_barcodes_df(seq, barcodes_dict)
    # Count barcodes in files
    for seq_file in os.listdir(runner.sequences):
        sample = format_filename(seq_file)
        logger.info(f"Counting Barcodes in {sample}")
        runner.sample_dict[sample] = deepcopy(barcodes)

        with Cd(runner.sequences):
            count_barcodes(seq_file, runner.sample_dict[sample])


    # Write to output
    logger.info("Writing results to")
    write_output(runner.sample_dict, barcodes, runner.experiment)

    # Confirm completion of barseq
    logger.info("***** barseq is complete! *****")
""" # -------- START HERE --------  # """
if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)

