# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


import os
import sqlite3

import helpers.log as Log
from constants.path import Path
from helpers.read import Read


class Database(object):

    @staticmethod
    def database_exists():
        return os.path.exists(Path.DATABASE)

    @staticmethod
    def get_db():
        """ Get database connection
        :return: connection object
        """
        try:
            return sqlite3.connect(Path.DATABASE)

        except sqlite3.Error as e:
            print(e)

    def create_database(self):
        """ Restore database from './database_sql' file
        :param database_sql: a CREATE DATABASE sql file content
        :return: 
        """
        try:
            con = self.get_db()
            cursor = con.cursor()
            cursor.executescript(Read.file(Path.DATABASE_SQL))
            return True

        except sqlite3.Error as e:
            print(e)
            return False

        finally:
            con.close()

    def select_one(self, query):
        """ Return single select query result
        :param query: database query
        :return: list with a single select query result
        """
        con = self.get_db()

        try:
            cursor = con.cursor()
            cursor.execute(query)
            return cursor.fetchone()[0]

        except sqlite3.Error as er:
            print(er)
            return []

        finally:
            con.close()

    def select(self, query):
        """ Return all select query results
        :param query: database query
        :return: list of all select query results
        """
        con = self.get_db()

        try:
            cursor = con.cursor()
            cursor.execute(query)
            return [item[0] for item in cursor.fetchall()]

        except sqlite3.Error as er:
            print(er)
            return []

        finally:
            con.close()

    def insert(self, query):
        """ Return boolean whether insert query succeeds
        :param query: database query
        :return: status whether query executions succeed or not
        """
        con = self.get_db()

        try:
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()
            return True

        except sqlite3.Error as er:
            print(er)
            return False

        finally:
            con.close()

    def update(self, query):
        """ Call insert function as update
        :param query: database query
        :return: insert function
        """
        return self.insert(query)

    def delete(self, query):
        """ Call insert function as delete
        :param query: database query
        :return: insert function
        """
        return self.insert(query)

    def write_to_db(self, data):
        """ Execute query to insert data in database
        :param data: data object
        :return: insert success boolean
        """
        query = '''INSERT INTO Dataset Values(null, "%s", "%s", "%s", "%s", "%s", "%s");'''

        try:
            db = self.get_db()
            conn = db.cursor()
            conn.execute(query % (data.name, data.field, data.link,
                                  data.type, data.content, data.update))
            db.commit()
            return True

        except sqlite3.Error as er:
            print(er)
            Log.write_log_to_db(data, er)
            return False

        except sqlite3.OperationalError as er:
            print(er)
            Log.write_log_to_db(data, er)
            return False

        except ValueError as er:
            print(er)
            Log.write_log_to_db(data, er)
            return False

        finally:
            db.close()
