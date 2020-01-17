# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem
from scrapyWeb.function import Function

class CndqjcSpider(scrapy.Spider):
    name = 'Cndqjc'
    allowed_domains = ['cndqjc.com']
    start_urls = [
    	'https://www.cndqjc.com/news/xingyejiaodian/',
     	'https://www.cndqjc.com/news/pinpaidongtai/',
     	'https://www.cndqjc.com/news/mingrenfangtan/',
     	'https://www.cndqjc.com/news/shichanghuodong/',
     	'https://www.cndqjc.com/news/jiamengzixun/',
     	'https://www.cndqjc.com/news/shipinzixun/',
     	'https://www.cndqjc.com/news/zhanhuixinxi/',
        'https://www.cndqjc.com/news/dingqiangbaike/',
    ]

    def parse(self, response):
        url = response.xpath('//div[@class="news-list"]/div[@class="bd"]/ul/li/div[@class="thumb"]/a/@href').extract()
        cover = response.xpath('//div[@class="news-list"]/div[@class="bd"]/ul/li/div[@class="thumb"]/a/img/@src').extract()
        title = response.xpath('//div[@class="news-list"]/div[@class="bd"]/ul/li/div[@class="r-info"]/div[@class="title clearfix"]/h5/a/text()').extract()
        #print(title)
        for index in range(len(url)):
            if(Function.hasTitle(title[index]) == 0):
        #if(index == 4):
                yield scrapy.Request('https://www.cndqjc.com' + url[index], meta={'cover': cover[index]}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//h1/text()').extract()[0]
        item['summary'] = response.xpath('//div[@class="content"]/p/span/text()').extract()[0]

        content = ''
        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)

        for con in response.xpath('//div[@class="content"]/p').extract():    
            con = a_rs.sub('',con)#去掉内容的a标签
            #con = "<p>" + con + "</p>"
            content = content + con


        item['content'] =  content
        item['pubtime'] = ''


        imageurl = []

        for img in response.xpath('//div[@class="content"]/p/span/img/@src').extract():
            imageurl.append(img)


        for img in response.xpath('//div[@class="content"]/p/img/@src').extract():
            imageurl.append(img)


        item['cover'] = imageurl[0]
        item['imageUrl'] = imageurl
        item['source_url'] = response.url
        item['source'] = "顶墙集成网"

        yield item


