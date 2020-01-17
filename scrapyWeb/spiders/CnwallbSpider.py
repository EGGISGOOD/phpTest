# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem


class CnwallbSpider(scrapy.Spider):
    name = 'Cnwallb'
    allowed_domains = ['cnwallb.com']
    start_urls = [
    	'https://www.cnwallb.com/news/list-7.html',
		'https://www.cnwallb.com/news/list-13.html',
		'https://www.cnwallb.com/news/list-21.html',
		'https://www.cnwallb.com/news/list-24.html',
    ]

    def parse(self, response):
    	url = response.xpath('//div[@class="channel_content"]/ul/li/dl/div/dt/a/@href').extract()

    	for index in range(len(url)):
    		#if(index == 2):
    		yield scrapy.Request(url[index], callback=self.parse_detail)

    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//div[@class="sherry_title"]/h1/text()').extract()[0]
        item['summary'] = response.xpath('//div[@class="introduce"]/text()').extract()[0]

        content = ''
        #a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)        

        for con in response.xpath('//div[@id="content"]/div').extract():    
            #con = a_rs.sub('',con)#去掉内容的a标签
            content = content + con

        item['content'] =  content
        item['pubtime'] = ''
 
        imageurl = []

        for img in response.xpath('//div[@id="content"]/div/img/@src').extract():
            imageurl.append(img)

        print(imageurl)
        item['cover'] = imageurl[0]
        item['imageUrl'] = imageurl
        item['source_url'] = response.url
        item['source'] = "墙布窗帘网"


        yield item