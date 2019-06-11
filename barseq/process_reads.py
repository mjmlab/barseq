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
    # Compile regex patterns
    flank_regex = re.compile("(GCTCATGCACTTGATTCC){e<=1}([ATGC]{18})(GACTTGACCTGGATGTCT){e<=1}")
    barcode_regex = dict()
    for b in barcode_dict:
        barcode_regex[b] = re.compile("(%s){e<=1}" % b)
    # Open sequence file
    with screed.open(seq_file) as reads:
        n_reads = 0
        for read in reads:
            try:
                putative_barcode = re.search(flank_regex, read.sequence)[2]
                for known_barcode in barcode_regex:
                    if re.search(barcode_regex[known_barcode], putative_barcode):
                        barcode_dict[known_barcode]["count"] += 1
                        break
                # Putative barcode present, does not match known barcodes
                else:
                    barcode_dict["_other"]["count"] += 1
                    _other_reads.append(read)
            # No putative barcode present
            except TypeError:
                barcode_dict["_other"]["count"] += 1
                _other_reads.append(read)
            n_reads += 1
    # Calculate matched reads
    matched_reads = sum([x['count'] for x in barcode_dict.values() if x["gene"] != "_other"])
    _other_reads = barcode_dict['_other']['count']

    logger.info(f"For {seq_file}, {matched_reads} of "
                f"{n_reads} ({round((matched_reads/n_reads) * 100, 2)}%) matched known barcodes.")
    logger.info(f"Reads without barcode match: {_other_reads} ({round((_other_reads/n_reads)*100, 2)}%) for {seq_file}")
    return


if __name__ == '__main__':
    pass
