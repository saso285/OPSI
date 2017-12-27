# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


from constants.query import Query
from helpers.database import Database
import helpers.timestamp as Timestamp

DB = Database()


def dataset_num():
    """ Get dataset row count
    :return: integer row count
    """
    return DB.select_one(Query.SELECT_COUNT_DATASET)


def error_percentage():
    """ Get error percentage
    :return: float error percentage
    """
    return float(error_count()) / float(dataset_num()) if dataset_num() > 0 else 0


def error_count():
    """ Get type occurrence percentage
    :param typ: data type
    :return: float occurrence percentage
    """
    return DB.select_one(Query.SELECT_COUNT_ERROR)


def all_type():
    """ Get all unique data type names
    :return: list of data types
    """
    return DB.select(Query.SELECT_ALL_TYPE)


def all_unknown_extension():
    """ Get all unqiue unknown data type names
    :return: list of unknown data types
    """
    return DB.select(Query.SELECT_ALL_UNKNOWN_EXTENSION)


def count_unknown_extension(ext):
    """ Get unknown data type row count
    :param ext: unknown data type extension
    :return: integer unknown data type count 
    """
    return DB.select(Query.SELECT_COUNT_UNKNOWN_EXTENSION.format(ext))


def type_count(typ):
    """ Get known data type row count
    :param ext: known data type extension
    :return: integer known data type count 
    """
    return DB.select_one(Query.SELECT_COUNT_TYPE.format(typ))


def accessible_data():
    """ Get data pull success rate percentage
    :return: float data pull success rate percentage
    """
    return DB.select(Query.SELECT_ACCESSIBLE_DATA)
