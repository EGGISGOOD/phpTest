# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time,datetime,scrapy
import re
import urllib.request
import oss2,os
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from xml.sax.saxutils import unescape
from . import settings
import pymysql


#只保存当天的数据
class SaveSameDayPipeline(object):
    def process_item(self, item, spider):
    	#获取 3天前的 
        nowTime = int(time.time())

        tss1 = time.strftime("%Y-%m-%d 00:00:00",time.localtime()) #获取当前的时间戳
        timeArray = time.strptime(tss1,"%Y-%m-%d %H:%M:%S")
        starttime = int(time.mktime(timeArray))
        tss2 = item['pubtime']+':00'
        timeArray2 = time.strptime(tss2,"%Y-%m-%d %H:%M:%S")
        datetime = int(time.mktime(timeArray2))#指定日期的时间戳
        if(datetime < nowTime and datetime > starttime):
            return item
        else:
            raise DropItem("Missing price in %s" % item)


#获取单个文章的封面图
class CoverPipeline(ImagesPipeline):
    def get_media_requests(self, item, info): 
        referer=item['cover']  # 处理防盗链
        yield scrapy.Request(item['cover'],meta={'item': item,'referer':referer})#配合

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        nowTime = int(time.time())
        folder = time.strftime("%Y"+'/'+"%m" , time.localtime())
        folder_strip = folder.strip()
        #image_guid = request.url.split('/')[-1]
        image_guid = time.strftime("%M%S" , time.localtime())+request.url.split('/')[-1]
        filename = u'{0}/{1}'.format(folder_strip, image_guid)

        return filename


    def item_completed(self, results, item, info):   
        image_paths = [x['path'] for ok, x in results if ok]

        if not image_paths:
            #raise DropItem("Item contains no images")
            return item

        item['cover'] = '/' + settings.IMAGES_BASE_URL +'/'+ image_paths[0]
        #print(settings.IMAGES_STORE+'/'+ item['cover'])
        
        settings.BUCKET.put_object_from_file(settings.IMAGES_BASE_URL+'/'+ image_paths[0],  settings.IMAGES_STORE+'/'+image_paths[0]) 

        return item



#获取单个文章的内文图并替换
class PostImgPipeline(ImagesPipeline):

    #处理资源
    def get_media_requests(self, item, info): 
        for image_url in item['imageUrl']:
            referer=image_url  # 处理防盗链
            yield scrapy.Request(image_url,meta={'item': item,'referer':referer})#配合
 
      
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        nowTime = int(time.time())
        folder = time.strftime("%Y"+'/'+"%m" , time.localtime()) #获取当前的时间戳
        folder_strip = folder.strip()
        image_guid = request.url.split('/')[-1]
        image_guid = time.strftime("%M%S" , time.localtime())+request.url.split('/')[-1]
        filename = u'{0}/{1}'.format(folder_strip, image_guid)

        return filename
 

    #新成资源后处理
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        #old_image_url = [x['url'] for ok, x in results if ok]
        if not image_paths:
            return item
            #raise DropItem("Item contains no images")
        
        
        for i in results:
            one_img = i[1] #单个 图片的新成记录        
            
            settings.BUCKET.put_object_from_file(settings.IMAGES_BASE_URL+'/'+ one_img['path'],  settings.IMAGES_STORE+'/'+one_img['path']) #先将图片上传 OSS

            old_img = one_img['url']

            new_img = settings.IMAGES_URLS_FIELD+'/'+settings.IMAGES_BASE_URL+'/'+one_img['path']
            pattern = '<\s*img\s+[^>]*?original="'+old_img+'"[^>]*?\/?\s*>' #处理是否懒加载图片
            reg = re.compile(pattern)
            #content = item['content']
            

            if reg.search(item['content']):
                item['content'] = re.sub(pattern, "<img src='"+new_img+ "'  />", item['content'])
                #content = content
            else:
                item['content'] = item['content'].replace(old_img, new_img) #替换html 内的图片

        
        item['imagePaths'] = image_paths
        
        return item


#保存数据到Mysql 
class MysqlPipeline(object):
    
    def __init__(self):
        # 建立连接
        self.connect  = pymysql.connect(**settings.MYSQL_CONFIG)  # 有中文要存入数据库的话要加charset='utf8'
        
        """
        self.connect = pymysql.connect(
            host='192.168.1.249',  # 数据库地址
            port=3306,  # 数据库端口
            db='jia400',  # 数据库名
            user='jia400_tp',  # 数据库用户名
            passwd='HY#2018john#gz2018',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
         
        """
        # 创建游标
        self.cursor = self.connect.cursor()
 
    def process_item(self,item,spider): 

        #如果存在就不入库 
        
        #sql = "select * from jia_article where title = '"+item['title']+"' "
        sql = "select * from article_scrapy where title = '"+item['title']+"' "
       #res =  1
        res = self.cursor.execute(sql)

        if(res == 0):
            # sql语句
            """
            insert_sql = """
                #insert into jia_article(title,summary,user_id,author,article_category_id,thumb,create_time,publish_time,source,source_url) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
          
            # 执行插入数据到数据库操作
            self.cursor.execute(insert_sql,(item['title'],item['summary'],1,'admin',98,item['cover'],int(time.time()),int(time.time()),item['source'],item['source_url']))
            """
            insert_sql = """
                insert into article_scrapy(title,summary,content,source,source_url,thumb,create_time,update_time,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            self.cursor.execute(insert_sql,(item['title'],item['summary'],item['content'],item['source'],item['source_url'],item['cover'],int(time.time()),int(time.time()),1))
            # 提交，不进行提交无法保存到数据库
            self.connect.commit()
           
            #article_id = self.cursor.lastrowid
            
           # insert_sql = """
               # insert into jia_article_attach(article_id,content) VALUES(%s,%s)
           # """
            
            #self.cursor.execute(insert_sql,(article_id,item['content']))

            #self.connect.commit()

        return item

 
    def close_spider(self,spider):
        # 关闭游标和连接
        self.cursor.close()
        self.connect.close()






#去重 
#
#from scrapy.exceptions import DropItem
#
#class DuplicatesPipeline(object):

#   def __init__(self):
#       self.ids_seen = set()

#    def process_item(self, item, spider):
#        if item['id'] in self.ids_seen:
#            raise DropItem("Duplicate item found: %s" % item)
#        else:
#            self.ids_seen.add(item['id'])
#            return item
#
#
#
#
#
#
#