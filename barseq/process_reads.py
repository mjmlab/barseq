#!/usr/bin/env python3

"""
Count barcode frequency in fastq/fasta files given by user.

"""

import screed
import logging
from Levenshtein import distance

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
        i = 0
        unmatched_reads = 0
        for read in reads:
            # Verbose
            seq = read.sequence
            if any(bar in seq for bar in barcode_ls):
                barcode = "".join([bar for bar in barcode_ls if bar in seq])
                # Check flanking sequences
                barcode_index = seq.index(barcode)
                split_sequence = read.sequence.split(barcode)

                left = split_sequence[0][barcode_index - 18: barcode_index]
                right = split_sequence[1][0:18]
                # Calculate Levenshtein distance
                left_distance = distance(left, LEFT_FLANK)
                right_distance = distance(right, RIGHT_FLANK)
                if max(left_distance, right_distance) > 1:
                    unmatched_reads += 1
                    pass
                barcode_dict[barcode]["count"] += 1
            # If did not found match, add to _other
            else:
                # Try both positions of index, 86 and 87
                index_86 = seq[86:104]
                index_87 = seq[87:105]

                candidate_barcodes_86 = {[distance(bar, index_86) for bar in barcode_ls if distance(bar, index_86) < 5] }
                candidate_barcodes_87 = [distance(bar, index_87) for bar in barcode_ls if distance(bar, index_87) < 5]

                print(max(candidate_barcodes_87[1], candidate_barcodes_86[1]))

                barcode_dict["_other"]["count"] += 1
            i += 1
    logger.info(f"Unmatched reads: {unmatched_reads} for {seq_file}")
    return
