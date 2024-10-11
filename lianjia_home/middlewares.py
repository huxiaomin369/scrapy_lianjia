# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class LianjiaHomeUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random
        # print(request.headers['User-Agent'])

class LianjiaHomeSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# import time
# from scrapy.http import HtmlResponse
# from selenium.webdriver.comom.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException,TimeoutException
class LianjiaHomeDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # 使用无界面浏览器命令请求网页，防反爬虫
        # if spider.name=="Lianjia_home" or spider.name=="lianjia_nc_new"
        #     spider.driver.get(request.url)
        #     try:
        #         wait = WebDriverWait(spider.driver, 5)#最长等待时长
        #         # 等到需要爬取的xxxx内容加载完成
        #         wait.until(EC.presence_of_element_located(By.XPATH,"//div[@class="xxxx"]"))
        #         # 模拟浏览器的向下滚动操作
        #         spider.driver.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
        #         for i in range(10):
        #             time.sleep(5)
        #             spider.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #         # 获取加载完成的页面
        #         origin_code = spider.driver.page_source
        #         res = HtmlResponse(url=request.url, encoding='utf8', 
        #                            body=origin_code,
        #                            request=request)
        #         return res
        #     except TimeoutException:
        #         print("time out")
        #     except NoSuchElementException:
        #         print("nosuch element")
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
