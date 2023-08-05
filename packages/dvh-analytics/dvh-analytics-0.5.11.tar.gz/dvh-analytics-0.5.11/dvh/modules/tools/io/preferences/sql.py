#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from future.utils import listitems
try:
    import pydicom as dicom  # for pydicom >= 1.0
except ImportError:
    import dicom
from ...get_settings import get_settings, parse_settings_file
from ...io.database.sql_connector import DVH_SQL


def is_sql_connection_defined():
    """
    Checks if sql_connection.cnf exists
    :rtype: bool
    """
    abs_file_path = get_settings('sql')
    if os.path.isfile(abs_file_path):
        return True
    else:
        return False


def write_sql_connection_settings(config):
    """
    :param config: a dict with keys 'host', 'dbname', 'port' and optionally 'user' and 'password'
    """

    text = ["%s %s" % (key, value) for key, value in listitems(config) if value]
    text = '\n'.join(text)

    abs_file_path = get_settings('sql')

    with open(abs_file_path, "w") as text_file:
        text_file.write(text)


def load_sql_settings():
    if is_sql_connection_defined():
        config = parse_settings_file(get_settings('sql'))
        config = validate_config(config)

    else:
        config = {'host': 'localhost',
                  'port': '5432',
                  'dbname': 'dvh',
                  'user': '',
                  'password': ''}

    return config


def validate_config(config):
    if 'user' not in list(config):
        config['user'] = ''
        config['password'] = ''

    if 'password' not in list(config):
        config['password'] = ''

    return config


def validate_sql_connection(config=None, verbose=False):
    """
    :param config: a dict with keys 'host', 'dbname', 'port' and optionally 'user' and 'password'
    :param verbose: boolean indicating if cmd line printing should be performed
    :return:
    """

    valid = True
    if config:
        try:
            cnx = DVH_SQL(config)
            cnx.close()
        except:
            valid = False
    else:
        try:
            cnx = DVH_SQL()
            cnx.close()
        except:
            valid = False

    if verbose:
        if valid:
            print("SQL DB is alive!")
        else:
            print("Connection to SQL DB could not be established.")
            if not is_sql_connection_defined():
                print("ERROR: SQL settings are not yet defined.  Please run:\n",
                      "    $ dvh settings --sql", sep="")

    return valid
