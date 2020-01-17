# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem
from scrapyWeb.function import Function


class ChinafloorSpider(scrapy.Spider):
    name = "Chinafloor"
    allowed_domains = ['chinafloor.cn']



    def __init__(self):
        self.start_urls = [

            "https://www.chinafloor.cn/news/attrlist-htm-a-h.html",
            "https://www.chinafloor.cn/news/attrlist-htm-a-o.html",
            "https://www.chinafloor.cn/news/list-1515.html",
            "https://www.chinafloor.cn/news/list-1958.html",
            "https://www.chinafloor.cn/news/list-1525.html",
            "https://www.chinafloor.cn/news/qiye/"
        ]


    def parse(self, response):

        
        #if(response.url.find('news.') > 0): #如果为主站
            #中华 主站 页面元素 
        url = response.xpath('//div[@class="db-mn-list"]/div/dl/dt/a/@href').extract()
        title = response.xpath('//div[@class="db-mn-list"]/div/dl/dd/h2/a/text()').extract()
        cover = response.xpath('//div[@class="db-mn-list"]/div/dl/dt/a/img/@original').extract()
        

       # print(url);
        for index in range(len(url)):
            #if(index == 2):
                #if(Function.hasTitle(title[index]) == 0):
                yield scrapy.Request(url[index], meta={'cover': cover[index]}, callback=self.parse_detail)


    def parse_detail(self, response):
        item = ScrapywebItem()
        #item['title'] = response.xpath('//div[@class="g-main-855 fl"]/div[@class="m-news-hd"]/h2/text()').extract()[0]
       # item['summary'] = response.xpath('//div[@class="g-main-855 fl"]/div[@class="m-news-bd js-anchor-newsnav"]/div[@class="m-news-box"]/div[@class="m-news-content"]/p/text()').extract()[0]
        item['title'] = response.xpath('//div[@class="db-ad-structure"]/h1/text()').extract()[0]
        item['summary'] = response.xpath('//div[@class="db-ad-structure"]/p[@class="db-lead"]/text()').extract()[0]
        content = ''


        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)
   
        #for con in response.xpath('//div[@class="g-main-855 fl"]/div[@class="m-news-bd js-anchor-newsnav"]/div[@class="m-news-box"]/div[@class="m-news-content"]/p').extract():
        for con in response.xpath('//div[@class="db-detail"]/div/p').extract():    
            con = a_rs.sub('',con)#去掉内容的a标签
            content = content + con


        item['content'] =  content
        item['pubtime'] = ''
        
        imageurl = []

        for img in response.xpath('//div[@class="db-detail"]/div/p/img/@original').extract():
            imageurl.append(img)


        item['imageUrl'] = imageurl
        item['cover'] = response.meta['cover']
        item['source_url'] = response.url
        item['source'] = "中华地板网"


        yield item


