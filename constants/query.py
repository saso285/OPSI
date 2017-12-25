# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


class Query(object):

    SELECT_COUNT_DATASET = """SELECT seq from sqlite_sequence WHERE name='Dataset';"""
    SELECT_COUNT_ERROR = """SELECT seq from sqlite_sequence WHERE name='Error';"""

    SELECT_ALL_TYPE = """SELECT DISTINCT type FROM Dataset"""
    SELECT_COUNT_TYPE = """SELECT COUNT(1) FROM Dataset WHERE type='{0}'"""
