# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


class Query(object):

    SELECT_ACCESSIBLE_DATA = """SELECT seq/CAST((SELECT SUM(seq) FROM sqlite_sequence WHERE name='Dataset' OR name='Error' OR name='Extension') AS float) FROM sqlite_sequence WHERE name='Dataset';"""
    SELECT_ALL_DATA = """SELECT SUM(seq) FROM sqlite_sequence WHERE name='Dataset' OR name='Error' OR name='Extension';"""
    SELECT_ALL_ACCESSIBLE_DATA = """SELECT seq FROM sqlite_sequence WHERE name='Dataset';"""

    SELECT_COUNT_DATASET = """SELECT seq from sqlite_sequence WHERE name='Dataset';"""
    SELECT_COUNT_ERROR = """SELECT seq from sqlite_sequence WHERE name='Error';"""
    SELECT_COUNT_DATA_PULL = """SELECT seq from sqlite_sequence WHERE name='Data_pull';"""

    SELECT_ALL_TYPE = """SELECT DISTINCT type FROM Dataset UNION SELECT DISTINCT format from Error;"""
    SELECT_COUNT_TYPE = """SELECT COUNT(1) FROM Dataset WHERE type='{0}';"""
    SELECT_COUNT_TYPE_FIELD = """SELECT COUNT(1) FROM Dataset WHERE type='{0}' AND field='{1}';"""

    SELECT_ALL_UNKNOWN_EXTENSION = """SELECT DISTINCT Provided FROM Extension;"""
    SELECT_COUNT_UNKNOWN_EXTENSION = """SELECT COUNT(1) FROM Extension WHERE Provided='{0}';"""
    INSERT_UNKNOWN_EXTENSION = """INSERT INTO Extension VALUES(null, '{0}', '{1}', '{2}', '{3}');"""

    SELECT_LAST_DATA_PULL_ID = """SELECT MAX(id) FROM Data_pull;"""
    SELECT_ACTIVE_DATA_PULL = """SELECT * FROM Data_pull WHERE id='{0}';"""
    INSERT_START_DATA_PULL = """INSERT INTO Data_pull VALUES(null, '{0}');"""

    SELECT_DATASET_EXISTS = """SELECT COUNT(1) FROM Dataset WHERE name='{0}' AND link='{1}';"""
    SELECT_DATASET_LAST_REVISION = """SELECT revision_id FROM Dataset WHERE name='{0}';"""

    SELECT_ALL_FIELD = """SELECT DISTINCT field from Dataset UNION SELECT DISTINCT field from Extension;"""
    SELECT_ALL_DATASET = """SELECT DISTINCT name from Dataset WHERE field='{0}';"""
    SELECT_ALL_FILES = """SELECT id, link, filename, type, revision_id FROM Dataset WHERE name='{0}';"""
    
    SELECT_GET_FILE = """SELECT content FROM Dataset WHERE filename='{0}';"""

    SELECT_ALL_TYPE_FORMAT = """SELECT DISTINCT type FROM Dataset UNION SELECT DISTINCT format from Error;"""