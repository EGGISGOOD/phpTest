# -*- coding: utf-8 -*-

# Scrapy settings for scrapyWeb project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import oss2,os

BOT_NAME = 'scrapyWeb'

SPIDER_MODULES = ['scrapyWeb.spiders']
NEWSPIDER_MODULE = 'scrapyWeb.spiders'

MONGO_URI = 'mongodb://192.168.1.252:27017/'
MONGO_DATABASE = 'ip_proxies'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyWeb (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
"""
MYSQL_CONFIG = {
                'host':'192.168.1.249',
                'port':3306,
                'user':'jia400_tp',
                'password':'HY#2018john#gz2018',
                'db':'jia400',
                'charset':'utf8',
                #'cursorclass':pymysql.cursors.DictCursor,
}
"""
MYSQL_CONFIG = {
                'host':'rm-wz9jkpbav55t9604q.mysql.rds.aliyuncs.com',
                'port':3306,
                'user':'article_collect',
                'password':'jTY%^uy8989gh5856gh8F$%l',
                'db':'jia400_log',
                'charset':'utf8',
                #'cursorclass':pymysql.cursors.DictCursor,
}


# Disable cookies (enabled by default)
COOKIES_ENABLED = False

 

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   # 'Host': 'www.xicidaili.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Upgrade-Insecure-Requests': '1'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapyWeb.middlewares.ScrapywebSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'scrapyWeb.middlewares.ScrapywebDownloaderMiddleware': 543,
    #'scrapyWeb.middlewares.TutorialDownloaderMiddleware': 543,
    'scrapyWeb.middlewares.HeadersDownloaderMiddleware':None,
    'scrapyWeb.rotateUserAgentMiddleware.RotateUserAgentMiddleware': 400, 
   # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
  #  'scrapyWeb.middlewares.MyproxiesSpiderMiddleware': 1,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapyWeb.pipelines.PostImgPipeline': 4,
    'scrapyWeb.pipelines.CoverPipeline': 3,
    'scrapyWeb.pipelines.MysqlPipeline': 5,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



"""
IMAGES_URLS_FIELD = "https://test-vote-huuyaa-com.oss-cn-shenzhen.aliyuncs.com"  #image_url是在items.py中配置的网络爬取得图片地址
AUTH = oss2.Auth('LTAIPx0WdjloRpcC', 'bdkhKSqgQUIdK3IcqJwmLlSQlY6w7I')
# Endpoint以杭州为例，其它Region请按实际情况填写。
BUCKET = oss2.Bucket(AUTH, 'oss-cn-shenzhen.aliyuncs.com', 'test-vote-huuyaa-com') 
"""
"""
IMAGES_URLS_FIELD = "https://test-jia400-com.oss-cn-shenzhen.aliyuncs.com"  #image_url是在items.py中配置的网络爬取得图片地址
AUTH = oss2.Auth('LTAI01nqUfswNYnk', 'p938oETetBoJ6AmeTIrx0AM1OkFm2R')
# Endpoint以杭州为例，其它Region请按实际情况填写。
BUCKET = oss2.Bucket(AUTH, 'oss-cn-shenzhen.aliyuncs.com', 'test-jia400-com') 
"""

IMAGES_URLS_FIELD = "https://image.jia400.com"  #image_url是在items.py中配置的网络爬取得图片地址
AUTH = oss2.Auth('LTAI01nqUfswNYnk', 'p938oETetBoJ6AmeTIrx0AM1OkFm2R')
# Endpoint以杭州为例，其它Region请按实际情况填写。
BUCKET = oss2.Bucket(AUTH, 'oss-cn-shenzhen.aliyuncs.com', 'www-jia400-com') 


IMAGES_BASE_URL = 'scrapy'
#配置保存本地的地址
PROJECT_DIR =  os.path.abspath(os.path.dirname(__file__))  #获取当前爬虫项目的绝对路径
IMAGES_STORE = os.path.join(os.path.dirname(os.path.dirname(__file__)),IMAGES_BASE_URL) #文件路径



#IMAGES_MIN_HEIGHT = 100#设定下载图片的最小高度
#IMAGES_MIN_WIDTH = 100#设定下载图片的最小宽度

 