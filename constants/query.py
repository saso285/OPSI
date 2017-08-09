# -*- coding: utf-8 -*-

__author__ = "Saso Maric"
__copyright__ = "Copyright 2017, by Saso Maric"
__email__ = "sm8024@student.uni-lj.si"
__status__ = "Development"
__version__ = "1.0.0"


class Query(object):

	############################################################################
	#																		   #
	# DATASET QUERIES														   #
	#																		   #
	############################################################################

	SELECT_DATASET = """SELECT * FROM Dataset
	WHERE name='{0}'"""

	INSERT_DATASET = """INSERT INTO Dataset
	(name, metadata, type, views, created, modified, field_id) 
	VALUES({0},{1},{2},{3},{4},{5},{6})"""

	UPDATE_DATASET = """UPDATE Dataset
	SET name='{1}', metadata='{2}', type='{3}', views='{4}', created='{5}', 
	modified='{6}', field_id='{7}' 
	WHERE id='{0}'"""

	DELETE_DATASET = """DELETE FROM Dataset 
	WHERE id='{0}'"""


	############################################################################
	#																		   #
	# FIELD QUERIES														       #
	#																		   #
	############################################################################

	SELECT_FIELD = """SELECT * FROM Field
	WHERE name='{0}'"""

	INSERT_FIELD = """INSERT INTO Field
	(name, views, created, modified) 
	VALUES({0},{1},{2},{3})"""

	UPDATE_FIELD = """UPDATE Field
	SET name='{1}', views='{2}', created='{3}', modified='{4}' 
	WHERE id='{0}'"""

	DELETE_FIELD = """DELETE FROM Field 
	WHERE id='{0}'"""
