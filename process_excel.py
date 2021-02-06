#!/usr/bin/python
# -*- coding: utf-8 -*-

# Process an Excel file
#
# This script can be invoked as follows:
# python process_excel.py [-v] [-o output-file] [file-name]
#

import argparse
import logging
import os
import sys
import pandas
import tempfile

logger = None

def process_sheet(df, sheet, output_file_name):
    headers = []
    for column_name, col in df.iteritems():
        headers.append(column_name)

    rows = []
    for index, row in df.iterrows():
        rows.append(row)

    with pandas.ExcelWriter(output_file_name) as writer:
        df = pandas.DataFrame(rows, columns=headers)
        df.to_excel(writer, sheet_name=sheet, header=True, index=False)

def process_file(file_name, sheet, output_file_name):
    logger.info("Process file {}".format(file_name))

    if sheet is None:
        sheets = pandas.read_excel(file_name, sheet_name=sheet)
        for sheet_name in sheets:
            process_sheet(sheets[sheet_name], sheet_name, output_file_name)
    else:
        df = pandas.read_excel(file_name, sheet_name=sheet)
        process_sheet(df, sheet, output_file_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', help='File name')
    parser.add_argument('-o', '--output-file', help='Output file name',
                        default=os.path.join(tempfile.gettempdir(),
                                             'output_file.xlsx'))
    parser.add_argument('-s', '--sheet', help='Sheet name', default=None)
    parser.add_argument('-v', '--verbose', help='Verbosity',
                        action='store_true')

    args = parser.parse_args()

    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler('process_excel.log')
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

    process_file(file_name, args.sheet, args.output_file)
