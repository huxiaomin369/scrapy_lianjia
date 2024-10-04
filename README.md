# scrapy_lianjia
scrapy爬虫 爬取nc链家房价数据

# 项目描述
本项目基于scrapy框架开发，包含两个爬虫
## 1、代理服务器爬虫
爬取几个免费代理网站的服务器，验证有效性并存入redis数据库
## 2、房价爬虫
读取redis缓存的代，使用代理进行爬取，爬取过程中会自动删除redis数据库中的无效代理，并将爬取到的房价数据存入MySQL数据库
# 使用
修改setting.py文件，更改数据库信息，运行main.py
- 项目依赖mysql redis 先启动数据库，再启动爬虫
