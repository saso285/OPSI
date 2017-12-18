# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


import json
import os
import sqlite3
import time
import zipfile

import requests
from bs4 import BeautifulSoup

from helpers.convert import Convert

OPSI_LINK = 'https://podatki.gov.si'
OPSI_METADATA_LINK = 'https://podatki.gov.si/api/3/action/package_show?id='

CONVERT = Convert()


class Data(object):

    def __init__(self, name=None, field=None, link=None, typ=None, content=None, update=None):
        self.name = name
        self.field = field
        self.link = link
        self.type = typ
        self.content = content
        self.update = update


def get_db():
    """ Get database connection
    :return: connection object
    """
    return sqlite3.connect('test.db')


def get_html(link):
    """ Get raw html from specific link
    :param link: link to website
    :return: html string
    """
    return requests.get(link).text


def get_file(link):
    """ Get file from specific link
    :param filename: link of the file
    :return: file content string
    """
    return requests.get(link).content


def archived(filename):
    """ Check if file is archived
    :param filename: name of the file
    :return: archive condition boolean
    """
    return "zip" in os.path.splitext(filename)[-1].lower()


def unzip(filename):
    """ Unzip a file
    :param filename: name of the file
    :return: dictionary of filenames
    """
    input_zip = zipfile.ZipFile(filename)
    return {name: input_zip.read(name) for name in input_zip.namelist()}


def download_dir():
    """ Get download directory of user
    :return: path string
    """
    return os.path.expanduser("~") + "/Downloads/"


def write_to_file(filepath, content):
    """ Write content to a file
    :param filepath: path to the file
    :param content: content of the file
    """
    file_path = os.path.join(download_dir() + filepath)

    with open(file_path, 'wb') as f:
        f.write(content)


def append_to_file(filepath, content):
    """ Append content to a file
    :param filepath: path to the file
    :param content: content of the file
    """
    file_path = os.path.join(download_dir() + filepath)

    with open(file_path, 'wb') as f:
        f.write(content)


def write_log_to_file(filename, content):
    """ Write content to a log file
    :param filepath: path to the file
    :param content: content of the file
    """
    append_to_file(filename, content)


def write_log_to_db(data, error):
    """ Write content to a log table in database
    :param data: data object
    :param error: error type
    """
    data.content = error
    data.timestamp = timestamp()
    data.dataset = data.name
    log_to_db(data)


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


def log_to_db(data):
    """ Execute query to log data in database
    :param data: data object 
    :return: insert success boolean
    """
    query = '''INSERT INTO Error Values(null, "%s", "%s", "%s", "%s", "%s", "%s");'''

    try:
        db = get_db()
        conn = db.cursor()
        conn.execute(query % (data.type, data.content, data.timestamp,
                              data.field, data.dataset, data.link))
        db.commit()
        return True

    except sqlite3.Error as er:
        print("log to db", e)
        return False

    finally:
        db.close()


def write_to_db(data):
    """ Execute query to insert data in database
    :param data: data object 
    :return: insert success boolean
    """
    query = '''INSERT INTO Dataset Values(null, "%s", "%s", "%s", "%s", "%s", "%s");'''

    try:
        db = get_db()
        conn = db.cursor()
        conn.execute(query % (data.name, data.field, data.link,
                              data.type, data.content, data.update))
        db.commit()
        return True

    except sqlite3.Error as e:
        print("write to db", e)
        write_log_to_db(data, e)
        return False

    except sqlite3.OperationalError as e:
        print("write to db", e)
        write_log_to_db(data, e)
        return False

    except ValueError as e:
        print("write to db", e)
        write_log_to_db(data, e)
        return False

    finally:
        db.close()


