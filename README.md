# scrapy_lianjia
scrapy爬虫 爬取nc链家房价数据

## 项目描述
本项目基于scrapy框架开发，包含两个爬虫
### 1、代理服务器爬虫
爬取几个免费代理网站的服务器，验证有效性并存入redis数据库
### 2、房价爬虫
读取redis缓存的代，使用代理进行爬取，爬取过程中会自动删除redis数据库中的无效代理，并将爬取到的房价数据存入MySQL数据库

## tips 
```sh
# 访问mysql数据库
docker exec -it mysql mysql -uroot -p

# 安装依赖
pip install -r requirements.txt

# 查看本机ip
hostname -I
```

```sql
# 创建数据库
CREATE DATABASE IF NOT EXISTS house
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

# 修改root 用户密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
```

