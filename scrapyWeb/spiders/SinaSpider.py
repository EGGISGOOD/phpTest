# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem

class SinaSpider(scrapy.Spider):
    name = 'Sina'
    allowed_domains = ['jiaju.sina.com.cn']
    start_urls = [
    				'https://news.jiaju.sina.com.cn/list-jiaju-m', #新浪家居
    				'http://news.jiaju.sina.com.cn/list-jiaju-h2', #家具
    				'http://news.jiaju.sina.com.cn/list-jiaju-h15',#门窗
    				'http://news.jiaju.sina.com.cn/list-jiaju-h8', #厨房
    				'http://news.jiaju.sina.com.cn/list-jiaju-h10'#衣柜
    			]

    def parse(self, response):
    	url1= response.xpath('//div[@class="mainCont"]/div[@class="main"]/div[@class="newslist"]/dl/h4/a/@href').extract()
    	url2 = response.xpath('//div[@class="mainCont"]/div[@class="main"]/div[@class="newslist"]/div/dl/h4/a/@href').extract()    	
    	url = url1+url2

    	for index in range(len(url)):
    		#if(index == 1):
    			#print(url[index])
            yield scrapy.Request(url[index], callback=self.parse_detail)



    def parse_detail(self, response):
        item = ScrapywebItem()
        item['title'] = response.xpath('//div[@class="main-left fl"]/h1/text()').extract()[0]
        item['summary'] = response.xpath('//div[@id="digest"]/p/text()').extract()[0]

        content = ''

        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)
   
        #for con in response.xpath('//div[@class="g-main-855 fl"]/div[@class="m-news-bd js-anchor-newsnav"]/div[@class="m-news-box"]/div[@class="m-news-content"]/p').extract():
        for con in response.xpath('//div[@id="articleText"]/p').extract():    
            con = a_rs.sub('',con)#去掉内容的a标签
            #con = "<p>" + con + "</p>"
            content = content + con

       
        item['content'] =  content
        item['pubtime'] = ''
 
        imageurl = []

        for img in response.xpath('//div[@id="articleText"]/p/img/@src').extract():
            imageurl.append(img)



        item['cover'] = imageurl[0]
        item['imageUrl'] = imageurl
        item['source_url'] = response.url
        item['source'] = "新浪家居"


        yield item