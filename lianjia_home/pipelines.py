# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.exceptions import DropItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LianjiaHomePipeline:
    def process_item(self, item, spider):
        return item


class FilterPipeline(object):
    def process_item(self, item, spider):
        item['total_area'] = re.findall(r'\d+\.?\d*', item['total_area'])[0]
        item['unit_price'] = re.findall(r'\d+,?\d*', item['unit_price'])[0].replace(",", '')
        for key, value in item.items():
            item[key] = value.strip()
        # if item['direction'] == '暂时无数据':
        #     raise DropItem(f'无朝向数据，抛弃此项目{item}')
        return item


class CSVPipeline(object):
    index = 0
    file = None
    file_name = None

    @classmethod
    def from_crawler(cls, crawler):
        cls.file_name = crawler.settings.get('SAVE_FILE_NAME', "house_info.txt")
        return cls()

    def open_spider(self, spider):
        self.file = open(self.file_name, 'w', encoding='GB2312')  # utf-8

    def process_item(self, item, spider):
        if self.index == 0:
            column_name = "标题,房屋结构,楼层信息,朝向,总面积,小区名, \
            所属区县,地区,装修信息,梯户比例,挂牌时间,房屋用途,产权信息,总价,单价,抵押信息\n"
            self.file.write(column_name)
            self.index = 1
        home_str = item['title'] + ',' + \
                   item['house_struct'] + ',' + \
                   item['floor_info'] + ',' + \
                   item['direction'] + ',' + \
                   item['total_area'] + ',' + \
                   item['village_name'] + ',' + \
                   item['district'] + ',' + \
                   item['region'] + ',' + \
                   item['fitment'] + ',' + \
                   item['elevator_rate'] + ',' + \
                   item['start_time'] + ',' + \
                   item['house_usage'] + ',' + \
                   item['house_property'] + ',' + \
                   item['total_price'] + ',' + \
                   item['unit_price'] + ',' + \
                   item['mortgage_info'] + '\n'
        self.file.write(home_str)
        return item

    def close_spiider(self, spider):
        self.file.close()
        pass
