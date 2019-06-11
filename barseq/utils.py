#!/usr/bin/env python3

"""
Script that provides helper functions for package.

"""

import csv
import pandas as pd
import re
import logging
import sys
from pathlib import Path

__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"

# Stdout logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)
# Get logger
logger = logging.getLogger("barseq")


def read_barcodes(barcodes_file: Path) -> dict:
    """
    Read in barcodes from file

    :param barcodes_file: path to csv file with barcodes and gene name
    :return barcode_dict:

    barcode_dict = {
        barcode_1 : {"gene": Gene_1, "count": 0}
        barcode_2 : {"gene": Gene_2, "count": 0}
    }
    """
    # Store barcodes
    barcode_dict = dict()
    with open(barcodes_file, "r") as csv_barcode:
        # Skip Header
        next(csv_barcode)
        for line in csv.reader(csv_barcode):
            # Ignore comments
            if not line[0].startswith("#"):
                gene = line[1]
                barcode = line[0].upper()
                # Check for duplicate barcode
                if barcode not in barcode_dict:
                    barcode_dict[barcode] = {"gene": gene, "count": 0}
                else:
                    logger.error(f"Barcode {barcode} already in dictionary.")
                    raise IOError(f"Duplicate error: {barcode} already in dictionary")
    # Add _other for barcode that do not match
    barcode_dict["_other"] = {"gene": "_other", "count": 0}
    return barcode_dict


def write_output(sample_dict: dict, barcode_dict: dict, runner) -> None:
    """
    Convert results file into a pandas dataframe with following
    structure.

    :param sample_dict: Dictionary with samples and barcode counts
    :param barcode_dict: Dictionary with barcode and gene names
    :param output_name: Name for output file
    :return None

    |    Gene    | Barcode |   Sample 1  |  Sample 2   | ... |
    |------------|---------|-------------|-------------|-----|
    |   Gene 1   | ATCGCGT |     500     |     10      | ... |

    """
    # Grab barcode and gene index
    index = list(sample_dict.values())[0]
    s_genes = pd.Series(data=[d["gene"] for d in index.values()], name="Gene")
    s_barcodes = pd.Series(data=[k for k in index.keys()], name="Barcodes")
    # Join them
    df = pd.concat([s_genes, s_barcodes], axis=1).set_index("Gene")
    # Sort samples
    sample_dict = dict(sorted(sample_dict.items()))
    # Grab counts from sample and add to df
    for sample in sample_dict:
        counts = {count_dict["gene"]: count_dict["count"] for count_dict in sample_dict[sample].values()}
        sample_df = pd.DataFrame.from_dict(counts, orient="index", columns=[sample])
        df = pd.concat([df, sample_df], axis=1)
    # Write to output
    df.to_csv(f"{runner.path}/barcode_counts_table.csv")
    return


def format_filename(name: str) -> str:
    """
    Converts input into a valid name for file and recording results

    :param name: Input name
    :return output: Formatted name
    """
    # Strip extension
    name = "".join(name.split(".")[0])
    # Taken from Pyinseq software
    return re.sub(r"(?u)[^-\w]", "", name.strip().replace(" ", "_"))


def make_barseq_directories(runner) -> None:
    """
    Helper function for creating experiment directories that are
    used in barseq run.

    :param runner: Run object given in main
    :return:
    """
    error_message =f"Barseq Error: {runner.experiment} directory already exists. Delete or rename {runner.experiment}, or provide new name for barseq run."
    results_folder = Path("results", runner.experiment)
    if results_folder.is_dir():
        logger.error(error_message)
        sys.exit(1)
    results_folder.mkdir(parents=True)
    runner.path = results_folder
    return


if __name__ == '__main__':
    pass
