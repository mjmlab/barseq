#!/usr/bin/env python3

"""
Test module for testing main barseq pipeline

"""

import subprocess

# Module import
from .test_setup import temp_dir


__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"


def test_barseq(temp_dir):
    input_sequence = temp_dir(["input", "sequences"])
    input_barcodes = temp_dir(["input", "samples.csv"])
    output_dir = temp_dir(["output"])

    # Call main with test data
    subprocess.call(["barseq",
                     "-i", input_sequence,
                     "-b", input_barcodes,
                     "-e", output_dir])

