# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"

import xlrd


class Store(object):

    def excel_to_csv(self, filename):
        """ Prepare excel file to be in complience before importing to orange
        :param filename: boolean whether the request succeeded or not
        :type filename: string
        :return: formated string in complience with orange csv
        :rtype filename: string
        """
        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)
        csv = ''
        for row_num in xrange(sheet.nrows):
            row = sheet.row_values(row_num)
            csv += self.__preprocess_line(row)
            workbook.release_resources()
        return csv[:-1]

    def preprocess_csv(self, filename):
        """ Prepare csv file to be in complience before importing to orange
        :param filename: boolean whether the request succeeded or not
        :type filename: string
        :return: formated string in complience with orange csv
        :rtype filename: string
        """
        f = open(filename, 'r')
        rows = f.read()
        csv = ''
        delimiter = ',' if rows.count(',') >= rows.count(';') else ';'
        for row in rows.split():
            csv += self.__preprocess_line(row.split(delimiter))
        f.close()
        return csv[:-1]

    @staticmethod
    def __preprocess_line(line):
        """ Format line to be in complience with csv format
        :param line: columns of excel file
        :type line: list
        :return: formated string in complience with csv format
        :rtype: string
        """
        csv = ''
        for elem in line:
            csv += ("'%s'," % str(elem).strip())
        return csv[:-1] + "\n"
