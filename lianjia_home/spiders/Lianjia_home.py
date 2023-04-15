import re

import redis
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from lianjia_home.items import LianjiaHomeItem
from lianjia_home import settings
from scrapy.loader import ItemLoader
import json

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

class LianjiaHomeSpider(scrapy.Spider):
    name = 'Lianjia_home'
    allowed_domains = ['nc.lianjia.com']

    def __init__(self):
        self.use_proxy = settings.USE_PROXY
        host = settings.REDIS_HOST
        port = settings.REDIS_PORT
        db_index = settings.REDIS_DB_INDEX
        db_psd = settings.REDIS_PASSWORD
        self.db_conn = redis.StrictRedis(host=host,
                                         port=port,
                                         password=db_psd,
                                         decode_responses=True)

    def start_requests(self):

        for key in districtDic.keys():
            url = f'https://nc.lianjia.com/ershoufang/{key}/co32/'
            if self.use_proxy:
                proxy = self.db_conn.srandmember('ip')
                self.logger.info(f"use proxy {proxy}")
                yield Request(url,
                              callback=self.parse,
                              errback=self.error_back,
                              meta={
                                  'proxy': proxy,
                                  'download_timeout': 10,
                                  "dont_retry": True,  # 请求不重试
                              },
                              dont_filter=True,  # 不过滤重复请求
                              )
            else:
                yield Request(url)

    def parse(self, response):
        list_selector = response.xpath("//div[@class='info clear']")
        for one_selector in list_selector:
            try:
                item = LianjiaHomeItem()
                house_info = one_selector.xpath("div[@class='address']/ \
                            div[@class='houseInfo']/text()").extract_first()
                info_list = house_info.split('|')
                house_struct = info_list[0].strip(" ")
                total_area = info_list[1].strip(" ")
                direction = info_list[2].strip(" ")
                fitment = info_list[3].strip(" ")
                floor_info = info_list[4].strip(" ")
                total_price = one_selector.xpath("div[@class='priceInfo']/ \
                            div[@class='totalPrice totalPrice2']/span/text()").extract_first()
                unit_price = one_selector.xpath("div[@class='priceInfo']/ \
                            div[@class='unitPrice']/span/text()").extract_first()
                item["title"] = one_selector.xpath("div[@class='title']/a/text()").extract_first()
                item["house_struct"] = house_struct
                item["floor_info"] = floor_info
                item["direction"] = direction
                item["total_area"] = total_area
                item["fitment"] = fitment
                item["total_price"] = total_price
                item["unit_price"] = unit_price
                detail_url = one_selector.xpath("div[@class='title']/a/@href").extract_first()
                yield Request(detail_url, meta={'item' : item}, callback=self.detail_parase)
            except Exception as e:
                print('Error:', e)

        page_info = response.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
        page_json_str = page_info.extract_first()
        total_page = 100
        current_page = 1
        if page_json_str:
            page_data = json.loads(page_json_str)
            total_page = int(page_data['totalPage'])
            current_page = int(page_data['curPage'])
        else:
            match = re.findall(r'pg(\d+)', response.url)
            if match:
                current_page = int(match[0])
            else:
                # raise Exception('None page Data find in xpath or url')
                self.logger.info('None page Data find in xpath or url')
        if current_page < total_page: #获取下一页
            try:
                sub_district = response.url.split('/')[4]
                next_url = f"https://nc.lianjia.com/ershoufang/{sub_district}/pg{current_page+1}co32/"
                proxy = self.db_conn.srandmember('ip')
                if self.use_proxy:
                    yield Request(next_url,
                                  callback=self.parse,
                                  errback=self.error_back,
                                  meta={
                                      'proxy': proxy,
                                      'download_timeout': 10,
                                      "dont_retry": True,  # 请求不重试
                                  },
                                  dont_filter=True,  # 不过滤重复请求
                                  )
                else:
                    yield Request(next_url)
            except Exception as e:
                self.logger.error(e)

    def detail_parase(self, response):
        item: LianjiaHomeItem = response.meta["item"]
        try:
            house_detail_selector = response.xpath("//div[@class='introContent']")[0]
            item['village_name'] = response.xpath("//div[@class='communityName']/a[1]/text()").extract_first()
            item['district'] = response.xpath("//div[@class='areaName']/span[2]/a[1]/text()").extract_first()
            item['region'] = response.xpath("//div[@class='areaName']/span[2]/a[2]/text()").extract_first()
            item['building_type'] = house_detail_selector.xpath("//div[@class='base']/div[2]/ul/li[6]/text()").extract_first()
            item['elevator_rate'] = house_detail_selector.xpath("//div[@class='base']/div[2]/ul/li[10]/text()").extract_first()
            item['start_time'] = house_detail_selector.xpath("//div[@class='transaction']/div[2]/ul/li[1]/span[2]/text()").extract_first()
            item['house_usage'] = house_detail_selector.xpath("//div[@class='transaction']/div[2]/ul/li[4]/span[2]/text()").extract_first()
            item['house_property'] = house_detail_selector.xpath("//div[@class='transaction']/div[2]/ul/li[6]/span[2]/text()").extract_first()
            item['mortgage_info'] = house_detail_selector.xpath("//div[@class='transaction']/div[2]/ul/li[7]/span[2]/text()").extract_first()
            item['house_id'] = response.xpath("//div[@class='aroundInfo']/div[@class='houseRecord']/span[2]/text()").extract_first()
        except Exception as e:
            self.logger.error(e)
        yield item

    def error_back(self, failure):
        self.logger.error(repr(failure))
        request = failure.request
        if self.db_conn.sismember("ip", request.meta['proxy']):
            self.db_conn.srem("ip", request.meta['proxy'])
        proxy = self.db_conn.srandmember('ip')
        self.logger.info(f'reuse proxy{proxy}')
        yield Request(request.url,
                      callback=self.parse,
                      errback=self.error_back,
                      meta={
                          'proxy': proxy,
                          'download_timeout': 10,
                          "dont_retry": True,  # 请求不重试
                      },
                      dont_filter=True,  # 不过滤重复请求
                      )



