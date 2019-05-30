#!/usr/bin/env python3

"""
Count barcode frequency in fastq/fasta files given by user.

"""

import screed
import logging
import regex as re
import sys

__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"

# Get logger
logger = logging.getLogger("barseq")


def count_barcodes(seq_file, barcode_dict) -> None:
    """
    Count barcode frequency in sequence file.
    Returns a DataFrame object

    :param seq_file: file with reads
    :param barcode_dict: barcode dictionary of sample
    :return:
    """
    _other_reads = list()
    # Create regex patterns
    flank_regex = re.compile("(GCTCATGCACTTGATTCC){e<=1}([ATGC]{18})(GACTTGACCTGGATGTCT){e<=1}")
    barcode_regex = dict()
    for b in barcode_dict.keys():
        pattern_barcode = "(%s){e<=1}" % b
        b_regex = re.compile(pattern_barcode)
        barcode_regex[pattern_barcode] = (b, b_regex)
    # Open sequence file
    with screed.open(seq_file) as reads:
        for read in reads:
            # Check with each regex
            barcode_found = False
            for regex_set in barcode_regex.values():
                bar_re_object = regex_set[1]
                m = re.search(bar_re_object, read.sequence)
                m_flank = re.search(flank_regex, read.sequence)
                # Check if match found
                if m and m_flank:
                    # Grab barcode by using regex match string
                    barcode = barcode_regex[bar_re_object.pattern][0]
                    barcode_dict[barcode]["count"] += 1
                    barcode_found = True
                    break
            # Add to _others if match was not found.
            if not barcode_found:
                barcode_dict["_other"]["count"] += 1
                _other_reads.append(read)

    logger.info(f"Reads without barcode match: {barcode_dict['_other']['count']} for {seq_file}")
    return
