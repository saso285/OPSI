# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


class Data(object):

    def __init__(self, name=None, field=None, link=None, typ=None, content=None,
                 update=None, dataset=None, filename=None, parsed_type=None):
        self.name = name
        self.field = field
        self.link = link
        self.type = typ
        self.parsed_type = parsed_type
        self.content = content
        self.update = update
        self.dataset = dataset
        self.filename = filename
