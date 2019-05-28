#!/usr/bin/env python3

"""
Test module for testing functions in barseq.

"""

# Module import
from barseq.utils import *


__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"


def test_read_tab_delimited_barcodes():
    barcode_file = "data/input/samples.csv"
    output_d = {'AGGGCCATTTATATACC': ['fake1::bar1', 0], 'AGGGCCAGGGATATACC': ['fake2::bar2', 0],
                'ACCCCCATGTATATATC': ['fake3::bar3', 0]}

    assert output_d == read_barcodes(barcode_file)

