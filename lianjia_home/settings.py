# Scrapy settings for lianjia_home project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lianjia_home'

SPIDER_MODULES = ['lianjia_home.spiders']
NEWSPIDER_MODULE = 'lianjia_home.spiders'

SAVE_FILE_NAME = 'house_ifo.csv'
MYSQL_DB_NAME = 'house'
MYSQL_HOST = 'localhost' #  172.18.0.4
MYSQL_PASSWORD = '971101'
MYSQL_USER = 'root' #mhu

REDIS_HOST = "localhost"#主机地址
REDIS_PORT = 6379        #端口
REDIS_DB_INDEX = 0       #索引
REDIS_PASSWORD = ""#密码

USE_CHROME=1

USE_PROXY = 0 #使用代理1，不使用0
CRAWL_WITH_DISTRICT = 0 #是否分行政区爬取，分行政区爬取数据全，数据量大
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "Mozilla/5.0 \
#             (Windows NT 10.0; Win64; x64)  \
#             AppleWebKit/537.36 (KHTML, like Gecko) \
#             Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lianjia_home.middlewares.LianjiaHomeSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
downLoadPrio = 101 if USE_CHROME else None
DOWNLOADER_MIDDLEWARES = {
    'lianjia_home.middlewares.LianjiaHomeDownloaderMiddleware': downLoadPrio,
    'lianjia_home.middlewares.LianjiaHomeUserAgentMiddleware': 100,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'lianjia_home.pipelines.LianjiaHomePipeline': 300,
    'lianjia_home.pipelines.FreeProxyPipeline': 50,
    'lianjia_home.pipelines.FilterPipeline': 100,
    # 'lianjia_home.pipelines.CSVPipeline': 200,
    'lianjia_home.pipelines.MySQLPipeLine': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
