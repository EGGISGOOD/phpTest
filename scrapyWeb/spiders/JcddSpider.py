# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem
from scrapyWeb.function import Function

class JcddSpider(scrapy.Spider):
    name = 'Jcdd'
    allowed_domains = ['jcdd.com']
    start_urls = [
    	'http://www.jcdd.com/news.html?cleanHtmlCache=1&page=1',
    	'http://www.jcdd.com/news.html?cleanHtmlCache=1&page=2',
    	'http://www.jcdd.com/news.html?cleanHtmlCache=1&page=3',
    	'http://www.jcdd.com/news.html?cleanHtmlCache=1&page=4',
    	'http://www.jcdd.com/news.html?cleanHtmlCache=1&page=5',
    	'http://www.jcdd.com/news.html?cleanHtmlCache=1&page=6',
    ]

    def parse(self, response):
        url = response.xpath('//div[@class="listnews"]/ul/li/div[@class="img fl"]/a/@href').extract()
        cover = response.xpath('//div[@class="listnews"]/ul/li/div[@class="img fl"]/a/img/@src').extract()
        title = response.xpath('//div[@class="listnews"]/ul/li/div[@class="img fl"]/a/@title').extract()
        #print(title)
        for index in range(len(url)):
            #if(index == 1):
            if(Function.hasTitle(title[index]) == 0):
                yield scrapy.Request(url[index], meta={'cover': cover[index]}, callback=self.parse_detail)    

    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//h1/text()').extract()[0]
        item['summary'] = response.xpath('//div[@class="content"]/h2/text()').extract()[0]
        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)
        
        content = ''

        for con in response.xpath('//div[@class="contentbox"]/p').extract():
        	con = a_rs.sub('',con)#去掉内容的a标签
        	content = content + con

           
        item['content'] =  content
        item['pubtime'] = ''
        
        imageurl = []

        for img in response.xpath('//div[@class="contentbox"]/p/img/@src').extract():
        	imageurl.append(img)



        item['imageUrl'] = imageurl
        item['cover'] = response.meta['cover']
        item['source_url'] = response.url
        item['source'] = "集成吊顶网"

        yield item