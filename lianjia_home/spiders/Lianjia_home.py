import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from lianjia_home.items import LianjiaHomeItem
from scrapy.loader import ItemLoader
import json


class LianjiaHomeSpider(scrapy.Spider):
    name = 'Lianjia_home'
    allowed_domains = ['nc.lianjia.com']

    def __init__(self):
        self.total_page = None
        self.current_page = 1

    def start_requests(self):
        url = 'https://nc.lianjia.com/ershoufang/co32/'
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
        if self.current_page == 1:
            page_info = response.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
            page_data = json.loads(page_info[0].extract())
            self.total_page = int(page_data['totalPage'])
            # self.total_page = 3
        self.current_page += 1
        if self.current_page <= self.total_page:
            next_url = f"https://nc.lianjia.com/ershoufang/pg{self.current_page}co32/"
            yield Request(next_url)

    def detail_parase(self, response):
        house_detail_selector = response.xpath("//div[@class='introContent']")[0]
        item: LianjiaHomeItem = response.meta["item"]
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
        yield item


