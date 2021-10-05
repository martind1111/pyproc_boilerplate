#!/usr/bin/python
# -*- coding: utf-8 -*-

# Process all files in a directory in a multi-threaded fashion.
# Cap the number of worker threads.
#
# This script can be invoked as follows:
# python process_dir_bounded_threads.py [-v] [-o output-directory] [directory]
#

import argparse
import logging
import os
import sys

from queue import Queue
from threading import Thread


MAX_THREADS = 32


def process_file(thread_id, file_name, output_directory):
    logger.debug(f"Thread #{thread_id}: Process file {file_name}")
    return {}


# Threaded function for queue processing.
def process_files(q, thread_id, result, output_directory):
    while not q.empty():
        # Fetch new work from the Queue.
        work = q.get()                      
        file_name = work[1]
        try:
            # Store data back at correct index.
            result[work[0]] = process_file(thread_id, file_name, output_directory)          
        except:
            logging.error(f"Error processing file {file_name}")
            result[work[0]] = {}
        # Signal to the queue that task has been processed.
        q.task_done()
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='Directory',
                        default='.')
    parser.add_argument('-v', '--verbose', help='Verbosity',
                        action='store_true')
    parser.add_argument('-o', '--output-directory', help='Output directory',
                        default=None)

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

    if args.directory is None:
        logger.error('Must provide directory')
        sys.exit(1)

    directory = str(args.directory)

    files = []

    for (dirpath, dirnames, filenames) in os.walk(directory):
        for file_name in filenames:
            input_file_name = os.path.join(dirpath, file_name)
            files.append(input_file_name)

    # Setting up the Queue

    # Set up the queue to hold the file names
    q = Queue(maxsize=0)
    # Use many threads (MAX_THREADS max, or one for each file)
    num_threads = min(MAX_THREADS, len(files))

    # Populating Queue with tasks
    results = [{} for x in files];
    # Load up the queue with the files to process and the index for each job (as a tuple):
    for i in range(len(files)):
        # Need the index and the url in each queue item.
        q.put((i, files[i]))

    # Starting worker threads on queue processing
    for i in range(num_threads):
        logging.debug(f"Starting thread {i}")
        worker = Thread(target=process_files, args=(q, i, results, args.output_directory))
        # Setting threads as "daemon" allows main program to 
        # exit eventually even if these don't finish 
        # correctly.
        worker.setDaemon(True)
        worker.start()

    # Now we wait until the queue has been processed.
    q.join()

    logging.info('All tasks completed.')
