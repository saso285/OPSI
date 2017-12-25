# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"

import os
import sqlite3

import helpers.timestamp as Timestamp
from constants.path import Path


def append_to_file(filepath, content):
    """ Append content to a file
    :param filepath: path to the file
    :param content: content of the file
    """
    file_path = os.path.join(Path.DOWNLOAD_DIR + filepath)

    with open(file_path, 'wb') as f:
        f.write(content)


def write_log_to_file(filename, content):
    """ Write content to a log file
    :param filepath: path to the file
    :param content: content of the file
    """
    append_to_file(filename, content)


def write_log_to_db(data, error):
    """ Write content to a log table in database
    :param data: data object
    :param error: error type
    """
    data.content = error
    data.timestamp = Timestamp.timestamp()
    data.dataset = data.name
    log_to_db(data)


def log_to_db(data):
    """ Execute query to log data in database
    :param data: data object
    :return: insert success boolean
    """
    from helpers.database import Database
    query = '''INSERT INTO Error Values(null, "%s", "%s", "%s", "%s", "%s", "%s");'''

    try:
        db = Database().get_db()
        conn = db.cursor()
        conn.execute(query % (data.type, data.content, data.timestamp,
                              data.field, data.dataset, data.link))
        db.commit()
        return True

    except sqlite3.Error as er:
        print(er)
        return False

    finally:
        db.close()
