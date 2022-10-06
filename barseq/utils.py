#!/usr/bin/env python3

"""
Script that provides helper functions for package.

"""

import re
import csv
import sys
import shutil
import logging
import pandas as pd
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


def write_output(sample_dict: dict, runner) -> None:
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
    df.to_csv(f"{runner.path}/barcode_counts_table.txt", sep='\t')
    return


def compile_regex_patterns(barcode_dict=None, runner=None):
    """
    Compies regex patterns for matching sequences in reads.
    If no barcode_dict is provided then just return flank_regex
    Flanking_regex -> finds flanking sequence and random 18bp barcode
    Barcode_regex -> compiles each reference barcode into regex object
    """
    # Regex pattern: match flanking sequence and random 18-bp barcode
    flank_regex = re.compile(runner.pattern)
    barcode_regex = dict()
    if barcode_dict:
        # Compile each barcode in dictionary as regex object
        for b in barcode_dict:
            barcode_regex[b] = "(%s){e<=1}" % b
        return flank_regex, barcode_regex
    else:
        return flank_regex


def format_filename(path: Path) -> str:
    """
    Converts input into a valid name for file and recording results

    :param path: Filepath
    :return output: Formatted name
    """
    # Strip extension
    name = "".join(path.stem.split(".")[0])
    # Taken from Pyinseq software
    return re.sub(r"(?u)[^-\w]", "", name.strip().replace(" ", "_"))


def make_barseq_directories(runner) -> None:
    """
    Helper function for creating experiment directories that are
    used in barseq run.

    :param runner: Run object given in main
    :return:
    """
    if runner.force:
        logger.info(f"--force option is True, {runner.path} will be overwritten")
        shutil.rmtree(runner.path, ignore_errors=True)
    elif runner.path.exists():
        logger.error(f"Barseq Error: {runner.experiment} directory already exists. "
                     f"Delete or rename {runner.experiment}, or provide new name for "
                     f"barseq run.")
        sys.exit(1)

    runner.path.mkdir(parents=True)
    return


def calculate_barcode_perc(barcode_dict, total_barcodes=0, min_count=20):
    """
    Calculate total number of `unique` barcodes and percentage.
    Return modified dictionary

    :param barcode_counts: dictionary where key=sequence, value=counts
    :return: barcode_stats
    """
    barcode_stats = {}
    for seq, count in barcode_dict.items():
        if count >= min_count and seq != 'no_barcode_found':
            seq_perc = round(count / total_barcodes * 100, 2)
            barcode_stats[seq] = [count, seq_perc]
    # quick sorting to ensure order
    barcode_stats = {k: v for k, v in sorted(barcode_stats.items(), key=lambda x: x[1][0], reverse=True)}
    return barcode_stats


def read_sample_ID(sample_file):
    """
    Reads csv file where rows = [seq_tag, sample_name]
    Returns a dictionary where key=seq_tag, value=sample_name

    :params sample_file: path to sample csv file
    :returns sample_ids: dictionary
    """
    sample_ids = {}
    with open(sample_file, 'r') as f:
        reader = csv.reader(f)
        # skip header
        next(reader)
        for seq_tag, sample_name in reader:
            sample_ids[seq_tag] = sample_name
    return sample_ids


def format_sample_data(barcode_dict, barcode_count=0, sample_id=None):
    """
    Grabs each unique barcode and formats into row for pandas
    :param barcode_dict: dict where key=sample
    """
    i = 1
    data = {'Sample_ID': sample_id, 'Total Barcode Count': barcode_count}
    for seq, values in barcode_dict.items():
        barcode_column = f"{i}° Barcode"
        count_column = f"{i}° Count"
        perc_column = f"{i}° %"

        data[barcode_column] = seq
        data[count_column] = values[0]
        data[perc_column] = values[1]
        i += 1
    return data


def convert_dict_to_dataframe(dict_collection):
    df_collection = []
    for data in dict_collection:
        df_collection.append(pd.DataFrame(data, index=[0]))
    return pd.concat(df_collection)


def save_results(data_collection, runner):
    print(data_collection)
    df = convert_dict_to_dataframe(data_collection)
    df.set_index('Sample_ID', inplace=True)
    df.to_csv(f'{runner.path}/barcode_counts_table.csv')
    # Filter for samples that have less than 75% on 1st barcode percentage
    df_less_75 = df[df['1° %'] <= 75]
    df_less_75.to_csv(f'{runner.path}/barcode_counts_less_75.csv')


if __name__ == '__main__':
    pass
