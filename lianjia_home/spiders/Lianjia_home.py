import re

import redis
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from lianjia_home.items import LianjiaHomeItem
from lianjia_home import settings
from scrapy.loader import ItemLoader
from selenium import webdriver
import json

import time
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException

import numpy as np
import cv2
from urllib.request import urlopen
import ddddocr

def url_to_image(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

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
        self.driver = webdriver.PhantomJS() # 无界面浏览器驱动(防反爬虫用)
        self.use_proxy = settings.USE_PROXY
        self.crawl_with_district = settings.CRAWL_WITH_DISTRICT
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
            for key in districtDic.keys():
                url = f'https://nc.lianjia.com/ershoufang/{key}/co32/'
                yield self.my_request(url, self.parse, self.error_back)
        else:
            url = 'https://nc.lianjia.com/ershoufang/co32/'
            yield self.my_request(url, self.parse, self.error_back)

    def my_request(self, url, callback, errback, item=None):
        headers = {
            'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "referer": "https://clogin.lianjia.com/",}   

        cookies = {
            'lianjia_token': '2.001530f5347b50df26049ddc05d55f62ee',}
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
                           headers=headers,
                           cookies=cookies,
                          callback=callback,
                          errback=errback,
                          meta=meta,
                          dont_filter=True,  # 不过滤重复请求
                          )
        else:
            meta = {'item': item} if (item is not None) else None
            return Request(url=url, callback=callback, meta=meta,headers=headers,cookies=cookies)

    def parse(self, response):
        if response.url.find('location=https') != -1: # 验证码页面
            print("********************************************************************************************************")
            self.driver.get(response.url)
            wait = WebDriverWait(self.driver, 5)#最长等待时长

            wait.until(EC.presence_of_element_located(By.CLASS_NAME,"bk-captcha-btn"))
            # element = spider.driver.find_element_by_css_selector("button[class='bk-captcha-btn']").click()
            print(self.driver.page_source)
            element = self.driver.find_element(By.CLASS_NAME, "bk-captcha-btn")
            imageUrl = element.get_attribute('src')
            print(imageUrl)
            codeImage = url_to_image(imageUrl)
            ocr = ddddocr.DdddOcr(use_gpu=False,show_ad=False,beta=True)
            ocr.set_ranges(0)  # 0:纯数字  6:大小写加数字
            result = ocr.classification(codeImage, probability=False,png_fix=True)
            input_element = self.driver.find_element(By.NAME, "imageCaptchaCode")
            input_element.clear()
            # 向 input 元素发送键盘输入
            input_element.send_keys(result)
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
                yield self.my_request(detail_url, self.detail_parase, self.detail_error_back, item=item)
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
            if self.crawl_with_district:
                try:
                    sub_district = response.url.split('/')[4]
                    next_url = f"https://nc.lianjia.com/ershoufang/{sub_district}/pg{current_page+1}co32/"
                    yield self.my_request(next_url, self.parse, self.error_back)
                except Exception as e:
                    self.logger.error(e)
            else:
                next_url = f"https://nc.lianjia.com/ershoufang/pg{current_page+1}co32/"
                yield self.my_request(next_url, self.parse, self.error_back)

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
            item['url'] = response.url
        except Exception as e:
            self.logger.error(e)
        yield item

    def error_back(self, failure):
        self.logger.error(repr(failure))
        request = failure.request
        yield self.re_request(request, self.parse, self.error_back)

    def detail_error_back(self, failure):
        self.logger.error(repr(failure))
        request = failure.request
        yield self.re_request(request, self.detail_parase, self.detail_error_back)

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



