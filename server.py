# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


import json
import os

from flask import Flask, Response, jsonify, redirect, render_template, request

import helpers.statistics as Statistics
from helpers.tree import Tree

app = Flask(__name__)
PORT = int(os.getenv('PORT', 3000))


@app.route('/')
def index():
    """ Return the index.html to client
    :return: html of index file
    """
    return render_template('index.html'), 200


@app.route('/statistics', methods=['GET'])
def statistics():
    """ Return the statistics.html to client
    :return: html of index file
    """
    return render_template('statistics.html'), 200


@app.route('/statistics/field', methods=['POST'])
def field():
    """ Return the statistics.html to client
    :return: html of index file
    """
    data = request.get_json()
    return jsonify(result=Statistics.field_type_count(data['field']))


@app.route('/statistics/error', methods=['GET'])
def error_percentage():
    """ Return the percentage of file saving or converting errors
    :return: array of dictionaries with labels and percents
    """
    error_percentage = Statistics.error_percentage()
    error = [{'label': 'complete', 'y': "{0:.2f}".format(
        (1 - error_percentage) * 100)}]
    if error_percentage > 0:
        error.append(
            {'label': 'error', 'y': "{0:.2f}".format(error_percentage * 100)})
    return jsonify(result=error)


@app.route('/statistics/types', methods=['GET'])
def type_count():
    """ Return the count of each type occurence
    :return: array of dictionaries with labels and counts
    """
    types = []
    for typ in Statistics.all_type():
        types.append({'label': typ.lower(), 'y': Statistics.type_count(typ)})
    return jsonify(result=types)


@app.route('/statistics/extension', methods=['GET'])
def unknown_extension_count():
    """ Return the count of each unknown extension occurence
    :return: array of dictionaries with labels and percents
    """
    extensions = []
    for ext in Statistics.all_unknown_extension():
        extensions.append(
            {'label': ext, 'y': Statistics.count_unknown_extension(ext)})
    return jsonify(result=extensions)


@app.route('/statistics/accessible', methods=['GET'])
def data_pull_success():
    """ Return the data about all data pulls
    :return: float data pull success percentage
    """
    return jsonify(result=Statistics.accessible_data())


@app.route('/fields', methods=['GET'])
def get_fields():
    """ Return all fields from OPSI
    :return: json containing list of all fields and their relative urls
    """
    return jsonify(result=Tree.fields())


@app.route('/fields', methods=['POST'])
def get_datasets():
    """ Return all datasets of specific field from OPSI
    :return: json containing list of all datasets and their relative urls
    """
    data = request.get_json()
    return jsonify(result=Tree.datasets(data['field']))


@app.route('/files', methods=['POST'])
def get_dataset():
    """ Return all info about specific dataset from OPSI
    :return: json containing all information about specific dataset
    """
    data = request.get_json()
    return jsonify(result=Tree.files(data['label']))


@app.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    """ Return all info about specific dataset from OPSI
    :return: json containing all information about specific dataset
    """
    content = Tree.file_content(filename)
    file_name = "attachment;filename={0}".format(filename)
    return Response(content, mimetype="text/plain",
                    headers={"Content-Disposition": file_name})


@app.route('/<path:path>')
def catch_all(path):
    """ Return the index.html to client because user requested non-existan
        endpoint
    :param path: relative url path
    :return: redirect function
    """
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=PORT, debug=True)
