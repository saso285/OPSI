# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


import sqlite3

from constants.path import Path


class Database(object):

    @staticmethod
    def get_db():
        """ Opens a new database connection for the current application context.
        :return: sqlite3 database connection
        :rtype: object
        """
        return sqlite3.connect(Path.DATABASE)

    def create_table(self, query):
        """ Create new table in database
        :param query: database query
        :type query: string
        :return: status whether query executions succeed or not
        :rtype: boolean
        """
        con = self.get_db()

        try:
            cursor = con.cursor()
            cursor.execute(query)
            return True

        except sqlite3.Error as er:
            print(er.message)
            return False

        finally:
            con.close()

    def select_one(self, query):
        """ Return single select query result
        :param query: database query
        :type query: string
        :return: list with a single select query result
        :rtype: list
        """
        con = self.get_db()

        try:
            cursor = con.cursor()
            cursor.execute(query)
            return cursor.fetchone()

        except sqlite3.Error as er:
            print(er.message)
            return []

        finally:
            con.close()

    def select(self, query):
        """ Return all select query results
        :param query: database query
        :type query: string
        :return: list of all select query results
        :rtype: list
        """
        con = self.get_db()

        try:
            cursor = con.cursor()
            cursor.execute(query)
            return cursor.fetchall()

        except sqlite3.Error as er:
            print(er.message)
            return []

        finally:
            con.close()

    def insert(self, query):
        """ Return boolean whether insert query succeeds
        :param query: database query
        :type query: string
        :return: status whether query executions succeed or not
        :rtype: boolean
        """
        con = self.get_db()

        try:
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()
            return True

        except sqlite3.Error as er:
            print(er.message)
            return False

        finally:
            con.close()

    def update(self, query):
        """ Call insert function as update
        :param query: database query
        :type query: string
        :return: insert function
        :rtype: def
        """
        return self.insert(query)

    def delete(self, query):
        """ Call insert function as delete
        :param query: database query
        :type query: string
        :return: insert function
        :rtype: def
        """
        return self.insert(query)
