# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"

from constants.query import Query
from helpers.database import Database

DB = Database()


class Tree(object):
    
    @staticmethod
    def fields():
        """ Get name of all fields
        :return: list of fields
        """
        return DB.select(Query.SELECT_ALL_FIELD)

    @staticmethod
    def datasets(field):
        """ Get all datasets of specific field
        :param field: field name
        :return: list of all datasets
        """
        return DB.select(Query.SELECT_ALL_DATASET.format(field))

    @staticmethod
    def files(dataset):
        """ Get all files of a specific dataset
        :param dataset: dataset name
        :return: list of files
        """
        files = []
        links = DB.select_many(Query.SELECT_ALL_FILES.format(dataset))

        for link in links:
            file_info = {
                'id': link[0],
                'url': link[1],
                'name': link[2],
                'type': link[3],
                'revision_id': link[4],
            }
            files.append(file_info)

        return files

    @staticmethod
    def file_content(file_name):
        """ Get content of a specific file
        :param file_name: file name
        :return: string content of specific file
        """
        return DB.select(Query.SELECT_GET_FILE.format(file_name))
