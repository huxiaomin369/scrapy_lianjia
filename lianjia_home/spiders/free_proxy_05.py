import scrapy
from scrapy import Request
from lianjia_home.items import FreeProxyItem
from twisted.internet.error import DNSLookupError,TimeoutError, TCPTimedOutError#导入错误模块
import re

class FreeProxy05Spider(scrapy.Spider):
    name = 'free_proxy_05'
    # allowed_domains = ['proxy.seofangfa.com']
    start_urls = ['https://proxycompass.com/cn/free-proxies/asia/china/', \
                  'https://www.89ip.cn/index_1.html']
    max_page = 10

    def __init__(self):
        self.test_url = 'https://nc.lianjia.com/ershoufang/co32/'

    def test_proxy_request(self, ip, port):
        url = f"http://{ip}:{port}"
        item: FreeProxyItem = FreeProxyItem(url=url)
        return Request(self.test_url,  # 测试网站的url
                       callback=self.test_parse,  # 回调函数
                       errback=self.error_back,  # 出错回调函数
                       meta={"proxy": url,  # 代理服务器地址
                             "dont_retry": True,  # 请求不重试
                             "download_timeout": 10,  # 超时时间
                             "item": item},
                       dont_filter=True  # 不过滤重复请求
                       )

    def parse(self, response):
        if response.url.find('proxycompass') != -1:
            table_selector = response.xpath("//table[@id='proxylister-table']")
            for selector in table_selector.xpath("tbody/tr"):
                ip = selector.xpath(f"td[1]/text()").extract_first()
                port = selector.xpath(f"td[2]/text()").extract_first()
                # self.parse_ip_port(ip, port)
                yield self.test_proxy_request(ip, port)
        elif response.url.find('89ip') != -1:
            table_selector = response.xpath("//table[@class='layui-table']")
            for selector in table_selector.xpath("tbody/tr"):
                ip = selector.xpath("td[1]/text()").extract_first().strip()
                port = selector.xpath("td[2]/text()").extract_first().strip()
                yield self.test_proxy_request(ip, port)
            match = re.search(r'index_(\d+)', response.url)
            if match and int(match.group(1)) < self.max_page:
                cur_page = int(match.group(1))
                next_url = f"https://www.89ip.cn/index_{cur_page+1}.html"
                yield Request(next_url)


    # 测试网站的数据解析
    def test_parse(self, response):
        self.logger.info("proxy usefull")
        yield response.meta["item"]

    #请求失败的回调函数
    def error_back(self,failure):
        #打印错误日志信息
        self.logger.error(repr(failure))
        #细化出错原因
        if failure.check(DNSLookupError):# DNS出错
            # 获取request
            request = failure.request
            #输出错误日志信息
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):#超时出错
            # 获取request
            request = failure.request
            #输出错误日志信息
            self.logger.error('TimeoutError on %s', request.url)