def write_to_cache(meta, metadata_json, field_name):
    """ Write file content to cache
    :param meta: metadata of specific document
    :param metadata_json: data metadata of specific dataset
    :param field_name: name of the field
    :return: cache file path string
    """
    dataset_title = metadata_json['result']['title']
    filename = meta['url'].split('/')[-1]

    if len(filename) > 255:
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (filename[:250], ext)

    create_dir(field_name[:255])
    dataset = field_name + '/' + metadata_json['result']['title']
    create_dir(dataset[:255])
    filename = dataset + '/' + filename
    write_to_file(filename, get_file(meta['url']))
    return download_dir() + filename


def create_dir(dirname):
    """ Create a new directory if it doesn't already exist
    :param dirname: name of the new directory
    """
    if not os.path.exists(os.path.join(download_dir() + dirname)):
        os.makedirs(os.path.join(download_dir() + dirname))


def filetype_known(extension):    
    """ Check if filetype is associated with the known ones
    :param extension: extension of a file 
    :return: extension known conditon boolean
    """
    return extension in known_filetypes


def filetype_convertable(extension):
    """ Check if filetype is associated with the ones that must be converted
    :param extension: extension of a file 
    :return: extension has to be converted conditon boolean
    """
    return extension in convertables


def exception(er, metadata_link):
    """ Timeout and repeat a file download request
    :param er: error type
    :param metadata_link: link to the requested file
    :return: repeated requests content string
    """
    print("exception", e)
    timeout(60)
    return json.loads(get_html(metadata_link))


html = get_html(OPSI_LINK)
soup = BeautifulSoup(html, 'lxml')

archives = ['zip', 'gz', 'bz2', 'rar']

known_filetypes = ['csv', 'json', 'pcaxis', 'px',
                   'xls', 'xlsx', 'doc', 'docx', 'pdf', 'txt']

convertables = ['xls', 'xlsx', 'doc', 'docx', 'pdf']

unknown_filetypes = set()

for field in soup.find('ul', attrs={'class': 'sectors'}).findAll('li')[-5:]: # OD FINANC NAPREJ!!!
    href = field.find('a').get('href')
    field_name = href.split('=')[-1]
    link = OPSI_LINK + href + "&page={0}"
    print("#" * 80)
    print("#", field_name)
    print("#", OPSI_LINK + href)
    print("#" * 80)
    print("\r")
    page_count = 1
    page = BeautifulSoup(get_html(link.format(page_count)), 'lxml')

    while page.find('div', {'class': 'tip-1'}):
        page = BeautifulSoup(get_html(link.format(page_count)), 'lxml')
        div = page.find('div', attrs={'class': 'padding up down'})

        for a in div.findAll('a', attrs={'class': 'dataset-header'}):
            metadata_link = OPSI_METADATA_LINK + a.get('href').split('/')[-1]

            try:
                metadata_json = json.loads(get_html(metadata_link))

            except requests.exceptions.HTTPError as e:
                print("main HTTPError", e)
                metadata_json = exception(e, metadata_link)

            except requests.exceptions.ConnectionError as e:
                print("main ConnectionError", e)
                metadata_json = exception(e, metadata_link)

            except requests.exceptions.ConnectTimeout as e:
                print("main ConnectTimeout", e)
                metadata_json = exception(e, metadata_link)

            dataset_title = metadata_json['result']['title']
            print(dataset_title)

            for meta in metadata_json['result']['resources']:
                extension = meta['url'].split('.')[-1].lower().strip()

                if filetype_known(extension):
                    print("[%s] - '%s' - " % (extension, meta['url']), end="")

                    filename = write_to_cache(meta, metadata_json, field_name)

                    if archived(meta['url']):
                        # content = unzip(get_html(meta['url']))
                        continue

                    if filetype_convertable(extension):
                        content = CONVERT.get_text(filename)

                    else:
                        content = get_html(meta['url']).replace('"', '\'')

                    data = Data(dataset_title, field_name, meta['url'],
                                meta['format'], content, meta['qa']['updated'])
                    print(write_to_db(data))

                else:
                    unknown_filetypes.add(meta['format'].lower().strip())
            print()
        print(unknown_filetypes, "\n")
        page_count += 1
