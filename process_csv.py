#!/usr/bin/python
# -*- coding: utf-8 -*-

# Process a CSV file
#
# This script can be invoked as follows:
# python process_csv.py [-v] [-o output-file] [file-name]
#

import argparse
import csv
import logging
import os
import sys
import tempfile

logger = None

def transform(row):
    return row

def process_file(file_name, output_file_name):
    logger.info(f"Process file {file_name}")
    with open(file_name, 'r') as csvfile:
        with open(output_file_name, 'w') as out:
            reader = csv.reader(csvfile, dialect=csv.excel, delimiter=';',
                                lineterminator='\r')

            for row in reader:
                print(transform(row), file=out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', help='File name')
    parser.add_argument('-o', '--output-file', help='Output file name',
                        default=os.path.join(tempfile.gettempdir(),
                                             'output_file'))
    parser.add_argument('-v', '--verbose', help='Verbosity',
                        action='store_true')

    args = parser.parse_args()

    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler('process_csv.log')
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    rootLogger.addHandler(consoleHandler)

    if args.verbose:
        rootLogger.setLevel(logging.DEBUG)
    else:
        rootLogger.setLevel(logging.INFO)

    logger = logging.getLogger()

    if args.file_name is None:
        logger.error('Must provide file name')
        sys.exit(1)

    file_name = str(args.file_name)

    process_file(file_name, args.output_file)
