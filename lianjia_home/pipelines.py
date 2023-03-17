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
        item['area'] = re.findall(r'\d+\.?\d*', item['area'])[0]
        item['unit_price'] = re.findall(r'\d+,?\d*', item['unit_price'])[0].replace(",", '')
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
        self.file = open(self.file_name, 'w', encoding='GB2312')#utf-8

    def process_item(self, item, spider):
        if self.index == 0:
            column_name = "title, type, area, direction, fitment, elevator \
            total_price, unit_price, property\n"
            self.file.write(column_name)
            self.index = 1
        home_str = item['title']+','+ \
                    item['type']+','+ \
                    item['area']+','+ \
                    item['direction']+','+ \
                    item['fitment'] + ',' + \
                    item['elevator'] + ',' + \
                    item['total_price'] + ',' + \
                    item['unit_price'] + ',' + \
                    item['property'] + "\n"
        self.file.write(home_str)
        return item

    def close_spiider(self, spider):
        self.file.close()