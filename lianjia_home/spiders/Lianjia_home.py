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
        url = 'https://nc.lianjia.com/ershoufang/'
        yield Request(url)

    def parse(self, response):
        list_selector = response.xpath("//div[@class='info clear']")
        for one_selector in list_selector:
            try:
                item = LianjiaHomeItem()
                house_info = one_selector.xpath("div[@class='address']/ \
                            div[@class='houseInfo']/text()").extract_first()
                info_list = house_info.split('|')
                htype = info_list[0].strip(" ")
                area = info_list[1].strip(" ")
                direction = info_list[2].strip(" ")
                fitment = info_list[3].strip(" ")
                height = info_list[4].strip(" ")
                elevator = info_list[5].strip(" ")
                total_price = one_selector.xpath("div[@class='priceInfo']/ \
                            div[@class='totalPrice totalPrice2']/span/text()").extract_first()
                unit_price = one_selector.xpath("div[@class='priceInfo']/ \
                            div[@class='unitPrice']/span/text()").extract_first()
                item["title"] = one_selector.xpath("div[@class='title']/a/text()").extract_first()
                item["type"] = htype
                item["area"] = area
                item["direction"] = direction
                item["fitment"] = fitment
                item["height"] = height
                item["elevator"] = elevator
                item["total_price"] = total_price
                item["unit_price"] = unit_price
                url = one_selector.xpath("div[@class='title']/a/@href").extract_first()
                yield Request(url, meta={'item' : item}, callback=self.property_parase)
            except Exception as e:
                print('Error:', e)

        if self.current_page == 1:
            page_info = response.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
            page_data = json.loads(page_info[0].extract())
            # total_page = 100
            self.total_page = int(page_data['totalPage'])
            self.total_page = 3
        self.current_page += 1
        if self.current_page <= self.total_page:
            next_url = f"https://nc.lianjia.com/ershoufang/pg{self.current_page}/"
            yield Request(next_url)

    def property_parase(self, response):
        house_detail_selector = response.xpath("//div[@class='introContent']")[0]
        house_property = house_detail_selector.xpath("//div[@class='transaction']/div[2]/ul/li[6]/span[2]/text()").extract_first()
        item = response.meta["item"]
        item['property'] = house_property
        yield item


