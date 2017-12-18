# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


import json
import requests

from bs4 import BeautifulSoup

from constants.urls import Urls


class Response(object):

    def __init__(self, status, text=""):
        """ Response object for passing the request information
        :param status: boolean whether the request succeeded or not
        :param text: parsed html of the webpage
        :type status: boolean
        :type text: string
        """
        self.status = status
        self.text = text


class Parse(object):

    @staticmethod
    def get_html(url):
        """ Get the html of a specific webpage
        :param url: url of the webpage
        :type url: string
        :return: response object containing boolean on whether the parse request
                 succeeded and the html of the webpage
        :rtype: object
        """
        try:
            return Response(True, requests.get(url).text.encode('UTF-8'))

        except requests.exceptions.RequestException as er:
            print(er)
            return Response(False)

    def get_soup(self, url):
        """ Return soup of the html
        :param url: url of the webpage
        :type url: string
        :return: response object containing boolean on whether the parse request
                 succeeded and the html of the webpage
        :rtype: object
        """
        response = self.get_html(url)

        if response.status:
            return Response(True, BeautifulSoup(response.text, 'lxml'))

        return response

    def fields(self):
        """ Return all fields found on OPSI
        :return: list of tuples of all the field names and their urls
        :rtype: list
        """
        field_list = []
        soup = self.get_soup(Urls.MAIN_URL)

        if soup.status:
            li_elem = soup.text.findAll(
                "li", attrs={"data-equalizer-watch": "sector"})

            for elem in li_elem:
                label = elem.find('div', attrs={'class': 'label'}).text
                url = elem.find('a', href=True)['href']
                field_list.append((label, url))

            return field_list

        return []

    def datasets(self, url):
        """ Return all datasets belonging to specific field
        :param url: link pointing to the specific field
        :type url: string
        :return: list of all datasets of specific field
        :rtype: list
        """
        dataset_list = []
        soup = self.get_soup("".join([Urls.MAIN_URL, url]))
        if soup.status:
            div = soup.text.findAll("div", attrs={"class": "dataset-summary"})

            for elem in div:
                name = elem.find(
                    'div', attrs={'class': 'underlined'}).contents[0].strip()
                label = elem.find(
                    'a', attrs={'class': 'dataset-header'})['href'].split("/")[-1]
                dataset_list.append((name, label))

            return dataset_list

        return []

    def dataset(self, name):
        """ Return all metadata about specific dataset
        :param name: dataset name
        :type name: string
        :return: metadata about specific dataset
        :rtype: json
        """
        return json.loads(self.get_html(Urls.API_SEARCH.format(name)).text)
