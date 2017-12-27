# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"

import os
from subprocess import call

import urllib3

from constants.path import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
devnull = open(os.devnull, 'w')


def download(url):
    file_name = url.split('/')[-1]
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)

    try:
        with open(Path.DOWNLOAD_DIR + file_name, 'wb') as f:
            f.write(r.read())

    except IOError as er:
        print(er)
        return False

    finally:
        f.close()

    r.release_conn()
    return True


def install_pip():
    try:
        import pip
        return True
    except ImportError:
        if download(Path.PIP_URL):
            return call(["python3", Path.DOWNLOAD_DIR + "get-pip.py"],
                        stdout=devnull, stderr=devnull) == 0
        return False


def install_prerequisites():
    return call(["pip3", "install", "-r", "requirements.txt"],
                stdout=devnull, stderr=devnull) == 0


if __name__ == '__main__':
    install_pip()
    install_prerequisites()
