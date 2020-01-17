# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem
from urllib.parse import urlparse
from scrapyWeb.function import Function

class Www27580cnSpider(scrapy.Spider):
    name = 'www27580cn'
    allowed_domains = ['27580.cn']
    start_urls = [
    	'http://www.27580.cn/?m=news&s=list',
    ]

    def parse(self, response):
        url = response.xpath('//div[@class="news_list inner-module"]/div[@class="media"]/a/@href').extract()
        summary = response.xpath('//div[@class="news_list inner-module"]/div[@class="media"]/div[@class="media-body"]/p/text()').extract()    
        
        for index in range(len(url)):
            #if(index == 0):
            #yield scrapy.Request(url[index], callback=self.parse_detail)
            yield scrapy.Request(url[index], meta={'summary': summary[index]}, callback=self.parse_detail)
        

    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//div[@class="detail_body"]/h1[@class="text-left"]/text()').extract()[0]

        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)
        
        content = ''

        for con in response.xpath('//div[@class="detail_content"]').extract():
        	con = a_rs.sub('',con)#去掉内容的a标签
        	content = content + con

           
        item['content'] =  content
        item['pubtime'] = ''
        
        imageurl = []

        for img in response.xpath('//div[@class="detail_content"]/p/img/@src').extract():
            item['content'] = item['content'].replace(img, 'http://www.27580.cn'+img) #替换html 内的图片
            imageurl.append('http://www.27580.cn'+img)
            #url_data = urlparse(img)

            #a_url = url_data.scheme+'://'+url_data.netloc+url_data.path
            #imageurl.append(a_url)

        for img in response.xpath('//div[@class="detail_content"]/div/img/@src').extract():
            item['content'] = item['content'].replace(img, 'http://www.27580.cn'+img) #替换html 内的图片
            imageurl.append('http://www.27580.cn'+img)


        item['summary'] = response.meta['summary']    
        item['imageUrl'] = imageurl
        item['cover'] = imageurl[0]
        item['source_url'] = response.url
        item['source'] = "中外涂料网"

        yield item