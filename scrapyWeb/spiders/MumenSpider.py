# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem
from scrapyWeb.function import Function

class MumenSpider(scrapy.Spider):
    name = 'Mumen'
    allowed_domains = ['mumen.com.cn']
    start_urls = [
	    'http://www.mumen.com.cn/news/list4.html',
	    'http://www.mumen.com.cn/news/list3.html',
	    'http://www.mumen.com.cn/news/list2.html',
	    'http://www.mumen.com.cn/news/list1.html',
    ]

    def parse(self, response):
    	url = response.xpath('//div[@class="newslist"]/ul/li/h2/a/@href').extract()
    	cover = response.xpath('//div[@class="newslist"]/ul/li/span/a/img/@src').extract()
    	title = response.xpath('//div[@class="newslist"]/ul/li/h2/a/text()').extract()
    	#print(title)
    	for index in range(len(url)):
    		if(Function.hasTitle(title[index]) == 0):
    			yield scrapy.Request(url[index], meta={'cover': cover[index]}, callback=self.parse_detail)    


    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//h1/text()').extract()[0]
        item['summary'] = response.xpath('//div[@class="txtzy"]/text()').extract()

        content = ''        
        for con in response.xpath('//div[@id="newdcont"]/p').extract():
        	#con = a_rs.sub('',con)#去掉内容的a标签
        	content = content + con

        item['content'] =  content
        item['pubtime'] =  ''
        imageurl = []

        for img in response.xpath('//div[@id="newdcont"]/p/img/@src').extract():
        	item['content'] = item['content'].replace(img, 'http://www.mumen.com.cn'+img) #替换html 内的图片
        	imageurl.append('http://www.mumen.com.cn'+img)


        item['cover'] = 'http://www.mumen.com.cn/'+response.meta['cover']
        item['imageUrl'] = imageurl
        item['source_url'] = response.url
        item['source'] = "木门网"

        yield item