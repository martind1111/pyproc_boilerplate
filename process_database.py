#!/usr/bin/python
# -*- coding: utf-8 -*-

# Process a database table
#
# This script can be invoked as follows:
# python process_database.py [-v] [-c config-file] [-t table-name]
#     [database-name]
#

import argparse
import logging
import mysql.connector
#import MySQLdb
import sys

from six.moves import configparser

logger = None

def get_database_connection(config_file, database_name):
    __SECTION = 'DatabaseConfig'
    config = configparser.ConfigParser()
    config.read_file(open(config_file))

    hostname = config.get(__SECTION, 'hostname')
    port = config.get(__SECTION, 'port')
    username = config.get(__SECTION, 'username')
    user_password = config.get(__SECTION, 'password')

    if hostname is None or username is None or user_password is None or \
       database_name is None:
        logging.error('Incomplete database config')
        sys.exit(1)
    if port is None:
        db_port = 3306
    else:
        db_port = int(port)

    if db_port == 3306:
        conn = mysql.connector.connect(host=hostname,
                                       user=username, password=user_password,
                                       database=database_name)
    else:
        conn = mysql.connector.connect(host=hostname,
                                       user=username, password=user_password,
                                       database=database_name, port=db_port)

    return conn

# Process row. Here, we are updating each row, but re-assigning the value of
# the first column of each row with current value in database. This effectively
# will not change anything in database, but it shows how we can perform
# an update opeartion.
def process_row(conn, table_name, columns, row):
    if len(columns) == 0:
        return
    column = columns[0][0]
    cursor = conn.cursor()
    query = (f"UPDATE {table_name} SET {column}=%s WHERE {column}=%s")
    cursor.execute(query, (row[0], row[0]))
    conn.commit()

def process_database_table(conn, table_name):
    logger.info(f"Process database table {table_name}")
    cursor = conn.cursor()
    query = ("SELECT * FROM " + table_name)
    cursor.execute(query)
    columns = cursor.description
    result = cursor.fetchall()

    rows = []
    for row in result:
        rows.append(row)

    for row in rows:
        process_row(conn, table_name, columns, row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('database_name', help='Database name',
                        default='data')
    parser.add_argument('-v', '--verbose', help='Verbosity',
                        action='store_true')
    parser.add_argument('-c', '--config-file', help='Configuration file name',
                        default='config.ini')
    parser.add_argument('-t', '--table-name', help='Table name',
                        default=None)

    args = parser.parse_args()

    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler('process_database.log')
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    rootLogger.addHandler(consoleHandler)

    if args.verbose:
        rootLogger.setLevel(logging.DEBUG)
    else:
        rootLogger.setLevel(logging.INFO)

    logger = logging.getLogger()

    if args.database_name is None:
        logger.error('Must provide database name')
        sys.exit(1)

    database_name = str(args.database_name)

    conn = get_database_connection(args.config_file, database_name)

    process_database_table(conn, args.table_name)

    conn.close()
