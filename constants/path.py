# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"

import os


class Path(object):

    ROOT_DIR = os.path.dirname(os.path.abspath("server.py"))
    DOWNLOAD_DIR = os.path.expanduser("~") + "/Downloads/"

    DATABASE = ROOT_DIR + '/database.db'
    DATABASE_SQL = ROOT_DIR + '/database.sql'

    PIP_URL = 'https://bootstrap.pypa.io/get-pip.py'
