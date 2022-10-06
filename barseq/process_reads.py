3  # !/usr/bin/env python3

"""
Count barcode frequency in fastq/fasta files given by user.

"""

import screed
import logging
import regex as re

# Module imports
from .utils import compile_regex_patterns

__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"

# Get logger
logger = logging.getLogger("barseq")


def count_barcodes(seq_file, barcode_dict, runner) -> None:
    """
    Count barcode frequency in sequence file.
    Returns a DataFrame object

    :param seq_file: file with reads
    :param runner: Run object
    :param barcode_dict: barcode dictionary of sample
    :return:
    """
    _other_reads = list()
    flank_regex, barcode_regex = compile_regex_patterns(barcode_dict, runner)
    # Open sequence file
    with screed.open(seq_file) as reads:
        n_reads = 0
        for read in reads:
            try:
                putative_barcode = re.search(runner.pattern, read.sequence)[2]
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
                f"{n_reads} ({round((matched_reads / n_reads) * 100, 2)}%) matched known barcodes.")
    logger.info(
        f"Reads without barcode match: {_other_reads} ({round((_other_reads / n_reads) * 100, 2)}%) for {seq_file}")
    return


def count_barcodes_reference_free(seq_file, runner):
    """
    Count barcode frequency in sequence file.
    Returns a DataFrame object

    :param seq_file: file with reads
    :param runner: Run object
    :return barcode_counts:
    """
    # Get regex pattern
    # flank_regex = compile_regex_patterns(runner=runner)
    # Search for barcodes in sequence file
    # Barcode count
    barcode_counts = dict()
    barcode_counts["no_barcode_found"] = 0
    n_reads = 0
    with screed.open(seq_file) as reads:
        for read in reads:
            match = re.search(runner.pattern, read.sequence)
            if match:
                # Add to dictionary and count
                barcode = match.groups(0)[1]
                if barcode not in barcode_counts.keys():
                    barcode_counts[barcode] = 0
                barcode_counts[barcode] += 1
            else:
                barcode_counts["no_barcode_found"] += 1
            n_reads += 1

    # Calculate matched reads
    good_barcode_count = sum([barcode_counts[s] for s in barcode_counts if s != "no_barcode_found"])
    _other_reads = barcode_counts['no_barcode_found']

    logger.info(f"For {seq_file}, {good_barcode_count} of "
                f"{n_reads} ({round((good_barcode_count / n_reads) * 100, 2)}%) are good barcodes.")
    logger.info(
        f"Reads without barcode match: {_other_reads} ({round((_other_reads / n_reads) * 100, 2)}%) for {seq_file}")
    return barcode_counts, good_barcode_count


if __name__ == '__main__':
    pass
