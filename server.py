# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


import os
import atexit
import sqlite3

from flask import Flask, g, jsonify, url_for, redirect, request, render_template

from helpers.parse import Parse


################################################################################
#                                                                              #
# VARIABLE INITIALIZATION                                                      #
#                                                                              #
################################################################################

app = Flask(__name__)
port = int(os.getenv('PORT', 8080))


################################################################################
#                                                                              #
# REST ENDPOINT REDIRECTIONS                                                   #
#                                                                              #
################################################################################

@app.route('/')
def index():
    """ Return the index.html to client
    :return: html of index file
    :rtype: object
    """
    return render_template('index.html'), 200

@app.route('/fields', methods=['GET'])
def get_fields():
    """ Return all fields from OPSI
    :return: json containing list of all fields and their relative urls 
    :rtype: json
    """
    return jsonify(result=Parse().fields())

@app.route('/fields', methods=['POST'])
def get_datasets():
    """ Return all datasets of specific field from OPSI
    :return: json containing list of all datasets and their relative urls 
    :rtype: json
    """
    data = request.get_json()
    return jsonify(result=Parse().datasets(data['url']))

@app.route('/field', methods=['POST'])
def get_dataset():
    """ Return all info about specific dataset from OPSI
    :return: json containing all information about specific dataset 
    :rtype: json
    """
    data = request.get_json()
    return jsonify(Parse().dataset(data['label']))

@app.route('/<path:path>')
def catch_all(path):
    """ Return the index.html to client because user requested non-existant 
        endpoint
    :param path: relative url path
    :type path: string
    :return: redirect function
    :rtype: function call
    """
    return redirect('/', code=302)


################################################################################
#                                                                              #
# MAIN EXECUTION AND TERMINATION                                               #
#                                                                              #
################################################################################

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port, debug=True)
