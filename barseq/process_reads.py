#!/usr/bin/env python3

"""
Count barcode frequency in fastq/fasta files given by user.

"""

import screed
import logging

# Module import
from .utils import sequence_distance

__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"

# Get logger
logger = logging.getLogger("barseq")

# Sequences used to confirm flanking DNA of barcode position.
LEFT_FLANK = "GCTCATGCACTTGATTCC"
RIGHT_FLANK = "GACTTGACCTGGATGTCT"


def count_barcodes(seq_file, barcode_dict) -> None:
    """
    Count barcode frequency in sequence file.
    Returns a DataFrame object

    :param seq_file: file with reads
    :param barcode_dict: barcode dictionary of sample
    :return:
    """
    # Grab left and right matching sequence
    barcode_ls = barcode_dict.keys()

    # Open sequence file
    with screed.open(seq_file) as reads:
        for read in reads:
            # Verbose
            seq = read.sequence
            if any(bar in seq for bar in barcode_ls):
                barcode = "".join([bar for bar in barcode_ls if bar in seq])
                # Check flanking sequences
                barcode_index = seq.index(barcode)
                split_sequence = read.sequence.split(barcode)

                # TODO: Finish matching check with flanking sequences
                left = split_sequence[0][barcode_index - 18: barcode_index]
                right = split_sequence[1][0:18]

                if LEFT_FLANK != left or RIGHT_FLANK != right:
                    #print(sequence_distance(right, RIGHT_FLANK))
                    pass
                else:
                    pass
                barcode_dict[barcode]["count"] += 1
            # If did not found match, add to _other
            else:
                # TODO: Logger warning
                barcode_dict["_other"]["count"] += 1
    return
