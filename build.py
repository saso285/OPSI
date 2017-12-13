# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


import os
import json
import time
import sqlite3
import zipfile
import requests

from bs4 import BeautifulSoup


OPSI_LINK = 'https://podatki.gov.si'
OPSI_METADATA_LINK = 'https://podatki.gov.si/api/3/action/package_show?id='


class Data(object):

    def __init__(self, name=None, field=None, link=None, typ=None, content=None, timestamp=None):
        self.name = name
        self.field = field
        self.link = link
        self.type = typ
        self.content = content
        self.timestamp = timestamp


def get_db():
    return sqlite3.connect('test.db')


def get_html(link):
    return requests.get(link).text


def get_file(link):
    return requests.get(link).content


def zipped(filename):
    return "zip" in os.path.splitext(filename)[-1].lower()


def unzip(filepath):
    input_zip = zipfile.ZipFile(filepath)
    return {name: input_zip.read(name) for name in input_zip.namelist()}


def write_to_file(file, content):
    file_path = os.path.join(os.path.expanduser("~"), "Downloads/" + file)
    with open(file_path, 'wb') as f:
        f.write(content)


def append_to_file(file, content):
    file_path = os.path.join(os.path.expanduser("~"), "Downloads/" + file)
    with open(file_path, 'wb') as f:
        f.write(content)


def write_log_to_file(file, content):
    append_to_file(file, content)


def write_log_to_db(data, e):
    data.content = e
    data.timestamp = timestamp()
    data.dataset = data.name
    log_to_db(data)


def timeout(sec):
    time.sleep(sec)


def timestamp():
    return int(time.time())


def log_to_db(data):
    query = '''INSERT INTO Error Values(null, "%s", "%s", "%s", "%s", "%s", "%s");'''
    try:
        db = get_db()
        conn = db.cursor()
        conn.execute(query % (data.type, data.content, data.timestamp,
                              data.field, data.dataset, data.link))
        db.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        db.close()


def write_to_db(data):
    query = '''INSERT INTO Dataset Values(null, "%s", "%s", "%s", "%s", "%s");'''
    try:
        db = get_db()
        conn = db.cursor()
        conn.execute(query % (data.name, data.field, data.link, data.type,
                              data.content))
        db.commit()
        return True
    except sqlite3.Error as e:
        write_log_to_db(data, e)
        return False
    except ValueError as e:
        write_log_to_db(data, e)
        return False
    finally:
        db.close()


def write_to_cache(meta, metadata_json, field_name):
    dataset_title = metadata_json['result']['title']
    filename = meta['url'].split('/')[-1]
    if len(filename) > 255:
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (filename[:250], ext)
    create_dir(field_name[:255])
    path = field_name + '/' + metadata_json['result']['title']
    create_dir(path[:255])
    write_to_file(path + '/' + filename, get_file(meta['url']))


def create_dir(dirname):
    if not os.path.exists(os.path.join(os.path.expanduser("~"), "Downloads/" + dirname)):
        os.makedirs(os.path.join(
            os.path.expanduser("~"), "Downloads/" + dirname))


def statistics_known_extenstions(ext):
    known_count_extensions[known_filetypes.index(ext)] += 1


def statistics_unknown_extenstions(ext):
    unknown_count_extensions[unknown_filetypes.index(ext)] += 1


def filetype_known(meta):
    return meta['url'].split('.')[-1].lower() in known_filetypes


html = get_html(OPSI_LINK)
soup = BeautifulSoup(html, 'lxml')

archives = ['zip', 'gz', 'bz2', 'rar']

known_filetypes = ['csv', 'json', 'pcaxis', 'px']
known_count_extensions = [0] * (len(known_filetypes) - 1)

unknown_filetypes = ['xls', 'xlsx', 'doc', 'docx', 'pdf']
unknown_count_extensions = [0] * (len(unknown_filetypes))


for field in soup.find('ul', attrs={'class': 'sectors'}).findAll('li')[-5:]:
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
                print(e)
                timeout(60)
                metadata_json = json.loads(get_html(metadata_link))

            except requests.exceptions.ConnectionError as e:
                print(e)
                timeout(60)
                metadata_json = json.loads(get_html(metadata_link))

            except ConectionResetError as e:
                print(e)
                timeout(60)
                metadata_json = json.loads(get_html(metadata_link))

            dataset_title = metadata_json['result']['title']
            print(dataset_title)

            for meta in metadata_json['result']['resources']:
                if filetype_known(meta):
                    statistics_known_extenstions(meta['format'].lower())
                    write_to_cache(meta, metadata_json, field_name)
                    print("[%s] - '%s' - " %
                          (meta['format'], meta['url']), end="")

                    if zipped(meta['url']):
                        content = unzip(get_html(meta['url']))
                        continue

                    elif meta['url'].split('.')[-1].lower() in known_filetypes:
                        content = get_html(meta['url']).replace('"', '\'')

                    else:
                        content = 'null'
                    data = Data(dataset_title, field_name,
                                meta['url'], meta['format'], content)
                    print(write_to_db(data))

                elif meta['format'].lower() in unknown_filetypes:
                    statistics_unknown_extenstions(
                        meta['format'].lower())

                else:
                    unknown_filetypes.append(meta['format'].lower())
                    unknown_count_extensions.append(0)
                    statistics_unknown_extenstions(
                        meta['format'].lower())
            print()
        page_count += 1
