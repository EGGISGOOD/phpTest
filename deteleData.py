#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import oss2
import os
import datetime
import time
import sys
import shutil
sys.path.append('./class'); #引入自定义的class目录
from MysqlHelper import MysqlHelper
from dateutil.relativedelta import relativedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

#https://help.aliyun.com/document_detail/88463.html?spm=a2c4g.11186623.6.869.8d471b38WDrl8p

prefix = "uploads/posts" #文件的目录

"""
for obj in oss2.ObjectIterator(bucket, prefix=prefix):
    bucket.delete_object(obj.key)
"""

"""
MYSQL_CONFIG = {
    'host': '192.168.1.249',
    'port': 3306,
    'user': 'jia400_tp',
    'passwd': 'HY#2018john#gz2018',
    'charset': 'utf8',
}
"""


MYSQL_CONFIG = {
                'host':'rm-wz9jkpbav55t9604q.mysql.rds.aliyuncs.com',
                'port':3306,
                'user':'article_collect',
                'passwd':'jTY%^uy8989gh5856gh8F$%l',
               # 'db':'jia400_log',
                'charset':'utf8',
                #'cursorclass':pymysql.cursors.DictCursor,
}


DB_NAME = 'jia400_log'
TABLE_NAME = 'article_scrapy'
BEFORE_MONTH = 6 #6个月之前
#prefix = "uploads/posts" #文件的目录
ossPrefix = "/scrapy/"



def delOssImg(prefix):
    auth = oss2.Auth('LTAIPx0WdjloRpcC', 'bdkhKSqgQUIdK3IcqJwmLlSQlY6w7I')
    bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'test-vote-huuyaa-com')

    for obj in oss2.ObjectIterator(bucket, prefix=prefix):
        bucket.delete_object(obj.key)


#prefix = "uploads/posts" #文件的目录


#如果为脚本模式
if __name__ == "__main__":
    tss1 = (datetime.date.today() - relativedelta(months=BEFORE_MONTH)).strftime("%Y-%m-%d %H:%M:%S")  # 获取 6个月 前的 时间 字符串 如 '2013-10-10 23:40:00'
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    thatTimetamp = int(time.mktime(timeArray))  # 获取时间戳
    imgDir = time.strftime("%Y/%m", timeArray)  # 获取日期的路径
    imageDir = BASE_DIR +'/'+'scrapy'+'/'+ imgDir #获取当前文件的目录路径
    ossDir = 'scrapy'+'/'+ imgDir +'/'

    mydb = MysqlHelper(MYSQL_CONFIG)
    mydb.selectDataBase(DB_NAME) #select db

    sql = " update article_scrapy set status = 0 where create_time <= " + str(thatTimetamp)

    mydb.executeSql(sql) #执行sql 语句删除代码
    print('已删除数据库')

    #delOssImg(ossDir)#删除啊里云的数据
    #print('已删除阿里云图片')

    print('正在删除 '+imageDir+' 图片')
    if os.path.exists(imageDir):
		shutil.rmtree(imageDir)  # 删除整个目录

    print('已删除本地文件夹的图片')




