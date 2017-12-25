# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


from helpers.database import Database
from constants.query import Query

DB = Database()


def dataset_num():
    return DB.select_one(Query.SELECT_COUNT_DATASET)


def type_percentage(typ):
    return float(type_count(typ)) / float(dataset_num()) if dataset_num() > 0 else 0


def error_percentage():
    return float(error_count()) / float(dataset_num()) if dataset_num() > 0 else 0


def error_count():
    return DB.select_one(Query.SELECT_COUNT_ERROR)


def all_type():
    return DB.select(Query.SELECT_ALL_TYPE)


def type_count(typ):
    return DB.select_one(Query.SELECT_COUNT_TYPE.format(typ))
