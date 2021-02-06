#!/usr/bin/python
# -*- coding: utf-8 -*-

# Process all files in specified directory.
#
# This script can be invoked as follows:
# python process_dir.py [-v] [-o output-dir] [directory]
#

import argparse
import logging
import os
import sys
import tempfile
import threading

from os import walk

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
    parser.add_argument('dir_name', help='Directory name',
                        default=None)
    parser.add_argument('-v', '--verbose', help='Verbosity',
                        action='store_true')
    parser.add_argument('-o', '--output-dir-name', help='Output directory name',
                        default=tempfile.gettempdir())

    args = parser.parse_args()

    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler('process_dir.log')
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    rootLogger.addHandler(consoleHandler)

    if args.verbose:
        rootLogger.setLevel(logging.DEBUG)
    else:
        rootLogger.setLevel(logging.INFO)

    logger = logging.getLogger()

    if args.dir_name is None:
        logger.error('Must provide directory name')
        sys.exit(1)

    dir_name = str(args.dir_name)

    for (dirpath, dirnames, filenames) in walk(dir_name):
        for file_name in filenames:
            f_name = os.path.join(dirpath, file_name)
            output_file_name = os.path.join(args.output_dir_name, file_name)
            t = threading.Thread(target=process_file,
                                 args=(f_name, output_file_name,))
            t.start()
            t.join()
