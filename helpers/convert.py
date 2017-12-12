# -*- coding: utf-8 -*-

import os
import csv
import docx
import xlrd

from PyPDF2 import PdfFileReader


class Convert(object):

    def excel(filename):
        path = abspath(filename) + "/{0}.csv"
        workbook = xlrd.open_workbook(filename)
        for sheet_name in workbook.sheet_names():
            sheet = workbook.sheet_by_name(sheet_name)
            if len(workbook.sheet_names()) == 1:
                raw_filename = os.path.basename(filename).split(".")[0]
                csv_file = open(path.format(raw_filename), 'w', encoding='utf-8')
            else:
                csv_file = open(path.format(sheet_name), 'w', encoding='utf-8')
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            for row in range(sheet.nrows):
                row_text = [item for item in sheet.row_values(row) if item]
                if row_text:
                    writer.writerow(row_text)
            csv_file.close()

    def document(filename):
        raw_filename = os.path.basename(filename).split(".")[0]
        txt_file = abspath(filename) + "/{0}.txt".format(raw_filename)
        output = open(txt_file, "w")
        document = docx.Document(filename)
        for row in document.paragraphs:
            if row.text:
                output.write(row.text)
        output.close()

    def pdf(filename):
        raw_filename = os.path.basename(filename).split(".")[0]
        txt_file = abspath(filename) + "/{0}.txt".format(raw_filename)
        output = open(txt_file, "w")
        input_file = open(filename, "rb")
        reader = PdfFileReader(input_file)
        content = reader.getPage(0).extractText().split('\n')
        for line in content:
            if line:
                output.write(line)
        output.close()
        input_file.close()


def abspath(filename):
    return os.path.dirname(os.path.abspath(filename))
