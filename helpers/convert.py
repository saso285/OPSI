# -*- coding: utf-8 -*-

import csv
import os

import xlrd

import docx
from PyPDF2 import PdfFileReader


class Convert(object):

    def excel_file(filename):
        path = abspath(filename) + "/{0}.csv"
        workbook = xlrd.open_workbook(filename)
        csv_file = None
        for sheet_name in workbook.sheet_names():
            sheet = workbook.sheet_by_name(sheet_name)
            try:
                if len(workbook.sheet_names()) == 1:
                    raw_filename = os.path.basename(filename).split(".")[0]
                    csv_file = open(path.format(
                                    raw_filename), 'w', encoding='utf-8')
                else:
                    csv_file = open(path.format(sheet_name),
                                    'w', encoding='utf-8')
            except IOError as e:
                print e
                return
            try:
                writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                for row in range(sheet.nrows):
                    row_text = [item for item in sheet.row_values(row) if item]
                    if row_text:
                        writer.writerow(row_text)
            except csv.Error as e:
                print e
                return
            finally:
                csv_file.close()

    def document_file(filename):
        raw_filename = os.path.basename(filename).split(".")[0]
        txt_file = abspath(filename) + "/{0}.txt".format(raw_filename)
        try:
            output = open(txt_file, "w")
            document = docx.Document(filename)
            for row in document.paragraphs:
                if row.text:
                    output.write(row.text)
        except IOError as e:
            print e
            return
        finally:
            output.close()

    def pdf_file(filename):
        raw_filename = os.path.basename(filename).split(".")[0]
        txt_file = abspath(filename) + "/{0}.txt".format(raw_filename)
        try:
            output = open(txt_file, "w")
            input_file = open(filename, "rb")
            reader = PdfFileReader(input_file)
            content = reader.getPage(0).extractText().split('\n')
            for line in content:
                if line:
                    output.write(line)
        except IOError as e:
            print e
            return
        finally:
            output.close()
            input_file.close()


def abspath(filename):
    return os.path.dirname(os.path.abspath(filename))
