# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


import os
import urllib3
import datetime

import xlrd

import docx
import helpers.log as Log
from helpers.data import Data
from PyPDF2 import PdfFileReader


class Convert(object):

    def get_text(self, filename):
        """ Excute the correct function based on the file extension
        :param filename: name of the file
        """
        extension = filename.split('.')[-1]
        if 'xls' in extension:
            return self.excel_text(filename)

        elif 'csv' in extension:
            return self.csv_text(filename)

        elif 'doc' in extension:
            return self.document_text(filename)

        elif 'pdf' in extension:
            return self.pdf_text(filename)

    def excel_text(self, filename):
        """ Return the excel based file as csv string
        :param filename: name of the file
        :return: string as csv
        """
        path = filename.split('/')[-3:]
        data = Data(typ=path[-1].split('.')[-1], field=path[-3], name=path[-2],
                    link='/'.join(path[-3:]))
        excel_content = []
        try:
            workbook = xlrd.open_workbook(filename)
            sheet_name = workbook.sheet_names()
            sheet = workbook.sheet_by_name(sheet_name[0])
            line = []
            for row in range(sheet.nrows):
                line = [str(item) for item in sheet.row_values(row) if item]

                if line:
                    excel_content.append(line)

            excel_content = self.parse_csv_table(excel_content)
            excel_content = [','.join(item) for item in excel_content]

        except xlrd.formula.FormulaError as er:
            Log.write_log_to_db(data, er)
            print(er)
            return None

        except xlrd.biffh.XLRDError as er:
            Log.write_log_to_db(data, er)
            print(er)
            return None

        except ValueError as er:
            Log.write_log_to_db(data, er)
            print(er)
            return None

        return '\n'.join(excel_content).replace('"', '\'').strip() or None

    def csv_text(self, filename):
        """ Parse content from csv file
        :param filename: name of the file
        :return: csv content
        """
        csv_content = []
        path = filename.split('/')[-3:]
        data = Data(typ=path[-1].split('.')[-1], field=path[-3], name=path[-2],
                    link='/'.join(path[-3:]))

        try:
            f = open(filename)
            csv_content = f.readlines()
            csv_table, delimiter = self.strip_table(csv_content)
            csv_table = self.set_column_types(self.parse_csv_table(csv_table))
            string = '\n'.join([delimiter.join(row) for row in csv_table])
            return string

        except UnicodeDecodeError as er:
            Log.write_log_to_db(data, er)
            print(er)
            return None

        except UnicodeEncodeError as er:
            Log.write_log_to_db(data, er)
            print(er)
            return None

        except IOError as er:
            Log.write_log_to_db(data, er)
            print(er)
            return None

        except ValueError as er:
            Log.write_log_to_db(data, er)
            print(er)
            return None

    @staticmethod
    def set_column_types(table):
        """ Determine types of columns in csv file
        :param filename: name of the file
        :return: string as csv
        """
        new_table = []
        transposed_table = list(zip(*table))
        patterns = [
            "%d-%m-%Y", "%Y-%m-%d", "%m-%d-%Y",
            "%Y.%m.%d", "%d.%m.%Y", "%m.%d.%Y",
            "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y",
            "%d-%m-%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m-%d-%Y %H:%M:%S",
            "%Y.%m.%d %H:%M:%S", "%d.%m.%Y %H:%M:%S", "%m.%d.%Y %H:%M:%S",
            "%Y/%m/%d %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%m/%d/%Y %H:%M:%S"
        ]
        for col in transposed_table:
            row = [col[0]]
            col_type = "s"

            for entity in col[1:]:
                for pattern in patterns:
                    try:
                        datetime.datetime.strptime(entity, pattern).date()
                        col_type = "t"

                    except:
                        pass

                if col_type != 't':
                    try:
                        int(entity)
                        col_type = "d"

                    except:
                        try:
                            float(entity.replace(".", ","))
                            col_type = "c"

                        except:
                            if any(col[1:].count(x) > 1 for x in col[1:]):
                                col_type = "d"

                            else:
                                col_type = "s"

            row.append(col_type)
            row += col[1:]
            new_table.append(row)
        return list(zip(*new_table))

    @staticmethod
    def most_common_len(excel_list):
        """ Return the most common row length from csv file
        :param excel_list: list of rows from csv file
        :return: most common row length
        """
        len_list = [len(elem) for elem in excel_list]
        count_list = [(elem, len_list.count(elem)) for elem in set(len_list)]

        return max(count_list, key=lambda item: item[1])[0]

    def parse_csv_table(self, excel_list):
        """ Parse rows with same length from csv file
        :param excel_list: list of rows from csv
        :return: list of rows with common length
        """
        end_list = []
        mcl = self.most_common_len(excel_list)

        for row in excel_list:
            if len(row) == mcl:
                end_list.append(row)

        return end_list

    def strip_table(self, table):
        """ Return file in correct stripped form
        :param table: list of rows
        :return: parsed/striped table content, delimiter
        """
        new_table = []
        delimiter = self.find_delimiter(table)

        for row in table:
            new_row = delimiter.join([str(i) for i in row.split(delimiter)[
                                     :-1]]).strip(' %s' % delimiter).split(delimiter)
            last_elem = [row.split(delimiter)[-1].strip()]

            if last_elem != ['']:
                new_row += last_elem

            if new_row != ['']:
                new_table.append(new_row)

        return new_table, delimiter

    @staticmethod
    def find_delimiter(table):
        """ Return the delimiter for cells in csv
        :param table: list of rows
        :return: delimiter
        """
        max_delimiter = ''
        count_semicolon = 0
        count_comma = 0

        for row in table:
            count_semicolon += row.count(';')
            count_comma += row.count(',')

        return ';' if count_comma < count_semicolon else ','

    @staticmethod
    def document_text(filename):
        """ Return the content of a document file
        :param filename: name of the file
        :return: document file content
        """
        path = filename.split('/')[-3:]
        data = Data(typ=path[-1].split('.')[-1], field=path[-3], name=path[-2],
                    link='/'.join(path[-3:]))
        document_content = ""

        try:
            document = docx.Document(filename)
            for row in document.paragraphs:
                if row.text:
                    document_content += row.text

        except docx.opc.exceptions.PackageNotFoundError as er:
            Log.write_log_to_db(data, er)
            print(er)

        except ValueError as er:
            Log.write_log_to_db(data, er)
            print(er)

        return document_content.replace('"', '\'').strip() or None

    @staticmethod
    def pdf_text(filename):
        """ Return the pdf based file as txt string
        :param filename: name of the file
        :return: string as txt
        """
        path = filename.split('/')[-3:]
        data = Data(typ=path[-1].split('.')[-1], field=path[-3], name=path[-2],
                    link='/'.join(path[-3:]))
        pdf_content = ""

        try:
            input_file = open(filename, "rb")
            reader = PdfFileReader(input_file, strict=False)

            for page in range(0, reader.getNumPages()):
                pdf_content += reader.getPage(page).extractText()

        except IOError as er:
            Log.write_log_to_db(data, er)
            print(er)

        except ValueError as er:
            Log.write_log_to_db(data, er)
            print(er)
            print(er)

        except KeyError as er:
            Log.write_log_to_db(data, er)
            print(er)

        except urllib3.exceptions.ProtocolError as er:
            Log.write_log_to_db(data, er)
            print(er)

        except ConnectionError as er:
            Log.write_log_to_db(data, er)
            print(er)

        return pdf_content.replace('"', '\'').strip() or None


def abspath(filename):
    """ Return the absolute path of the file
    :param filename: name of the file
    :return: absolute path
    """
    return os.path.dirname(os.path.abspath(filename))
