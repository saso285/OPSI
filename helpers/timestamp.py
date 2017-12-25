# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"

import time
from datetime import datetime


def timeout(sec):
    """ Sleep for a certain amount of time
    :param sec: number of seconds to sleep
    """
    time.sleep(sec)


def timestamp():
    """ Get unix epoch timestamp
    :return: timestamp integer
    """
    return int(time.time())


def convert_to_timestamp(timestamp):
    """ Convert OPSI given datetime format to unix epoch timestamp
    :return: timestamp integer
    """
    timestamp = timestamp.lower().split('t')
    date = timestamp[0]
    time = timestamp[1].split(".")[0][:-3]
    timestamp = date + " " + time
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M").strftime("%s")
