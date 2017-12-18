# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


import os

import xlrd

import docx
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

    @staticmethod
    def excel_text(filename):
        """ Return the excel based file as csv string
        :param filename: name of the file
        :return: string as csv
        """
        excel_content = []
        workbook = xlrd.open_workbook(filename)
        for sheet_name in workbook.sheet_names():
            sheet = workbook.sheet_by_name(sheet_name)
            line = []
            for row in range(sheet.nrows):
                line = [str(item) for item in sheet.row_values(row) if item]
                if line:
                    excel_content.append(line)
        # max_len = max(len(item) for item in excel_content)
        # excel_content = [item for item in excel_content if len(item) == max_len]
        text = [','.join(item) for item in excel_content]
        return '\n'.join(text).replace('"', '\'').strip() or None

    @staticmethod
    def document_text(filename):
        """ Return the document based file as txt string
        :param filename: name of the file
        :return: string as txt
        """
        document_content = ""
        document = docx.Document(filename)
        for row in document.paragraphs:
            if row.text:
                document_content += row.text
        return document_content.replace('"', '\'').strip() or None

    @staticmethod
    def pdf_text(filename):
        """ Return the pdf based file as txt string
        :param filename: name of the file
        :return: string as txt
        """
        pdf_content = ""
        try:
            input_file = open(filename, "rb")
            reader = PdfFileReader(input_file, strict=False)
            for page in range(0, reader.getNumPages()):
                pdf_content += reader.getPage(page).extractText()
        except IOError as er:
            print(er)
        return pdf_content.replace('"', '\'').strip() or None


def abspath(filename):
    """ Return the absolute path of the file
    :param filename: name of the file
    :return: absolute path
    """
    return os.path.dirname(os.path.abspath(filename))
