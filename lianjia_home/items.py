# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FreeProxyItem(scrapy.Item):
    url = scrapy.Field()#url
    cryptonym = scrapy.Field()#是否高匿名

class LianjiaHomeItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    house_struct = scrapy.Field()
    floor_info = scrapy.Field()#楼层信息
    direction = scrapy.Field()#朝向
    total_area = scrapy.Field()
    village_name = scrapy.Field()#小区名
    district = scrapy.Field()#区
    region = scrapy.Field()#地区
    building_type = scrapy.Field()#建筑结构
    fitment = scrapy.Field()#装修信息
    elevator_rate = scrapy.Field()#梯户比例
    start_time = scrapy.Field()#上架时间
    house_usage = scrapy.Field()#房屋用途（住宅？）
    house_property = scrapy.Field()#产权信息
    total_price = scrapy.Field()#总价
    unit_price = scrapy.Field()#单价
    mortgage_info = scrapy.Field() #抵押信息
    house_id = scrapy.Field()
