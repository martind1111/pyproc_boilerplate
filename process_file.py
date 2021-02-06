#!/usr/bin/python
# -*- coding: utf-8 -*-

# Process a file
#
# This script can be invoked as follows:
# python process_file.py [-v] [-o output-file] [file-name]
#

import argparse
import logging
import os
import sys
import tempfile

logger = None

def transform(line):
    return line

def process_line(line, out):
    transformed = transform(line)
    out.write(transformed)

def process_file(file_name, output_file_name):
    logger.info(f"Process file {file_name}")
    with open(file_name) as f:
        with open(output_file_name, 'w') as out:
            for line in f.readlines():
                process_line(line, out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', help='File name',
                        default='data')
    parser.add_argument('-v', '--verbose', help='Verbosity',
                        action='store_true')
    parser.add_argument('-o', '--output-file', help='Output file name',
                        default=os.path.join(tempfile.gettempdir(),
                                             'output_file'))

    args = parser.parse_args()

    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler('process_file.log')
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
