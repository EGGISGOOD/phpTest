# -*- coding: utf-8 -*-
import scrapy
from . import settings
import pymysql

class Function():

	def hasTitle(title):
		connect = pymysql.connect(**settings.MYSQL_CONFIG)
		cursor = connect.cursor()
		#sql = "select * from jia_article where title = '"+title+"' "
		sql = "select * from article_scrapy where title = '"+title+"' "
		res = cursor.execute(sql)

		cursor.close()
		connect.close()
		return res
