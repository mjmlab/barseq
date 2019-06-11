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
from .utils import write_output, read_barcodes, format_filename, make_barseq_directories
from .process_reads import count_barcodes


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
        self.experiment = args.experiment
        self.sequences = Path(args.input)
        self.barcodes = Path(args.barcodes)
        # self.barseq_sample_collection = list()
        self.sample_dict = dict()
        self.path = f"results/{self.experiment}/"
        self.log = f"{self.path}log.txt"


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
    make_barseq_directories(runner)
    # Add file handler
    fh = logging.FileHandler(runner.log, mode="w")
    fh.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M"))
    logger.addHandler(fh)
    logger.info("***** Starting barseq *****")
    # Read in barcode
    logger.info(f"Reading in barcodes from {runner.barcodes.name}")
    barcodes = read_barcodes(runner.barcodes)
    # Process each sequencing file
    seq_files_list = sorted(os.listdir(runner.sequences))
    for seq_file in seq_files_list:
        if not seq_file.endswith(".DS_Store"):
            sample = format_filename(seq_file)
            logger.info(f"Counting Barcodes in {sample}")
            runner.sample_dict[sample] = deepcopy(barcodes)
            # Change cwd
            with Cd(runner.sequences):
                count_barcodes(seq_file, runner.sample_dict[sample])

    # TODO: Add basic analysis

    # Write to output
    logger.info(f"Writing results to {runner.path}")
    write_output(runner.sample_dict, barcodes, runner)

    # Confirm completion of barseq
    logger.info("***** barseq is complete! *****")


if __name__ == "__main__":

    """ # -------- START HERE --------  # """
    args = sys.argv[1:]
    main(args)

