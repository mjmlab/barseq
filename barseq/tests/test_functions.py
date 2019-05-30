#!/usr/bin/env python3

"""
Test module for testing functions in barseq.

"""

# Module import
from BarSeq.utils import read_barcodes, format_filename
from BarSeq.main import Run

__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"


def test_read_tab_delimited_barcodes():
    barcode_file = "BarSeq/tests/data/input/samples.csv"
    output_d = {'AGGGCCATTTATATACC': {'count': 0, 'gene': 'gene1::bar1'},
                'AGGGCCAGGGATATACC': {'count': 0, 'gene': 'gene2::bar2'},
                'ACCCCCATGTATATATC': {'count': 0, 'gene': 'gene3::bar3'},
                '_other': {"gene": "_other", "count": 0}
                }
    assert output_d == read_barcodes(barcode_file)


def test_format_filename():
    assert "weird_file-name_" == format_filename("weird:_file-%$name_='][")
    assert "weird_file-name_" == format_filename("      weird:_file-%$name_='][")
    assert "weird_file-name_" == format_filename("weird:_file-%$name_='][     ")



# def test_Run_class():
#     run = Run("input_test", "barcodes_test", "experiment_test")
#     assert run.sequences == "input_test"
#     assert run.barcodes == "barcodes_test"
#     assert run.experiment == "experiment_test"
#     assert run.path == "results/experiment_test"
#     assert type(run.sample_dict) == dict
