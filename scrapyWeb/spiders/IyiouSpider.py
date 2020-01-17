# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem
from scrapyWeb.function import Function

class IyiouSpider(scrapy.Spider):
    name = 'Iyiou'
    allowed_domains = ['iyiou.com']
    start_urls = [
    	'https://www.iyiou.com/jiazhuang/5.html',
    	'https://www.iyiou.com/jiazhuang/4.html',
    	'https://www.iyiou.com/jiazhuang/3.html',
    	'https://www.iyiou.com/jiazhuang/2.html',
    	'https://www.iyiou.com/jiazhuang/1.html',
    ]

    def parse(self, response):
        url = response.xpath('//ul[@class="newestArticleList"]/li/div/a/@href').extract()
        title = response.xpath('//ul[@class="newestArticleList"]/li/div/a/@title').extract()
        cover = response.xpath('//ul[@class="newestArticleList"]/li/div/a/img/@src').extract()
        print(url)
        for index in range(len(url)):
            #if(Function.hasTitle(title[index]) == 0):
            #if(index == 2):
            #print(url[index])
            yield scrapy.Request(url[index], meta={'cover': cover[index]}, callback=self.parse_detail)    




    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//h1[@id="post_title"]/text()').extract()[0]
        item['summary'] = response.xpath('//div[@id="post_brief"]/text()').extract()[0]
        item['cover'] = response.meta['cover']
        content = ''

        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)

        for con in response.xpath('//div[@id="post_description"]/p').extract():
        	con = a_rs.sub('',con)#去掉内容的a标签
        	content = content + con

        item['content'] = '<p style="text-align: center;"><img src="'+item['cover']+'" /></p>' + content
        
        item['pubtime'] = response.xpath('//div[@id="post_date"]/text()').extract()[0]

        imageurl = []


        #for img in response.xpath('//div[@id="post_description"]/p/img/@src').extract():
        imageurl.append(item['cover'])


        item['imageUrl'] = imageurl
        item['source_url'] = response.url
        item['source'] = "亿欧"

        yield item
