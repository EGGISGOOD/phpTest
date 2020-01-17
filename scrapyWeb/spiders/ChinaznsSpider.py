# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem
from scrapyWeb.function import Function

class ChinaznsSpider(scrapy.Spider):
    name = 'Chinazns'
    allowed_domains = ['chinazns.com']
    start_urls = [
    	'http://www.chinazns.com/news/p_1.html',
    	'http://www.chinazns.com/news/p_2.html',
    	'http://www.chinazns.com/news/p_3.html',
    	'http://www.chinazns.com/news/p_4.html',
    	'http://www.chinazns.com/news/p_5.html',
    ]

    def parse(self, response):
        url = response.xpath('//ul[@class="zx-list"]/li/dl/a/@href').extract()
        title = response.xpath('//ul[@class="zx-list"]/li/dl/a/@title').extract()
        cover = response.xpath('//ul[@class="zx-list"]/li/dl/a/dt/img/@src').extract()
        domain = 'http://www.chinazns.com'
        #print(title)
        for index in range(len(url)):
            #if(Function.hasTitle(title[index]) == 0):
            #if(index == 2):
            yield scrapy.Request(domain + url[index], meta={'cover' : cover[index]}, callback=self.parse_detail)    

    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//h1/text()').extract()[0]
        item['summary'] = response.xpath('//div[@class="infor_detail"]/p/text()').extract()[0]

        content = ''
        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)

        for con in response.xpath('//div[@class="infor_detail"]/p').extract():    
            con = a_rs.sub('',con)#去掉内容的a标签
            #con = "<p>" + con + "</p>"
            content = content + con


        item['content'] =  content
        item['pubtime'] = ''


        imageurl = []
        domain = 'http://www.chinazns.com'

        for img in response.xpath('//div[@class="infor_detail"]/p/img/@src').extract():
            item['content'] = item['content'].replace(img, domain+img) #替换html 内的图片
            imageurl.append(domain+img)

        item['cover'] = domain+response.meta['cover']
        item['imageUrl'] = imageurl
        item['source_url'] = response.url
        item['source'] = "智能锁网"


        yield item



