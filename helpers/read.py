# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


class Read(object):

    @staticmethod
    def file(filename):
        """ Return content of the provided file
        :param filename: name of the file
        :return: csv content as string
        """
        return str(open(filename, 'r').read())
