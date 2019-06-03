#!/usr/bin/env python3

"""
Test module for testing main barseq pipeline

"""

import subprocess
import filecmp
import os
import pathlib

# Module import
from .test_setup import temp_dir


__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"


def test_barseq(temp_dir):
    # Create testing paths
    input_sequence = temp_dir(["data", "input", "sequences"])
    input_barcodes = temp_dir(["data", "input", "samples.csv"])
    expected_output = temp_dir(["data", "output"])
    test_output = temp_dir(["results", "barseq_pytest"])
    experiment = "barseq_pytest"

    # Move into temp_dir
    os.chdir(temp_dir())
    # Call main with test data
    subprocess.call(["barseq",
                     "-i", input_sequence,
                     "-b", input_barcodes,
                     "-e", experiment])
    # Check output
    assert filecmp.dircmp(expected_output, test_output)
    assert filecmp.cmp(expected_output.joinpath("barcode_counts_table.csv"),
                       test_output.joinpath("barcode_counts_table.csv"))

