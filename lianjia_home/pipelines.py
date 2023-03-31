# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
import MySQLdb
import redis
from scrapy.exceptions import DropItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LianjiaHomePipeline:
    def process_item(self, item, spider):
        return item

class FreeProxyPipeline(object):
    db_conn = None
    #Spider开启时，获取数据库配置信息，连接redis数据库服务器
    def open_spider(self,spider):
        if spider.name == "free_proxy_05":
            #获取配置文件中redis配置信息
            host = spider.settings.get("REDIS_HOST")#主机地址
            port = spider.settings.get("REDIS_PORT",)#端口
            db_index = spider.settings.get("REDIS_DB_INDEX")#索引
            db_psd = spider.settings.get("REDIS_PASSWORD")#密码
            #连接redis，得到一个连接对象
            self.db_conn = redis.StrictRedis(host=host,port=port,db=db_index,
                                             password=db_psd,decode_responses=True)
            self.db_conn.delete("ip")

    #将数据存储于redis数据库
    def process_item(self, item, spider):
        if spider.name == "free_proxy_05":
            #将item转换为字典类型
            item_dict = dict(item)
            #将item_dict保存于key为ip的集合中
            self.db_conn.sadd("ip",item_dict["url"])
        return item

    def close_spider(self, spider):
        self.db_conn.connection_pool.disconnect()

class FilterPipeline(object):
    def process_item(self, item, spider):
        if spider.name != "Lianjia_home":
            return
        item['total_area'] = re.findall(r'\d+\.?\d*', item['total_area'])[0]
        item['unit_price'] = re.findall(r'\d+,?\d*', item['unit_price'])[0].replace(",", '')
        for key, value in item.items():
            if item[key] is not None:
                item[key] = value.strip()
        # if item['direction'] == '暂时无数据':
        #     raise DropItem(f'无朝向数据，抛弃此项目{item}')
        return item


class MySQLPipeLine(object):
    db_conn = None
    db_cursor = None
    def open_spider(self, spider):
        db_name = spider.settings.get('MYSQL_DB_NAME')
        host = spider.settings.get('MYSQL_HOST')
        user = spider.settings.get('MYSQL_USER')
        pwd = spider.settings.get('MYSQL_PASSWORD')
        self.db_conn = MySQLdb.connect(db=db_name, host=host, user=user,
                                       password=pwd, charset='utf8')
        self.db_cursor = self.db_conn.cursor()

    def process_item(self, item, spider):
        if spider.name != "Lianjia_home":
            return
        house_id = item['house_id']
        title = item['title']
        house_struct = item['house_struct']
        floor_info = item['floor_info'].split('(')[0]
        total_floor = re.findall(r'\d+', item['floor_info'])[0]
        direction = item['direction']
        total_area = item['total_area']
        village_name = item['village_name']
        district = item['district']
        region = item['region']
        fitment = item['fitment']
        elevator_rate = item['elevator_rate']
        start_time = item['start_time']
        house_usage = item['house_usage']
        house_property = item['house_property']
        total_price = item['total_price']
        unit_price = item['unit_price']
        mortgage_info = item['mortgage_info']
        values = (house_id, title, house_struct, floor_info, total_floor,direction,
                  total_area,village_name,district,region,fitment,elevator_rate,
                  start_time,house_usage,house_property,total_price,unit_price,mortgage_info)
        sql = 'insert into lianjia_nc (house_id, title, house_struct, floor_info, total_floor,direction,\
                  total_area,village_name,district,region,fitment,elevator_rate,\
                  start_time,house_usage,house_property,total_price,unit_price,mortgage_info)' \
              ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.db_cursor.execute(sql, values)
        return item

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_cursor.close()
        self.db_conn.close()


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
