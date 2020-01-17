# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapyWeb.items import ScrapywebItem
from scrapyWeb.function import Function


class Jia360Spider(scrapy.Spider):
    name = 'Jia360'
    allowed_domains = ['jia360.com']

    start_urls = [
    	'http://www.jia360.com/index/getNews?cid=16&p=5',
    	'http://www.jia360.com/index/getNews?cid=16&p=4',
    	'http://www.jia360.com/index/getNews?cid=16&p=3',
    	'http://www.jia360.com/index/getNews?cid=16&p=2',
    	'http://www.jia360.com/index/getNews?cid=16&p=1',
    ]

    def parse(self, response):
        data =  json.loads(response.text)
        jia360_new_url = 'http://www.jia360.com/new/';

        if(data):
            for index in range(len(data)):
                title = data[index]['title']
                url = jia360_new_url + data[index]['id'] + '.html'
                smeta = data[index]['smeta']
                desc =  data[index]['desc'] 
                thumb = json.loads(smeta)
                thumb =  thumb['thumb'][0] if True else ''
                #print(title)
                #if(Function.hasTitle(title) == 0):
                yield scrapy.Request(url, meta={'cover': thumb,'summary':desc}, callback=self.parse_detail)


    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//div[@class="fl newsD_left"]/h6/text()').extract()[0]
        item['summary'] = response.meta['summary']
        item['cover'] = response.meta['cover']

        content = ''
        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)
        
        for con in response.xpath('//div[@class="newsD_contend"]/p').extract():    
            con = a_rs.sub('',con)#去掉内容的a标签
            #con = "<p>" + con + "</p>"
            content = content + con



        imageurl = []

        for img in response.xpath('//div[@class="newsD_contend"]/p/img/@src').extract():
        	imageurl.append(img)

        item['imageUrl'] = imageurl	
        item['content'] =  content
        item['pubtime'] = ''
        item['source_url'] = response.url
        item['source'] = "腾讯家居"

        yield item