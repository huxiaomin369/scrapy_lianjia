# scrapy_lianjia
scrapy爬虫 爬取nc链家房价数据

# 项目描述
本项目基于scrapy框架开发，包含两个爬虫
## 1、代理服务器爬虫
爬取几个免费代理网站的服务器，验证有效性并存入redis数据库
## 2、房价爬虫
读取redis缓存的代理，使用代理进行爬取，并将爬取到的房价数据存入MySQL数据库
# 使用
修改setting.py文件，更改数据库，运行main.py
