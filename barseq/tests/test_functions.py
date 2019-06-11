#!/usr/bin/env python3

"""
Test module for testing functions in barseq.

"""

# Module import
from barseq.utils import read_barcodes, format_filename
from barseq.main import Run

__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"


def test_read_tab_delimited_barcodes():
    barcode_file = "barseq/tests/data/input/samples.csv"
    output_d = {'ATGAAGACTGTTGCCGTA': {'count': 0, 'gene': 'bar1'},
                'CACGACGCCCTCCGCGGA': {'count': 0, 'gene': 'bar2'},
                'ACTATTACGCAAAATAAT': {'count': 0, 'gene': 'bar3'},
                'ATGGAAGATATTATTATT': {'count': 0, 'gene': 'bar4'},
                'CCTCTCCAACCGGGTCTG': {'count': 0, 'gene': 'bar5'},
                'CCCGGTCGCCTAGCCCCG': {'count': 0, 'gene': 'bar6'},
                'GGCCCCCCGCCCGTCCCC': {'count': 0, 'gene': 'bar7'},
                'GGATCACTGCTAGCGTAT': {'count': 0, 'gene': 'bar8'},
                'CCTGCAGCAGCGGCCCGC': {'count': 0, 'gene': 'bar9'},
                'ACACATGCAGACATAGAG': {'count': 0, 'gene': 'bar10'},
                'CGCGCCATCCGCCGCCCA': {'count': 0, 'gene': 'bar11'},
                'AATATTCAGATGGGACGT': {'count': 0, 'gene': 'bar12'},
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
#     assert run.path == "results/experiment_test/"
#     assert type(run.sample_dict) == dict
