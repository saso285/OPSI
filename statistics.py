# -*- coding: utf-8 -*-

from helpers.database import Database
from constants.query import Query

db = Database()


def dataset_num():
    return db.select_one(Query.SELECT_COUNT_DATASET)


def type_percentage(typ):
    return float(type_count(typ)) / float(dataset_num()) if dataset_num() > 0 else 0


def error_percentage():
    return float(error_count()) / float(dataset_num()) if dataset_num() > 0 else 0


def error_count():
    return db.select_one(Query.SELECT_COUNT_ERROR)


def all_type():
    return db.select(Query.SELECT_ALL_TYPE)


def type_count(typ):
    return db.select_one(Query.SELECT_COUNT_TYPE.format(typ))


# Test
for typ in all_type():
    print("[%s] -" % typ, "Percentage:", type_percentage(typ))
