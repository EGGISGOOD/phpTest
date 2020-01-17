# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem
from scrapyWeb.function import Function

class ZnjjSpider(scrapy.Spider):
    name = 'Znjj'
    allowed_domains = ['znjj.tv']
    start_urls = [
    	'http://www.znjj.tv/news/list-1/',
    	'http://www.znjj.tv/news/list-11/',
    	'http://www.znjj.tv/news/list-12/',
    	'http://www.znjj.tv/news/list-3/',
    	'http://www.znjj.tv/news/list-2/',
    	'http://www.znjj.tv/news/list-13/',
    	'http://www.znjj.tv/news/list-6/',
    	'http://www.znjj.tv/news/list-14/',
    	'http://www.znjj.tv/news/list-9/',
    ]

    def parse(self, response):
        url = response.xpath('//div[@class="pd_jsxq"]/ul/li/dl/a/@href').extract()
        cover = response.xpath('//div[@class="pd_jsxq"]/ul/li/dl/a/dt/img/@src').extract()
        title = response.xpath('//div[@class="pd_jsxq"]/ul/li/dl/a/@title').extract()
        #print(title)
        for index in range(len(url)):
            if(Function.hasTitle(title[index]) == 0):
            #if(index == 2):
                a_cover = cover[index].replace('http://www.znjj.tv', cover[index])
                yield scrapy.Request(url[index], meta={'cover': a_cover}, callback=self.parse_detail)


    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//h1/text()').extract()[0]
        item['summary'] = response.xpath('//div[@class="infor_detail"]/p/text()').extract()[0]
        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)
        link_rs = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

        content = ''
        #for con in response.xpath('//div[@class="g-main-855 fl"]/div[@class="m-news-bd js-anchor-newsnav"]/div[@class="m-news-box"]/div[@class="m-news-content"]/p').extract():
        content = response.xpath('//div[@class="infor_detail"]').extract()[0]
        more_message =  response.xpath('//div[@class="infor_detail"]/div[@class="more_message"]').extract()[0]  
        content = content.replace(more_message,'')# div 中的 infor_detail
        content = a_rs.sub('',content)#去掉内容的a标签
        


        item['content'] =  content
        item['pubtime'] = ''
        
        imageurl = []

        for img in response.xpath('//div[@class="infor_detail"]/center/img/@src').extract():
            item['content'] = item['content'].replace(img, 'http://www.znjj.tv'+img) #替换html 内的图片
            imageurl.append('http://www.znjj.tv'+img)


        for img in response.xpath('//div[@class="infor_detail"]/p/img/@src').extract():
            #imageurl.append(img)
            item['content'] = item['content'].replace(img, 'http://www.znjj.tv'+img) #替换html 内的图片
            imageurl.append('http://www.znjj.tv'+img)

        




        item['imageUrl'] = imageurl
        item['cover'] = 'http://www.znjj.tv' + response.meta['cover']
        item['source_url'] = response.url
        item['source'] = "智家网"

        yield item