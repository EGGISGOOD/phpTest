# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapywebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()        #定义标题项
    content = scrapy.Field()     #定义内容项
    pubtime = scrapy.Field()    #定义发表时间
    imageUrl = scrapy.Field()    #定义图片链接地址
    summary =  scrapy.Field()
    cover =  scrapy.Field()
    source = scrapy.Field() #来源
    source_url = scrapy.Field() #来源连接
    imagePaths = scrapy.Field()
