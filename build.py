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

    def __init__(self, name=None, field=None, link=None, typ=None, content=None):
        self.name = name
        self.field = field
        self.link = link
        self.type = typ
        self.content = content


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


def write_log(file, content):
    append_to_file(file, content)


def write_to_db(data):
    query = '''INSERT INTO Dataset Values(null, "%s", "%s", "%s", "%s", "%s");'''
    try:
        db = get_db()
        conn = db.cursor()
        conn.execute(query % (data.name, data.field,
                              data.link, data.type, data.content))
        db.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        db.close()


def create_dir(dirname):
    if not os.path.exists(os.path.join(os.path.expanduser("~"), "Downloads/" + dirname)):
        os.makedirs(os.path.join(
            os.path.expanduser("~"), "Downloads/" + dirname))


def statistics_known_extenstions(ext):
    known_count_extensions[known_extensions.index(ext)] += 1


def statistics_unknown_extenstions(ext):
    unknown_count_extensions[unknown_extensions.index(ext)] += 1


html = get_html(OPSI_LINK)
soup = BeautifulSoup(html, 'lxml')

archives = ['zip', 'gz', 'bz2', 'rar']

known_extensions = ['csv', 'json', 'xls', 'xlsx',
                    'pdf', 'doc', 'docx', 'zip', 'pcaxis', 'px']
known_count_extensions = [0] * (len(known_extensions) - 1)

unknown_extensions = []
unknown_count_extensions = []

for field in soup.find('ul', attrs={'class': 'sectors'}).findAll('li'):
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
            except requests.exceptions.ConnectionResetError as e:
                time.sleep(60)
                metadata_json = json.loads(get_html(metadata_link))
            dataset_title = metadata_json['result']['title']
            for meta in metadata_json['result']['resources']:
                if meta['format'].lower() in known_extensions and meta['url'].split('.')[-1].lower() in known_extensions:
                    statistics_known_extenstions(
                        meta['format'].lower())
                    filename = meta['url'].split('/')[-1]
                    # if len(filename) > 255:
                    #     ext = filename.split('.')[-1]
                    #     filename = "%s.%s" % (filename[:250], ext)
                    # create_dir(field_name[:255])
                    path = field_name + '/' + \
                        metadata_json['result']['title']
                    # create_dir(path[:255])
                    # write_to_file(path + '/' + filename, get_file(meta['url']))
                elif meta['format'].lower() in unknown_extensions:
                    statistics_unknown_extenstions(
                        meta['format'].lower())
                else:
                    unknown_extensions.append(meta['format'].lower())
                    unknown_count_extensions.append(0)
                    statistics_unknown_extenstions(
                        meta['format'].lower())
        page_count += 1

# Statistika
print(unknown_extensions, unknown_count_extensions)
print(known_extensions, known_count_extensions)



# page = BeautifulSoup(get_html(link.format(page_count)), 'lxml')
# if "<span>»</span>" in str(page.find("ul", {"class": "pagination"}).findAll("li")[-1]):
#     print("Number of datasets per page:", len(page.find("div", attrs={"class": "common-dataset-list"}).findAll("div")))
#     print("Page count:", page_count)
#     div = page.find('div', attrs={'class': 'padding up down'})
#     for a in div.findAll('a', attrs={'class': 'dataset-header'}):
#         metadata_link = OPSI_METADATA_LINK + \
#             a.get('href').split('/')[-1]
#         metadata_json = json.loads(get_html(metadata_link))
#         dataset_title = metadata_json['result']['title']
#         print('LINK - ', metadata_link)
#         # for meta in metadata_json['result']['resources']:
#         #     print("\n[%s] - '%s'" % (meta['format'], meta['url']))
#         #     if zipped(meta['url']):
#         #         content = unzip(get_html(meta['url']))
#         #     else:
#         #         content = get_html(meta['url']) if meta['format'].lower(
#         #     ) in known_extensions else 'null'
#         #     if meta['url'].split('.')[-1].lower() != meta['format'].lower():
#         #         content = 'null'
#         #     data = Data(dataset_title, field_name,
#         #                 meta['url'], meta['format'], content)
#         #     write_to_db(data)
# page_count += 1
