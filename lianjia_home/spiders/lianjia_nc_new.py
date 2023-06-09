import scrapy
from lianjia_home import settings
from scrapy import Request
from lianjia_home.items import LianjiaNCNewItem
import redis
import datetime
import re

districtDic = {
    'donghuqu': "东湖区",
    'nanchangxian': '南昌县',
    'xinjianqu': '新建区',
    'wanliqu': '湾里区',
    'honggutan1': '红谷滩',
    'xihuqu': '西湖区',
    'jinxianxian': '进贤县',
    'qingyunpuqu': '青云谱区',
    'qingshanhuqu': '青山湖区',
    'gaoxinqu11': '高新区',
    'jingkaiqu8': '经开区',
}

class LianjiaNcNewSpider(scrapy.Spider):
    name = 'lianjia_nc_new'
    allowed_domains = ['nc.fang.lianjia.com']

    def __init__(self):
        self.use_proxy = settings.USE_PROXY
        self.crawl_with_district = settings.CRAWL_WITH_DISTRICT
        # TODO 暂时无法获取总页数的临时做法
        self.total_page = 10 if self.crawl_with_district else 30
        if self.use_proxy:
            host = settings.REDIS_HOST
            port = settings.REDIS_PORT
            db_index = settings.REDIS_DB_INDEX
            db_psd = settings.REDIS_PASSWORD
            self.db_conn = redis.StrictRedis(host=host,
                                            port=port,
                                            password=db_psd,
                                            decode_responses=True)

    def start_requests(self):
        if self.crawl_with_district:
            for key in districtDic:
                url = f'https://nc.fang.lianjia.com/loupan/{key}/#{key}'
                yield self.my_request(url, self.parse, self.error_back)
        else:
            url = 'https://nc.fang.lianjia.com/loupan/'
            yield self.my_request(url, self.parse, self.error_back)

    def my_request(self, url, callback, errback, item=None):
        if self.use_proxy:
            proxy = self.db_conn.srandmember('ip')
            self.logger.info(f"use proxy {proxy}")
            meta = {
                'proxy': proxy,
                'download_timeout': 10,
                "dont_retry": True,  # 请求不重试
            }
            if item:
                meta['item'] = item
            return Request(url,
                           callback=callback,
                           errback=errback,
                           meta=meta,
                           dont_filter=True,  # 不过滤重复请求
                           )
        else:
            meta = {'item': item} if (item is not None) else None
            return Request(url=url, callback=callback, meta=meta)

    def parse(self, response):
        list_selector = response.xpath("//div[@class='resblock-desc-wrapper']")
        for oen_selector in list_selector:
            try:
                href = oen_selector.xpath("div[@class='resblock-name']/a[1]/@href").extract_first()
                url = f"https://nc.fang.lianjia.com{href}"
                yield self.my_request(url, self.detailURL_get_parse,self.detailURL_get_error_back)
            except Exception as e:
                self.logger.error(e)
        cur_page_str = re.findall(r'pg(\d+)', response.url)
        cur_page = 1
        if not cur_page_str: #如果是第一页
            toltal_page_str = response.xpath("//div[@class='page-box']/a[4]/text()").extract_first()
            #TODO 获取总页数 
            self.total_page = int(toltal_page_str) if toltal_page_str else self.total_page
        else:
            cur_page = int(cur_page_str[0])
        if cur_page < self.total_page:
            if self.crawl_with_district:
                try:
                    sub_district = response.url.split('/')[4]
                    next_url = f"https://nc.fang.lianjia.com/loupan/{sub_district}/pg{cur_page}/#{sub_district}"
                    yield self.my_request(next_url, self.parse, self.error_back)
                except Exception as e:
                    self.logger.error(e)
            else:
                next_url = f"https://nc.fang.lianjia.com/loupan/pg{cur_page+1}/"
                yield self.my_request(next_url, self.parse, self.error_back)

    def detailURL_get_parse(self, response):
        vilage_name = response.xpath("//div[@class='middle-info animation']/ul[1]/li[1]/span[2]/text()").extract_first()
        unit_price = response.xpath("//div[@class='price']/span[@class='price-number']/text()").extract_first()
        sale_date = response.xpath("//div[@class='open-date']/span[2]/text()").extract_first()
        item :LianjiaNCNewItem = LianjiaNCNewItem()
        item['village_name'] = vilage_name
        item['url'] = response.url
        item['unit_price'] = unit_price
        item['sale_date'] = sale_date
        href = response.xpath("//div[@class='middle-info animation']/div[@class='more-building']/a[1]/@href").extract_first()
        detail_url = f"https://nc.fang.lianjia.com{href}"
        yield self.my_request(detail_url,self.detail_parse,self.detail_error_back,item=item)

    def detail_parse(self, response):
        # open_date_paths = response.xpath("//div[@class='fenqi-ul']/li")
        # deliver_date = datetime.datetime(2300, 1, 1)
        # for date_path in open_date_paths:
        #     time_str = date_path.xpath("span[1]/span[1]/text()").extract_first()
        #     type = date_path.xpath("span[2]/span[1]/text()").extract_first()
        #     time = datetime.datetime.strptime(time_str, '%Y-%m-%d')
        #     if type == "交房" and time < deliver_date:
        #         deliver_date = time
        item = response.meta['item']
        # item['deliver_date'] = deliver_date.strftime('%Y-%m-%d')
        info = response.xpath("//div[@class='big-left fl']/ul[1]")
        if not info:
            self.logger.error(f"none detail with url:{response.url}")
        house_usage = info.xpath("li[1]/span[2]/text()").extract_first()
        specials = info.xpath("li[3]/span[2]/text()").extract_first()
        district = info.xpath("li[4]/span[2]/a[1]/text()").extract_first()
        region = info.xpath("li[5]/span[2]/text()").extract_first()
        developer_name = info.xpath("li[7]/span[2]/text()").extract_first()
        house_property = response.xpath("//div[@class='big-left fl']/ul[3]/li[8]/span[2]/text()").extract_first()
        building_type = response.xpath("//div[@class='big-left fl']/ul[3]/li[1]/span[2]/text()").extract_first()
        deliver_date = response.xpath("//div[@class='big-left fl']/ul[3]/li[10]/span[2]/text()").extract_first()
        house_num = response.xpath("//div[@class='big-left fl']/ul[3]/li[7]/span[2]/text()").extract_first()
        item['house_usage'] = house_usage
        item['specials'] = specials
        item['district'] = district
        item['region'] = region
        item['developer_name'] = developer_name
        item['house_property'] = house_property
        item['building_type'] = building_type
        item['deliver_date'] = deliver_date
        item['house_num'] = house_num
        yield item
            


    def error_back(self, failure):
        self.logger.error(repr(failure))
        request = failure.request
        yield self.re_request(request, self.parse, self.error_back)

    def detailURL_get_error_back(self, failure):
        self.logger.error(repr(failure))
        request = failure.request
        yield self.re_request(request, self.detailURL_get_parse, self.detailURL_get_error_back)
    
    def detail_error_back(self, failure):
        self.logger.error(repr(failure))
        request = failure.request
        yield self.re_request(request, self.detail_parse, self.detail_error_back)

    def re_request(self, odlRequest, callbackFunc, errobackFunc):
        if self.db_conn.sismember("ip", odlRequest.meta['proxy']):
            self.db_conn.srem("ip", odlRequest.meta['proxy'])
        proxy = self.db_conn.srandmember('ip')
        self.logger.info(f'reuse proxy{proxy}')
        meta = odlRequest.meta
        meta['proxy'] = proxy
        return Request(odlRequest.url,
                        callback=callbackFunc,
                        errback=errobackFunc,
                        meta=meta,
                        dont_filter=True,  # 不过滤重复请求
                        )
