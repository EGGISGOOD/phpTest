# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem
from urllib.parse import urlparse
from scrapyWeb.function import Function

class Home163Spider(scrapy.Spider):
    name = 'Home163'
    allowed_domains = ['163.com']
    start_urls = ['http://home.163.com/special/latest/']

    def parse(self, response):
        url = response.xpath('//div[@class="main f-fl"]//div/div[@class="list-block-n f-cb"]/div[@class="right-box f-pr"]/h4/a/@href').extract()
        title = response.xpath('//div[@class="main f-fl"]//div/div[@class="list-block-n f-cb"]/div[@class="right-box f-pr"]/h4/a/text()').extract()
        summary = response.xpath('//div[@class="main f-fl"]//div/div[@class="list-block-n f-cb"]/div[@class="right-box f-pr"]/p/text()').extract()    
        
        #print(title)
       	for index in range(len(url)):
            if(Function.hasTitle(title[index]) == 0):
            #if(index == 0):	
                yield scrapy.Request(url[index], meta={'summary': summary[index]}, callback=self.parse_detail)

        
       # nextLink = []
       # nextLink = response.xpath('//div[@class="pagediv"]/div[@class="pagebox m_page cl"]/a/@href').extract()


       # if nextLink:
           # nextLink = nextLink[0]
          #  nextpage= nextLink.split('./')[1]
          #  yield Request("https://jcz.chinabm.cn/news/hangye/" + nextpage + '/',callback=self.parse)


    def parse_detail(self, response):
        item = ScrapywebItem()
        #item['title'] = response.xpath('//div[@class="g-main-855 fl"]/div[@class="m-news-hd"]/h2/text()').extract()[0]
       # item['summary'] = response.xpath('//div[@class="g-main-855 fl"]/div[@class="m-news-bd js-anchor-newsnav"]/div[@class="m-news-box"]/div[@class="m-news-content"]/p/text()').extract()[0]
        item['title'] = response.xpath('//div[@class="post_content_main"]/h1/text()').extract()[0]
        #item['summary'] = response.xpath('//div[@class="m-news-content"]/p/text()').extract()[0]
        item['source_url'] = response.url
        item['source'] = "网易家居"
        content = ''


        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)
   
        #for con in response.xpath('//div[@class="g-main-855 fl"]/div[@class="m-news-bd js-anchor-newsnav"]/div[@class="m-news-box"]/div[@class="m-news-content"]/p').extract():
        for con in response.xpath('//div[@class="post_text"]/p').extract():    
            con = a_rs.sub('',con)#去掉内容的a标签
            content = content + con

       
        item['content'] =  content
        item['pubtime'] = ''
        
        imageurl = []
        for img in response.xpath('//div[@class="post_text"]/p/img/@src').extract():
        	url_data = urlparse(img)
        	a_url = url_data.scheme+'://'+url_data.netloc+url_data.path
        	imageurl.append(a_url)

        item['cover'] = imageurl[0]

        item['imageUrl'] = imageurl
        item['summary'] = response.meta['summary']



        yield item