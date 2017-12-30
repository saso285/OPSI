# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


import os
import urllib3

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

    @staticmethod
    def parse_csv_table(excel_list):
        lens = [len(row) for row in excel_list]
        new_idx = max_idx = 0
        new_len = max_len = 0
        curr = lens[0]

        for elem in lens:
            if elem == curr:
                new_len += 1
                if max_len < new_len:
                    max_len, max_idx = new_len, new_idx

            else:
                if max_len < new_len:
                    max_len, max_idx = new_len, new_idx

                new_idx, new_len = lens.index(elem), 1
                curr = elem

        return excel_list[max_idx:max_idx+max_len]

    @staticmethod
    def document_text(filename):
        """ Return the document based file as txt string
        :param filename: name of the file
        :return: string as txt
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
