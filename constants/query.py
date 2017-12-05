# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


class Query(object):

    SELECT_FIELD = """SELECT {} FROM Field {}"""
    INSERT_FIELD = """INSERT INTO Field VALUES(null, '{}','{}')"""
    UPDATE_FIELD = """UPDATE Field SET name='{}', link='{}')"""
    DELETE_FIELD = """DELETE FROM Field WHERE {}"""

    SELECT_TYPE = """SELECT {} FROM Type {}"""
    INSERT_TYPE = """INSERT INTO Type VALUES(null, '{}')"""
    UPDATE_TYPE = """UPDATE Type SET name='{}'"""
    DELETE_TYPE = """DELETE FROM Type WHERE {}"""

    SELECT_FILE = """SELECT {} FROM File {}"""
    INSERT_FILE = """INSERT INTO File VALUES(null, '{}','{}','{}')"""
    UPDATE_FILE = """UPDATE File SET name='{}, type='{}', content='{}'"""
    DELETE_FILE = """DELETE FROM File WHERE {}"""

    SELECT_DATASET = """SELECT {} FROM Dataset {}"""
    INSERT_DATASET = """INSERT INTO Dataset VALUES(null, '{}','{}','{}')"""
    UPDATE_DATASET = """UPDATE Dataset SET name='{}', link='{}'"""
    DELETE_DATASET = """DELETE FROM Dataset WHERE {}"""
