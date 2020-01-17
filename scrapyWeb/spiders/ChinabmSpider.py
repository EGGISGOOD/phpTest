# -*- coding: utf-8 -*-
import scrapy
import re
from scrapyWeb.items import ScrapywebItem
from scrapyWeb.function import Function


class ChinabmSpider(scrapy.Spider):
    name = "Chinabm"
    allowed_domains = ['chinabm.cn']


    def __init__(self):
        self.start_urls = [
            # "https://news.chinabm.cn/yejiejy/",
            "https://news.chinabm.cn/jcnews/",
            "https://news.chinabm.cn/jcnews/2",
            "https://news.chinabm.cn/hangye/",
            "https://news.chinabm.cn/hangye/2/",
            "https://news.chinabm.cn/dongtai/",
            "https://news.chinabm.cn/dongtai/2/",
            "https://news.chinabm.cn/cuxiao/",
            "https://news.chinabm.cn/cuxiao/2/",
            "https://news.chinabm.cn/lingxiu/",
            "https://news.chinabm.cn/lingxiu/2/",
            "https://news.chinabm.cn/yejiejy/",
            "https://news.chinabm.cn/yejiejy/2/",
            "https://news.chinabm.cn/weiquan/",
            "https://news.chinabm.cn/weiquan/2/",
            'https://news.chinabm.cn/qynews/',
            'https://news.chinabm.cn/qynews/2',
           # "https://menchuang.chinabm.cn/news/hangye/1/",
           # "https://menchuang.chinabm.cn/news/hangye/2/",
           # "https://yigui.chinabm.cn/news/hangye/1/",
           # "https://yigui.chinabm.cn/news/hangye/2/",
           # "https://zhinengsuo.chinabm.cn/news/hangye/1/",
            #"https://zhinengsuo.chinabm.cn/news/hangye/2/",
          #  "https://clby.chinabm.cn/news/hangye/1/",
          #  "https://clby.chinabm.cn/news/hangye/2/",
          #  "https://chugui.chinabm.cn/news/hangye/1/",
           # "https://chugui.chinabm.cn/news/hangye/2/",
        ]


    def parse(self, response):

        
        if(response.url.find('news.') > 0): #如果为主站
            #中华 主站 页面元素 
            url = response.xpath('//div[@class="news_tlist"]/dl/dt/a/@href').extract()
            title = response.xpath('//div[@class="news_tlist"]/dl/dd/h3/a[2]/text()').extract()
            cover = response.xpath('//div[@class="news_tlist"]/dl/dt/a/img/@original').extract()
        else:
             #中华 分站 页面元素 
            url = response.xpath('//div[@class="news_tlist"]/dl/dd/h3/a/@href').extract()
            title = response.xpath('//div[@class="news_tlist"]/dl/dd/h3/a/text()').extract()
            cover = response.xpath('//div[@class="news_tlist"]/dl/dt/a/img/@original').extract()    

        #print(title)
        #print(Function.hasTitle('七夕│这波狗粮，我先记下了'))

        #for url in response.xpath('//div[@class="news_tlist"]/dl/dd/h3/a/@href').extract():
            #yield scrapy.Request(url, callback=self.parse_detail)

        for index in range(len(url)):
            #if(index == 0):
            if(Function.hasTitle(title[index]) == 0):
                yield scrapy.Request(url[index], meta={'cover': cover[index]}, callback=self.parse_detail)
                
        
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
        item['title'] = response.xpath('//div[@class="m-news-hd"]/h2/text()').extract()[0]
        item['summary'] = response.xpath('//div[@class="m-news-content"]/p/text()').extract()[0]
        content = ''


        a_rs = re.compile(r"<a[^>]*>|<\/a>", re.S)
   
        #for con in response.xpath('//div[@class="g-main-855 fl"]/div[@class="m-news-bd js-anchor-newsnav"]/div[@class="m-news-box"]/div[@class="m-news-content"]/p').extract():
        for con in response.xpath('//div[@class="m-news-content"]/p').extract():    
            con = a_rs.sub('',con)#去掉内容的a标签
            content = content + con


        item['content'] =  content
        item['pubtime'] = response.xpath('//div[@class="infos"]/span/text()').extract()[0]
        
        imageurl = []
        for img in response.xpath('//div[@class="m-news-content"]/p/img/@original').extract():
            imageurl.append(img)


        item['imageUrl'] = imageurl
        item['cover'] = response.meta['cover']
        item['source_url'] = response.url
        item['source'] = "中华建材网"


        yield item


