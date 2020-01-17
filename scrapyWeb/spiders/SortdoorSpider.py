# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem

class SortdoorSpider(scrapy.Spider):
    name = 'Sortdoor'
    allowed_domains = ['sortdoor.com']
    start_urls = [
    	'http://www.sortdoor.com/newsc/',
    ]

    def parse(self, response):
    	url = response.xpath('//div[@class="programa-mod-grid"]/div/div[@class="m-main"]/ul/li/a//@href').extract()
    	#cover = response.xpath('//ul[@class="newestArticleList"]/li/div/a/img/@src').extract()
 
    	for index in range(len(url)):
    		#if(index == 1):
    		yield scrapy.Request(url[index], callback=self.parse_detail)


    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//h1[@class="article-title"]/text()').extract()[0]
        item['summary'] = response.xpath('//p[@class="describe"]/text()').extract()[0]

        content = ''        
        for con in response.xpath('//div[@class="article-content fontSizeSmall BSHARE_POP"]/p').extract():
        	#con = a_rs.sub('',con)#去掉内容的a标签
        	content = content + con

        item['content'] =  content
        item['pubtime'] =  response.xpath('//span[@class="date"]/text()').extract()[0]

        imageurl = []

        for img in response.xpath('//div[@class="article-content fontSizeSmall BSHARE_POP"]/p/img/@src').extract():
            imageurl.append(img)

        item['cover'] = imageurl[0]
        item['imageUrl'] = imageurl
        item['source_url'] = response.url
        item['source'] = "搜门网"

        yield item



        