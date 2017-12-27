# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


class Query(object):

    SELECT_ACCESSIBLE_DATA = """SELECT seq/CAST((SELECT SUM(seq) FROM sqlite_sequence WHERE name='Dataset' OR name='Error' OR name='Extension') AS float) FROM sqlite_sequence WHERE name='Dataset';"""

    SELECT_COUNT_DATASET = """SELECT seq from sqlite_sequence WHERE name='Dataset';"""
    SELECT_COUNT_ERROR = """SELECT seq from sqlite_sequence WHERE name='Error';"""
    SELECT_COUNT_DATA_PULL = """SELECT seq from sqlite_sequence WHERE name='Data_pull';"""

    SELECT_ALL_TYPE = """SELECT DISTINCT type FROM Dataset;"""
    SELECT_COUNT_TYPE = """SELECT COUNT(1) FROM Dataset WHERE type='{0}';"""

    SELECT_ALL_UNKNOWN_EXTENSION = """SELECT DISTINCT Provided FROM Extension;"""
    SELECT_COUNT_UNKNOWN_EXTENSION = """SELECT COUNT(1) FROM Extension WHERE Provided='{0}';"""
    INSERT_UNKNOWN_EXTENSION = """INSERT INTO Extension VALUES(null, '{0}', '{1}');"""

    SELECT_LAST_DATA_PULL_ID = """SELECT MAX(id) FROM Data_pull;"""
    SELECT_ACTIVE_DATA_PULL = """SELECT * FROM Data_pull WHERE id='{0}';"""
    INSERT_START_DATA_PULL = """INSERT INTO Data_pull VALUES(null, '0', '{0}');"""
    UPDATE_START_DATA_PULL = """INSERT Data_pull SET finished='1' WHERE id='{0}';"""

    SELECT_DATASET_EXISTS = """SELECT COUNT(1) FROM Dataset WHERE name='{0}' AND link='{1}';"""
    SELECT_DATASET_LAST_REVISION = """SELECT revision_id FROM Dataset WHERE name='{0}';"""